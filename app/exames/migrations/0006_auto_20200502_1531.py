# Generated by Django 3.0.5 on 2020-05-02 18:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exames', '0005_auto_20200428_1906'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exame_referencia',
            name='colesterol_max',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='exame_referencia',
            name='glicose',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='exame_referencia',
            name='hdl_min',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='exame_referencia',
            name='ldl_max',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='exame_referencia',
            name='triglicerides_max',
            field=models.IntegerField(),
        ),
    ]