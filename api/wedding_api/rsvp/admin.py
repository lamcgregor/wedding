from django.contrib import admin

from import_export import resources
from import_export.admin import ExportMixin
from import_export.admin import ImportExportModelAdmin
from .models import Guest, Group

class GuestInline(admin.TabularInline):
    model = Guest


class GuestAdmin(ImportExportModelAdmin):
    # inlines = [
    #     GroupInline
    # ]
    pass

class GroupAdmin(ImportExportModelAdmin):
    inlines = [
        GuestInline
    ]

admin.site.register(Group, GroupAdmin)
admin.site.register(Guest, GuestAdmin)
