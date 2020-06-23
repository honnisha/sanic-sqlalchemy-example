import json


async def test_register_errors(test_cli):
    resp = await test_cli.post('/api/register')
    assert resp.status == 415, ('test for register without data', resp.status)

    resp = await test_cli.post('/api/register', data=json.dumps(
        {'email': '123'}
    ))
    assert resp.status == 400, resp.status

    resp = await test_cli.post('/api/register', data=json.dumps(
        {'email': 'test_asd@asd.as', 'password': '123'}
    ))
    assert resp.status == 400, resp.status

    resp = await test_cli.post('/api/register', data=json.dumps(
        {'email': 'test_asd@asd.as', 'password': '123123', 'currency': '123'}
    ))
    assert resp.status == 400, resp.status


async def test_register(test_cli):
    data = json.dumps({'email': 'test_asd@asd.as', 'password': '123123', 'currency': 'RUB'})
    resp = await test_cli.post('/api/register', data=data)
    assert resp.status == 200, await resp.text()

    resp = await test_cli.post('/api/register', data=data)
    assert resp.status == 400, resp.status


async def test_login_errors(test_cli):
    resp = await test_cli.post('/api/login')
    assert resp.status == 415, ('test for login without json', resp.status)


async def test_login(test_cli):
    resp = await test_cli.get('/api/logout')
    assert resp.status == 403, resp.status

    data = json.dumps({'email': 'test_login@login.as', 'password': '123123', 'currency': 'RUB'})
    resp = await test_cli.post('/api/register', data=data)

    data = json.dumps({'email': 'test_login@login.as', 'password': 'wrong'})
    resp = await test_cli.post('/api/login', data=data)
    assert resp.status == 400, ('test for wrong password', resp.status)

    data = json.dumps({'email': 'test_login@login.as', 'password': '123123'})
    resp = await test_cli.post('/api/login', data=data)
    assert resp.status == 200, ('test for success', resp.status)

    token = json.loads(await resp.text())['token']
    headers = {'Authorization': f'JWT {token}'}

    resp = await test_cli.get('/api/logout', headers=headers)
    assert resp.status == 200, ('test for success logout', resp.status)
