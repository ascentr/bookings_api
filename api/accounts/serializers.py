from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import gettext_lazy as _


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = get_user_model()
        fields = ['name', 'username', 'email', 'password', 'phone_number']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = get_user_model().objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            name=validated_data['name'],
            password=validated_data['password']
        )
        if 'phone_number' in validated_data:
            user.phone_number = validated_data['phone_number']
        user.role = get_user_model().CUSTOMER
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'), email=email, password=password)
            if not user:
                msg = _('Unable to login with provided credentials')
                raise serializers.ValidationError(msg, code='authorization')
            return user
        else:
            msg = _('Must include "email" and "password"')
            raise serializers.ValidationError(msg, code='authorization')
