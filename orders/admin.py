from django.contrib import admin
from .models import Rozmitacka, Hoblovani, Baliky
from django.conf.locale.en import formats as en_formats
from django.conf.locale.cs import formats as cs_formats
from django.utils.html import mark_safe
import copy

# pdf generation
from reportlab.platypus import Table, SimpleDocTemplate, TableStyle, Image, PageBreak, Paragraph
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.units import cm
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

class BalikyInline(admin.TabularInline):
    model = Baliky
    fields = ('ks', 'done')


admin.site.site_url = '/app'

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

    def modrin_name(self, obj):
        if obj.modrin:
            return mark_safe('<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css"><p class="fa fa-tree" style="color: blue;"></p>')
    modrin_name.short_description = ""

    def duplicate(modeladmin, request, queryset):
        new_qs = copy.copy(queryset)
        for obj in new_qs:
            obj.id = None
            obj.ks = 0
            obj.pozadovane_datum_vyroby = datetime.datetime.today() + datetime.timedelta(days=30)
        Rozmitacka.objects.bulk_create(new_qs)
    duplicate.short_description = "Zkopírovat"

    def rozmery(self, obj):
        return f"{obj.pozadovany_rozmer} / {obj.pozadovana_delka}"
    rozmery.short_description = "Rozměry"

    def name(self, obj):
        res = mark_safe(f"{obj.zakaznik}" + (self.modrin_name(obj) or ""))
        return res
        
    # what shows in the list
    list_display = ("name", "vytvoreno", "priority", "rozmery", "hotovo", 
                    "kontrola", "do_vyroby", "get_material", "button", "kusy_baliky", "ks")
    list_editable = ("hotovo", "kontrola", "do_vyroby","get_material")
    # filter and search the list
    list_filter = ("hotovo", "vytvoreno", "kontrola", "do_vyroby", )
    search_fields = ("zakaznik", )
    # exclude in the form
    exclude = ("get_material", "get_zbytek", "odpad",)
    # actions which the admin page can do to orders
    actions = [do_vyroby_a_material, duplicate]

    readonly_fields = ("pozadovana_delka", )

    def kusy_baliky(self, obj):
        return f"{obj.ks_hotovo} / {obj.baliky_celkem}"
    kusy_baliky.short_description = "Hotovo / Balíky"


    class Meta:
        ordering = ("pozadovane_datum_vyroby", "zakaznik",)
    
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields["zakaznik"].label = "Zákazník"
        form.base_fields["material"].label = "Materiál"
        form.base_fields["umisteni_materialu"].label = "Umístění materiálu"
        form.base_fields["pozadovany_rozmer"].label = "Požadovaný rozměr"
        #form.base_fields["pozadovana_delka"].label = "Požadovaná délka"
        form.base_fields["pozadovana_delka_cislo"].label = "Požadovaná délka"
        form.base_fields["pozadovana_delka_jednotky"].label = "Požadovaná délka - jednotky"
        form.base_fields["poznamka"].label = "Poznámka"
        form.base_fields["ks"].label = "Kusů"
        form.base_fields["baleni"].label = "Balení (proklad)"
        form.base_fields["kapovani"].label = "Kapování"
        form.base_fields["pozadovane_datum_vyroby"].label = "Požadované datum výroby"
        
        
        return form
    
    fields = ("zakaznik", "material", "modrin", "umisteni_materialu", "pozadovany_rozmer", "pozadovana_delka", "pozadovana_delka_cislo", "pozadovana_delka_jednotky", "poznamka", "ks", "jednotky", "kvalita", "baleni", "impregnace", "kapovani", "hotovo", "kontrola", "do_vyroby", "priority", "pozadovane_datum_vyroby")

    inlines = [BalikyInline]


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

    def duplicate(modeladmin, request, queryset):
        new_qs = copy.copy(queryset)
        for obj in new_qs:
            obj.id = None
            obj.ks = 0
            obj.pozadovane_datum_vyroby = datetime.datetime.today() + datetime.timedelta(days=30)
        Hoblovani.objects.bulk_create(new_qs)
    duplicate.short_description = "Zkopírovat"

    def modrin_name(self, obj):
        if obj.modrin:
            return mark_safe('<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css"><p class="fa fa-tree" style="color: blue;"></p>')
    modrin_name.short_description = ""

    def name(self, obj):
        res = mark_safe(f"{obj.zakaznik}" + (self.modrin_name(obj) or ""))
        return res

    def create_pdf_with_pictures(modeladmin, request, queryset):
        response = HttpResponse()
        date = datetime.datetime.now().strftime("%Y-%m-%d")
        response['Content-Disposition'] = f'attachment; filename=hoblovani-s-obrazky-{date}.pdf'
        pdfmetrics.registerFont(TTFont('Verdana', 'orders/fonts/verdana/verdana.ttf'))
        style = ParagraphStyle(name="Normal", fontName="Verdana", fontSize=10, leading=12)
        elements = []
        doc = SimpleDocTemplate(response, rightMargin=0, leftMargin=0, topMargin=0.3 * cm, bottomMargin=0, pagesize=landscape(A4))
        data = [("Zákazník", "Materiál", Paragraph("Požadovaný rozměr", style), "Poznámka", "Kusy", Paragraph("Balení (proklad)", style), "Kvalita", "Impregnace", "Kapování", Paragraph("Místo hoblování", style), "Vyrobit do", "Priorita", "Obrázek",),]
        images = []
        names = []
        for order in queryset:
            pozadovana_delka = str(order.pozadovana_delka_cislo) + " " + order.pozadovana_delka_jednotky
            if order.impregnace:
                impregnace = "Ano"
            else:
                impregnace = "Ne"
            if order.kapovani:
                kapovani = "Ano"
            else:
                kapovani = "Ne"
            try:
                img = Image(order.image)
                img.drawHeight = 18 * cm
                img.drawWidth = 18 * cm
                images.append(img)
                names.append(order.zakaznik)
            except:
                pass
            if order.image:
                imgMin = Image(order.image)
                imgMin.drawHeight = doc.width/13
                imgMin.drawWidth = doc.width/13-1
                data.append((Paragraph(order.zakaznik, style), Paragraph(order.skladovy_material, style), Paragraph(f"{order.pozadovany_rozmer} x {pozadovana_delka}"), Paragraph(order.poznamka, style), f"{order.ks} {order.jednotky}", Paragraph(order.baleni, style), Paragraph(order.kvalita, style), Paragraph(impregnace), Paragraph(kapovani), Paragraph(order.misto_hoblovani, style), order.pozadovane_datum_vyroby, order.priority, imgMin))
            else:
                data.append((Paragraph(order.zakaznik, style), Paragraph(order.skladovy_material, style), Paragraph(f"{order.pozadovany_rozmer} x {pozadovana_delka}"), Paragraph(order.poznamka, style), f"{order.ks} {order.jednotky}", Paragraph(order.baleni, style), Paragraph(order.kvalita, style), Paragraph(impregnace), Paragraph(kapovani), Paragraph(order.misto_hoblovani, style), order.pozadovane_datum_vyroby, order.priority))


        table = Table(data, colWidths=doc.width/13-1)
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
    
    def create_pdf_without_pictures(modeladmin, request, queryset):
        response = HttpResponse()
        date = datetime.datetime.now().strftime("%Y-%m-%d")
        response['Content-Disposition'] = f'attachment; filename=hoblovani-bez-obrazku-{date}.pdf'
        pdfmetrics.registerFont(TTFont('Verdana', 'orders/fonts/verdana/verdana.ttf'))
        style = ParagraphStyle(name="Normal", fontName="Verdana", fontSize=10, leading=12)
        elements = []
        doc = SimpleDocTemplate(response, rightMargin=0, leftMargin=0, topMargin=0.3 * cm, bottomMargin=0, pagesize=landscape(A4))
        data = [("Zákazník", "Materiál", Paragraph("Požadovaný rozměr", style), "Poznámka", "Kusy", Paragraph("Balení (proklad)", style), "Kvalita", "Impregnace", "Kapování", Paragraph("Místo hoblování", style), "Vyrobit do", "Priorita", "Obrázek",),]
        images = []
        names = []
        for order in queryset:
            pozadovana_delka = str(order.pozadovana_delka_cislo) + " " + order.pozadovana_delka_jednotky
            if order.impregnace:
                impregnace = "Ano"
            else:
                impregnace = "Ne"
            if order.kapovani:
                kapovani = "Ano"
            else:
                kapovani = "Ne"
            try:
                img = Image(order.image)
                img.drawHeight = 18 * cm
                img.drawWidth = 18 * cm
                images.append(img)
                names.append(order.zakaznik)
            except:
                pass
            if order.image:
                imgMin = Image(order.image)
                imgMin.drawHeight = doc.width/13
                imgMin.drawWidth = doc.width/13-1
                data.append((Paragraph(order.zakaznik, style), Paragraph(order.skladovy_material, style), Paragraph(f"{order.pozadovany_rozmer} x {pozadovana_delka}"), Paragraph(order.poznamka, style), f"{order.ks} {order.jednotky}", Paragraph(order.baleni, style), Paragraph(order.kvalita, style), Paragraph(impregnace), Paragraph(kapovani), Paragraph(order.misto_hoblovani, style), order.pozadovane_datum_vyroby, order.priority, imgMin))
            else:
                data.append((Paragraph(order.zakaznik, style), Paragraph(order.skladovy_material, style), Paragraph(f"{order.pozadovany_rozmer} x {pozadovana_delka}"), Paragraph(order.poznamka, style), f"{order.ks} {order.jednotky}", Paragraph(order.baleni, style), Paragraph(order.kvalita, style), Paragraph(impregnace), Paragraph(kapovani), Paragraph(order.misto_hoblovani, style), order.pozadovane_datum_vyroby, order.priority))


        table = Table(data, colWidths=doc.width/13-1)
        table.setStyle(TableStyle([ ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                                    ('BOX', (0, 0), (-1, -1), 0.25, colors.black),]))
        elements.append(table)
        doc.build(elements)
        return response
    
    create_pdf_without_pictures.short_description = "Vytvořit PDF bez obrázků"
    create_pdf_with_pictures.short_description = "Vytvořit PDF s obrázky"
    def button(self, obj):
        return mark_safe('<input type="submit" name="_save" class="default" value="Uložit">')
    button.short_description = 'Uložit'

    # def rozmery(self, obj):
    #     return f"{obj.pozadovany_rozmer} / {obj.pozadovana_delka}"
    # rozmery.short_description = "Rozměry"
    # what shows in the list
    list_display = ("name", "image_preview", "vytvoreno", "priority", "rozmery", "hotovo", 
                    "kontrola", "do_vyroby", "get_material", "do_susarny", "suche", "button", "kusy_baliky", "ks")
    list_editable = ("hotovo", "kontrola", "do_vyroby", "do_susarny", "suche", "get_material")
    # filter and search the list
    list_filter = ("hotovo", "vytvoreno", "kontrola", "do_vyroby", "do_susarny", "suche")
    search_fields = ("zakaznik", )
    # exclude in the form
    exclude = ("get_material", "get_zbytek", "odpad", )
    # actions which the admin page can do to orders
    actions = [do_vyroby_a_material, create_pdf_with_pictures, create_pdf_without_pictures, duplicate, ]

    readonly_fields = ("image_preview", "pozadovana_delka", )
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
        #form.base_fields["pozadovana_delka"].label = "Požadovaná délka"
        form.base_fields["pozadovana_delka_cislo"].label = "Požadovaná délka"
        form.base_fields["pozadovana_delka_jednotky"].label = "Požadovaná délka - jednotky"
        form.base_fields["poznamka"].label = "Poznámka"
        form.base_fields["ks"].label = "Kusů"
        form.base_fields["baleni"].label = "Balení (proklad)"
        form.base_fields["kapovani"].label = "Kapování"
        form.base_fields["misto_hoblovani"].label = "Místo hoblování"
        form.base_fields["pozadovane_datum_vyroby"].label = "Požadované datum výroby"
        form.base_fields["image"].label = "Obrázek"
        
        return form

    def kusy_baliky(self, obj):
        return f"{obj.ks_hotovo} / {obj.baliky_celkem}"
    kusy_baliky.short_description = "Hotovo / Balíky"

    fields = ("zakaznik", "skladovy_material", "modrin", "pozadovany_rozmer", "pozadovana_delka", "pozadovana_delka_cislo", "pozadovana_delka_jednotky", "poznamka", "ks", "jednotky", "kvalita", "baleni", "misto_hoblovani", "impregnace", "kapovani", "hotovo", "kontrola", "do_vyroby", "do_susarny", "suche", "priority", "pozadovane_datum_vyroby", "image", "image_preview")

    inlines = [BalikyInline]



