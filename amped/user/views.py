from django.shortcuts import render

# Create your views here.
from rest_framework import mixins, views, status
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from user.models import User
from user.serializers import UserSerializer, ProfileImageSerializer


class UserViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get_permissions(self):
        if self.action == 'create':
            return ()
        return (IsAuthenticated(), )

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_201_CREATED, data=serializer.data)

    @action(detail=False, methods=['GET'], url_name='user-retrieve', url_path='')
    def get(self, request, *args, **kwargs):
        user = request.user
        serializer = self.get_serializer(user, context={'request': request})
        return Response(data=serializer.data)

    @action(detail=False, methods=['PUT'], url_name='user-update', url_path='')
    def put(self, request, *args, **kwargs):
        user = request.user
        serializer = self.get_serializer(user, data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data)

    @action(detail=False, methods=['PATCH'], url_name='user-path', url_path='')
    def patch(self, request, *args, **kwargs):
        user = request.user
        serializer = self.get_serializer(user, data=request.data, context={'request': request}, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data)

    @action(detail=False, methods=['PUT'], url_name='user-profile-image', url_path='upload-profile-image')
    def upload_profile_image(self, request):
        user = request.user
        serializer = ProfileImageSerializer(user, data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        return Response(data=serializer.data)
