# Generated by Django 3.2.3 on 2021-12-01 14:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_alter_hoblovani_get_zbytek'),
    ]

    operations = [
        migrations.AddField(
            model_name='hoblovani',
            name='do_vyroby',
            field=models.BooleanField(default=False, verbose_name='Do Výroby'),
        ),
        migrations.AddField(
            model_name='rozmitacka',
            name='do_vyroby',
            field=models.BooleanField(default=False, verbose_name='Do Výroby'),
        ),
    ]
