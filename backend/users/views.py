from main import auth
from sanic import Blueprint, response
from sqlalchemy.orm.exc import NoResultFound
from users.models import User
from users.utils import verify_password

users_blueprint = Blueprint('users_blueprint', url_prefix='/api')

AUTH_ERROR_MESSAGE = "An account could not be found for the provided username and password"


@users_blueprint.route('/login', methods=['POST'])
async def login(request):
    email = request.form.get('email')
    password = request.form.get('password')

    try:
        user = session.query(User).filter(email == email).one()
    except NoResultFound:
        pass

    if user and verify_password(user.password_hash, password):
        auth.login_user(request, user)
        return response.text("Logged in successfully")

    return response.text(AUTH_ERROR_MESSAGE)


@users_blueprint.route('/logout')
@auth.login_required
async def logout(request):
    auth.logout_user(request)
    return response.text("Logged out successfully")
