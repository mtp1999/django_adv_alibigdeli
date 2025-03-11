from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt import views as jwt_views
from mail_templated import EmailMessage
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from app_account.api.v1 import serializers
from app_account.models import User
from app_account.utils import EmailThread


class RegistrationAPIView(generics.GenericAPIView):
    serializer_class = serializers.RegistrationSer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            email = serializer.validated_data['email']
            user_object = get_object_or_404(User, email=email)
            token = self.get_jwt_access_token_for_user(user_object)
            email_object = EmailMessage('email/account_verification.tpl', {'token': token}, "from@example.com", to=[email])
            EmailThread(email_object).start()
            return Response(
                {'detail': 'your account created successfully. now check your email to verify your account'},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def get_jwt_access_token_for_user(user_object):
        refresh = RefreshToken.for_user(user_object)
        return str(refresh.access_token)


class GetAuthTokenView(ObtainAuthToken):

    serializer_class = serializers.GetAuthTokenSer

    def post(self, request, *args, **kwargs):
        """
        description: get user auth token.
        input --> like login form (email and password)
        output --> auth_token and other custom data
        """

        serializer = self.serializer_class(data=request.data, context={'request': request})

        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'user_id': user.pk,
                'email': user.email
            })
        else:
            print(serializer.errors)
            return Response(serializer.errors)


class DeleteAuthTokenView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        """
        description: delete user's auth token
        """
        try:
            request.user.auth_token.delete()
        except (AttributeError, ObjectDoesNotExist):
            pass
        return Response({'detail': 'auth token deleted'}, status=status.HTTP_204_NO_CONTENT)


class CreateJwtView(jwt_views.TokenObtainPairView):
    """
    description: create user jwt tokens(access and refresh tokens).
    input --> like login form (email and password)
    output --> jwt tokens and other custom data
    """
    serializer_class = serializers.CreateJwtSer


class ChangePasswordView(APIView):
    serializer_class = serializers.ChangePasswordSer
    permission_classes = [IsAuthenticated]

    def get_user_object(self, queryset=None):
        obj = self.request.user
        return obj

    def put(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user = self.get_user_object()

        if not user.check_password(serializer.data.get("old_password")):
            return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)

        # set_password also hashes the password that the user will get
        user.set_password(serializer.data.get("new_password"))
        user.save()

        return Response({'detail': 'Password updated successfully'})


class ProfileView(generics.RetrieveUpdateAPIView):
    """
    description: get, update user's profile
    """
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.ProfileSer

    def get_object(self):
        return self.request.user.profile


class TestSendEmailView(generics.GenericAPIView):

    def get(self, request, *args, **kwargs):

        email_object = EmailMessage('email/test.tpl', {'name': 'the admin1'}, "from@example.com", to=["to@example.com"])
        thread1 = EmailThread(email_object).start()
        return Response({'detail': 'email sent.'})


class VerificationView(generics.GenericAPIView):

    def get(self, request, token, *args, **kwargs):
        try:
            decoded_token = AccessToken(token)
            payload = decoded_token.payload
            user_object = get_object_or_404(User, pk=payload.get('user_id'))
            if user_object.is_verified:
                return Response({'detail': 'user is already verified!'}, status=status.HTTP_400_BAD_REQUEST)
            user_object.is_verified = True
            user_object.save()
            return Response({'detail': 'user is verified successfully!'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e) or 'Unknown error'}, status=status.HTTP_400_BAD_REQUEST)


class VerificationResendView(generics.GenericAPIView):
    serializer_class = serializers.VerificationResendSer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_object = serializer.validated_data['user_object']
        token = self.get_jwt_access_token_for_user(user_object)
        email_object = EmailMessage(
            'email/account_verification.tpl', {'token': token}, "from@example.com", to=[user_object.email]
        )
        EmailThread(email_object).start()
        return Response({'detail': 'check your email to verify your account.'}, status=status.HTTP_200_OK)

    @staticmethod
    def get_jwt_access_token_for_user(user_object):
        refresh = RefreshToken.for_user(user_object)
        return str(refresh.access_token)