from rest_framework import serializers
from .models import Arac, Surucu, Gorev, KilometreKaydi, Harcama

class AracSerializer(serializers.ModelSerializer):
    class Meta:
        model = Arac
        fields = '__all__'

class SurucuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Surucu
        fields = '__all__'

class GorevSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gorev
        fields = '__all__'

class KilometreKaydiSerializer(serializers.ModelSerializer):
    class Meta:
        model = KilometreKaydi
        fields = '__all__'

class HarcamaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Harcama
        fields = '__all__' 