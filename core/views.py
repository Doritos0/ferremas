

from django.shortcuts import render
from .utils import cambio_moneda
import requests
from django.views.decorators.csrf import csrf_exempt

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

    url = 'http://127.0.0.1:8001/lista_productos/'
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            productos = [type('', (object,), item)() for item in data]
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

            return render(request, 'core/index.html', {'herra': productos})
        else:
            print('Error al consultar la API')
            return render(request, 'core/error.html')
    except Exception as e:
        print('Ocurrió un error:', e)
        return render(request, 'core/error.html')
