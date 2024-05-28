from django.urls import path
from .views import index, initiate_payment, confirm_payment

urlpatterns = [
    path('', index, name="index"),
    path('initiate/', initiate_payment, name='initiate_payment'),
    path('confirm/', confirm_payment, name='confirm_payment'),
]