# Generated by Django 3.0.5 on 2020-05-08 12:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('consulta', '0005_auto_20200508_1249'),
    ]

    operations = [
        migrations.AlterField(
            model_name='consulta',
            name='data',
            field=models.DateTimeField(),
        ),
    ]