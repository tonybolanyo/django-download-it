from django.contrib import admin

from .models import Download


class DownloadAdmin(admin.ModelAdmin):

    list_display = ('title', 'status', 'registered_only', 'downloads')
    list_editable = ('status', 'registered_only',)
    prepopulated_fields = {'slug': ('title',), }

    class Meta:
        model = Download

admin.site.register(Download, DownloadAdmin)
