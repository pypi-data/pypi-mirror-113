from rest_framework.test import APIClient

import pytest

from pytest_factoryboy import register

from .account_factories import AccountFactory

pytestmark = pytest.mark.django_db

register(AccountFactory)

@pytest.fixture(autouse=True)
def enable_db_access(db):
    pass

@pytest.fixture
def http_client():
    return APIClient()
