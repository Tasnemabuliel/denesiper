from django.db import models
from django.contrib.auth.models import User  # Assuming you have user accounts
from django.utils import timezone

class Lawyer(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    specialization = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    photo = models.ImageField(upload_to='lawyer_photos/', null=True, blank=True)
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=0.0)
    price_range = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    years_of_experience = models.PositiveIntegerField()
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)  # Automatically set the current time


    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Review(models.Model):
    lawyer = models.ForeignKey(Lawyer, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Review author
    rating = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 6)])  # 1-5 stars
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user} for {self.lawyer}"
