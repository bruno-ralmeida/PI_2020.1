# Generated by Django 3.0.5 on 2020-05-08 12:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('consulta', '0004_auto_20200508_1247'),
    ]

    operations = [
        migrations.AlterField(
            model_name='consulta',
            name='data',
            field=models.DateField(),
        ),
    ]
