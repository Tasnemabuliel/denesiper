from django.db import models

class Lawyer(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15)
    specialization = models.CharField(max_length=200)
    location = models.CharField(max_length=100, null=True, blank=True)  # The location field
    created_at = models.DateTimeField(auto_now_add=True)
    photo = models.ImageField(upload_to='lawyers_photos/', null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
