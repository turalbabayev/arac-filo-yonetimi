from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Arac(models.Model):
    KAYNAK_TIPI = [
        ('ozmal', 'Özmal'),
        ('kiralik', 'Kiralık'),
    ]
    plaka = models.CharField(max_length=20, unique=True)
    marka = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    yil = models.PositiveIntegerField()
    tip = models.CharField(max_length=50)
    kaynak_tipi = models.CharField(max_length=10, choices=KAYNAK_TIPI)
    mevcut_durum = models.CharField(max_length=50, default='havuzda')
    aciklama = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.plaka} - {self.marka} {self.model}"

    class Meta:
        verbose_name = 'Araç'
        verbose_name_plural = 'Araçlar'

class Surucu(models.Model):
    ad = models.CharField(max_length=100)
    soyad = models.CharField(max_length=100)
    ehliyet_no = models.CharField(max_length=20)
    kullanici = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    telefon = models.CharField(max_length=20, default="")
    aktif = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.ad} {self.soyad}"

    class Meta:
        verbose_name = 'Sürücü'
        verbose_name_plural = 'Sürücüler'

class Gorev(models.Model):
    DURUM_CHOICES = [
        ('beklemede', 'Beklemede'),
        ('devam_ediyor', 'Devam Ediyor'),
        ('tamamlandi', 'Tamamlandı'),
        ('iptal_edildi', 'İptal Edildi'),
    ]
    baslik = models.CharField(max_length=200, default="Görev")
    arac = models.ForeignKey(Arac, on_delete=models.CASCADE)
    surucu = models.ForeignKey(Surucu, on_delete=models.CASCADE)
    baslangic_tarihi = models.DateField()
    bitis_tarihi = models.DateField(null=True, blank=True)
    aciklama = models.TextField(default="")
    durum = models.CharField(max_length=20, choices=DURUM_CHOICES, default='beklemede')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.baslik} - {self.arac.plaka} - {self.surucu.ad} {self.surucu.soyad}"

    class Meta:
        verbose_name = 'Görev'
        verbose_name_plural = 'Görevler'

class KilometreKaydi(models.Model):
    arac = models.ForeignKey(Arac, on_delete=models.CASCADE)
    tarih = models.DateField()
    kilometre = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.arac} - {self.tarih} - {self.kilometre} km"

    class Meta:
        verbose_name = 'Kilometre Kaydı'
        verbose_name_plural = 'Kilometre Kayıtları'

class Harcama(models.Model):
    HARCAMA_TIPI = [
        ('bakim', 'Bakım'),
        ('kasko', 'Kasko'),
        ('yakıt', 'Yakıt'),
        ('lastik', 'Lastik'),
        ('tamir', 'Tamir'),
    ]
    arac = models.ForeignKey(Arac, on_delete=models.CASCADE)
    tarih = models.DateField()
    tip = models.CharField(max_length=20, choices=HARCAMA_TIPI)
    tutar = models.DecimalField(max_digits=10, decimal_places=2)
    aciklama = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.arac} - {self.tip} - {self.tutar} TL"

    class Meta:
        verbose_name = 'Harcama'
        verbose_name_plural = 'Harcamalar'
