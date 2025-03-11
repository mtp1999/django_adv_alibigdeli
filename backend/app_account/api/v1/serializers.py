from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from app_account.models import User, Profile
import django.contrib.auth.password_validation as validators
from django.core import exceptions
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt import serializers as jwt_serializers


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
            raise serializers.ValidationError({'errors': list(e.messages)})

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
            if not user.is_verified:
                raise serializers.ValidationError({'detail': 'User is not verified.'})
        else:
            msg = _('Must include "email" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs


class CreateJwtSer(jwt_serializers.TokenObtainPairSerializer):
    """
    customize serializer to return email and user_id beside the tokens.
    """
    def validate(self, attrs):
        validated_data = super().validate(attrs)
        validated_data['email'] = self.user.email
        validated_data['user_id'] = self.user.id
        return validated_data


class ChangePasswordSer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    new_password1 = serializers.CharField(required=True)

    def validate(self, attrs):
        if attrs.get('new_password') != attrs.get('new_password1'):
            raise serializers.ValidationError({'error': 'passwords not match!'})

        try:
            validators.validate_password(attrs.get('new_password'))
        except exceptions.ValidationError as e:
            raise serializers.ValidationError({'errors': list(e.messages)})

        return super().validate(attrs)


class ProfileSer(serializers.ModelSerializer):
    email = serializers.EmailField(source='user.email', read_only=True)
    user_id = serializers.IntegerField(source='user.pk', read_only=True)
    profile_id = serializers.IntegerField(source='pk', read_only=True)

    class Meta:
        model = Profile
        fields = ['user_id', 'email', 'profile_id', 'username', 'first_name', 'last_name', 'description']


class VerificationResendSer(serializers.Serializer):
    email = serializers.EmailField()

    def validate(self, attrs):
        """
        description:
            1-check if the user exists with the sent email.
            2-check the user is not verified.
            3-return user object.
        """
        user_object = get_object_or_404(User, email=attrs.get('email'))
        if user_object.is_verified:
            raise ValidationError("User is already verified.", code="already_verified")
        attrs['user_object'] = user_object
        return super().validate(attrs)
