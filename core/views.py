from django.shortcuts import render, redirect
from .utils import cambio_moneda, agregar, restar
import requests
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.template.loader import render_to_string
import json
from django.urls import reverse
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


fecha_actual = datetime.now().strftime('%Y-%m-%d')

def create(request):
    return render(request, 'core/create.html')

def nuevo_prod(request):
    if request.method == 'POST':
        url_producto = f'http://127.0.0.1:8001/lista_productos/'
        nombre = request.POST.get('nombre_producto')
        id_tipo = request.POST.get('tipo_producto')

        data = {'nombre':nombre, 'oferta': 0, 'porcentaje':0, 'id_tipo': id_tipo}

        response = requests.post(url_producto, data=data)

        if response.status_code == 201:
            producto = response.json()

            id_producto = producto.get('id_producto')

            url_stock = f'http://127.0.0.1:8001/lista_stocks/'
            url_precio = f'http://127.0.0.1:8001/lista_precios/'


            cantidad = request.POST.get('cantidad')
            precio = request.POST.get('precio')
            stock = {'id_producto': id_producto, 'cantidad': cantidad}
            precio_obj = {'id_producto': id_producto, 'fec_ini': '2024-07-01', 'fec_ter': '2024-07-31', 'precio': precio}

            response_stock = requests.post(url_stock, data=stock)
            response_precio = requests.post(url_precio, data=precio_obj)

            if response_stock.status_code and response_precio.status_code == 201:
                return redirect(crud)
            else:
                return redirect(crud)
        else:
            print("Salio mal")

    return redirect(crud)

def crud(request):
    url = 'http://127.0.0.1:8001/'
    url_productos = url + 'lista_productos/'

    
    try:
        response_productos = requests.get(url_productos)
        if response_productos.status_code == 200:
            data_productos = response_productos.json()
            
            return render(request, 'core/crud.html', {'data': data_productos})

    except Exception as e:
        print('Ocurrió un error:', e)
        return render(request, 'core/error.html')
    

def crud_eliminar(request, id):
    url = 'http://127.0.0.1:8001/detalle_producto/'+id
    print(url)
    response = requests.delete(url)


    if response.status_code == 204:  
        return HttpResponseRedirect(reverse('crud')) 
    else:
        return HttpResponse(f'Error al eliminar el producto: {response.status_code}', status=response.status_code)

def crud_modificar(request, id):
    url_producto = f'http://127.0.0.1:8001/detalle_producto/{id}'
    url_stock = f'http://127.0.0.1:8001/detalle_stock/{id}'
    url_precios = f'http://127.0.0.1:8001/detalle_precio/{id}'

    try:
        response_producto = requests.get(url_producto)
        response_stock = requests.get(url_stock)
        response_precios = requests.get(url_precios)

        if response_producto.status_code == 200:
            data_producto = response_producto.json()
            data_stock = response_stock.json()
            data_precio = response_precios.json()

            # Procesamiento de los datos recibidos...
            
            return render(request, 'core/modificar.html', {'producto': data_producto, 'stock': data_stock, 'precio': data_precio})
        else:
            return render(request, 'core/error.html')
    
    except json.JSONDecodeError as e:
        print(f'Error de decodificación JSON: {str(e)}')
        return render(request, 'core/error.html', {'error_message': 'Error al decodificar la respuesta JSON'})

    except requests.RequestException as e:
        print(f'Error en la solicitud HTTP: {str(e)}')
        return render(request, 'core/error.html', {'error_message': 'Error en la solicitud HTTP'})

    except Exception as e:
        print(f'Otro error: {str(e)}')
        return render(request, 'core/error.html', {'error_message': 'Error desconocido'})

def mod_nombre_prod(request, id):
    if request.method == 'POST':
        nuevo_nombre = request.POST.get('nombre')
        url_producto = f'http://127.0.0.1:8001/detalle_producto/{id}'
        payload = {'nombre': nuevo_nombre}
        response = requests.patch(url_producto, json=payload)

        if response.status_code == 200:
            return redirect('crud_modificar', id=id)
        else:
            return redirect('crud_modificar', id=id)
        
def mod_oferta_prod(request, id):
    if request.method == 'POST':
        # Obtener los datos del formulario
        oferta = request.POST.get('oferta')
        porcentaje = request.POST.get('porcentaje')

        
        payload = {'oferta': oferta, 'porcentaje':porcentaje}
        url_producto = f'http://127.0.0.1:8001/detalle_producto/{id}'

        
        response = requests.patch(url_producto, json=payload)

        if response.status_code == 200:
            return redirect('crud_modificar', id=id)
        else:
            return redirect('crud_modificar', id=id)

def mod_tipo_prod(request, id):
    if request.method == 'POST':
        id_tipo = request.POST.get('tipo_producto')
        print(id_tipo)
        url_producto = f'http://127.0.0.1:8001/detalle_producto/{id}'
        payload = {'id_tipo': id_tipo}
        response = requests.patch(url_producto, json=payload)

        if response.status_code == 200:
            return redirect('crud_modificar', id=id)
        else:
            return redirect('crud_modificar', id=id)
        
def mod_stock_prod(request, id):
    if request.method == 'POST':
        cantidad = request.POST.get('cantidad')
        url_stock = f'http://127.0.0.1:8001/detalle_stock/{id}'
        payload = {'cantidad': cantidad}
        response = requests.patch(url_stock, json=payload)

        if response.status_code == 200:
            return redirect('crud_modificar', id=id)
        else:
            return redirect('crud_modificar', id=id)
        
def mod_precio_prod(request, id):
    if request.method == 'POST':
        precio = request.POST.get('precio')
        url_precio = f'http://127.0.0.1:8001/detalle_precio/{id}'
        payload = {'precio': precio}
        response = requests.patch(url_precio, json=payload)

        if response.status_code == 200:
            return redirect('crud_modificar', id=id)
        else:
            return redirect('crud_modificar', id=id)


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

            #VARIABLE PARA VER SI HAY OFERTAS ACTIVAS

            ofertas = False

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
                if n.oferta == 1:
                    ofertas = True

            # MANEJO DE PRECIOS PRODUCTOS QUE SI TIENEN PRECIO
            for p in productos:
                for n in precios:
                    if n.id_producto == p.id_producto:
                        if fecha_actual >= n.fec_ini and fecha_actual <= n.fec_ter:
                            if p.oferta == 1:
                                n.precio = n.precio - (n.precio * (p.porcentaje/100))
                                valores = Valores(n.id_producto, n.precio)
                                lista_precios.append(valores)
                            else:
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

            
            # MANEJO DEL CAMBIO DE MONEDA
            if request.method == 'POST':
                moneda = request.POST.get('moneda')
                if moneda == '2':
                    for n in lista_precios:
                        n.valor = round((n.valor / dolar), 2)
                elif moneda == '3':
                    for n in lista_precios:
                        n.valor = round((n.valor / euro), 2)

            

            # Verifica si la solicitud es AJAX
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                html = render_to_string('core/productos.html', {'herra': productos, 'precios': lista_precios, 'stocks': lista_stocks})
                return JsonResponse({'html': html})

            return render(request, 'core/index.html', {'herra': productos, 'tipos': tipos, 'stocks': lista_stocks, 'precios': lista_precios, 'fecha_actual': fecha_actual, 'oferta' : ofertas})
        else:
            return render(request, 'core/error.html')
    except Exception as e:
        print('Ocurrió un error:', e)
        return render(request, 'core/error.html')
    
def envio(request):
    total_compra = request.session.get('total_compra', 0)
    if total_compra == 0:
        print("El carro esta vacio")
        return redirect("index")
    return render(request, 'core/envio.html')

def initiate_payment(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        direccion = data.get('direccion', 'Sin Direccion')
        correo = data.get('correo')

        if not correo:
            return JsonResponse({'status': 'ERROR', 'message': 'Correo es requerido'})

        if not request.session.session_key:
            request.session.save()

        total_compra = request.session.get('total_compra', 0)
        if total_compra == 0:
            return JsonResponse({'status': 'ERROR', 'message': 'El carro esta vacio'})

        orden = str(uuid.uuid4())
        buy_order = orden[:4]
        session_id = request.session.session_key[:4]
        amount = total_compra
        return_url = request.build_absolute_uri(reverse('confirm_payment'))

        transaction = Transaction()

        try:
            response = transaction.create(buy_order=buy_order, session_id=session_id, amount=amount, return_url=return_url)
            # Store the order details in the session for later use
            request.session['order_details'] = {
                "direccion": direccion,
                "correo": correo,
                "detalle_pedido": str(json.dumps(request.session.get('compra', {}))),
                "fecha_pedido": str(datetime.now().date()),
                "tipo_pedido": 0 if direccion == 'Sin Direccion' else 1,
                "estado_pedido": 'En proceso',
                "total": amount
            }
            return JsonResponse({'status': 'AUTHORIZED', 'redirect_url': response['url'] + '?token_ws=' + response['token']})
        except Exception as e:
            return JsonResponse({'status': 'ERROR', 'message': str(e)})

    return JsonResponse({'status': 'ERROR', 'message': 'Método no permitido'})

def confirm_payment(request):
    token = request.GET.get('token_ws')

    if not token:
        return HttpResponse("Token no encontrado en la solicitud.")

    transaction = Transaction()

    try:
        response = transaction.commit(token=token)
        if response['status'] == 'AUTHORIZED':
            compra = Compra(request)
            productos_en_carrito = compra.compra  # Diccionario de productos en el carrito

            url_base = 'http://127.0.0.1:8001/'
            headers = {
                'Content-Type': 'application/json'
            }

            # Iterar sobre los productos en el carrito para actualizar el stock
            for id_producto, detalles in productos_en_carrito.items():
                cantidad_comprada = detalles['Unidades']
                id_stock = detalles.get('id_stock')  # Suponiendo que id_stock se ha guardado en el carrito

                if id_stock:
                    # Obtener el stock actual del producto
                    url_get_stock = f'{url_base}detalle_stock/{id_stock}'
                    response_get = requests.get(url_get_stock)
                    if response_get.status_code == 200:
                        data = response_get.json()
                        stock_actual = data['cantidad']

                        # Calcular el nuevo stock
                        nuevo_stock = max(0, stock_actual - cantidad_comprada)
                        
                        # Actualizar el stock
                        url_mod_stock = f'{url_base}detalle_stock/{id_stock}'
                        data = {
                            'cantidad': nuevo_stock  # Datos que deseas actualizar
                        }
                        response_stock = requests.patch(url_mod_stock, json=data, headers=headers)
                        if response_stock.status_code == 400:
                            print(f'Error al actualizar el stock para el producto {id_producto}')
                        else:
                            print(f'Stock actualizado para el producto {id_producto}')
                    else:
                        print(f'Error al obtener el stock actual para el producto {id_producto}')

            order_details = request.session.get('order_details', {})
            if not order_details:
                return HttpResponse("No se encontraron detalles de la orden.")

            print(order_details)

            url_api = 'http://127.0.0.1:8001/lista_pedidos/'
            headers = {
                'Content-Type': 'application/json'
            }

            response_api = requests.post(url_api, json=order_details, headers=headers)
            if response_api.status_code in [200, 201]:
                return render(request, 'core/success.html', {'response': response,'response_stock' : response_stock})
            else:
                return HttpResponse("Error al enviar los detalles de la orden a la API.")

        else:
            return render(request, 'core/failure.html', {'response': response})
    except Exception as e:
        return HttpResponse(f"Error: {e}")
    

def agregar_producto(request, id_producto):
    agregar(request, id_producto)
    previous_url = request.META.get('HTTP_REFERER', 'index')
    return redirect(previous_url)


def eliminar_producto(request, id_producto):
    compra = Compra(request)
    compra.eliminar(id_producto)
    return redirect("index")

def restar_producto(request, id_producto):
    restar(request, id_producto)
    previous_url = request.META.get('HTTP_REFERER', 'index')
    return redirect(previous_url)

def limpiar_compra (request):
    compra = Compra(request)
    compra.limpiar()
    return redirect("index")

def volver_de_compra(request):
    compra = Compra(request)
    compra.limpiar()
    return redirect("index")