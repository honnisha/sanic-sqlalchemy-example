from currencies.models import currency_choices


email_validation = {
    'type': 'string',
    'regex': r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$",
    'required': True,
}
password_validation = {
    'type': 'string',
    'minlength': 6,
    'maxlength': 64,
    'required': True,
}
currency_validation = {
    'type': 'string',
    'allowed': currency_choices,
    'required': True,
}


register_schema = {
    'email': email_validation,
    'password': password_validation,
    'currency': currency_validation,
}

login_schema = {
    'email': email_validation,
    'password': password_validation,
}
