# Generated by Django 3.0.5 on 2020-04-17 02:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medico', '0007_auto_20200416_2353'),
    ]

    operations = [
        migrations.AlterField(
            model_name='medico',
            name='foto',
            field=models.ImageField(blank=True, upload_to='fotos/1587092053.0768147'),
        ),
    ]
