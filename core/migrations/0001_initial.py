# Generated by Django 4.2.21 on 2025-05-10 18:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Arac',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('plaka', models.CharField(max_length=20, unique=True)),
                ('marka', models.CharField(max_length=50)),
                ('model', models.CharField(max_length=50)),
                ('yil', models.PositiveIntegerField()),
                ('tip', models.CharField(max_length=50)),
                ('kaynak_tipi', models.CharField(choices=[('ozmal', 'Özmal'), ('kiralik', 'Kiralık')], max_length=10)),
                ('mevcut_durum', models.CharField(default='havuzda', max_length=50)),
                ('aciklama', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Surucu',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ad', models.CharField(max_length=50)),
                ('soyad', models.CharField(max_length=50)),
                ('ehliyet_no', models.CharField(max_length=30)),
                ('kullanici', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='KilometreKaydi',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tarih', models.DateField()),
                ('kilometre', models.PositiveIntegerField()),
                ('arac', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.arac')),
            ],
        ),
        migrations.CreateModel(
            name='Harcama',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tarih', models.DateField()),
                ('tip', models.CharField(choices=[('bakim', 'Bakım'), ('kasko', 'Kasko'), ('yakıt', 'Yakıt'), ('lastik', 'Lastik'), ('tamir', 'Tamir')], max_length=20)),
                ('tutar', models.DecimalField(decimal_places=2, max_digits=10)),
                ('aciklama', models.TextField(blank=True, null=True)),
                ('arac', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.arac')),
            ],
        ),
        migrations.CreateModel(
            name='Gorev',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('baslangic_tarihi', models.DateField()),
                ('bitis_tarihi', models.DateField(blank=True, null=True)),
                ('arac', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.arac')),
                ('surucu', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.surucu')),
            ],
        ),
    ]
