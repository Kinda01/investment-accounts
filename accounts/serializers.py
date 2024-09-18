from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import InvestmentAccount, Transaction, AccountUser, CustomUser


class InvestmentAccountSerializer(serializers.ModelSerializer):
    users = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all(), many=True)

    class Meta:
        model = InvestmentAccount
        fields = ('id', 'name', 'users')


class TransactionSerializer(serializers.ModelSerializer):
    account = InvestmentAccountSerializer(read_only=True)

    class Meta:
        model = Transaction
        fields = ('id', 'account', 'amount', 'date', 'transaction_type')


class InvestmentAccountDetailSerializer(serializers.ModelSerializer):
    transactions = TransactionSerializer(many=True, read_only=True)
    users = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all(), many=True)

    class Meta:
        model = InvestmentAccount
        fields = ('id', 'name', 'users', 'transactions')

    def validate(self, attrs):
        """
        Ensures a user cannot be assigned multiple times to the same investment account
        with the same permission level.
        """
        users = attrs.get('users')
        if users:
            account_user_set = []
            for user in users:
                permission_level = self.context.get('permission_level')
                if (user, permission_level) in account_user_set:
                    raise serializers.ValidationError(
                        "A user cannot have the same permission level for an investment account multiple times."
                    )
                account_user_set.append((user, permission_level))
        return attrs


class AccountUserSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all())
    account = serializers.PrimaryKeyRelatedField(queryset=InvestmentAccount.objects.all())

    class Meta:
        model = AccountUser
        fields = ('id', 'user', 'account', 'permission_level')
        validators = [
            UniqueTogetherValidator(queryset=AccountUser.objects.all(), fields=('user', 'account')),
        ]