# Generated by Django 3.2.3 on 2022-06-04 10:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0029_auto_20220604_1249'),
    ]

    operations = [
        migrations.AddField(
            model_name='rozmitacka',
            name='pozadovana_delka_cislo',
            field=models.IntegerField(default=0, verbose_name='Požadovaná délka'),
        ),
        migrations.AddField(
            model_name='rozmitacka',
            name='pozadovana_delka_jednotky',
            field=models.CharField(blank=True, max_length=128, verbose_name='Požadovaná délka - jednotky'),
        ),
    ]
