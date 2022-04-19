from django.shortcuts import render
import hashlib

from rest_framework import status, viewsets, parsers
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from file.models import FileStorage
from file.serializers import FileSerializer

from file.permissions import IsAuthor


class FileViewset(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,IsAuthor)

    serializer_class = FileSerializer
    parser_classes = [parsers.MultiPartParser, parsers.FormParser]
    http_method_names = ['get', 'post', 'patch', 'delete']

    def perform_create(self, serializer):
        serializer.create(self.request)

    def get_queryset(self):
        queryset = FileStorage.objects.all().filter(user=self.request.user)
        return queryset


