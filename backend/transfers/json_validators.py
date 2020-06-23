from users.json_validators import email_validation, currency_validation


transfer_schema = {
    'email': email_validation,
    'value': {
        'type': 'float',
        'min': 0.1,
        'required': True,
    },
}
