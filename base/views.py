from .models import Contact, About
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ViewSet
from .serializers import ContactSerializer, AboutSerializer
from .utils import send_message_telegram


class ContactViewSet(ViewSet):
    def contact_list(self, request, *args, **kwargs):
        serializer = ContactSerializer(Contact.objects.all(), many=True)
        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK
        )

    def contact_create(self, request, *args, **kwargs):
        serializer = ContactSerializer(data=request.data)
        if serializer.is_valid():
            obj = serializer.save()
            send_message_telegram(obj)
            return Response(
                data=serializer.data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            data=serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class AboutViewSet(ViewSet):
    def about_view(self, request, *args, **kwargs):
        serializer = AboutSerializer(About.objects.all())
        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK
        )
