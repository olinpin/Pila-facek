# Generated by Django 3.2.3 on 2021-06-03 16:25

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Rozmitacka',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('zakaznik', models.CharField(max_length=128)),
                ('material', models.CharField(max_length=128)),
                ('u_materialu', models.CharField(max_length=128)),
                ('p_rozmer', models.CharField(max_length=128)),
                ('p_delka', models.CharField(max_length=128)),
                ('poznamka', models.CharField(max_length=128)),
                ('ks', models.CharField(max_length=128)),
                ('kvalita', models.CharField(max_length=128)),
                ('baleni', models.CharField(max_length=128)),
                ('impregnace', models.CharField(max_length=128)),
                ('kapovani', models.CharField(max_length=128)),
                ('date_due', models.DateField()),
            ],
        ),
    ]
