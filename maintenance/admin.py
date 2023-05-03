from django.contrib import admin
from maintenance.models import Oprava
from django.utils.html import mark_safe
# Register your models here.

from django.conf.locale.en import formats as en_formats
from django.conf.locale.cs import formats as cs_formats
from django.utils.html import mark_safe


# change the english date format in admin display
en_formats.DATE_FORMAT = "d.m.Y"
en_formats.DATETIME_FORMAT = "d.m.Y H:i" #:s for seconds

# change the czech date format in admin display
cs_formats.DATE_FORMAT = "d.m.Y"
cs_formats.DATETIME_FORMAT = "d.m.Y H:i" #:s for seconds




@admin.register(Oprava)
class OpravaAdmin(admin.ModelAdmin):
    list_display = ("placement", "description", "person_assigned", "replacement_parts", "done", "button")
    list_editable = ("done", )
    list_filter = ("done", "date_added")


    def button(self, obj):
        return mark_safe('<input type="submit" name="_save" class="default" value="Uložit">')
    button.short_description = 'Uložit'

