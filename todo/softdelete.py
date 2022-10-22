from ast import Delete
from django.db import models

from todo.models import Todo


class SoftDeleteManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)



class SoftDeletedObjects(models.Manager):

    def get_queryset(self):
        return super().get_queryset().filter(is_deleted = True)



class SoftDeleteModel(models.Model):
    is_deleted = models.BooleanField(default=False)
    objects = SoftDeleteManager()
    del_objects = SoftDeletedObjects()



    class Meta:
        abstract = True

    def destroy(self):
        self.is_deleted=True
        Todo.status = 'trash'

        self.save()

        
    def restore(self):
        self.is_deleted=False
        self.save()