from rest_framework import serializers
from django.db.models import Count, Q
from .models import Todo


class TodoSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Todo
        fields = ["id", "title", "description", "status", "created", "updated", "nBacklog", 'nInProgress', 'nFinished', 'nOverDue', 'nTrash']



    nBacklog = serializers.IntegerField(read_only = True)
    nInProgress = serializers.IntegerField(read_only = True)
    nFinished = serializers.IntegerField(read_only = True)
    nOverDue = serializers.IntegerField(read_only = True)
    nTrash = serializers.IntegerField(read_only = True)

