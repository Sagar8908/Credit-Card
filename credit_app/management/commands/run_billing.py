from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal
from credit_app.models import User, Billing

class Command(BaseCommand):
    help = 'Run billing cycle'

    def handle(self, *args, **options):
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
                
                Billing.objects.create(
                    user=user,
                    billing_date=today,
                    due_date=due,
                    min_due=min_due
                )
                self.stdout.write(
                    self.style.SUCCESS(f'Created billing for user {user.name} with min due {min_due}')
                ) 