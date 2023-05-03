from django.db import models
import datetime
# Create your models here.




class Oprava(models.Model):
    date_added = models.DateField("Datum zadání", default=datetime.date.today)
    placement = models.CharField("Umístění", max_length=128)
    description = models.CharField("Popis závady", max_length=128)
    replacement_parts = models.CharField("Náhradní díly", max_length=128, blank=True, null=True)
    est_finish_date = models.DateField("Předpokládané datum opravy", blank=True, null=True)
    person_assigned = models.CharField("Kdo řeší", max_length=128, blank=True, null=True)
    scope = models.CharField("Rozsah práce", max_length=128, blank=True, null=True)
    date_finished = models.DateField("Datum dokončení", blank=True, null=True)
    note = models.CharField("Poznámka", max_length=128, blank=True, null=True)
    done = models.BooleanField("Hotovo", default=False)
    work_estimated = models.CharField("Odhad práce", max_length=128, blank=True, null=True)


    def __str__(self):
        return f"{self.date_added} - {self.placement} - {self.description}"


    class Meta:
        verbose_name = "Oprava"
        verbose_name_plural = "Opravy"

