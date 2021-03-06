from django.db import models
from django.db.models import signals
from django.dispatch import receiver

# Create your models here.

# model of Rozmitacka table
class Rozmitacka(models.Model):
    zakaznik = models.CharField("Zákazník",blank=True, max_length=128)
    material = models.CharField("Materiál", blank=True, max_length=128)
    umisteni_materialu = models.CharField("Umístění materiálu", blank=True, max_length=128)
    pozadovany_rozmer = models.CharField("Požadovaný rozměr", blank=True, max_length=128)
    pozadovana_delka = models.CharField("Požadovaná délka", blank=True, max_length=128)
    poznamka = models.CharField("Poznámka", blank=True, max_length=128)
    ks = models.IntegerField("Kusů", default=1)
    ks_hotovo = models.IntegerField("Kusů hotovo", default=0)
    jednotky = models.CharField("Jednotky", default="ks", max_length=128)
    kvalita = models.CharField(blank=True, max_length=128)
    baleni = models.CharField("Balení", blank=True, max_length=128)
    impregnace = models.CharField(max_length=128, choices=[("Ano", "Ano"), ("Ne", "Ne")])
    kapovani = models.CharField("Kapování", max_length=128, choices=[("Ano", "Ano"), ("Ne", "Ne")])
    pozadovane_datum_vyroby = models.DateField("Požadované datum výroby")
    hotovo = models.BooleanField("Hotovo", default=False)
    kontrola = models.BooleanField("Kontrola", default=False)
    do_vyroby = models.BooleanField("Do výroby", default=False)
    get_material = models.BooleanField("Materiál", default=False)
    get_zbytek = models.BooleanField("Zbytek", default=False)
    vytvoreno = models.DateTimeField("Vytvořeno", auto_now_add=True)


    # return function for string
    def __str__(self):
        return f"{self.zakaznik}"
    class Meta:
        verbose_name_plural = "Rozmítačka"
        verbose_name = "Rozmítačka"

# model of Hoblovani table
class Hoblovani(models.Model):
    zakaznik = models.CharField("Zákazník", blank=True, max_length=128)
    skladovy_material = models.CharField("Skladový materiál", blank=True, max_length=128)
    pozadovany_rozmer = models.CharField("Požadovaný rozměr", blank=True, max_length=128)
    pozadovana_delka = models.CharField("Požadovaná délka", blank=True, max_length=128)
    poznamka = models.CharField("Poznámka", blank=True, max_length=128)
    ks = models.IntegerField("Kusů", default=1)
    ks_hotovo = models.IntegerField("Kusů hotovo", default=0)
    jednotky = models.CharField("Jednotky", default="ks", max_length=128)
    kvalita = models.CharField(blank=True, max_length=128)
    baleni = models.CharField("Balení", blank=True, max_length=128)
    impregnace = models.CharField(max_length=128, choices=[("Ano", "Ano"), ("Ne", "Ne")])
    kapovani = models.CharField("Kapování", max_length=128, choices=[("Ano", "Ano"), ("Ne", "Ne")])
    misto_hoblovani = models.CharField(blank=True, max_length=128)
    pozadovane_datum_vyroby = models.DateField("Požadované datum výroby")
    hotovo = models.BooleanField("Hotovo", default=False)
    kontrola = models.BooleanField("Kontrola", default=False)
    do_vyroby = models.BooleanField("Do výroby", default=False)
    get_material = models.BooleanField("Materiál", default=False)
    get_zbytek = models.BooleanField("Odvoz", default=False)
    vytvoreno = models.DateTimeField("Vytvořeno", auto_now_add=True)

    def __str__(self):
        return f"{self.zakaznik}"# - {self.pozadovane_datum_vyroby.strftime('%d.%m.%Y')},  {'Hotovo' if self.hotovo == True else f'{self.ks_hotovo}/{self.ks}' }, Kontrola - {'Ano' if self.kontrola == True else 'Ne' }"

    class Meta:
        verbose_name_plural = "Hoblování"
        verbose_name = "Hoblování"

