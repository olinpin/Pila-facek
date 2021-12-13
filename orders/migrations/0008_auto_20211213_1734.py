# Generated by Django 3.2.3 on 2021-12-13 16:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0007_auto_20211202_1653'),
    ]

    operations = [
        migrations.AddField(
            model_name='hoblovani',
            name='jednotky',
            field=models.CharField(default='ks', max_length=128, verbose_name='Jednotky'),
        ),
        migrations.AddField(
            model_name='rozmitacka',
            name='jednotky',
            field=models.CharField(default='ks', max_length=128, verbose_name='Jednotky'),
        ),
        migrations.AlterField(
            model_name='hoblovani',
            name='pozadovane_datum_vyroby',
            field=models.DateField(verbose_name='Požadované datum výroby'),
        ),
        migrations.AlterField(
            model_name='rozmitacka',
            name='pozadovane_datum_vyroby',
            field=models.DateField(verbose_name='Požadované datum výroby'),
        ),
    ]
