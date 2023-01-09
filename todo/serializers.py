from rest_framework import serializers
from django.db.models import Count, Q
from .models import Todo


class TodoSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Todo
        fields = ["id", "title", "description", "status", "created", "updated"]



    