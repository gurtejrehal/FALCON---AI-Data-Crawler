from django.contrib import admin
from .models import UserProfile, Notifications, Keyword, Category, Link, CrawledLinks

admin.site.site_header = 'Falcon administration'

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'crawled_links', 'scraped_data', )
    search_fields = ['user']

class NotificationsAdmin(admin.ModelAdmin):
    list_display = ('user', 'pub_date', )
    search_fields = ['user']

    class Meta:
        verbose_name_plural = 'Notifications'

class LinkAdmin(admin.ModelAdmin):
    list_display = ('keyword', 'category', 'link',)
    search_fields = ['keyword', 'category']
    list_filter = ['keyword', 'category']


class CrawledLinksAdmin(admin.ModelAdmin):
    list_display = ('userprofile', 'reschedule', 'link', )
    search_fields = ['userprofile', 'link__keyword__name', 'link__category__name']
    list_filter = ['userprofile', 'link__category', 'link__keyword__name', ]
    list_editable = ('reschedule', )


# admin.site.unregister(auth.models.Group)
# admin.site.unregister(auth.models.User)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Notifications, NotificationsAdmin)


admin.site.register(Keyword)
admin.site.register(Category)
admin.site.register(Link, LinkAdmin)
admin.site.register(CrawledLinks, CrawledLinksAdmin)