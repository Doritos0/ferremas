from django.urls import path
from .views import index, initiate_payment, confirm_payment, agregar_producto, eliminar_producto, restar_producto, limpiar_compra

urlpatterns = [
    path('', index, name="index"),
    path('initiate/', initiate_payment, name='initiate_payment'),
    path('confirm/', confirm_payment, name='confirm_payment'),
    path ('agregar/<id_producto>/', agregar_producto, name="agregar_producto"),
    path ('eliminar/<id_producto>/', eliminar_producto, name="eliminar"),
    path ('restar/<id_producto>/', restar_producto, name="restar"),
    path ('limpiar/', limpiar_compra, name="limpiar"),
]