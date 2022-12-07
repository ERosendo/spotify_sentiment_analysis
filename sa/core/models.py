import uuid

from django.db import models
from django.utils import timezone


class BaseModel(models.Model):
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True, editable=False)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True

    def delete(self, cascade=None):
        self.deleted_at = timezone.now()
        if cascade:
            self.cascade_deleted = True
        self.save()

    def restore(self):
        self.deleted_at = None
        self.cascade_deleted = None
        self.save()
