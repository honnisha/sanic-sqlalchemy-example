from sanic import Blueprint, response
from main import auth

users_blueprint = Blueprint('users_blueprint')


# @app.middleware('request')
# async def add_session_to_request(request):
#     # setup session

@users_blueprint.route('/login', methods=['GET', 'POST'])
async def login(request):
    username = request.form.get('username')
    password = request.form.get('password')

    user = None
    if not user:
        return response.text("Error")

    auth.login_user(request, user)
    return response.text("Logged in successfully")


@users_blueprint.route('/logout')
@auth.login_required
async def logout(request):
    auth.logout_user(request)
    return response.text("Logged out successfully")
