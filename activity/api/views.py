from rest_framework import generics, status, permissions
from rest_framework.response import Response
from ..models import Block, Pined, ReportedUser
from .serializers import ReportedUserSerializers
from profiles.models import Profile


class BlockRetravie(generics.RetrieveAPIView):
    queryset = Block.objects.all()
    serializer_class = ReportedUserSerializers
    lookup_field = "pk"
    lookup_url_kwarg = "pk"


class BlockCreateApivIew(generics.CreateAPIView):
    queryset = Block.objects.all()
    serializer_class = ReportedUserSerializers

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ReportListApiView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = ReportedUserSerializers

    def get(self, request, *args, **kwargs):
        reported_list = ReportedUser.objects.all(from_user=request.user)
        reported_profile = Profile.objects.filter(user__in=reported_list.va)


class ReportCreateApiView(generics.GenericAPIView):
    serializer_class = ReportedUserSerializers

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(form_user=request.user)
            context = {"is_done": True, "message": "", "data": serializer.data}
            return Response(data=context, status=status.HTTP_201_CREATED)
        context = {"is_done": False, "message": "", "data": serializer.errors}
        return Response(data=context, status=status.HTTP_406_NOT_ACCEPTABLE)
