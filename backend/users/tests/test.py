import json

import pytest

from users.views import NO_DATA_ERROR, ALREADY_EXSITS_ERROR, AUTH_ERROR_MESSAGE


async def test_register_errors(test_cli):
    resp = await test_cli.post('/api/register')
    assert resp.status == 400, resp.status
    text = await resp.text()
    assert text == NO_DATA_ERROR, text

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
    assert await resp.text() == ALREADY_EXSITS_ERROR


async def test_login_errors(test_cli):
    resp = await test_cli.post('/api/login')
    assert resp.status == 401, resp.status
    text = await resp.text()
    assert text == NO_DATA_ERROR, text


async def test_login(test_cli):
    resp = await test_cli.get('/api/logout')
    assert resp.status == 403, resp.status

    data = json.dumps({'email': 'test_login@login.as', 'password': '123123', 'currency': 'RUB'})
    await test_cli.post('/api/register', data=data)

    data = json.dumps({'email': 'test_login@login.as', 'password': 'wrong'})
    resp = await test_cli.post('/api/login', data=data)
    text = await resp.text()
    assert resp.status == 401, (resp.status, text)
    assert text == AUTH_ERROR_MESSAGE, text

    data = json.dumps({'email': 'test_login@login.as', 'password': '123123'})
    resp = await test_cli.post('/api/login', data=data)
    assert resp.status == 200, resp.status

    resp = await test_cli.get('/api/logout')
    assert resp.status == 200, resp.status
