# Generated by Django 3.2.3 on 2022-01-18 11:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0016_auto_20220110_1042'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hoblovani',
            name='pozadovane_datum_vyroby',
            field=models.DateField(verbose_name='Vyrobit do'),
        ),
        migrations.AlterField(
            model_name='rozmitacka',
            name='pozadovane_datum_vyroby',
            field=models.DateField(verbose_name='Vyrobit do'),
        ),
    ]