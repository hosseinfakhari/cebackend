from django.db import models

from django.core.management import call_command


class ActivityDataFile(models.Model):
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)


class EmissionFactorFile(models.Model):
    file = models.FileField(upload_to='uploads/')
    update_factors = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.update_factors:
            call_command('load_factors_csv', self.file.path)


class EmissionFactor(models.Model):
    activity = models.CharField(max_length=255)
    lookup_identifiers = models.CharField(max_length=512)
    unit = models.CharField(max_length=50)
    co2e = models.FloatField()
    scope = models.IntegerField(null=True)
    category = models.IntegerField(null=True)

    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
