from  django.urls import path
from . import views
# from rest_framework.authtoken import views


urlpatterns = [
    path('api-token-auth/', views.ObtainAuthToken.as_view(), name='login'),
    path('api-logout/', views.LogoutAPIView.as_view(), name='api_logout'),
]