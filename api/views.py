import json
from django.http import JsonResponse
from django.shortcuts import redirect, render

# CREACION DE API
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.parsers import JSONParser

#IMPORTAMOS EL MODELO
from .models import Productos
from .serializers import ProductoSerializer

# Create your views here.

@csrf_exempt
@api_view(['GET', 'POST'])
def lista_productos (request):
    if request.method == 'GET':
        query = Productos.objects.all()
        serializer = ProductoSerializer(query, many = True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = ProductoSerializer(data = request.data)
        print("❤️ ", serializer)
        if serializer.is_valid():
            id = request.POST.get('id_producto', None)
            print(id)
            if id in Productos.objects.values_list('id_producto', flat=True):
                print("💙 ESTE PRODUCTO YA HA SIDO INGRESADO")
                return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
            else:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)