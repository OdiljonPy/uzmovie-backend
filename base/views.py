import requests
from .models import Contact
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ViewSet
from .serializers import ContactSerializer


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
            TOKEN = "6912718237:AAH2v2r4x2TuYnHqfpbi1ci43AxYKEiBWoE"
            CHAT_ID = "5093765356"
            message = {f"Project:Uzmovi-backend\n"
                       f"phone_number:{obj.phone_number}\n"
                       f"first_name:{obj.first_name}\n"
                       f"last_name:{obj.last_name}\n"
                       f"email:{obj.email}\n"
                       f"message:{obj.message}"
                       }

            TELEGRAM_API_URL = f"https://api.telegram.org/bot{TOKEN}/sendMessage?text={message}&chat_id={CHAT_ID}"
            requests.get(TELEGRAM_API_URL)
            return Response(
                data=serializer.data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            data=serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
