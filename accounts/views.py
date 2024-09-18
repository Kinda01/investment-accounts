from django.db import models  # Import models to use aggregation functions like Sum
from rest_framework import viewsets, permissions, status, serializers  # Import serializers
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import InvestmentAccount, Transaction, AccountUser, CustomUser  # Import models
from .serializers import (  # Import all serializers here
    InvestmentAccountSerializer,
    TransactionSerializer,
    InvestmentAccountDetailSerializer,
)


class InvestmentAccountViewSet(viewsets.ModelViewSet):
    queryset = InvestmentAccount.objects.all()
    serializer_class = InvestmentAccountSerializer

    def get_permissions(self):
        """Defines permissions based on request method and user role."""
        if self.request.method in permissions.SAFE_METHODS:
            return [permissions.IsAuthenticatedOrReadOnly()]

        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        """Filters investment accounts based on user permissions."""
        user = self.request.user
        if user.is_superuser:
            return self.queryset
        return InvestmentAccount.objects.filter(accountuser__user=user)

    @action(detail=True, methods=['get'])
    def details(self, request, pk=None):
        """Provides detailed information for an investment account, including transactions."""
        account = self.get_object()
        serializer = InvestmentAccountDetailSerializer(account)
        return Response(serializer.data)


class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        """Ensures the user has permission to create transactions for the investment account."""
        account = serializer.validated_data['account']
        user = self.request.user
        if not account.accountuser_set.filter(user=user, permission_level__in=['ADMIN', 'TRANSACTION_POSTER']):
            raise serializers.ValidationError("You don't have permission to create transactions for this account.")
        serializer.save()


class UserTransactionListView(viewsets.ReadOnlyModelViewSet):
    """Admin endpoint to view all transactions for a user with a date range filter."""
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAdminUser]

    def get_queryset(self):
        user_id = self.kwargs['user_pk']
        start_date = self.request.query_params.get('start_date', None)
        end_date = self.request.query_params.get('end_date', None)
        queryset = Transaction.objects.filter(account__accountuser__user=user_id)
        if start_date and end_date:
            queryset = queryset.filter(date__range=(start_date, end_date))
        return queryset.annotate(total_balance=models.Sum('amount'))  # Using models.Sum now works correctly
