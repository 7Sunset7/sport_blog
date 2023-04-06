from django.contrib import admin
from .models import *


class AthleteAdmin(admin.ModelAdmin):
    list_display = ('name', 'age', 'content', 'photo')
    prepopulated_fields = {'slug': ('name',)}


class AthleteSportAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Athlete, AthleteAdmin)
admin.site.register(AthleteSport, AthleteSportAdmin)



