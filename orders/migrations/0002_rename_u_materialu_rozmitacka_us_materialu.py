# Generated by Django 3.2.3 on 2021-06-07 13:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='rozmitacka',
            old_name='u_materialu',
            new_name='us_materialu',
        ),
    ]