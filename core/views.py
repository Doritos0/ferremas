from django.shortcuts import render
from .models import Herramienta
from .utils import cambio_moneda

from django.views.decorators.csrf import csrf_exempt

#VARIABLES CAMBIO MONEDA
dolar=int(float(cambio_moneda("F073.TCO.PRE.Z.D")))
euro=int(float(cambio_moneda("F072.CLP.EUR.N.O.D")))


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