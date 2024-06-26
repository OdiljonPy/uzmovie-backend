from .models import About
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ViewSet
from .serializers import ContactSerializer, AboutSerializer
from .utils import send_message_telegram
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema


class ContactViewSet(ViewSet):
    @swagger_auto_schema(
        operation_description="Create Contact",
        operation_summary="Create Contact",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['first_name', 'last_name', 'message', 'email', 'phone_number'],
            properties={
                'first_name': openapi.Schema(type=openapi.TYPE_STRING, title='Contact first name'),
                'last_name': openapi.Schema(type=openapi.TYPE_STRING, title='Contact last name'),
                'message': openapi.Schema(type=openapi.TYPE_STRING, title='Contact message'),
                'email': openapi.Schema(type=openapi.TYPE_STRING, title='Contact email address'),
                'phone_number': openapi.Schema(type=openapi.TYPE_STRING, title='Contact phone number'),
            }
        ),
        responses={201: ContactSerializer()},
        tags=['contact']

    )
    def contact_create(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response(
                data={'error': 'Not authenticated'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        serializer = ContactSerializer(data=request.data)
        if serializer.is_valid():
            obj = serializer.save()
            response = send_message_telegram(obj)
            if response.status_code != 200:
                return Response(
                    data={"error": "Could not send message"},
                    status=status.HTTP_400_BAD_REQUEST)
            return Response(
                data=serializer.data,
                status=status.HTTP_201_CREATED
            )


class AboutViewSet(ViewSet):
    @swagger_auto_schema(
        operation_description="About us",
        operation_summary="About us",
        responses={200: AboutSerializer()},
        tags=['contact']
    )
    def about(self, request):
        if not request.user.is_authenticated:
            return Response(
                data={'error': 'Not authenticated'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        serializer = AboutSerializer(About.objects.all(), many=True)
        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK
        )
