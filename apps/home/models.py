from django.db import models
import uuid


class BaseModel(models.Model):
    guid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    created_date = models.DateTimeField(auto_now_add=True, null=True)
    edited_date = models.DateTimeField(auto_now=False, null=True, blank=True)
    
    class Meta:
        abstract = True