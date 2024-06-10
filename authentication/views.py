from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from .models import User, OTPRegisterResend
from .serializers import (UserSerializer, RegisterUserSerializer, UpdateUserSerializer,
                          OTPRegisterResendSerializer, OTPResendSerializer,
                          OTPRegisterVerifySerializer, ResetUserPasswordSerializer, SetNewPasswordSerializer)
from drf_yasg.utils import swagger_auto_schema
from .utils import (check_code_expire, checking_number_of_otp,
                    send_otp_code_telegram, check_resend_otp_code)
from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken


class LoginView(ViewSet):
    @swagger_auto_schema(
        operation_description="Log in ",
        operation_summary="Login verified user",
        responses={200: 'access and refresh tokens'},
        request_body=RegisterUserSerializer(),
        tags=['auth']

    )
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

    @swagger_auto_schema(
        operation_description="User detail",
        operation_summary="Returns user detail by token",
        responses={200: UserSerializer()},
        tags=['auth']

    )
    def auth_me(self, request, *args, **kwargs):
        if not (request.user.is_authenticated and request.user.is_verified):
            return Response({"Error": "Please authenticate "}, status.HTTP_401_UNAUTHORIZED)
        token = request.META.get('HTTP_AUTHORIZATION', " ").split(' ')[1]
        token = AccessToken(token)
        user_id = token.payload.get('user_id')
        serializer = UserSerializer(User.objects.filter(id=user_id).first())
        return Response(serializer.data, status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Profile update",
        operation_summary="Register new users",
        responses={201: OTPRegisterResendSerializer()},
        request_body=UpdateUserSerializer(),
        tags=['auth']

    )
    def profile_update(self, request, *args, **kwargs):
        user = request.user
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')
        profile_picture = request.FILES.get('profile_picture')
        serializer = UserSerializer(user, data={"first_name": first_name,
                                                "last_name": last_name,
                                                "profile_picture": profile_picture}, partial=True)

        if not serializer.is_valid:
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(serializer.data, status.HTTP_201_CREATED)


class AuthenticateViewSet(ViewSet):
    @swagger_auto_schema(
        operation_description="Register",
        operation_summary="Register new users",
        responses={201: OTPRegisterResendSerializer()},
        request_body=RegisterUserSerializer(),
        tags=['auth']

    )
    def register(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        user = User.objects.filter(username=username).first()
        if user and user.is_verified:
            return Response(data={"error": "You already registered"}, status=status.HTTP_400_BAD_REQUEST)
        if user:
            serializer = UserSerializer(user, data={'password': make_password(password)}, partial=True)
        else:
            serializer = UserSerializer(data={"username": username, "password": make_password(password)})
        if not serializer.is_valid():
            return Response({"error": serializer.errors}, status.HTTP_400_BAD_REQUEST)
        serializer.save()
        objs = OTPRegisterResend.objects.filter(otp_user=serializer.instance, otp_type=1).order_by('-created_at')

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

    @swagger_auto_schema(
        operation_description="Register",
        operation_summary="Verify registered user",
        responses={200: "success"},
        request_body=OTPRegisterVerifySerializer(),
        tags=['auth']

    )
    def verify_register(self, request, *args, **kwargs):
        otp_key = request.data.get('otp_key')
        otp_code = request.data.get('otp_code')
        if not request.user.is_authenticated:
            return Response({"detail": "You should register first"}, status.HTTP_401_UNAUTHORIZED)
        if request.user.is_verified:
            return Response({"detail": "U already verified"}, status.HTTP_400_BAD_REQUEST)
        if not otp_code:
            return Response({"error": "Send otp code"}, status.HTTP_400_BAD_REQUEST)
        otp_code = int(otp_code)
        otp_obj = OTPRegisterResend.objects.filter(otp_key=otp_key).first()
        if otp_obj is None:
            return Response({"error": "Make sure otp key is right"}, status.HTTP_400_BAD_REQUEST)
        if otp_obj.attempts > 2:
            return Response({"error": "Come back 12 hours later"}, status.HTTP_400_BAD_REQUEST)
        if otp_obj.otp_code != otp_code:
            otp_obj.attempts += 1
            otp_obj.save()
            return Response(data={"error": "otp code is wrong"}, status=status.HTTP_400_BAD_REQUEST)

        if not check_code_expire(otp_obj.created_at):
            return Response(data={"error": "Code is expired"}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.filter(id=otp_obj.otp_user.id).first()
        if not user:
            return Response(data={"error": "User does not exist"}, status=status.HTTP_404_NOT_FOUND)

        user.is_verified = True
        user.save(update_fields=['is_verified'])
        OTPRegisterResend.objects.filter(otp_user=user).delete()
        return Response(data={"detail": "Success"}, status=status.HTTP_200_OK)


class ResendAndResetViewSet(ViewSet):

    def reset_password(self, request, *args, **kwargs):
        data = request.data
        user = User.objects.filter(username=data.get('username')).first()
        if user:
            send_code = OTPRegisterResend.objects.create(otp_user=user, otp_type=3)
            send_code.save()
            send_otp_code_telegram(send_code)
            return Response({'code has been sent'})
        # if not user.is_authenticated:
        #     return Response({'/log in please'}, status=status.HTTP_403_FORBIDDEN)

        return Response({'/User not found'}, status=status.HTTP_403_FORBIDDEN)

    def verify_reset_password(self, request, *args, **kwargs):
        otp_code = request.data.get('otp_code')
        new_password = request.data.get('password')
        otp_key = request.data.get('key')

        objects = OTPRegisterResend.objects.filter(otp_key=otp_key, otp_code=otp_code, otp_type=3).first()

        if objects and check_code_expire(objects.created_at):
            changepassword = User.objects.filter(id=objects.otp_user_id).first()
            changepassword.password = make_password(new_password)
            changepassword.save(update_fields=['password'])

            delete_otp_code = OTPRegisterResend.objects.filter(otp_key=otp_key).first()
            delete_otp_code.delete()

            return Response(data={'changed'}, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_403_FORBIDDEN, data={"Invalid data or code expired"})

    @swagger_auto_schema(
            operation_description="Resend",
            operation_summary="Verify registered user",
            responses={200: OTPRegisterResendSerializer()},
            request_body=OTPResendSerializer(),
            tags=['auth']

        )

    def resend_otp_code(self, request, *args, **kwargs):
        otp_key = request.data.get('otp_key')
        otp_obj = OTPRegisterResend.objects.filter(otp_key=otp_key).first()
        if not otp_obj:
            return Response(data={"error": "Otp key is wrong"}, status=status.HTTP_400_BAD_REQUEST)

        objs = OTPRegisterResend.objects.filter(otp_user=otp_obj.otp_user, otp_type=2).order_by('-created_at')
        if not checking_number_of_otp(objs):
            return Response(data={"error": "Try again 12 hours later"}, status=status.HTTP_400_BAD_REQUEST)

        if checking_number_of_otp(objs) == 'delete':
            OTPRegisterResend.objects.filter(otp_user=otp_obj.otp_user, otp_type=2).delete()

        if not check_resend_otp_code(otp_obj.created_at):
            return Response(data={"error": "Try again a minute later"}, status=status.HTTP_400_BAD_REQUEST)

        new_otp = OTPRegisterResend.objects.create(otp_user=otp_obj.otp_user, otp_type=2)
        new_otp.save()
        response = send_otp_code_telegram(new_otp)
        if response.status_code != 200:
            new_otp.delete()
            return Response({"error": "Could not send otp to telegram"}, status.HTTP_400_BAD_REQUEST)
        otp_obj.delete()
        return Response(data={"otp_key": new_otp.otp_key}, status=status.HTTP_200_OK)
