

from django.shortcuts import render
from .utils import cambio_moneda
import requests
from django.views.decorators.csrf import csrf_exempt

from datetime import datetime

#VARIABLES CAMBIO MONEDA
dolar=int(float(cambio_moneda("F073.TCO.PRE.Z.D")))
euro=int(float(cambio_moneda("F072.CLP.EUR.N.O.D")))

"""
# Create your views here.
@csrf_exempt
def index (request):
    herramientas = Herramienta.objects.all()
    if request.method == 'POST':
        moneda = request.POST.get('moneda')
        print("valor moneda: ",moneda)
        if moneda == '2': 
            for herramienta in herramientas:
                herramienta.precio = round((herramienta.precio / dolar),2)
                print("precio: ",herramienta.precio)
        elif moneda == '3': 
            for herramienta in herramientas:
                herramienta.precio = round((herramienta.precio / euro),2)
                print("precio: ",herramienta.precio)
        else :
            for herramienta in herramientas:
                herramienta.precio = herramienta.precio
    return render(request, 'core/index.html', {'herra': herramientas})

    """

def index(request):

    fecha_actual = datetime.now().strftime('%Y/%m/%d')

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
            
            productos = [type('', (object,), item)() for item in data_productos]
            tipos = [type('', (object,), item)() for item in data_tipos]
            stocks = [type('', (object,), item)() for item in data_stocks]
            precios = [type('', (object,), item)() for item in data_precios]

            if request.method == 'POST':
                moneda = request.POST.get('moneda')
                print("valor moneda: ",moneda)
                if moneda == '2': 
                    for herramienta in productos:
                        herramienta.precio = round((herramienta.precio / dolar),2)
                        print("precio: ",herramienta.precio)
                elif moneda == '3': 
                    for herramienta in productos:
                        herramienta.precio = round((herramienta.precio / euro),2)
                        print("precio: ",herramienta.precio)
                else :
                    for herramienta in productos:
                        herramienta.precio = herramienta.precio

            return render(request, 'core/index.html', {'herra': productos, 'tipos':tipos, 'stocks': stocks,'precios': precios, 'fecha_actual': fecha_actual})
        else:
            print('Error al consultar la API')
            return render(request, 'core/error.html')
    except Exception as e:
        print('Ocurrió un error:', e)
        return render(request, 'core/error.html')
