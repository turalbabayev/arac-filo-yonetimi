from django.shortcuts import render
from rest_framework import viewsets
from .models import Arac, Surucu, Gorev, KilometreKaydi, Harcama
from .serializers import AracSerializer, SurucuSerializer, GorevSerializer, KilometreKaydiSerializer, HarcamaSerializer

# Create your views here.

class AracViewSet(viewsets.ModelViewSet):
    queryset = Arac.objects.all()
    serializer_class = AracSerializer

class SurucuViewSet(viewsets.ModelViewSet):
    queryset = Surucu.objects.all()
    serializer_class = SurucuSerializer

class GorevViewSet(viewsets.ModelViewSet):
    queryset = Gorev.objects.all()
    serializer_class = GorevSerializer

class KilometreKaydiViewSet(viewsets.ModelViewSet):
    queryset = KilometreKaydi.objects.all()
    serializer_class = KilometreKaydiSerializer

class HarcamaViewSet(viewsets.ModelViewSet):
    queryset = Harcama.objects.all()
    serializer_class = HarcamaSerializer
