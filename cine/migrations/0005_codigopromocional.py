# Generated by Django 5.1 on 2024-11-18 01:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cine', '0004_productoconfiteria'),
    ]

    operations = [
        migrations.CreateModel(
            name='CodigoPromocional',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo', models.CharField(max_length=20, unique=True)),
                ('descuento', models.DecimalField(decimal_places=2, max_digits=4)),
            ],
        ),
    ]
