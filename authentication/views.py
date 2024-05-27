from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from .models import User, OTP_code_save
from .serializers import UserSerializer
from django.contrib.auth.hashers import make_password
from .utils import check_for_valideness, check_code_expire, send_otp_code_telegram, generate_otp_code

class AuthenticateViewSet(ViewSet):
    def register(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email')
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')

        serializer = UserSerializer(data={'username': username,
                                          'password': password,
                                          'email': email,
                                          'first_name': first_name,
                                          'last_name': last_name})

        if check_for_valideness(email) is True:

            create_otp_obj = OTP_code_save.objects.create(otp=generate_otp_code(), username=username)

            send_otp_code_telegram(create_otp_obj)



            if serializer.is_valid():
                serializer.validated_data['is_verified'] = False
                serializer.save()
                return Response(status=status.HTTP_200_OK)

        return Response(status=status.HTTP_200_OK)

    def verify_register(self, request, *args, **kwargs):
        username = request.data.get('username')
        otp = request.data.get('otp')

        User_otp_info = OTP_code_save.objects.filter(username=username, otp=otp).values()

        if User_otp_info is not None:
            # print(50*'*', f'{User_otp_info[0]['created_at']}')
            created_at = User_otp_info[0]['created_at']
            if check_code_expire(created_at):
                User.objects.filter(username=username).update(is_verified=True)

            return Response({'user verified :)'}, status=status.HTTP_200_OK)

        return Response({'Error': 'Username or OTP code does not exist'}, status=status.HTTP_400_BAD_REQUEST)





    def login(self, request, *args, **kwargs):
        pass








class ResendAndResetViewSet(ViewSet):
    def reset_password(self, request, *args, **kwargs):
        pass

    def verify_reset_password(self, request, *args, **kwargs):
        pass

    def resend_otp_code(self, request, *args, **kwargs):
        pass

