from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User

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


# class AuthTokenSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ('email', 'password')
#         extra_kwargs = {'password': {'write_only': True}}
    
#     def validate(self, data):
#         user_obj = None
#         email = data.get('email')
#         password = data.get('password')
#         if email and password:
#             user_obj = User.objects.filter(email=email).first()
#             if not user_obj:
#                 raise serializers.ValidationError("This email is not registered")
#             if not user_obj.check_password(password):
#                 raise serializers.ValidationError("Incorrect credentials")
#         return data