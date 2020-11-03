from django.contrib import admin
from .models import userdata, workshop

@admin.register(userdata)
class userdataAdmin(admin.ModelAdmin):
    list_display = ('name', 'message')
    ordering = ('name',)


@admin.register(workshop)
class wshopsdataAdmin(admin.ModelAdmin):
    list_display = ('topic', 'date', 'desc')
    ordering = ('date',)