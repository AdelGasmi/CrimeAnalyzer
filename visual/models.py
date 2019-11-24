from django.contrib import admin
from django.db import models


class Crime(models.Model):
    Case_Number = models.TextField(max_length=1000, default='')
    Date = models.DateField()
    Block = models.TextField(max_length=1000, default='null')
    #IUCR = models.IntegerField()
    Primary_Type = models.TextField(max_length=1000)
    #Description = models.TextField(max_length=1000)
    Location_Description = models.TextField(max_length=1000, default='null')
    Arrest = models.BooleanField()
    #Domestic = models.TextField(max_length=1000)
    #Beat = models.IntegerField()
    District = models.IntegerField(default=0)
    #Ward = models.IntegerField()
    #Community_Aarea = models.IntegerField()
    Code_Penal = models.TextField(max_length=100, default='0')
    #X_coordinate = models.IntegerField()
    #Y_coordinate = models.IntegerField()
    #Year = models.IntegerField()
    #Updated_on = models.DateTimeField()
    Latitude = models.FloatField(default=0)
    Longitude = models.FloatField(default=0)

    def __str__(self):
        ret = self.Case_Number + ',' + \
            str(self.District) + ',' + self.Primary_Type + \
            ',' + self.Location_Description
        return ret

    class Meta:
        managed = True
        db_table = 'crimes_table'


class CrimeAdmin(admin.ModelAdmin):
    list_display = ('Case_Number', 'District')
