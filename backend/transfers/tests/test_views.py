import json

from users.utils import create_user
from transfers.views import NOT_VALID_EMAIL, NOT_ENOUGH_MONEY, USER_EMAIL_NOT_FOUND


async def test_transfer(test_cli, database, mocker):
    resp = await test_cli.post('/api/transfer')
    assert resp.status == 403, resp.status

    await create_user(database, 'test_source@asd.as', 100.0, 'RUB', 'pass')
    await create_user(database, 'test_target@asd.as', 50.0, 'USD', 'pass')
    
    data = json.dumps({'email': 'test_source@asd.as', 'password': 'pass'})
    resp = await test_cli.post('/api/login', data=data)
    assert resp.status == 200, resp.status

    resp = await test_cli.post('/api/transfer')
    assert resp.status == 400, resp.status

    resp = await test_cli.post('/api/transfer', data=json.dumps({'value': '1000', 'email': 'asd@das.ru'}))
    assert resp.status == 400, resp.status
    assert await resp.text() == NOT_ENOUGH_MONEY

    resp = await test_cli.post('/api/transfer', data=json.dumps({'value': '20', 'email': 'asd@.ru'}))
    assert resp.status == 400, resp.status
    assert await resp.text() == NOT_VALID_EMAIL

    resp = await test_cli.post('/api/transfer', data=json.dumps({'value': '20', 'email': 'asd@gasd.ru'}))
    assert resp.status == 400, resp.status
    assert await resp.text() == USER_EMAIL_NOT_FOUND

    resp = await test_cli.post('/api/transfer', data=json.dumps({'value': '20', 'email': 'test_target@asd.as'}))
    assert resp.status == 200, resp.status
