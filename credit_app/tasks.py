import pandas as pd
from decimal import Decimal
from celery import shared_task
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from .models import User, Billing

@shared_task
def calculate_credit_score(user_id):
    user = User.objects.get(unique_user_id=user_id)
    df = pd.read_csv(settings.BASE_DIR / 'transactions.csv')
    df_user = df[df['AADHAR ID']==user.aadhar_id]
    df_user['signed'] = df_user.apply(lambda row: row['Amount'] if row['Transaction_type']=='CREDIT' else -row['Amount'], axis=1)
    balance = df_user['signed'].sum()
    if balance >= 1000000:
        score = 900
    elif balance <= 10000:
        score = 300
    else:
        score = 300 + int((balance - 10000)//15000)*10
    user.credit_score = score
    user.save()

@shared_task
def run_billing_cycle():
    today = timezone.now().date()
    users = User.objects.filter(created_at__lte=today - timedelta(days=30))
    for user in users:
        last = user.billings.order_by('-billing_date').first()
        next_bill = (last.billing_date + timedelta(days=30)) if last else (user.created_at.date() + timedelta(days=30))
        if next_bill == today:
            due = today + timedelta(days=15)
            # calculate min due
            bal = sum([t.amount if t.transaction_type=='CREDIT' else -t.amount for t in user.transactions.all()])
            apr = Decimal('0.12')
            daily = (apr/Decimal('365')).quantize(Decimal('0.001'))
            # interest for billing cycle
            interest = (daily * Decimal('30') * bal).quantize(Decimal('0.01'))
            min_due = (bal*Decimal('0.03') + interest).quantize(Decimal('0.01'))
            Billing.objects.create(user=user, billing_date=today, due_date=due, min_due=min_due) 