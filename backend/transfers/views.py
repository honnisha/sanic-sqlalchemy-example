from sanic import Blueprint, response

transfers_blueprint = Blueprint('transfers_blueprint')

@transfers_blueprint.route('/test/', methods=['GET'])
async def test(request):
    return response.text("test")
