# Generated by Django 3.2.3 on 2021-07-20 12:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0012_auto_20210708_0811'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rozmitacka',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]