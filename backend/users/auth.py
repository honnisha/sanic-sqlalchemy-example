import datetime
import inspect
import json
import uuid
from abc import ABC, abstractmethod
from functools import wraps
from typing import Optional

import jwt
import redis
from redis import ConnectionPool
from sanic import response

import settings
from users.utils import generate_hash, get_user, verify_hash


def login_required(insert_user=False):
    def decorator(f):
        @wraps(f)
        async def decorated_function(request, *args, **kwargs):

            user_id = await user_auth_method().get_id_if_authorized(request)
            if user_id is not None:

                if insert_user:

                    user = await get_user(request.app.config['database'], user_id=user_id)
                    res = f(request, user, *args, **kwargs)

                    if inspect.isawaitable(res):
                        return await res

                    return res

                return await f(request, *args, **kwargs)
            else:
                return response.json(
                    {'error': {'message': 'Not authorized'}},
                    status=403
                )
        return decorated_function
    return decorator


class AbstractAuthorization(ABC):
    @classmethod
    @abstractmethod
    async def get_id_if_authorized(cls, request) -> int:
        pass

    @classmethod
    @abstractmethod
    async def user_authorize(cls, request, user_id: int, email: str) -> Optional[str]:
        pass

    @classmethod
    @abstractmethod
    async def user_unauthorize(cls, request):
        pass


class SessionAuthorization:
    @staticmethod
    def _get_session(request):
        return request.ctx.session

    @classmethod
    async def get_id_if_authorized(cls, request) -> int:
        return cls._get_session(request)['user_id']

    @classmethod
    async def user_authorize(cls, request, user_id: int, email: str) -> Optional[str]:
        cls._get_session(request)['user_id'] = user_id
        return None

    @classmethod
    async def user_unauthorize(cls, request):
        del cls._get_session(request)['user_id']


AbstractAuthorization.register(SessionAuthorization)


class JWTAuthorization:
    @staticmethod
    def _generate_token(redis_pool: ConnectionPool, email: str, user_id: int) -> str:
        '''Generate token and store it, return token_key'''

        conn = redis.Redis(connection_pool=redis_pool)
        token_key = str(uuid.uuid4())
        store_data = {
            'user_id': user_id,
            'token_hash': generate_hash(token_key)
        }
        conn.set(f'tokens_{email}', json.dumps(store_data), ex=datetime.timedelta(hours=24))
        return token_key

    @staticmethod
    def _remove_token(redis_pool: ConnectionPool, email: str):
        '''Remove token from storage'''

        conn = redis.Redis(connection_pool=redis_pool)
        conn.delete(email)

    @staticmethod
    def _get_jwt_data_from_request(request) -> Optional[dict]:
        authorization = request.headers.get('Authorization')
        if not authorization or not authorization.startswith('JWT '):
            return None

        return jwt.decode(authorization[4:], settings.JWT_SECRET, algorithms=['HS256'])

    @classmethod
    async def get_id_if_authorized(cls, request) -> Optional[int]:
        jwt_data = cls._get_jwt_data_from_request(request)
        redis_pool = request.app.config['redis_pool']

        if jwt_data is None:
            return None

        conn = redis.Redis(connection_pool=redis_pool)
        email = jwt_data['email']
        store_data = json.loads(conn.get(f'tokens_{email}'))
        if not store_data:
            return None

        token_hash = store_data['token_hash']

        if verify_hash(token_hash, jwt_data['token']):
            return int(store_data['user_id'])

        return None

    @classmethod
    async def user_authorize(cls, request, user_id: int, email: str) -> str:
        redis_pool = request.app.config['redis_pool']
        token = cls._generate_token(redis_pool, email, user_id)

        lwt_data = {'email': email, 'token': token}
        jwt_encoded = jwt.encode(lwt_data, settings.JWT_SECRET, algorithm='HS256')
        return jwt_encoded.decode("utf-8") 

    @classmethod
    async def user_unauthorize(cls, request):
        redis_pool = request.app.config['redis_pool']
        jwt_data = cls._get_jwt_data_from_request(request)
        assert jwt_data

        cls._remove_token(redis_pool, jwt_data['email'])


AbstractAuthorization.register(JWTAuthorization)


METHODS = {
    'JWT': JWTAuthorization,
    'SESSION': SessionAuthorization,
}


def user_auth_method() -> AbstractAuthorization:
    return METHODS[settings.AUTHORIZATION_METHOD]
