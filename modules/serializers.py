from rest_framework import serializers

from modules.models import Module


class ModuleSerializer(serializers.ModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())

    class Meta:
        model = Module
        fields = '__all__'
