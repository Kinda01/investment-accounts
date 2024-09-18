from django.db.models.signals import post_migrate
from django.contrib.auth.models import Permission
from django.dispatch import receiver

@receiver(post_migrate)
def create_custom_permissions(sender, **kwargs):
    """Creates custom permissions after migrations are applied."""
    permissions = [
        {'codename': 'view_investment_account', 'name': 'Can view investment account'},
        {'codename': 'add_investment_account', 'name': 'Can add investment account'},
        {'codename': 'change_investment_account', 'name': 'Can change investment account'},
        {'codename': 'delete_investment_account', 'name': 'Can delete investment account'},
        {'codename': 'view_transaction', 'name': 'Can view transaction'},
        {'codename': 'add_transaction', 'name': 'Can add transaction'},
    ]

    for perm in permissions:
        Permission.objects.get_or_create(codename=perm['codename'], defaults={'name': perm['name']})
