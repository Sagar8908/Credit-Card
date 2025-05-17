from rest_framework import serializers
from .models import User, Loan, EMI, Payment, Billing

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['aadhar_id', 'name', 'email', 'annual_income']

class LoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = ['loan_type', 'principal', 'interest_rate', 'term_period', 'disbursement_date']

class PaymentSerializer(serializers.Serializer):
    loan_id = serializers.UUIDField()
    amount = serializers.DecimalField(max_digits=12, decimal_places=2)

class StatementSerializer(serializers.Serializer):
    loan_id = serializers.UUIDField()

class BillingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Billing
        fields = ['billing_date', 'due_date', 'min_due', 'paid_amount'] 