from django.contrib import admin

from import_export import resources
from import_export.admin import ExportMixin
from import_export.admin import ImportExportModelAdmin
from .models import Rsvp

class RsvpAdmin(ImportExportModelAdmin):
    pass

admin.site.register(Rsvp, RsvpAdmin)