from django.contrib.auth import get_user_model
from rest_framework import serializers
from apps.accounts.models import EmailUser
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate


class AuthTokenSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(style={'input_type': 'password'})

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if email and password:
            user = authenticate(email=email, password=password)
            if user:
                if not user.is_active:
                    msg = _('User account is disabled.')
                    return msg
            else:
                msg = _('Unable to log in with provided credentials.')
                return msg
        else:
            msg = _('Must include "email" and "password".')
            return msg

        data['user'] = user
        return data


class CreateEmailUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    token = serializers.SerializerMethodField()

    class Meta:
        model = EmailUser
        fields = ('id', 'first_name', 'last_name', 'email', 'token', 'password')


    def get_token(self, validated_data):
        user = EmailUser.objects.filter(email=validated_data.email)
        token = Token.objects.get(user=user[0])
        return token.key


class UpdateUserInfoSerializer(serializers.ModelSerializer):
    token = serializers.SerializerMethodField()

    class Meta:
        model = EmailUser
        exclude = ('email', 'password')

    def get_token(self, validated_data):
        user = EmailUser.objects.filter(email=self.context['request'].data['email'])
        token = Token.objects.get(user=user)
        return token.key
