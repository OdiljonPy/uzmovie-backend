from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from .models import User, OTPRegisterResend
from .serializers import (UserSerializer, UserRequestSerializer, LoginSerializer,
                          OTPRegisterResendSerializer, OTPRegisterResendRequestSerializer)
from drf_yasg.utils import swagger_auto_schema
from .utils import check_code_expire, checking_numberOfOTPs
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
            checking = OTPRegisterResend.objects.filter(otp_user=serializer.instance).order_by('-created_at')

            if checking_numberOfOTPs(checking) == 'delete':
                OTPRegisterResend.objects.filter(otp_user=serializer.instance).delete()

            elif not checking_numberOfOTPs(checking):
                return Response(data={"error": "Try again 12 hours later"}, status=status.HTTP_403_FORBIDDEN)

            serializer.save()
            otp = OTPRegisterResend.objects.create(otp_user=serializer.instance)
            otp.save()
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
        if otp_obj:
            if check_code_expire(otp_obj.created_at):
                user = User.objects.filter(id=otp_obj.otp_user).first()
                if user:
                    user.is_verified = True
                    user.save(updated_fields=['is_verified'])
                    otp_obj.delete()
                    return Response(data=UserSerializer(user).data, status=status.HTTP_200_OK)
                return Response(data={"error": "something went wrong"}, status=status.HTTP_404_NOT_FOUND)
            return Response(data={"error": "Code is expired"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(data={"error": "otp code is wrong"}, status=status.HTTP_404_NOT_FOUND)


class ResendAndResetViewSet(ViewSet):
    def reset_password(self, request, *args, **kwargs):
        pass

    def verify_reset_password(self, request, *args, **kwargs):
        pass

    def resend_otp_code(self, request, *args, **kwargs):
        pass

