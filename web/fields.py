import jwe
from django.db import models
from my_secrets import secrets

SENSITIVE_DATA_KEY = jwe.kdf(
    secrets.JWE_SECRET.encode('utf-8'),
    secrets.JWE_SALT.encode('utf-8')
)


def encrypt_string(value, prefix=b'jwe:::'):
    if value:
        value = value.encode()
        if value and not value.startswith(prefix):
            value = (prefix + jwe.encrypt(value, SENSITIVE_DATA_KEY)).decode()
    return value


def decrypt_string(value, prefix=b'jwe:::'):
    if value:
        value = value.encode()
        if value.startswith(prefix):
            value = jwe.decrypt(value[len(prefix):], SENSITIVE_DATA_KEY).decode()
    return value


class EncryptedTextField(models.TextField):
    """
    This field transparently encrypts data in the database. It should probably only be used with PG unless
    the user takes into account the db specific trade-offs with TextFields.
    """
    prefix = b'jwe:::'

    def get_db_prep_value(self, value, **kwargs):
        return encrypt_string(value, prefix=self.prefix)

    def to_python(self, value):
        return decrypt_string(value, prefix=self.prefix)

    def from_db_value(self, value, expression, connection):
        return self.to_python(value)
