from django.urls import path
from .views import index, webpay_init, webpay_return, webpay_final

urlpatterns = [
    path('', index, name="index"),
    path('webpay_init/', webpay_init, name="webpay_init"),
    path('webpay_return/', webpay_return, name="webpay_return"),
    path('webpay_final/', webpay_final, name="webpay_final"),
]