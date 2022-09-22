from django.contrib.auth import get_user_model
from django.db import models

# Create your models here.
User = get_user_model()


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    registered = models.DateTimeField(auto_now_add=True)
