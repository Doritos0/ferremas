from django.shortcuts import render
from .models import Herramienta
from .utils import cambio_moneda

from django.views.decorators.csrf import csrf_exempt

# Create your views here.
@csrf_exempt
def index (request):
    herramientas = Herramienta.objects.all()
    if request.method == 'POST':
        moneda = request.POST.get('moneda')
        print("valor moneda: ",moneda)
        if moneda == '2': 
            cod = "F073.TCO.PRE.Z.D"
            for herramienta in herramientas:
                herramienta.precio = round(herramienta.precio / int(float(cambio_moneda(cod))), 2)
                print("precio: ",herramienta.precio)
        elif moneda == '3': 
            cod = "F072.CLP.EUR.N.O.D"
            for herramienta in herramientas:
                herramienta.precio = round(herramienta.precio / int(float(cambio_moneda(cod))), 2)
                print("precio: ",herramienta.precio)
        else :
            for herramienta in herramientas:
                herramienta.precio = herramienta.precio
    return render(request, 'core/index.html', {'herra': herramientas})