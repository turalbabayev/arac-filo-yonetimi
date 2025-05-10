from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Sum, Count
from django.utils import timezone
from datetime import datetime, timedelta
from .models import Arac, Surucu, Gorev, KilometreKaydi, Harcama
from .serializers import AracSerializer, SurucuSerializer, GorevSerializer, KilometreKaydiSerializer, HarcamaSerializer

# Create your views here.

class AracViewSet(viewsets.ModelViewSet):
    queryset = Arac.objects.all()
    serializer_class = AracSerializer
    permission_classes = [IsAuthenticated]

class SurucuViewSet(viewsets.ModelViewSet):
    queryset = Surucu.objects.all()
    serializer_class = SurucuSerializer
    permission_classes = [IsAuthenticated]

class GorevViewSet(viewsets.ModelViewSet):
    queryset = Gorev.objects.all()
    serializer_class = GorevSerializer
    permission_classes = [IsAuthenticated]

class KilometreKaydiViewSet(viewsets.ModelViewSet):
    queryset = KilometreKaydi.objects.all()
    serializer_class = KilometreKaydiSerializer
    permission_classes = [IsAuthenticated]

class HarcamaViewSet(viewsets.ModelViewSet):
    queryset = Harcama.objects.all()
    serializer_class = HarcamaSerializer
    permission_classes = [IsAuthenticated]

@api_view(['GET'])
def dashboard_stats(request):
    total_vehicles = Arac.objects.count()
    active_drivers = Surucu.objects.filter(aktif=True).count()
    
    # Son 30 günlük görev ve harcama sayısı
    thirty_days_ago = timezone.now() - timedelta(days=30)
    monthly_tasks = Gorev.objects.filter(created_at__gte=thirty_days_ago).count()
    monthly_expenses = Harcama.objects.filter(created_at__gte=thirty_days_ago).aggregate(total=Sum('miktar'))['total'] or 0
    
    return Response({
        'total_vehicles': total_vehicles,
        'active_drivers': active_drivers,
        'monthly_tasks': monthly_tasks,
        'monthly_expenses': monthly_expenses
    })

@api_view(['GET'])
def recent_activities(request):
    # Son 7 günlük aktiviteleri getir
    seven_days_ago = timezone.now() - timedelta(days=7)
    
    # Her modelden son 10 kayıt
    recent_vehicles = AracSerializer(Arac.objects.filter(created_at__gte=seven_days_ago).order_by('-created_at')[:10], many=True).data
    recent_tasks = GorevSerializer(Gorev.objects.filter(created_at__gte=seven_days_ago).order_by('-created_at')[:10], many=True).data
    recent_mileages = KilometreKaydiSerializer(KilometreKaydi.objects.filter(created_at__gte=seven_days_ago).order_by('-created_at')[:10], many=True).data
    recent_expenses = HarcamaSerializer(Harcama.objects.filter(created_at__gte=seven_days_ago).order_by('-created_at')[:10], many=True).data
    
    # Tüm aktiviteleri birleştir ve tarihe göre sırala
    all_activities = []
    
    for vehicle in recent_vehicles:
        all_activities.append({
            'type': 'vehicle',
            'data': vehicle,
            'created_at': vehicle['created_at']
        })
    
    for task in recent_tasks:
        all_activities.append({
            'type': 'task',
            'data': task,
            'created_at': task['created_at']
        })
    
    for mileage in recent_mileages:
        all_activities.append({
            'type': 'mileage',
            'data': mileage,
            'created_at': mileage['created_at']
        })
    
    for expense in recent_expenses:
        all_activities.append({
            'type': 'expense',
            'data': expense,
            'created_at': expense['created_at']
        })
    
    # Tarihe göre sırala
    all_activities.sort(key=lambda x: x['created_at'], reverse=True)
    
    return Response(all_activities[:10])

@api_view(['GET', 'POST'])
def vehicle_list(request):
    if request.method == 'GET':
        vehicles = Arac.objects.all()
        serializer = AracSerializer(vehicles, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = AracSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def vehicle_detail(request, pk):
    vehicle = get_object_or_404(Arac, pk=pk)
    
    if request.method == 'GET':
        serializer = AracSerializer(vehicle)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = AracSerializer(vehicle, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        vehicle.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST'])
def driver_list(request):
    if request.method == 'GET':
        drivers = Surucu.objects.all()
        serializer = SurucuSerializer(drivers, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = SurucuSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def driver_detail(request, pk):
    driver = get_object_or_404(Surucu, pk=pk)
    
    if request.method == 'GET':
        serializer = SurucuSerializer(driver)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = SurucuSerializer(driver, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        driver.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST'])
def task_list(request):
    if request.method == 'GET':
        tasks = Gorev.objects.all()
        serializer = GorevSerializer(tasks, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = GorevSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def task_detail(request, pk):
    task = get_object_or_404(Gorev, pk=pk)
    
    if request.method == 'GET':
        serializer = GorevSerializer(task)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = GorevSerializer(task, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST'])
def mileage_list(request):
    if request.method == 'GET':
        mileages = KilometreKaydi.objects.all()
        serializer = KilometreKaydiSerializer(mileages, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = KilometreKaydiSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def mileage_detail(request, pk):
    mileage = get_object_or_404(KilometreKaydi, pk=pk)
    
    if request.method == 'GET':
        serializer = KilometreKaydiSerializer(mileage)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = KilometreKaydiSerializer(mileage, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        mileage.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST'])
def expense_list(request):
    if request.method == 'GET':
        expenses = Harcama.objects.all()
        serializer = HarcamaSerializer(expenses, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = HarcamaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def expense_detail(request, pk):
    expense = get_object_or_404(Harcama, pk=pk)
    
    if request.method == 'GET':
        serializer = HarcamaSerializer(expense)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = HarcamaSerializer(expense, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        expense.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
