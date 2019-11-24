from django.contrib import admin
from django.contrib.auth.models import auth, User, Group
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _

# Register your models here.

from .models import Crime
from users.models import Settings

admin.site.site_header = 'Administration de CrimeAnalyzer'

#admin.site.register(Crime)
admin.site.register(Settings)

@admin.register(Crime)
class CrimeAdmin(admin.ModelAdmin):
    list_display = ('Case_Number', 'District',
                    'Primary_Type', 'Location_Description')
    search_fields = ('Case_Number',)


admin.site.unregister(Crime)
admin.site.register(Crime, CrimeAdmin)


class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )


admin.site.unregister(User)
admin.site.unregister(Group)
admin.site.register(User, CustomUserAdmin)
