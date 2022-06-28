import random

from django.contrib.auth import get_user_model
from rest_framework import (authentication, generics, mixins, permissions,
                            status)
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from ..models import OtpCode
from ..utils import send_otp
from .serializers import AuthSerializer, VerifySerializer

user = get_user_model()


# class UserApiView(
#     mixins.CreateModelMixin,
#     mixins.ListModelMixin,
#     mixins.RetrieveModelMixin,
#     generics.GenericAPIView):
#     serializer_class =
#     queryset =
#     lookup_field =
#     permission_classes = [permissions.IsAuthenticated]
#     authentication_classes = [authentication.SessionAuthentication]
#
#     def get(self, request, *args, **kwargs):
#         pk = kwargs.get('pk')
#         if pk:
#             return self.retrieve(request, *args, **kwargs)
#         return self.list(request, *args, **kwargs)
#
#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)
#
#     def perform_create(self, serializer):
#         serializer.save()


class AuthApiView(generics.GenericAPIView):
    serializer_class = AuthSerializer
    permission_classes = [AllowAny, ]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            random_code = random.randint(000000, 999999)
            phone_number = serializer.validated_data['phone_number']
            send_otp(phone_number=phone_number, code=random_code)
            OtpCode.objects.create(phone_number=phone_number, code=random_code)
            context = {
                'is_done': True,
                'message': 'پیام ارسال شد',
                'data': serializer.data
            }
            return Response(data=context, status=status.HTTP_200_OK)
        context = {
            'is_done': False,
            'message': 'خطا در پارامتر ارسالی',
            'data': serializer.errors
        }
        return Response(data=context, status=status.HTTP_400_BAD_REQUEST)


class VerifyApiView(generics.GenericAPIView):
    serializer_class = VerifySerializer
    permission_classes = [AllowAny, ]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            phone_number = serializer.validated_data['phone_number']
            code = serializer.validated_data['code']
            otp_obj = OtpCode.objects.get(phone_number=phone_number, code=code)
            if otp_obj:
                user_obj = user.objects.filter(phone_number=phone_number)
                if user_obj:
                    token_obj = Token.objects.get_or_create(user_id=user_obj.id)
                    context = {
                        'is_done': True,
                        'message': 'کاربر با موفقیت وارد شد',
                        'token': token_obj.key
                    }
                    return Response(data=context, status=status.HTTP_200_OK)
                else:
                    user_obj = user.objects.create_user(phone_number=phone_number)
                    token_obj = Token.objects.create(user=user_obj)
                    context = {
                        'is_done': True,
                        'message': 'کاربر با موفیت ساخته شد',
                        'token': token_obj.key
                    }
                    return Response(data=context, status=status.HTTP_200_OK)
            else:
                context = {
                    'is_done': False,
                    'message': 'کد ارسال برای کاربر با کد ذزیافتی همخوانی ندارد',
                }
                return Response(data=context, status=status.HTTP_400_BAD_REQUEST)
        context = {
            'is_done': False,
            'message': 'خطا در پارامتر ارسالی',
        }
        return Response(data=context, status=status.HTTP_400_BAD_REQUEST)


class LogoutApiView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated, ]

    @staticmethod
    def delete(request, *args, **kwargs):
        request.user.auth_token.delete()
        context = {
            "is_done": False,
            "message": "token کاربر با موفقیت حذف شد",
        }
        return Response(data=context, status=status.HTTP_200_OK)
