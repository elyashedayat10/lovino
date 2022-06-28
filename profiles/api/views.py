from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response

from ..models import Image
from .permissions import OwnerPermissions
from .serializers import ImageSerializer, ProfileSerializer

class ProfileListApiView(generics.GenericAPIView):
    serializer_class =
    def get(self,request,*args,**kwargs):



class ProfileApiView(generics.GenericAPIView):
    serializer_class = ProfileSerializer

    def get(self, request, *args, **kwargs):
        serializer = self.serializer_class(instance=request.user.profile)
        context = {
            'is_done': True,
            'message': 'اطاعات کاربر برای شما ارسال شد',
            'data': serializer.data
        }
        return Response(data=context, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        serializer = self.serializer_class(instance=request.user.profile, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user)
            context = {
                'is_done': True,
                'message': 'اطاعات کاربر با موفقیت به روزرسانی شد',
                'data': serializer.data
            }
            return Response(data=context, status=status.HTTP_200_OK)
        context = {
            'is_done': False,
            'message': 'خطا در به روزرسانی کاربر',
            'data': serializer.errors
        }
        return Response(data=context, status=status.HTTP_400_BAD_REQUEST)


class UserImageUploadApiView(generics.GenericAPIView):
    serializer_class = ImageSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            image = serializer.validated_data['image']
            Image.objects.create(image=image, user=request.user)
            context = {
                'is_done': True,
                'message': 'عکس با موفقیت اپلود شد',
                'data': serializer.data
            }
            return Response(data=context, status=status.HTTP_200_OK)
        context = {
            'is_done': False,
            'message': 'خطلا در اپلود پروفایل',
            'data': serializer.data
        }
        return Response(data=context, status=status.HTTP_400_BAD_REQUEST)


class ImageDeleteApiView(generics.DestroyAPIView):
    queryset = Image.objects.all()
    permission_classes = [OwnerPermissions, ]

    # def delete(self, request, pk, format=None):
    #     snippet = self.get_object(pk)
    #     snippet.delete()
    #     context = {
    #                 'is_done': True,
    #                 'message': 'عگس پروفایل با موفقیت جذف شد',
    #             }
    #     return Response(data=context, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        image_id = kwargs.get('id')
        try:
            image_obj = get_object_or_404(Image, id=image_id)
            image_obj.delete()
            context = {
                'is_done': True,
                'message': 'عگس پروفایل با موفقیت جذف شد',
            }
            return Response(data=context, status=status.HTTP_200_OK)
        except  Exception as e:
            context = {
                'is_done': False,
                'message': 'خطا دز انجام عملیات',
            }
            return Response(data=context, status=status.HTTP_400_BAD_REQUEST)
