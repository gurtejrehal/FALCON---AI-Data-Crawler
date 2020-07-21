from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    picture = models.ImageField(null=True, upload_to='profile_images')
    crawled_links = models.IntegerField(default=0)
    scraped_data = models.IntegerField(default=0)


    def __str__(self):
        return self.user.username

    #
    # def time_spent_scraping(self):
    #
    #     now = timezone.now()


