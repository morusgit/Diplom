from rest_framework import serializers

from modules.models import Module
from modules.validators import YoutubeUrlValidator, ForbiddenWordsValidator


class ModuleSerializer(serializers.ModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())

    class Meta:
        model = Module
        fields = '__all__'
        validators = [
            YoutubeUrlValidator(field='url_video'),
            ForbiddenWordsValidator(field='name'),
            ForbiddenWordsValidator(field='description'),
            serializers.UniqueTogetherValidator(
                queryset=Module.objects.all(),
                fields=('name', 'description'),
                message='Модуль с таким названием и описанием уже существует'
            ),
        ]
