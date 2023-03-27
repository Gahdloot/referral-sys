from django.shortcuts import render
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import parsers, renderers
from .authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.generics import GenericAPIView
from rest_framework.authtoken.views import ObtainAuthToken
from .models import User, Campaign, CampaignClick, Candidate
from django.core.exceptions import ObjectDoesNotExist

from .serializers import AuthCustomTokenSerializer, UserSerializer, UserProfileSerializer, CampaignListSerializer, CampaignCreationSerializer


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

    permission_classes = [IsAuthenticated]
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
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def post(self, request, format=None, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfilePage(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request):
        data = {}
        user = request.user
        token_user = request.auth.user
        # Token belongs to the current user
        user_queryset = User.objects.get(pk=user.id)
        user_serializer = UserProfileSerializer(user_queryset)
        data['user profile'] = user_serializer.data

        try:
            campaign_counts_queryset = Campaign.objects.filter(host__id=user.id).count()
            data['campaign_counts'] = campaign_counts_queryset

        except ObjectDoesNotExist:
            # Handle the case where no queryset is found
            data['campaign_counts'] = 0

        return Response(data)


class Campaign_page_list(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request):
        data = {}
        user = request.user
        token_user = request.auth.user
        try:
            campaign_counts_queryset = Campaign.objects.filter(host__id=user.id).count()
            data['campaign_counts'] = campaign_counts_queryset
            campaign_list = Campaign.objects.filter(host__id=user.id)
            campaign_list = CampaignListSerializer(campaign_list, many=True)
            data['campaign_list'] = campaign_list.data


        except ObjectDoesNotExist:
            # Handle the case where no queryset is found
            data['campaign_counts'] = 0
            data['message'] = 'No campaign available'


class CreateCampaign(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    def post(self, request):
        data = {}
        user = request.user
        try:
            user = User.objects.get(id=user.id)
        except ObjectDoesNotExist:
            data['message'] = 'Cannot get user for this task, please reloging'
            return Response(data)
        serializer = CampaignCreationSerializer(instance=Campaign, data= request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'success': True, 'message': 'Creation complete'})



