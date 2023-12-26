from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    pass


class Note(models.Model):
    id = models.AutoField(primary_key=True)
    note_data = models.TextField()
    notes_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notes")
