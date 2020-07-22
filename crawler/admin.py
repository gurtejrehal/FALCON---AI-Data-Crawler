from django.contrib import admin
from .models import UserProfile, Notifications

admin.site.site_header = 'Falcon administration'

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'crawled_links', 'scraped_data', )
    search_fields = ['user']

class NotificationsAdmin(admin.ModelAdmin):
    list_display = ('user', 'pub_date', )
    search_fields = ['user']

    class Meta:
        verbose_name_plural = 'Notifications'


# admin.site.unregister(auth.models.Group)
# admin.site.unregister(auth.models.User)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Notifications, NotificationsAdmin)