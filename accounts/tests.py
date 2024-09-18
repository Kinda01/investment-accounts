from django.test import TestCase
from rest_framework.test import APIRequestFactory, force_authenticate
from rest_framework.authtoken.models import Token

from .models import InvestmentAccount, Transaction, AccountUser, CustomUser
from .views import InvestmentAccountViewSet, TransactionViewSet, UserTransactionListView


class InvestmentAccountViewSetTestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = CustomUser.objects.create_user('testuser', 'test@example.com')
        self.token = Token.objects.create(user=self.user)
        self.account = InvestmentAccount.objects.create(name='Test Account')
        self.account_user = AccountUser.objects.create(user=self.user, account=self.account, permission_level='ADMIN')

    def test_list_investment_accounts(self):
        request = self.factory.get('/investment-accounts/', HTTP_AUTHORIZATION='Token ' + self.token.key)
        view = InvestmentAccountViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.account, response.data['results'])

    def test_retrieve_investment_account(self):
        request = self.factory.get(f'/investment-accounts/{self.account.pk}/', HTTP_AUTHORIZATION='Token ' + self.token.key)
        view = InvestmentAccountViewSet.as_view({'get': 'retrieve'})
        response = view(request, pk=self.account.pk)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], self.account.name)

    # Add more tests for create, update, and delete operations

class TransactionViewSetTestCase(TestCase):
    # ... your transaction viewset tests here

class UserTransactionListViewTestCase(TestCase):
    def test_admin_can_view_user_transactions(self):
        # Create an admin user and log in
        admin_user = CustomUser.objects.create_superuser('admin', 'admin@example.com', 'admin')
        request = self.factory.get(f'/admin-transactions/{self.user.pk}/', HTTP_AUTHORIZATION='Token ' + Token.objects.create(user=admin_user).key)
        view = UserTransactionListView.as_view({'get': 'list'})
        response = view(request, user_pk=self.user.pk)
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.transaction, response.data['results'])

    # Add more tests for date range filtering and total balance calculation
    