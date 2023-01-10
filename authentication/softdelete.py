from django.db import models


class SoftDelete(models.Model):

    is_deleted = models.BooleanField(default=False)


    class Meta:
        abstract = True