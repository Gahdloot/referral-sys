from django.shortcuts import render
from rest_framework import status
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import parsers, renderers
from .authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.generics import GenericAPIView
from rest_framework.authtoken.views import ObtainAuthToken

from .serializers import AuthCustomTokenSerializer, UserSerializer


# Create your views here.
class LogInAPIView(ObtainAuthToken):
    serializer_class = AuthCustomTokenSerializer

    def post(self, request):
        serializer = AuthCustomTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        content = {
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'phone': user.phone,
            'token': token.key,
        }
        return Response(content, status=status.HTTP_200_OK)



class LogoutAPIView(APIView):

    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def post(self, request, *args, **kwargs):
        """
        Handle POST request to logout user.
        """
        # perform any additional logic you need here
        request.user.auth_token.delete() # This deletes the authentication token associated with the user
        return Response(status=status.HTTP_200_OK)


class RegisterAPIView(APIView):
    # serializer_class = RegisterUserSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def post(self, request, format=None, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

