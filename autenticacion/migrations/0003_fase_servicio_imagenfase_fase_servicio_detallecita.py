# Generated by Django 5.0.1 on 2024-03-10 02:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('autenticacion', '0002_cita'),
    ]

    operations = [
        migrations.CreateModel(
            name='Fase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Servicio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('descripcion', models.TextField()),
                ('precio', models.DecimalField(decimal_places=2, max_digits=8)),
            ],
        ),
        migrations.CreateModel(
            name='ImagenFase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('imagen_path', models.CharField(max_length=255)),
                ('fecha_subida', models.DateTimeField(auto_now_add=True)),
                ('cita', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='autenticacion.cita')),
                ('fase', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='autenticacion.fase')),
            ],
        ),
        migrations.AddField(
            model_name='fase',
            name='servicio',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='autenticacion.servicio'),
        ),
        migrations.CreateModel(
            name='DetalleCita',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total', models.FloatField()),
                ('cita', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='autenticacion.cita')),
                ('servicio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='autenticacion.servicio')),
            ],
        ),
    ]
