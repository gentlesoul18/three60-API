from rest_framework import serializers
from .models import Todo


class TodoSerializer(serializers.ModelSerializer):
    status = serializers.CharField(required=True)
    class Meta:
        model = Todo
        fields = ["id", "title", "description", "status", "created", "updated"]



    