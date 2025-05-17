import uuid
from decimal import Decimal
from django.db import models

class User(models.Model):
    unique_user_id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    aadhar_id = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    annual_income = models.DecimalField(max_digits=12, decimal_places=2)
    credit_score = models.IntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.aadhar_id})"

class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')
    date = models.DateField()
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    TRANSACTION_TYPE = [('DEBIT','DEBIT'), ('CREDIT','CREDIT')]
    transaction_type = models.CharField(choices=TRANSACTION_TYPE, max_length=6)

    def __str__(self):
        return f"{self.transaction_type} - {self.amount} on {self.date}"

class Loan(models.Model):
    LOAN_TYPE_CHOICES = [('CC','CREDIT_CARD')]
    loan_id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='loans')
    loan_type = models.CharField(choices=LOAN_TYPE_CHOICES, max_length=2)
    principal = models.DecimalField(max_digits=12, decimal_places=2)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)
    term_period = models.PositiveIntegerField()  # months
    disbursement_date = models.DateField()
    emi_amount = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"{self.loan_type} - {self.principal} for {self.user.name}"

class EMI(models.Model):
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE, related_name='emis')
    due_date = models.DateField()
    amount_due = models.DecimalField(max_digits=12, decimal_places=2)
    paid = models.BooleanField(default=False)

    def __str__(self):
        return f"EMI {self.due_date} - {self.amount_due} ({'Paid' if self.paid else 'Unpaid'})"

class Payment(models.Model):
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE, related_name='payments')
    date = models.DateField(auto_now_add=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"Payment {self.amount} on {self.date}"

class Billing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='billings')
    billing_date = models.DateField()
    due_date = models.DateField()
    min_due = models.DecimalField(max_digits=12, decimal_places=2)
    paid_amount = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))

    def __str__(self):
        return f"Bill {self.billing_date} - Min Due: {self.min_due}"
