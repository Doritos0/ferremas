import requests
from datetime import datetime

fecha_actual = datetime.now()
fecha_actual = fecha_actual.strftime("%Y-%m-%d")

def cambio_moneda(codigo):
    url = 'https://si3.bcentral.cl/SieteRestWS/SieteRestWS.ashx?user=meyesblue@gmail.com&pass=ASDFghjk1&firstdate='+fecha_actual+'&timeseries='+codigo+'&function=GetSeries'

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        valor = data['Series']['Obs'][0]['value']
        print("💚 ", valor)
        return valor
    else:
        print('Error al consultar la API del Banco Central de Chile')

