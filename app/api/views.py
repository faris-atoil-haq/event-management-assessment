from django.core.mail import send_mail
from django.utils import timezone
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from app.models import Event, Attendee
from .serializers import (
    EventSerializer, EventCreateSerializer, UserSerializer
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)
from django.conf import settings

class EventListView(generics.ListCreateAPIView):
    queryset = Event.objects.all().order_by('-created_at')
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return EventCreateSerializer
        return EventSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class EventDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Only allow owners to edit or delete their events
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return Event.objects.filter(user=self.request.user)
        return Event.objects.all()


class MyEventsView(generics.ListAPIView):
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        registration = Attendee.objects.filter(user=self.request.user)
        if registration.exists():
            return Event.objects.filter(registrations__in=registration).distinct()
        return Event.objects.none()


@api_view(['GET'])
def SendEmailView(request, email=None):
    if email:
        res = send_mail('Test Email from Event Management System',
                        f'This is a test email sent from the https://event-management-assessment.vercel.app/ with Django backend.',
                        settings.EMAIL_HOST_USER, [email],
                        True)
        if res:
            return Response({"message": "Email sent successfully."})
        else:
            return Response({"message": "Failed to send email."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return Response({"message": "No email provided."}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_profile(request):
    serializer = UserSerializer(request.user)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def register_to_event(request, event_id):
    try:
        event = Event.objects.get(id=event_id)
        Attendee.objects.create(user=request.user, event=event, status='pending')
        return Response({
            'message': f'Successfully registered to {event.title}',
            'event_id': event.id
        })
    except Event.DoesNotExist:
        return Response(
            {'error': 'Event not found'},
            status=status.HTTP_404_NOT_FOUND
        )


class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        if response.status_code == 200:
            # Get token lifetimes from settings
            access_lifetime = settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME']
            refresh_lifetime = settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME']

            # Calculate expiration times
            now = timezone.now()
            access_expires_at = now + access_lifetime
            refresh_expires_at = now + refresh_lifetime
            
            response.data['access_token'] = response.data.pop('access')
            response.data['refresh_token'] = response.data.pop('refresh')
            # Add expiration info to response
            response.data.update({
                'access_token_expires_at': access_expires_at.isoformat(),
                'refresh_token_expires_at': refresh_expires_at.isoformat(),
                'access_token_expires_in': int(access_lifetime.total_seconds()),
                'refresh_token_expires_in': int(refresh_lifetime.total_seconds()),
            })

        return response


class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        if response.status_code == 200:
            # Get token lifetimes from settings
            access_lifetime = settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME']
            refresh_lifetime = settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME']

            # Calculate expiration times
            now = timezone.now()
            access_expires_at = now + access_lifetime
            refresh_expires_at = now + refresh_lifetime

            # Add expiration info to response
            response.data.update({
                'access_token_expires_at': access_expires_at.isoformat(),
                'refresh_token_expires_at': refresh_expires_at.isoformat(),
                'access_token_expires_in': int(access_lifetime.total_seconds()),
                'refresh_token_expires_in': int(refresh_lifetime.total_seconds()),
            })

        return response


class CustomTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        if response.status_code == 200:
            # Get token lifetimes from settings
            access_lifetime = settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME']

            # Calculate expiration times
            now = timezone.now()
            access_expires_at = now + access_lifetime
            
            response.data['access_token'] = response.data.pop('access')

            # If refresh token is rotated, add new refresh token expiration
            if 'refresh' in response.data:
                refresh_lifetime = settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME']
                refresh_expires_at = now + refresh_lifetime
                response.data['refresh_token'] = response.data.pop('refresh')

                response.data.update({
                    'access_token_expires_at': access_expires_at.isoformat(),
                    'refresh_token_expires_at': refresh_expires_at.isoformat(),
                    'access_token_expires_in': int(access_lifetime.total_seconds()),
                    'refresh_token_expires_in': int(refresh_lifetime.total_seconds())
                })
            else:
                # Add expiration info to response
                response.data.update({
                    'access_token_expires_at': access_expires_at.isoformat(),
                    'access_token_expires_in': int(access_lifetime.total_seconds())
                })
                
        return response
