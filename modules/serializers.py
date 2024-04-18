from rest_framework import serializers

from modules.models import Module, Subscription
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


class SubscriptionSerializer(serializers.ModelSerializer):
    module_name = serializers.SerializerMethodField()
    user_email = serializers.SerializerMethodField()

    def get_module_name(self, obj):
        return obj.module.name

    def get_user_email(self, obj):
        return obj.user.email

    class Meta:
        model = Subscription
        fields = '__all__'
        extra_fields = ['module_name', 'user_email']
