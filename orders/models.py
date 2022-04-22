from django.db import models
from django.utils.html import mark_safe

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
    pozadovane_datum_vyroby = models.DateField("Vyrobit do")
    hotovo = models.BooleanField("Hotovo", default=False)
    kontrola = models.BooleanField("Kontrola", default=False)
    do_vyroby = models.BooleanField("Do výroby", default=False)
    get_material = models.BooleanField("Materiál", default=False)
    get_zbytek = models.BooleanField("Zbytek", default=False)
    odpad = models.BooleanField("Odpad", default=False)
    vytvoreno = models.DateTimeField("Vytvořeno", auto_now_add=True)
    priority = models.IntegerField("Priorita", default=10) 


    # return function for string
    def __str__(self):
        return f"{self.zakaznik}"
    class Meta:
        verbose_name_plural = "Rozmítačka"
        verbose_name = "Rozmítačka"
        ordering = ['-priority', '-vytvoreno']

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
    pozadovane_datum_vyroby = models.DateField("Vyrobit do")
    hotovo = models.BooleanField("Hotovo", default=False)
    kontrola = models.BooleanField("Kontrola", default=False)
    do_vyroby = models.BooleanField("Do výroby", default=False)
    get_material = models.BooleanField("Materiál", default=False)
    get_zbytek = models.BooleanField("Odvoz", default=False)
    odpad = models.BooleanField("Odpad", default=False)
    vytvoreno = models.DateTimeField("Vytvořeno", auto_now_add=True)
    priority = models.IntegerField("Priorita", default=10)
    image = models.ImageField(upload_to='media/images', blank=True)
    do_susarny = models.BooleanField("Do sušárny", default=True)
    suche = models.BooleanField("Suché", default=False)

    @property
    def image_preview(self):
        if self.image:
            return mark_safe(f'<img src="{self.image.url}" width="100" height="100" />')
        return ""
    
    # save the suche and do_susarny in another variable
    __suche_original = None
    __do_susarny_original = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__suche_original = self.suche
        self.__do_susarny_original = self.do_susarny

    # check which of the suche or do_susarny has changed and change the other one accordingly
    def save(self, *args, **kwargs):
        if not self.do_vyroby:
            if self.__suche_original != self.suche:
                self.do_susarny = not self.suche
            elif self.__do_susarny_original != self.do_susarny:
                self.suche = not self.do_susarny
        if self.hotovo and not self.do_vyroby:
            self.priority = 10
        return super(Hoblovani, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.zakaznik}"# - {self.pozadovane_datum_vyroby.strftime('%d.%m.%Y')},  {'Hotovo' if self.hotovo == True else f'{self.ks_hotovo}/{self.ks}' }, Kontrola - {'Ano' if self.kontrola == True else 'Ne' }"

    class Meta:
        verbose_name_plural = "Hoblování"
        verbose_name = "Hoblování"
        ordering = ['-priority', '-vytvoreno']

