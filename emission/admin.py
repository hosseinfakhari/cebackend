from django.contrib import admin
from .models import EmissionFactor, EmissionFactorFile


class EmissionFactorFileAdmin(admin.ModelAdmin):
    list_display = ('file_name', 'file_path',)

    @admin.display(description='File Name')
    def file_name(self, obj):
        return obj.file.name

    @admin.display(description='File Path')
    def file_path(self, obj):
        return obj.file.path


class EmissionFactorAdmin(admin.ModelAdmin):
    list_display = ['activity', 'lookup_identifiers', 'co2e', 'active']


admin.site.register(EmissionFactor, EmissionFactorAdmin)
admin.site.register(EmissionFactorFile, EmissionFactorFileAdmin)
