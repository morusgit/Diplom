from rest_framework import serializers
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    """ Сериализатор пользователя. """
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'telegram', 'password', 'role', 'is_active')
        # fields = '__all__'
