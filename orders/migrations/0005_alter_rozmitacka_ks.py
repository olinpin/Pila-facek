# Generated by Django 3.2.3 on 2021-06-10 12:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0004_alter_rozmitacka_ks'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rozmitacka',
            name='ks',
            field=models.IntegerField(),
        ),
    ]