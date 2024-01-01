from django.contrib import admin
from .models import Advertiser, Ad


class AdAdmin(admin.ModelAdmin):
    list_display = ['title', 'approve']
    list_editable = ['approve']
    list_filter = ['approve']
    search_fields = ['title']


admin.site.register(Ad, AdAdmin)
admin.site.register(Advertiser)

