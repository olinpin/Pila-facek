# Generated by Django 3.2.3 on 2022-06-04 10:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0028_auto_20220604_1238'),
    ]

    operations = [
        migrations.AddField(
            model_name='hoblovani',
            name='pozadovana_delka_cislo',
            field=models.IntegerField(default=0, verbose_name='Požadovaná délka'),
        ),
        migrations.AddField(
            model_name='hoblovani',
            name='pozadovana_delka_jednotky',
            field=models.CharField(blank=True, max_length=128, verbose_name='Požadovaná délka - jednotky'),
        ),
    ]
