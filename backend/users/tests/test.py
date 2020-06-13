import json

import pytest

from users.views import NO_DATA_ERROR


async def test_register(test_cli):
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

    resp = await test_cli.post('/api/register', data=json.dumps(
        {'email': 'test_asd@asd.as', 'password': '123123', 'currency': 'RUB'}
    ))
    assert resp.status == 200, await resp.text()
