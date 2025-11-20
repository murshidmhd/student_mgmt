from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    # in this cause two values beacuse if we when ever create select that time the secound value show in the list but the first value store in the data base 
    ROLE_CHOICES = (("admin", "Admin"), ("student", "Student"))


    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    def __str__(self):
        return f"{self.username} , ({self.role})"



