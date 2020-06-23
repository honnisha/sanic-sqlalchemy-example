import json
from decimal import Decimal, getcontext

from currencies.convertate import convert
from currencies.models import CurrenciesEnum
from currencies.tests.test_utils import MOCK_CURRENCIES
from currencies.utils import update_currencies
from users.utils import create_user, get_user, transfer_money


async def test_transfer(test_cli, database, mocker):
    context = getcontext()
    context.prec = 5

    get_from_mock = mocker.patch('currencies.utils.get_from_url')
    get_from_mock.return_value = MOCK_CURRENCIES
    resp = await update_currencies(database)

    user_id = await create_user(database, 'test_source@asd.as', 100.0, 'RUB', 'passpass')
    target_user_id = await create_user(database, 'test_target@asd.as', 50.0, 'USD', 'pass')

    user = await get_user(database, user_id=user_id)
    target_user = await get_user(database, user_id=target_user_id)

    await transfer_money(database, None, user, target_user, Decimal(20.0))

    user = await get_user(database, user_id=user_id)
    target_user = await get_user(database, user_id=target_user_id)

    assert user['_balance'] == 80.0
    new_target_balance = context.create_decimal_from_float(50.0) + await convert(
        Decimal(20.0), CurrenciesEnum.RUB.value, CurrenciesEnum.USD.value, database
    )
    assert context.create_decimal_from_float(target_user['_balance']) == new_target_balance


async def test_transfer_api(test_cli, database, mocker):
    get_from_mock = mocker.patch('currencies.utils.get_from_url')
    get_from_mock.return_value = MOCK_CURRENCIES
    resp = await update_currencies(database)

    target_user_id = await create_user(database, 'test_target@pass.as', 50.0, 'USD', 'pass')

    data = json.dumps({'email': 'test_source@asd.as', 'password': 'passpass'})
    resp = await test_cli.post('/api/transfer', data=data)
    assert resp.status == 403, ('test for transfer without login', await resp.text())

    user_id = await create_user(database, 'test_source@asd.as', 100.0, 'RUB', 'passpass')
    target_user_id = await create_user(database, 'test_target@asd.as', 50.0, 'USD', 'passpass')

    data = json.dumps({'email': 'test_source@asd.as', 'password': 'passpass'})
    resp = await test_cli.post('/api/login', data=data)
    assert resp.status == 200, ('test for login for transfer', await resp.text())
    token = json.loads(await resp.text())['token']
    headers = {'Authorization': f'JWT {token}'}

    resp = await test_cli.post('/api/transfer', headers=headers)
    assert resp.status == 415, ('test for login without data', await resp.text())

    resp = await test_cli.post('/api/transfer', data=json.dumps({'value': 1000, 'email': 'asd@das.ru'}), headers=headers)
    assert resp.status == 400, ('test for not enough money', await resp.text())

    resp = await test_cli.post('/api/transfer', data=json.dumps({'value': 20, 'email': 'asd@.ru'}), headers=headers)
    assert resp.status == 400, ('test for wrong email', await resp.text())

    resp = await test_cli.post('/api/transfer', data=json.dumps({'value': 20, 'email': 'asd@gasd.ru'}), headers=headers)
    assert resp.status == 400, ('test for user not found', await resp.text())

    resp = await test_cli.post('/api/transfer', data=json.dumps({'value': 20, 'email': 'test_target@pass.as'}), headers=headers)
    assert resp.status == 200, ('test for success', await resp.text())
