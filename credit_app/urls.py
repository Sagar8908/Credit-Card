from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.RegisterUser.as_view(), name='register'),
    path('apply-loan/', views.ApplyLoan.as_view(), name='apply-loan'),
    path('payment/', views.MakePayment.as_view(), name='payment'),
    path('statement/', views.GetStatement.as_view(), name='statement'),
] 