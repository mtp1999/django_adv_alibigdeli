from django.core.exceptions import ObjectDoesNotExist
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from app_account.api.v1.serializers import RegistrationSer, GetAuthTokenSer


class RegistrationAPIView(generics.GenericAPIView):
    serializer_class = RegistrationSer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.validated_data['email'])
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetAuthTokenView(ObtainAuthToken):

    serializer_class = GetAuthTokenSer

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
