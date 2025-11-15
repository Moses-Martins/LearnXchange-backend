import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustomUser(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    bio = models.TextField(null=True, blank=True)
    profile_image_url = models.CharField(max_length=255, null=True, blank=True)