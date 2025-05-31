from django.db import models

class CitySearch(models.Model):

    city = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)
    session_key = models.CharField(max_length=200)
    user_agent = models.TextField()
    ip_address = models.GenericIPAddressField(protocol="both")

    def __str__(self) -> str:
        return f"{self.city} at {self.timestamp.strftime('%Y-%m-%d %H:%M')}"
