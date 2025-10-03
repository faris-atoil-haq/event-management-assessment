from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework_simplejwt.views import (
    TokenObtainPairView
)
from app.models import Event
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.utils import timezone
from django.conf import settings

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']


class EventSerializer(serializers.ModelSerializer):
    organizer = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Event
        fields = ['id', 'title', 'description', 'date_start', 'date_end',
                  'venue', 'capacity', 'organizer', 'created_at']
        read_only_fields = ['organizer', 'created_at']

    def validate(self, data):
        if data['date_start'] >= data['date_end']:
            raise serializers.ValidationError(
                "Start date must be before end date")
        return data


class EventCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['title', 'description', 'date_start',
                  'date_end', 'venue', 'capacity']


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        # Get token lifetimes from settings
        access_lifetime = settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME']
        refresh_lifetime = settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME']

        # Calculate expiration times
        now = timezone.now()
        access_expires_at = now + access_lifetime
        refresh_expires_at = now + refresh_lifetime

        data['access_token'] = data.pop('access')
        data['refresh_token'] = data.pop('refresh')
        # Add expiration info to response
        data.update({
            'access_token_expires_at': access_expires_at.isoformat(),
            'refresh_token_expires_at': refresh_expires_at.isoformat(),
            'access_token_expires_in': int(access_lifetime.total_seconds()),
            'refresh_token_expires_in': int(refresh_lifetime.total_seconds()),
        })

        return data

# Update the view to use custom serializer


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
