from django.contrib import admin
from django.contrib.admin.options import ModelAdmin
from .models import Rozmitacka, Hoblovani
from django.db import models
from django.conf.locale.en import formats as en_formats
from django.conf.locale.cs import formats as cs_formats

# change the english date format in admin display
en_formats.DATE_FORMAT = "d.m.Y"
en_formats.DATETIME_FORMAT = "d.m.Y H:i" #:s for seconds

# change the czech date format in admin display
cs_formats.DATE_FORMAT = "d.m.Y"
cs_formats.DATETIME_FORMAT = "d.m.Y H:i" #:s for seconds

# Register your models here.



@admin.register(Rozmitacka)
class RozmitackaAdmin(admin.ModelAdmin):
    # what shows in the list
    list_display = ("zakaznik", "pozadovane_datum_vyroby", "vytvoreno", "hotovo", "kontrola")
    list_editable = ("hotovo", "kontrola")
    # filter and search the list
    list_filter = ("hotovo", "vytvoreno", "kontrola", "get_material", "get_zbytek")
    search_fields = ("zakaznik__startswith", )
    # exclude in the form
    exclude = ("ks_hotovo", "get_material", "get_zbytek")


    class Meta:
        ordering = ("pozadovane_datum_vyroby", "zakaznik",)
    
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields["zakaznik"].label = "Zákazník"
        form.base_fields["material"].label = "Materiál"
        form.base_fields["umisteni_materialu"].label = "Umístění materiálu"
        form.base_fields["pozadovany_rozmer"].label = "Požadovaný rozměr"
        form.base_fields["pozadovana_delka"].label = "Požadovaná délka"
        form.base_fields["poznamka"].label = "Poznámka"
        form.base_fields["ks"].label = "Kusů"
        form.base_fields["baleni"].label = "Balení (proklad)"
        form.base_fields["kapovani"].label = "Kapování"
        form.base_fields["pozadovane_datum_vyroby"].label = "Požadované datum výroby"
        
        return form

@admin.register(Hoblovani)
class HoblovaniAdmin(admin.ModelAdmin):
    # what shows in the list
    list_display = ("zakaznik", "pozadovane_datum_vyroby", "vytvoreno", "hotovo", "kontrola")
    list_editable = ("hotovo", "kontrola")
    # filter and search the list
    list_filter = ("hotovo", "vytvoreno", "kontrola", "get_material", "get_zbytek")
    search_fields = ("zakaznik__startswith", )
    # exclude in the form
    exclude = ("ks_hotovo", "get_material", "get_zbytek",)

    class Meta:
        ordering = ("pozadovane_datum_vyroby", "zakaznik",)
    
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields["zakaznik"].label = "Zákazník"
        form.base_fields["skladovy_material"].label = "Skladový materiál"
        form.base_fields["pozadovany_rozmer"].label = "Požadovaný rozměr"
        form.base_fields["pozadovana_delka"].label = "Požadovaná délka"
        form.base_fields["poznamka"].label = "Poznámka"
        form.base_fields["ks"].label = "Kusů"
        form.base_fields["baleni"].label = "Balení (proklad)"
        form.base_fields["kapovani"].label = "Kapování"
        form.base_fields["misto_hoblovani"].label = "Místo hoblování"
        form.base_fields["pozadovane_datum_vyroby"].label = "Požadované datum výroby"
        
        return form
