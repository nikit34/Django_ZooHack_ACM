from django.contrib import admin
from .models import Witness, Claim, Status


@admin.register(Witness)
class WitnessAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'second_name', 'date_order', 'date_incident')
    fields = ['first_name', 'second_name', ('date_order', 'date_incident')]


@admin.register(Claim)
class ClaimAdmin(admin.ModelAdmin):
    list_display = ('witness', 'title')


@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_filter = ('status', 'borrower', 'claim')
