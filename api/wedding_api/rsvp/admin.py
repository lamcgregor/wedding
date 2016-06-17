from django.contrib import admin
from django.forms.models import inlineformset_factory

from import_export import resources
from import_export.admin import ExportMixin
from import_export.admin import ImportExportModelAdmin
from .models import Guest, Group
from .forms import GuestInlineForm


class GuestResource(resources.ModelResource):

    class Meta:
        model = Guest
        import_id_fields = ('first_name', 'last_name')
        fields = ('first_name', 'last_name', 'email', 'attending', 'dietary_requirements', 'dietary_other', 'comments')


class GuestInline(admin.StackedInline):
    model = Guest
    extra = 1
    form = GuestInlineForm


class GuestAdmin(ImportExportModelAdmin):
    resource_class = GuestResource


class GroupAdmin(ImportExportModelAdmin):
    inlines = [
        GuestInline
    ]

admin.site.register(Group, GroupAdmin)
admin.site.register(Guest, GuestAdmin)
