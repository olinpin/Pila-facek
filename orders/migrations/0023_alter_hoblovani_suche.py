# Generated by Django 3.2.3 on 2022-04-28 10:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0022_auto_20220406_1422'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hoblovani',
            name='suche',
            field=models.BooleanField(default=False, verbose_name='Připravené'),
        ),
    ]
