# Generated by Django 3.2.3 on 2022-03-31 18:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0017_auto_20220118_1254'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='hoblovani',
            options={'ordering': ['-priority', '-vytvoreno'], 'verbose_name': 'Hoblování', 'verbose_name_plural': 'Hoblování'},
        ),
        migrations.AlterModelOptions(
            name='rozmitacka',
            options={'ordering': ['-priority', '-vytvoreno'], 'verbose_name': 'Rozmítačka', 'verbose_name_plural': 'Rozmítačka'},
        ),
        migrations.AddField(
            model_name='hoblovani',
            name='image',
            field=models.ImageField(blank=True, upload_to='images/% Y/% m/% d'),
        ),
    ]