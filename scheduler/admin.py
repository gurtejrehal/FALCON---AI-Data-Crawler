from django.contrib import admin
from scheduler.models import ScrapedLink, RescrapedLink

class ScrapedLinkAdmin(admin.ModelAdmin):

    list_display = ('link', 'schedule_day', 'pub_date', )
    search_fields = ['link']
    list_filter = ['link', 'pub_date', ]
    list_editable = ('schedule_day', )


class RescrapedLinkAdmin(admin.ModelAdmin):

    list_display = ('link', 'score', 'done', 'pub_date', )
    search_fields = ['link']
    list_filter = ['link', 'pub_date', ]
    list_editable = ('done', )


admin.site.register(ScrapedLink, ScrapedLinkAdmin)
admin.site.register(RescrapedLink, RescrapedLinkAdmin)
