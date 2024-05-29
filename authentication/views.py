from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from .models import User, OTPRegisterResend
from .serializers import (UserSerializer, UserRequestSerializer, LoginSerializer,
                          OTPRegisterResendSerializer, OTPRegisterResendRequestSerializer)
from drf_yasg.utils import swagger_auto_schema
from .utils import (check_code_expire, checking_number_of_otp,
                    send_otp_code_telegram, generate_otp_code, check_resend_otp_code)
from rest_framework_simplejwt.views import TokenObtainPairView


class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer


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
        serializer = UserSerializer(data={'username': username, 'password': password})
        if serializer.is_valid():
            objs = OTPRegisterResend.objects.filter(otp_user=serializer.instance, otp_type=1).order_by('-created_at')

            if not checking_number_of_otp(objs):
                return Response(data={"error": "Try again 12 hours later"}, status=status.HTTP_403_FORBIDDEN)

            if checking_number_of_otp(objs) == 'delete':
                OTPRegisterResend.objects.filter(otp_user=serializer.instance, otp_type=1).delete()

            serializer.save()
            otp = OTPRegisterResend.objects.create(otp_user=serializer.instance)
            otp.save()
            send_otp_code_telegram(otp)
            return Response(data={"otp_key": otp.otp_key}, status=status.HTTP_201_CREATED)
        return Response(data={"error": "please enter valid username or password"}, status=status.HTTP_400_BAD_REQUEST)

    swagger_auto_schema(
        operation_description="Verifying registration",
        operation_summary="Verify registered user",
        responses={200: UserSerializer()},
        request_body=OTPRegisterResendRequestSerializer(),
        tags=['auth']

    )

    def verify_register(self, request, *args, **kwargs):
        otp_key = request.GET.get('otp_key')
        otp_code = request.data.get('otp_code')
        otp_obj = OTPRegisterResend.objects.filter(otp_key=otp_key, otp_code=otp_code).first()

        if not otp_obj:
            return Response(data={"error": "otp code is wrong"}, status=status.HTTP_404_NOT_FOUND)

        if check_code_expire(otp_obj.created_at):
            return Response(data={"error": "Code is expired"}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.filter(id=otp_obj.otp_user).first()
        if not user:
            return Response(data={"error": "User does not exist"}, status=status.HTTP_404_NOT_FOUND)

        user.is_verified = True
        user.save(updated_fields=['is_verified'])
        otp_obj.delete()
        return Response(data=UserSerializer(user).data, status=status.HTTP_200_OK)


class ResendAndResetViewSet(ViewSet):
    def reset_password(self, request, *args, **kwargs):
        pass

    def verify_reset_password(self, request, *args, **kwargs):
        pass

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
        send_otp_code_telegram(new_otp)
        return Response(data={"otp_key": new_otp.otp_key}, status=status.HTTP_200_OK)

