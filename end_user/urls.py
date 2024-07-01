from django.urls import path
from .views import *

urlpatterns = [
    path('user_billing/', UserBillingAPIView.as_view(), name='user-billing'),
    path('generate_bill/', generate_bill, name='billing'),
    path('generate_bill/<int:id>/', billing_page, name='billing'),
]

