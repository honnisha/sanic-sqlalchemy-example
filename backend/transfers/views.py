from sanic import Blueprint, response

transfers_blueprint = Blueprint('transfers_blueprint', url_prefix='/api')

@transfers_blueprint.route('/test/', methods=['GET'])
async def test(request):
    return response.text("test")
