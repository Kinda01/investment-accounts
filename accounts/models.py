from django.contrib.auth.models import AbstractUser, Permission
from django.db import models


class CustomUser(AbstractUser):
    """Custom user model extending Django's AbstractUser."""
    # Add any custom fields for your user model here
    pass


class InvestmentAccount(models.Model):
    """Model representing an investment account."""
    name = models.CharField(max_length=100)
    users = models.ManyToManyField(CustomUser, through='AccountUser')

    def get_total_balance(self):
        """Calculates the total balance of the investment account."""
        transactions = self.transaction_set.all()
        total_balance = sum(transaction.amount for transaction in transactions)
        return total_balance


class Transaction(models.Model):
    """Model representing a transaction for an investment account."""
    account = models.ForeignKey(InvestmentAccount, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    transaction_type = models.CharField(
        max_length=20,
        choices=[('DEPOSIT', 'Deposit'), ('WITHDRAWAL', 'Withdrawal')],
        default='DEPOSIT'
    )


class AccountUser(models.Model):
    """Model representing the relationship between a user and an investment account, with permissions."""
    account = models.ForeignKey(InvestmentAccount, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    permissions = models.ManyToManyField(Permission)
    permission_level = models.CharField(
        max_length=20,
        choices=[
            ('VIEWER', 'Viewer'),
            ('ADMIN', 'Admin'),
            ('TRANSACTION_POSTER', 'Transaction Poster')
        ],
        default='VIEWER'
    )


# Custom permissions creation (This should generally be placed in a migration or admin-related function)
def create_custom_permissions():
    Permission.objects.get_or_create(codename='view_investment_account', name='Can view investment account')
    Permission.objects.get_or_create(codename='add_investment_account', name='Can add investment account')
    Permission.objects.get_or_create(codename='change_investment_account', name='Can change investment account')
    Permission.objects.get_or_create(codename='delete_investment_account', name='Can delete investment account')
    Permission.objects.get_or_create(codename='view_transaction', name='Can view transaction')
    Permission.objects.get_or_create(codename='add_transaction', name='Can add transaction')
