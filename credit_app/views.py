from django.shortcuts import render
from datetime import timedelta, date
from decimal import Decimal
from django.db import transaction
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from .models import User, Loan, EMI, Payment, Billing
from .serializers import UserSerializer, LoanSerializer, PaymentSerializer, StatementSerializer
from .tasks import calculate_credit_score

# Create your views here.

class RegisterUser(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            with transaction.atomic():
                user = serializer.save(aadhar_id=request.data['Aadhar ID'])
            calculate_credit_score.delay(str(user.unique_user_id))
            return Response({'unique_user_id': user.unique_user_id, 'error': None})
        return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class ApplyLoan(APIView):
    def post(self, request):
        data = request.data
        try:
            user = User.objects.get(unique_user_id=data['unique_user_id'])
        except User.DoesNotExist:
            return Response({'error':'User not found'}, status=400)
        
        if user.credit_score < 450 or user.annual_income < 150000:
            return Response({'error':'Eligibility criteria not met'}, status=400)
        
        if Decimal(data['loan_amount'])>5000:
            return Response({'error':'Loan amount too high'}, status=400)
        
        # EMI calc: principal per month + interest per month
        P = Decimal(data['loan_amount'])
        r = Decimal(data['interest_rate'])/Decimal('100')/Decimal('12')
        n = int(data['term_period'])
        emi = (P/n + P*r).quantize(Decimal('0.01'))
        
        monthly_income = user.annual_income/Decimal('12')
        if emi > monthly_income* Decimal('0.2'):
            return Response({'error':'EMI exceeds 20% monthly income'}, status=400)
        
        if (P*r) < 50:
            return Response({'error':'Monthly interest less than ₹50'}, status=400)
        
        disb_date = date.fromisoformat(data['disbursement_date'])
        loan = Loan.objects.create(
            user=user,
            loan_type='CC',
            principal=P,
            interest_rate=data['interest_rate'],
            term_period=n,
            disbursement_date=disb_date,
            emi_amount=emi
        )
        
        # schedule EMIs
        for i in range(1, n+1):
            due = disb_date + timedelta(days=30*i)
            EMI.objects.create(loan=loan, due_date=due, amount_due=emi)
        
        dues = [{'date': e.due_date, 'amount_due': e.amount_due} for e in loan.emis.all()]
        return Response({'loan_id':loan.loan_id, 'due_dates':dues, 'error':None})

class MakePayment(APIView):
    def post(self, request):
        ser = PaymentSerializer(data=request.data)
        if not ser.is_valid():
            return Response({'error':ser.errors}, status=400)
        
        data = ser.validated_data
        try:
            loan = Loan.objects.get(loan_id=data['loan_id'])
        except Loan.DoesNotExist:
            return Response({'error':'Loan not found'}, status=400)
        
        next_emi = loan.emis.filter(paid=False).order_by('due_date').first()
        if not next_emi:
            return Response({'error':'All EMIs paid'}, status=400)
        
        if loan.payments.filter(date=timezone.now().date(), amount=data['amount']).exists():
            return Response({'error':'Payment already recorded for today'}, status=400)
        
        if next_emi.due_date > timezone.now().date():
            return Response({'error':'Previous EMIs unpaid'}, status=400)
        
        amt = data['amount']
        if amt != next_emi.amount_due:
            # recalc future EMIs
            paid_amt = amt - (loan.principal/loan.term_period)
        
        next_emi.paid = True
        next_emi.save()
        Payment.objects.create(loan=loan, amount=amt)
        return Response({'error':None})

class GetStatement(APIView):
    def get(self, request):
        loan_id = request.query_params.get('loan_id')
        try:
            loan = Loan.objects.get(loan_id=loan_id)
        except Loan.DoesNotExist:
            return Response({'error':'Loan not found'}, status=400)
        
        past = []
        for pay in loan.payments.all():
            past.append({'date':pay.date,'amount_paid':pay.amount})
        
        upcoming = []
        for emi in loan.emis.filter(paid=False):
            upcoming.append({'date':emi.due_date,'amount_due':emi.amount_due})
        
        return Response({
            'past_transactions': past,
            'upcoming_transactions': upcoming,
            'error': None
        })
