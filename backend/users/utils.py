import binascii
import hashlib
import os
from functools import wraps
from sanic import response


def generate_password_hash(password):
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    pwdhash = hashlib.pbkdf2_hmac(
        'sha512', password.encode('utf-8'), salt, 100000
    )
    pwdhash = binascii.hexlify(pwdhash)
    return (salt + pwdhash).decode('ascii')

def verify_password(stored_password, password):
    salt = stored_password[:64]
    stored_password = stored_password[64:]
    pwdhash = hashlib.pbkdf2_hmac(
        'sha512', provided_password.encode('utf-8'), salt.encode('ascii'), 100000
    )
    pwdhash = binascii.hexlify(pwdhash).decode('ascii')
    return pwdhash == stored_password


def login_required():
    def decorator(f):
        @wraps(f)
        async def decorated_function(request, *args, **kwargs):
            is_authorized = request.ctx.session.get('user_id')

            if is_authorized:
                return await f(request, *args, **kwargs)
            else:
                # the user is not authorized.
                return response.text('Not authorized', status=403)
        return decorated_function
    return decorator
