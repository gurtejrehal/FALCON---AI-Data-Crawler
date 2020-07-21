from django.contrib import admin
from .models import UserProfile

admin.site.site_header = 'Falcon administration'

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'crawled_links', 'scraped_data', )
    search_fields = ['user']


# admin.site.unregister(auth.models.Group)
# admin.site.unregister(auth.models.User)
admin.site.register(UserProfile, UserProfileAdmin)