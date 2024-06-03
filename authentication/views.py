from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from .models import User, OTPRegisterResend
from .serializers import (UserSerializer, UserRequestSerializer, LoginSerializer,
                          OTPRegisterResendSerializer, OTPRegisterResendRequestSerializer)
from drf_yasg.utils import swagger_auto_schema
from .utils import (check_code_expire, checking_number_of_otp,
                    send_otp_code_telegram, generate_otp_code, check_resend_otp_code)
from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.tokens import RefreshToken
# serialzierni validate qismini yozish kerak


class LoginView(ViewSet):
    def login(self, request, *args, **kwargs):
        data = request.data
        user = User.objects.filter(username=data.get('username')).first()
        if not user:
            return Response(data={'error': 'user with this username not found', 'ok': False},
                            status=status.HTTP_400_BAD_REQUEST)
        if not user.is_verified:
            return Response(data={"error": "user is not verified", "ok": False}, status=status.HTTP_400_BAD_REQUEST)

        if user.check_password(data.get('password')):
            token = RefreshToken.for_user(user)
            return Response(data={'access': str(token.access_token), 'refresh': str(token)}, status=status.HTTP_200_OK)
        return Response(data={'error': 'password is incorrect', 'ok': False}, status=status.HTTP_400_BAD_REQUEST)


class AuthenticateViewSet(ViewSet):
    swagger_auto_schema(
        operation_description="Register",
        operation_summary="Register new users",
        responses={201: OTPRegisterResendSerializer()},
        request_body=UserRequestSerializer(),
        tags=['auth']

    )

    def register(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        user = User.objects.filter(username=username).first()
        if user and user.is_verified:
            return Response(data={"error": "You already registered"}, status=status.HTTP_403_FORBIDDEN)
        if user:
            serializer = UserSerializer(user, data={'password': make_password(password)}, partial=True)
        else:
            serializer = UserSerializer(data={"username": username, "password": make_password(password)})
        if not serializer.is_valid():
            return Response({"error": serializer.errors}, status.HTTP_400_BAD_REQUEST)
        serializer.save()
        objs = OTPRegisterResend.objects.filter(otp_user=serializer.instance, otp_type=1).order_by('created_at')

        if not checking_number_of_otp(objs):
            return Response(data={"error": "Try again 12 hours later"}, status=status.HTTP_403_FORBIDDEN)

        if checking_number_of_otp(objs) == 'delete':
            OTPRegisterResend.objects.filter(otp_user=serializer.instance, otp_type=1).delete()

        otp = OTPRegisterResend.objects.create(otp_user=serializer.instance)
        otp.save()

        response = send_otp_code_telegram(otp)
        if response.status_code != 200:
            otp.delete()
            return Response({"error": "Error occured while sending otp code"})
        return Response(data={"otp_key": otp.otp_key}, status=status.HTTP_201_CREATED)

    swagger_auto_schema(
        operation_description="Verifying registration",
        operation_summary="Verify registered user",
        responses={200: UserSerializer()},
        request_body=OTPRegisterResendRequestSerializer(),
        tags=['auth']

    )

    def verify_register(self, request, *args, **kwargs):
        otp_obj = OTPRegisterResend.objects.filter(otp_key=request.data.get('otp_key'), otp_code=request.data.get('otp_code')).first()
        print(50 * '*', otp_obj, 50 * '*')
        if otp_obj is False:
            return Response(data={"error": "otp code is wrong"}, status=status.HTTP_404_NOT_FOUND)

        if not check_code_expire(otp_obj.created_at):
            return Response(data={"error": "Code is expired"}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.filter(id=otp_obj.otp_user.id).first()
        if not user:
            return Response(data={"error": "User does not exist"}, status=status.HTTP_404_NOT_FOUND)

        user.is_verified = True
        user.save(update_fields=['is_verified'])
        otp_obj.delete()
        return Response(data=UserSerializer(user).data, status=status.HTTP_200_OK)


class ResendAndResetViewSet(ViewSet):
    def reset_password(self, request, *args, **kwargs):
        data = request.data
        user = User.objects.filter(username=data.get('username')).first()
        if user.is_authenticated:
            send_code = OTPRegisterResend.objects.create(otp_user=user, otp_type=2)
            send_code.save()
            send_otp_code_telegram(send_code)
            return Response({'code has been sent'})
        if not user.is_authenticated:
            return Response({'/log in please'}, status=status.HTTP_403_FORBIDDEN)



        return Response(data={"log in please"}, status=status.HTTP_200_OK)







    def verify_reset_password(self, request, *args, **kwargs):
        otp_code = request.data.get('otp_code')
        new_password = request.data.get('password')
        otp_key = request.data.get('key')

        objects = OTPRegisterResend.objects.filter(otp_key=otp_key, otp_code=otp_code).first()
        print(objects.otp_code, 50*'*')
        #if checking_number_of_otp(otp_objects):
        if objects:
            changed_password = User.objects.filter(id=objects.otp_user_id)
            changed_password.password = make_password(new_password)
            #changed_password.save()
            return Response(data={'changed'}, status=status.HTTP_200_OK)
        return Response(data={"log in please"}, status=status.HTTP_200_OK)






    swagger_auto_schema(
        operation_description="Verifying registration",
        operation_summary="Verify registered user",
        responses={200: OTPRegisterResendSerializer()},
        tags=['auth']

    )

    def resend_otp_code(self, request, *args, **kwargs):
        otp_key = request.GET.get('otp_key')
        otp_obj = OTPRegisterResend.objects.filter(otp_key=otp_key).first()
        # bu yerda otp codni qayta tekshirish uchun otp key soralyapti
        if not otp_obj:
            return Response(data={"error": "Otp key is wrong"}, status=status.HTTP_404_NOT_FOUND)

        objs = OTPRegisterResend.objects.filter(otp_user=otp_obj.otp_user, otp_type=2).order_by('-created_at')
        if not checking_number_of_otp(objs):
            return Response(data={"error": "Try again 12 hours later"}, status=status.HTTP_403_FORBIDDEN)

        if checking_number_of_otp(objs) == 'delete':
            OTPRegisterResend.objects.filter(otp_user=otp_obj.otp_user, otp_type=2).delete()

        if not check_resend_otp_code(otp_obj.created_at):
            return Response(data={"error": "Try again a minute later"}, status=status.HTTP_403_FORBIDDEN)

        new_otp = OTPRegisterResend.objects.create(otp_user=otp_obj.otp_user)
        new_otp.save()
        response = send_otp_code_telegram(new_otp)
        if response.status_code != 200:
            new_otp.delete()
            return Response({"error": "Could not send otp to telegram"}, status.HTTP_400_BAD_REQUEST)
        otp_obj.delete()
        return Response(data={"otp_key": new_otp.otp_key}, status=status.HTTP_200_OK)

