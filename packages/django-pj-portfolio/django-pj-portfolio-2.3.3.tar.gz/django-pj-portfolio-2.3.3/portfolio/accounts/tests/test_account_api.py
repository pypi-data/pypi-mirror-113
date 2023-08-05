# 3rd party

from django.core.urlresolvers import reverse
from django.utils import timezone

from rest_framework.test import APITestCase
from rest_framework import status


class TestAccountApi():

    def test_account_api_returns_existing_account_list(self, account, http_client):
        """
        Check the account api returns existing accounts
        """

        response = http_client.get(reverse('api-account-list'))

        assert response.status_code == status.HTTP_200_OK
        for returned_account in response.data:
            # Account should have name
            assert 'name' in returned_account
