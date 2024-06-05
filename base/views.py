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
                obj.delete()
                return Response(
                    data=serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST
                )
            return Response(
                data=serializer.data,
                status=status.HTTP_201_CREATED
            )


class AboutViewSet(ViewSet):
    @swagger_auto_schema(
        operation_description="About us",
        operation_summary="About us",
        manual_parameters=[
            openapi.Parameter('for_advertise', type=openapi.TYPE_INTEGER, description='for_advertise',
                              in_=openapi.IN_QUERY),
            openapi.Parameter('watch_movie', type=openapi.TYPE_INTEGER, description='watch_movie',
                              in_=openapi.IN_QUERY),
            openapi.Parameter('movie_number', type=openapi.TYPE_STRING, description='movie_number',
                              in_=openapi.IN_QUERY),
            openapi.Parameter('qr_image', type=openapi.TYPE_FILE, description='qr_image', in_=openapi.IN_QUERY),
            openapi.Parameter('phone_number', type=openapi.TYPE_STRING, description='phone_number',
                              in_=openapi.IN_QUERY),
            openapi.Parameter('email', type=openapi.TYPE_STRING, description='email', in_=openapi.IN_QUERY),
            openapi.Parameter('location', type=openapi.TYPE_STRING, description='location', in_=openapi.IN_QUERY)
        ],
        responses={200: AboutSerializer()},
        tags=['contact']
    )
    def about(self, request):
        if not request.user.is_authenticated:
            return Response(
                data={'error': 'Not authenticated'},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = AboutSerializer(About.objects.all(), many=True)
        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK
        )
