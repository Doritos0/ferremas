from django.shortcuts import render, redirect
from .utils import cambio_moneda
import requests
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from django.template.loader import render_to_string

from core.compra import Compra

from datetime import datetime

#IMPORTS PARA TRANSBANK
import uuid
from django.shortcuts import render, redirect
from django.http import HttpResponse
from transbank.webpay.webpay_plus.transaction import Transaction

from .transbank_config import *

# VARIABLES CAMBIO MONEDA
dolar = int(float(cambio_moneda("F073.TCO.PRE.Z.D")))
euro = int(float(cambio_moneda("F072.CLP.EUR.N.O.D")))

# CLASES CREADAS PARA FACILITAR HTML
class Valores:
    def __init__(self, id_producto, valor):
        self.id_producto = id_producto
        self.valor = valor

class Stocks:
    def __init__(self, id_producto, cantidad):
        self.id_producto = id_producto
        self.cantidad = cantidad

url = 'http://127.0.0.1:8001/'
url_productos = url + 'lista_productos/'
url_tipos = url + 'lista_tipos/'
url_stocks = url + 'lista_stocks/'
url_precios = url + 'lista_precios/'

try:
        response_productos = requests.get(url_productos)
        response_tipos = requests.get(url_tipos)
        response_stocks = requests.get(url_stocks)
        response_precios = requests.get(url_precios)

        if response_productos.status_code == 200:
            data_productos = response_productos.json()
            data_tipos = response_tipos.json()
            data_stocks = response_stocks.json()
            data_precios = response_precios.json()

            productos = [type('', (object,), item)() for item in data_productos]
            tipos = [type('', (object,), item)() for item in data_tipos]
            stocks = [type('', (object,), item)() for item in data_stocks]
            precios = [type('', (object,), item)() for item in data_precios]

except Exception as e:
        print('Ocurrió un error:', e)


fecha_actual = datetime.now().strftime('%Y-%m-%d')

@csrf_exempt
def index(request):
    fecha_actual = datetime.now().strftime('%Y-%m-%d')

    url = 'http://127.0.0.1:8001/'
    url_productos = url + 'lista_productos/'
    url_tipos = url + 'lista_tipos/'
    url_stocks = url + 'lista_stocks/'
    url_precios = url + 'lista_precios/'

    try:
        response_productos = requests.get(url_productos)
        response_tipos = requests.get(url_tipos)
        response_stocks = requests.get(url_stocks)
        response_precios = requests.get(url_precios)

        if response_productos.status_code == 200:
            data_productos = response_productos.json()
            data_tipos = response_tipos.json()
            data_stocks = response_stocks.json()
            data_precios = response_precios.json()

            # LISTA_PRECIOS QUE LE PASARE AL HTML
            lista_precios = []
            lista_stocks = []

            # CREACION LISTA CON IDS QUE SI TIENEN PRECIO // PARA LA EXCEPCION DONDE UN PRODUCTO NO TENGA PRECIO REGISTRADO
            lista_idconprecios = []
            lista_idconstocks = []

            # LISTA ID_PRODUCTOS PARA AGREGARLE UN PRECIO / STOCKS A LOS QUE NO LO TIENEN
            lista_idprod = []

            productos = [type('', (object,), item)() for item in data_productos]
            tipos = [type('', (object,), item)() for item in data_tipos]
            stocks = [type('', (object,), item)() for item in data_stocks]
            precios = [type('', (object,), item)() for item in data_precios]

            # AGREGO TODOS LOS PRODUCTOS A UNA LISTA PARA REALIZAR LA VERIFICACION DE PRECIOS Y STOCKS
            for n in productos:
                lista_idprod.append(n.id_producto)

            # MANEJO DEL CAMBIO DE MONEDA
            if request.method == 'POST':
                moneda = request.POST.get('moneda')
                if moneda == '2':
                    for n in precios:
                        n.precio = round((n.precio / dolar), 2)
                elif moneda == '3':
                    for n in precios:
                        n.precio = round((n.precio / euro), 2)

            # MANEJO DE PRECIOS PRODUCTOS QUE SI TIENEN PRECIO
            for p in productos:
                for n in precios:
                    if n.id_producto == p.id_producto:
                        if fecha_actual > n.fec_ini and fecha_actual < n.fec_ter:
                            valores = Valores(n.id_producto, n.precio)
                            lista_precios.append(valores)

            # MANEJO DE STOCKS PRODUCTOS QUE SI TIENE STOCK
            for p in productos:
                for n in stocks:
                    if n.id_producto == p.id_producto:
                        stock = Stocks(n.id_producto, n.cantidad)
                        lista_stocks.append(stock)

            # ESTAS ID TIENEN PRECIO
            for n in lista_precios:
                lista_idconprecios.append(n.id_producto)

            # ESTAS ID TIENEN STOCK REGISTRADO
            for n in lista_stocks:
                lista_idconstocks.append(n.id_producto)

            # SI PRECIOS ES VACIO, LE AGREGA A TODOS LOS PRODUCTOS UN SIN PRECIO
            if not precios:
                for n in productos:
                    valores = Valores(n.id_producto, "Sin Precio")
                    lista_precios.append(valores)
            else:
                for p in lista_idprod:
                    if p not in lista_idconprecios:
                        valores = Valores(p, "Sin Precio")
                        lista_precios.append(valores)

            # SI STOCKS ES VACIO, LE AGREGA A TODOS SIN STOCKS
            if not stocks:
                for n in productos:
                    stock = Stocks(n.id_producto, "Sin Stock")
                    lista_stocks.append(stock)
            else:
                for p in lista_idprod:
                    if p not in lista_idconstocks:
                        stock = Stocks(p, "Sin Stock")
                        lista_stocks.append(stock)

            # Verifica si la solicitud es AJAX
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                html = render_to_string('core/productos.html', {'herra': productos, 'precios': lista_precios, 'stocks': lista_stocks})
                return JsonResponse({'html': html})

            return render(request, 'core/index.html', {'herra': productos, 'tipos': tipos, 'stocks': lista_stocks, 'precios': lista_precios, 'fecha_actual': fecha_actual})
        else:
            return render(request, 'core/error.html')
    except Exception as e:
        print('Ocurrió un error:', e)
        return render(request, 'core/error.html')

def initiate_payment(request):

    if not request.session.session_key:
        request.session.save()
        
    total_compra = request.session.get('total_compra', 0) 
    print(total_compra)

    if total_compra == 0:
        print("El carro esta vacio")
        return redirect("index")

    orden = str(uuid.uuid4())
    buy_order = orden[:4] # Identificador único de la transacción
    session_id = request.session.session_key[:4]  # Identificador de sesión
    amount = total_compra    # Monto de la transacción
    return_url = request.build_absolute_uri('/confirm/')  # URL de retorno

    print("BUY_OrDER :",buy_order)

    transaction = Transaction()  # Crear instancia de Transaction

    try:
        response = transaction.create(buy_order=buy_order, session_id=session_id, amount=amount, return_url=return_url)
        return redirect(response['url'] + '?token_ws=' + response['token'])
    except Exception as e:
        return HttpResponse(f"Error: {e}")

def confirm_payment(request):
    token = request.GET.get('token_ws')
    
    if not token:
        return HttpResponse("Token no encontrado en la solicitud.")

    transaction = Transaction()  # Crear instancia de Transaction

    try:
        response = transaction.commit(token=token)
        if response['status'] == 'AUTHORIZED':
            return render(request, 'core/success.html', {'response': response})
        else:
            return render(request, 'core/failure.html', {'response': response})
    except Exception as e:
        return HttpResponse(f"Error: {e}")
    

#FUNCIONES PARA EL FUNCIONAMIENTO DE LA COMPRA
def agregar_producto(request, id_producto):
    producto = None
    precio = None
    compra = Compra(request)
    numero = int(id_producto)
    for p in productos:
        if p.id_producto == numero:
            print("LLEGAAAAAA")
            print(p.nombre)
            producto = p.nombre

    for n in precios:
        if n.id_producto == numero:
            precio = n.precio

    compra.agregar(id_producto, producto, precio)
    return redirect("index")

def eliminar_producto(request, id_producto):
    compra = Compra(request)
    compra.eliminar(id_producto)
    return redirect("index")

def restar_producto(request, id_producto):
    print("VAMOOOOOOOO")
    producto = None
    precio = None
    compra = Compra(request)
    numero = int(id_producto)
    for p in productos:
        if p.id_producto == numero:
            producto = p.nombre

    for n in precios:
        if n.id_producto == numero:
            print(n.precio, "PRECIOOOOOOO")
            precio = n.precio

    compra.restar(numero, precio)
    return redirect("index")

def limpiar_compra (request):
    compra = Compra(request)
    compra.limpiar()
    return redirect("index")