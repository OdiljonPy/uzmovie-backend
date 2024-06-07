from .models import Contact, About
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ViewSet
from .serializers import ContactSerializer, AboutSerializer
from .utils import send_message_telegram
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema


class ContactViewSet(ViewSet):
    @swagger_auto_schema(
        operation_description="Contact list",
        operation_summary="Contact list",
        responses={200: ContactSerializer()},
        tags=['contact']
    )
    def contact_list(self, request, *args, **kwargs):
        serializer = ContactSerializer(Contact.objects.all(), many=True)
        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK
        )

    @swagger_auto_schema(
        operation_description="Create Contact",
        operation_summary="Create Contact",
        manual_parameters=[
            openapi.Parameter(
                'first_name', type=openapi.TYPE_STRING, description='first_name', in_=openapi.IN_QUERY, required=True),
            openapi.Parameter(
                'last_name', type=openapi.TYPE_STRING, description='last_name_name', in_=openapi.IN_QUERY, required=True),
            openapi.Parameter(
                'message', type=openapi.TYPE_STRING, description='message', in_=openapi.IN_QUERY, required=True),
            openapi.Parameter(
                'email', type=openapi.TYPE_STRING, description='email', in_=openapi.IN_QUERY, required=True),
            openapi.Parameter(
                'phone_number', type=openapi.TYPE_STRING, description='phone_number', in_=openapi.IN_QUERY,
                required=True),
        ],
        responses={
            404: 'Not Found',
            200: ContactSerializer()
        },
        tags=['contact']
    )
    def contact_create(self, request, *args, **kwargs):
        serializer = ContactSerializer(data=request.data)
        if serializer.is_valid():
            obj = serializer.save()
            a = send_message_telegram(obj)
            if a == 200:
                return Response(
                    data=serializer.data,
                    status=status.HTTP_201_CREATED
                )
        return Response(
            data=serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class AboutViewSet(ViewSet):
    @swagger_auto_schema(
        operation_description="About us",
        operation_summary="About us",
        responses={200: ContactSerializer()},
        tags=['contact']
    )
    def about_view(self, request, *args, **kwargs):
        serializer = AboutSerializer(About.objects.all())
        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK
        )
