from django.contrib import admin
from django.contrib.admin.options import ModelAdmin
from .models import Rozmitacka, Hoblovani
from django.db import models
from django.conf.locale.en import formats as en_formats
from django.conf.locale.cs import formats as cs_formats
from django.utils.html import mark_safe

# pdf generation
from reportlab.platypus import Table, SimpleDocTemplate, TableStyle, Image, PageBreak, Paragraph
from reportlab.lib.units import cm, inch
from reportlab.lib import colors
from django.http import HttpResponse
from reportlab.lib.pagesizes import A4, landscape
import datetime


# change the english date format in admin display
en_formats.DATE_FORMAT = "d.m.Y"
en_formats.DATETIME_FORMAT = "d.m.Y H:i" #:s for seconds

# change the czech date format in admin display
cs_formats.DATE_FORMAT = "d.m.Y"
cs_formats.DATETIME_FORMAT = "d.m.Y H:i" #:s for seconds

# Register your models here.


@admin.register(Rozmitacka)
class RozmitackaAdmin(admin.ModelAdmin):
    list_per_page = 50
    # checks do_vyroby a get_material fields True
    def do_vyroby_a_material(modeladmin, request, queryset):
        for order in queryset:
            order.do_vyroby = True
            order.get_material = True
            order.save()
    do_vyroby_a_material.short_description = "Zaškrtnout do výroby a materiál"
    def button(self, obj):
        return mark_safe('<input type="submit" name="_save" class="default" value="Uložit">')
    button.short_description = 'Uložit'
    # what shows in the list
    list_display = ("zakaznik", "pozadovane_datum_vyroby", "vytvoreno", "priority", "hotovo", 
                    "kontrola", "do_vyroby", "get_material", "button", "ks_hotovo", "ks")
    list_editable = ("hotovo", "kontrola", "do_vyroby","get_material")
    # filter and search the list
    list_filter = ("hotovo", "vytvoreno", "kontrola", "do_vyroby", )
    search_fields = ("zakaznik__startswith", )
    # exclude in the form
    exclude = ("ks_hotovo", "get_material", "get_zbytek", "odpad",)
    # actions which the admin page can do to orders
    actions = [do_vyroby_a_material,]


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
    
    fields = ("zakaznik", "material", "umisteni_materialu", "pozadovany_rozmer", "pozadovana_delka", "poznamka", "ks", "jednotky", "kvalita", "baleni", "impregnace", "kapovani", "hotovo", "kontrola", "do_vyroby", "priority", "pozadovane_datum_vyroby",)

@admin.register(Hoblovani)
class HoblovaniAdmin(admin.ModelAdmin):
    list_per_page = 50
    # checks do_vyroby a get_material fields True
    def do_vyroby_a_material(modeladmin, request, queryset):
        for order in queryset:
            order.do_vyroby = True
            order.get_material = True
            order.save()
    do_vyroby_a_material.short_description = "Zaškrtnout do výroby a materiál"

    def createPDF(modeladmin, request, queryset):
        response = HttpResponse()
        date = datetime.datetime.now().strftime("%Y-%m-%d")
        response['Content-Disposition'] = f'attachment; filename=hoblovani-{date}.pdf'

        elements = []
        doc = SimpleDocTemplate(response, rightMargin=0, leftMargin=0, topMargin=0.3 * cm, bottomMargin=0, pagesize=landscape(A4))
        data = [("Zákazník", "Materiál", Paragraph("Požadovaný rozmer"), "Poznámka", "Kusy", Paragraph("Balení (proklad)"), "Kvalita", "Impregnace", "Kapování", Paragraph("Místo hoblování"), "Vyrobit do", "Priorita",),]
        images = []
        names = []
        for order in queryset:
            try:
                img = Image(order.image)
                img.drawHeight = 18 * cm
                img.drawWidth = 18 * cm
                images.append(img)
                names.append(order.zakaznik)
            except:
                pass
            
            data.append((Paragraph(order.zakaznik), Paragraph(order.skladovy_material), Paragraph(f"{order.pozadovany_rozmer} x {order.pozadovana_delka}"), Paragraph(order.poznamka), f"{order.ks} {order.jednotky}", Paragraph(order.baleni), Paragraph(order.kvalita), Paragraph(order.impregnace), Paragraph(order.kapovani), Paragraph(order.misto_hoblovani), order.pozadovane_datum_vyroby, order.priority))
        
        table = Table(data, colWidths=[inch*0.95])
        table.setStyle(TableStyle([ ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                                    ('BOX', (0, 0), (-1, -1), 0.25, colors.black),]))
        elements.append(table)
        try:
            for i in range(len(images)):
                elements.append(PageBreak())
                elements.append(Paragraph(names[i]))
                elements.append(images[i])
        except:
            pass
        doc.build(elements)
        return response
    
    createPDF.short_description = "Vytvořit PDF"
    def button(self, obj):
        return mark_safe('<input type="submit" name="_save" class="default" value="Uložit">')
    button.short_description = 'Uložit'
    # what shows in the list
    list_display = ("zakaznik", "image_preview", "pozadovane_datum_vyroby", "vytvoreno", "priority", "hotovo", 
                    "kontrola", "do_vyroby", "get_material", "do_susarny", "suche", "button", "ks_hotovo", "ks")
    list_editable = ("hotovo", "kontrola", "do_vyroby", "do_susarny", "suche", "get_material")
    # filter and search the list
    list_filter = ("hotovo", "vytvoreno", "kontrola", "do_vyroby", "do_susarny", "suche")
    search_fields = ("zakaznik__startswith", )
    # exclude in the form
    exclude = ("ks_hotovo", "get_material", "get_zbytek", "odpad", )
    # actions which the admin page can do to orders
    actions = [do_vyroby_a_material, createPDF,]

    readonly_fields = ("image_preview",)
    def image_preview(self, obj):
        return obj.image_preview

    image_preview.short_description = "Obrázek"
    image_preview.allow_tags = True

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
        form.base_fields["image"].label = "Obrázek"
        
        return form

    fields = ("zakaznik", "skladovy_material", "pozadovany_rozmer", "pozadovana_delka", "poznamka", "ks", "jednotky", "kvalita", "baleni", "misto_hoblovani", "impregnace", "kapovani", "hotovo", "kontrola", "do_vyroby", "do_susarny", "suche", "priority", "pozadovane_datum_vyroby", "image", "image_preview")
