# Generated by Django 3.2.3 on 2022-01-10 07:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0010_auto_20220110_0835'),
    ]

    operations = [
        migrations.AddField(
            model_name='rozmitacka',
            name='odpad',
            field=models.BooleanField(default=False, verbose_name='Odpad'),
        ),
    ]
