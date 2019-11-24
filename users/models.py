from django.db import models
from django.contrib.auth.models import User

# Create your models here.
#Store users settings here
class Settings(models.Model):
    user = models.OneToOneField(User, on_delete="models.CASCADE")
    limit = models.IntegerField(default=20000)
    class Meta:
        managed = True

