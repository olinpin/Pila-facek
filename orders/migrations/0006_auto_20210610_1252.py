# Generated by Django 3.2.3 on 2021-06-10 12:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0005_alter_rozmitacka_ks'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rozmitacka',
            name='baleni',
            field=models.CharField(blank=True, max_length=128),
        ),
        migrations.AlterField(
            model_name='rozmitacka',
            name='impregnace',
            field=models.CharField(blank=True, max_length=128),
        ),
        migrations.AlterField(
            model_name='rozmitacka',
            name='kapovani',
            field=models.CharField(blank=True, max_length=128),
        ),
        migrations.AlterField(
            model_name='rozmitacka',
            name='ks',
            field=models.IntegerField(blank=True),
        ),
        migrations.AlterField(
            model_name='rozmitacka',
            name='kvalita',
            field=models.CharField(blank=True, max_length=128),
        ),
        migrations.AlterField(
            model_name='rozmitacka',
            name='material',
            field=models.CharField(blank=True, max_length=128),
        ),
        migrations.AlterField(
            model_name='rozmitacka',
            name='pozadovana_delka',
            field=models.CharField(blank=True, max_length=128),
        ),
        migrations.AlterField(
            model_name='rozmitacka',
            name='pozadovane_datum_vyroby',
            field=models.DateField(blank=True),
        ),
        migrations.AlterField(
            model_name='rozmitacka',
            name='pozadovany_rozmer',
            field=models.CharField(blank=True, max_length=128),
        ),
        migrations.AlterField(
            model_name='rozmitacka',
            name='poznamka',
            field=models.CharField(blank=True, max_length=128),
        ),
        migrations.AlterField(
            model_name='rozmitacka',
            name='umisteni_materialu',
            field=models.CharField(blank=True, max_length=128),
        ),
        migrations.AlterField(
            model_name='rozmitacka',
            name='zakaznik',
            field=models.CharField(blank=True, max_length=128),
        ),
    ]
