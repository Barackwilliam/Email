from django.db import models
from django.contrib.auth.models import User

class EmailEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    region = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    school_name = models.CharField(max_length=200)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)

    def __str__(self):
        return self.school_name
