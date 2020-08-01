from django.db import models

class IPLink(models.Model):
    """
    IP Links to get IP's
    """
    link = models.TextField(max_length=250, blank=False, null=False)
    pub_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.link


class IP(models.Model):
    """
    IP Database for random IP's
    """
    ip = models.TextField(max_length=50, blank=False)
    pub_date = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.ip


