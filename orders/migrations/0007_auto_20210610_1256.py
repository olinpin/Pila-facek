# Generated by Django 3.2.3 on 2021-06-10 12:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0006_auto_20210610_1252'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rozmitacka',
            name='impregnace',
            field=models.CharField(choices=[('Ano', 'Ano'), ('Ne', 'Ne')], max_length=128),
        ),
        migrations.AlterField(
            model_name='rozmitacka',
            name='kapovani',
            field=models.CharField(choices=[('Ano', 'Ano'), ('Ne', 'Ne')], max_length=128),
        ),
    ]
