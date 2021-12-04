# Generated by Django 3.2.3 on 2021-12-01 15:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0004_auto_20211201_1546'),
    ]

    operations = [
        migrations.AddField(
            model_name='hoblovani',
            name='modified_date',
            field=models.DateField(auto_now=True),
        ),
        migrations.AddField(
            model_name='rozmitacka',
            name='modified_date',
            field=models.DateField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='hoblovani',
            name='do_vyroby',
            field=models.BooleanField(default=False, verbose_name='Do výroby'),
        ),
        migrations.AlterField(
            model_name='rozmitacka',
            name='do_vyroby',
            field=models.BooleanField(default=False, verbose_name='Do výroby'),
        ),
    ]