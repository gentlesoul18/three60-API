from django.db import models
from django.conf import settings



User = settings.AUTH_USER_MODEL
# Create your models here.


class Todo(models.Model):
    BACKLOG = "Backlog"
    IN_PROGRESS = "In Progress"
    FINISHED = "Finished"
    OVER_DUE = "Over Due"
    TRASH = "Trash"
    TODO_STATUS_CHOICES = [
        (BACKLOG, "Backlog"),
        (IN_PROGRESS, "In Progress"),
        (FINISHED, "Finished"),
        (OVER_DUE, "Over Due"),
        (TRASH, "Trash"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=500)
    status = models.CharField(
        max_length=20, choices=TODO_STATUS_CHOICES, default=BACKLOG
    )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)
    

    def hide(self):
        self.deleted = True
        self.status = "Trash"
        self.save()

    def restore(self):
        self.deleted = False
        self.save()

    class Meta:
        ordering = ["title"]

    def __str__(self) -> str:
        # string to be used when the models is queried
        return self.title
