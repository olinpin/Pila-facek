# Generated by Django 3.2.3 on 2021-11-01 14:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0018_auto_20211101_1434'),
    ]

    operations = [
        migrations.RenameField(
            model_name='hoblovani',
            old_name='material',
            new_name='get_material',
        ),
        migrations.AddField(
            model_name='rozmitacka',
            name='get_material',
            field=models.BooleanField(default=False, verbose_name='Materiál'),
        ),
        migrations.AlterField(
            model_name='rozmitacka',
            name='material',
            field=models.CharField(blank=True, max_length=128, verbose_name='Materiál'),
        ),
    ]
