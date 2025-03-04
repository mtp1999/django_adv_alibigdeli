from rest_framework import serializers
from app_account.models import User
import django.contrib.auth.password_validation as validators
from django.core import exceptions
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _


class RegistrationSer(serializers.ModelSerializer):
    password1 = serializers.CharField(max_length=255, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'password1']

    def validate(self, attrs):
        if attrs.get('password') != attrs.get('password1'):
            raise serializers.ValidationError({'error': 'passwords not match!'})

        try:
            validators.validate_password(attrs.get('password'))
        except exceptions.ValidationError as e:
            raise serializers.ValidationError({'errors': list(e)})

        return super().validate(attrs)

    def create(self, validated_data):
        return User.objects.create_user(email=validated_data['email'], password=validated_data['password'])


class GetAuthTokenSer(serializers.Serializer):
    email = serializers.CharField(
        label=_("email"),
        style={'input_type': 'email'},
        write_only=True
    )
    password = serializers.CharField(
        label=_("Password"),
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )
    token = serializers.CharField(
        label=_("Token"),
        read_only=True
    )

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'),
                                email=email, password=password)

            # The authenticate call simply returns None for is_active=False
            # users. (Assuming the default ModelBackend authentication
            # backend.)
            if not user:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = _('Must include "email" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs