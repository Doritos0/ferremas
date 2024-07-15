from django.urls import path
from .views import nuevo_prod, create, mod_oferta_prod, mod_precio_prod, index, initiate_payment, confirm_payment, agregar_producto, eliminar_producto, restar_producto, limpiar_compra, volver_de_compra, envio, crud, crud_eliminar, crud_modificar, mod_nombre_prod, mod_tipo_prod, mod_stock_prod

urlpatterns = [
    path('', index, name="index"),
    path('initiate/', initiate_payment, name='initiate_payment'),
    path('confirm/', confirm_payment, name='confirm_payment'),
    path ('agregar/<id_producto>/', agregar_producto, name="agregar_producto"),
    path ('eliminar/<id_producto>/', eliminar_producto, name="eliminar"),
    path ('restar/<id_producto>/', restar_producto, name="restar"),
    path ('limpiar/', limpiar_compra, name="limpiar"),
    path ('envio/', envio, name="envio"),
    path ('volver_de_compra/', volver_de_compra, name="volver_de_compra"),
    path ('crud/', crud, name="crud"),
    path ('create/', create, name="create"),
    path ('nuevo_prod/', nuevo_prod, name="nuevo_prod"),
    path ('crud_eliminar/<id>', crud_eliminar, name="crud_eliminar"),
    path ('crud_modificar/<id>', crud_modificar, name="crud_modificar"),
    path ('mod_nombre_prod/<id>', mod_nombre_prod, name="mod_nombre_prod"),
    path ('mod_tipo_prod/<id>', mod_tipo_prod, name="mod_tipo_prod"),
    path ('mod_stock_prod/<id>', mod_stock_prod, name="mod_stock_prod"),
    path ('mod_precio_prod/<id>', mod_precio_prod, name="mod_precio_prod"),
    path ('mod_oferta_prod/<id>', mod_oferta_prod, name="mod_oferta_prod"),
]