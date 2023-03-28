import re
from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User, Campaign, Candidate, CampaignClick
from . import validators


class AuthCustomTokenSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(username=email, password=password)

            if user:
                if not user.is_active:
                    # msg = _('User account is disabled.')
                    msg = {"error": ("User account is disabled.")}
                    raise serializers.ValidationError(msg)
            else:
                msg = {"error": ('Unable to log in with provided credentials.')}
                raise serializers.ValidationError(msg)
        else:
            msg = {"error": ('Must include "email" and "password"')}
            raise serializers.ValidationError(msg)

        attrs['user'] = user
        return attrs

    

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(required=True, max_length=255, allow_blank=False, write_only=True)
    confirm_password = serializers.CharField(required=True, max_length=255, allow_blank=False, write_only=True)

    class Meta:
        model = User
        fields =( 
            'email', 
            'first_name', 
            'last_name', 
            'phone', 
            'company_name',
            'password',
            'confirm_password',
            )


    def create(self, validated_data):
        user = User(
            email=validated_data.get('email'),
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            phone=validated_data.get('phone', ''),
            company_name=validated_data.get('company_name', ''),
        )
        user.set_password(validated_data.get('password'))
        user.save()
        return user
    

    def validate(self, data):
        """
        Check if password match.
        """
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Password does not match!!!")
        return data

    def validate_phone(self, value):
        """
        Validate phone number using regular expression
        """
        if value:
            phone_regex = re.compile(r'^\d{11}$')
            result = phone_regex.match(value)
            if not result:
                raise serializers.ValidationError(f'{value} is not a valid phone number')
            # print(result.group())
        return value


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'phone_number', 'company_name']


class CampaignListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Campaign
        fields = ['id', 'name', 'clicks', 'is_active']

class CampaignCreationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Campaign
        fields = ['host', 'name', 'link', 'closing_date']

class CampaignPageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Campaign
        fields = ['host', 'name', 'link', 'created_at', 'closing_date', 'is_active', 'description', 'contestant_number']

class CandidateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Candidate
        fields = ['name', 'clicks', 'referral_code']