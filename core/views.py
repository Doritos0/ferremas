from django.shortcuts import render
from .utils import cambio_moneda
import requests
from django.views.decorators.csrf import csrf_exempt

from datetime import datetime


#VARIABLES CAMBIO MONEDA
dolar=int(float(cambio_moneda("F073.TCO.PRE.Z.D")))
euro=int(float(cambio_moneda("F072.CLP.EUR.N.O.D")))

#CLASES CREADAS PARA FACILITAR HTML
class Valores:
    def __init__(self, id_producto, valor):
        self.id_producto = id_producto
        self.valor = valor

class Stocks:
    def __init__(self, id_producto, cantidad):
        self.id_producto = id_producto
        self.cantidad = cantidad

def index(request):

    fecha_actual = datetime.now().strftime('%Y-%m-%d')

    url = 'http://127.0.0.1:8001/'
    url_productos = url+'lista_productos/'
    url_tipos = url+'lista_tipos/'
    url_stocks = url+'lista_stocks/'
    url_precios = url+'lista_precios/'

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

            #LISTA_PRECIOS QUE LE PASARE AL HTML
            lista_precios = []
            lista_stocks = []

            #CREACION LISTA CON IDS QUE SI TIENEN PRECIO // PARA LA EXCEPCION DONDE UN PRODUCTO NO TENGA PRECIO REGISTRADO
            lista_idconprecios = []
            lista_idconstocks = []

            #LISTA ID_PRODUCTOS PARA AGREGARLE UN PRECIO / STOCKS A LOS QUE NO LO TIENEN
            lista_idprod = []

            productos = [type('', (object,), item)() for item in data_productos]
            tipos = [type('', (object,), item)() for item in data_tipos]
            stocks = [type('', (object,), item)() for item in data_stocks]
            precios = [type('', (object,), item)() for item in data_precios]

            #AGREGO TODOS LOS PRODUCTOS A UNA LISTA PARA REALIZAR LA VERIFICACION DE PRECIOS Y STOCKS
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

                        #MANEJO DE PRECIOS PRODUCTOS QUE SI TIENEN PRECIO
            for p in productos:
                for n in precios:
                    if n.id_producto == p.id_producto:
                        if fecha_actual > n.fec_ini and fecha_actual < n.fec_ter:
                            valores = Valores(n.id_producto, n.precio)
                            lista_precios.append(valores)
                            print("SE AGREGO UN PRECIO CORRECTO A LA LISTA 💙💙")
                        else:
                            print("ESTE PRECIO NO ES VALIDO AHORA MISMO❤️❤️")
                            valores = Valores(p.nombre, "Sin Precio")
                            lista_precios.append(valores)
                        
                        #MANEJO DE STOCKS PRODUCTOS QUE SI TIENE STOCK
            for p in productos:
                for n in stocks:
                    if n.id_producto == p.id_producto:
                        print("Este Producto si tiene un stocks registrado")
                        stock=Stocks(n.id_producto, n.cantidad)
                        lista_stocks.append(stock)

            #ESTAS ID TIENEN PRECIO
            for n in lista_precios:
                lista_idconprecios.append(n.id_producto)

            #ESTAS ID TIENEN STOCK REGISTRADO
            for n in lista_stocks:
                lista_idconstocks.append(n.id_producto)
            print("LISTA PRODUCTOS CON STOCK REGISTRADO")
            print(lista_idconstocks)



            #SI PRECIOS ES VACIO, LE AGREGA A TODOS LOS PRODUCTOS UN SIN PRECIO
            if not precios:
                for n in productos:
                    print("ESTO SE MOSTRADA CUANDO NO HAYAN PRECIOS INGRESADOS")
                    valores = Valores(n.id_producto, "Sin Precio")
                    lista_precios.append(valores)
            #SI PRECIO NO ESTA VACIO, VERIFICA SI TIENEN PRECIO, Y SI NO TIENE UN
            #PRECIO REGISTRADO LES ASIGNA SIN PRECIO
            else:
                for p in lista_idprod:
                    if p in lista_idconprecios:
                        print("Esto Tiene Precio 💙")
                    else:
                        #print("ESTO NO TIENE PRECIO, SE LE ASIGNA SIN PRECIO ❤️")
                        valores = Valores(p, "Sin Precio")
                        lista_precios.append(valores)
                

            # SI STOCKS ES VACIO, LE AGREGA A TODOS SIN STOCKS
            if not stocks:
                stock=Stocks("Sin ID", "Sin Stock")
                lista_stocks.append(stock)
            #SI STOCKS NO ESTA VACIO, VERIFICA SI TIENEN UN STOCK REGISTRADO, Y SI NO TIENE UN
            #STOCK REGISTRADO LES ASIGNA SIN STOCK
            else:
                for p in lista_idprod:
                    print("ESTOS SON LOS IDS DE PRODUCTOS ESTE MENSAJE DEBERIA SALIR 3 VECES")
                    print(p)
                    if p in lista_idconstocks:
                        print("Esto Tiene Stock 💙")
                    else:
                        print("Esto No tiene Stock Registrado")
                        stock=Stocks(p, "Sin Stock")
                        lista_stocks.append(stock)
            
            print("💜💜💜💜")
            for n in lista_stocks:
                print("ID ",n.id_producto," CANTIDAD ",n.cantidad)

            return render(request, 'core/index.html', {'herra': productos, 'tipos':tipos, 'stocks': lista_stocks,'precios': lista_precios, 'fecha_actual': fecha_actual})
        else:
            print('Error al consultar la API')
            return render(request, 'core/error.html')
    except Exception as e:
        print('Ocurrió un error:', e)
        return render(request, 'core/error.html')