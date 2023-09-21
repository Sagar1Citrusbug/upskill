from django.db import models


class BaseTimestampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class BaseUserTrackedModel(models.Model):
    created_by = models.EmailField(blank=True, null=True)
    updated_by = models.EmailField(blank=True, null=True)

    class Meta:
        abstract = True


class AuditModelMixin(BaseTimestampedModel, BaseUserTrackedModel):
    class Meta:
        abstract = True
