from django.contrib import admin
from .models import User, Transaction, Loan, EMI, Payment, Billing

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('name', 'aadhar_id', 'email', 'annual_income', 'credit_score', 'created_at')
    search_fields = ('name', 'aadhar_id', 'email')
    list_filter = ('credit_score', 'created_at')

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'amount', 'transaction_type')
    list_filter = ('transaction_type', 'date')
    search_fields = ('user__name', 'user__aadhar_id')

@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    list_display = ('user', 'loan_type', 'principal', 'interest_rate', 'term_period', 'disbursement_date')
    list_filter = ('loan_type', 'disbursement_date')
    search_fields = ('user__name', 'user__aadhar_id')

@admin.register(EMI)
class EMIAdmin(admin.ModelAdmin):
    list_display = ('loan', 'due_date', 'amount_due', 'paid')
    list_filter = ('paid', 'due_date')
    search_fields = ('loan__user__name', 'loan__user__aadhar_id')

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('loan', 'date', 'amount')
    list_filter = ('date',)
    search_fields = ('loan__user__name', 'loan__user__aadhar_id')

@admin.register(Billing)
class BillingAdmin(admin.ModelAdmin):
    list_display = ('user', 'billing_date', 'due_date', 'min_due', 'paid_amount')
    list_filter = ('billing_date', 'due_date')
    search_fields = ('user__name', 'user__aadhar_id')
