# Generated by Django 3.0.5 on 2020-04-17 03:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('paciente', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='paciente',
            name='imc',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
    ]