import hashlib

from rest_framework import serializers
from file.models import FileStorage

from users.models import User


class FileSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        read_only=True,
        slug_field='id'
    )

    class Meta:
        model = FileStorage
        fields = ["id", 'created', 'updated', 'content', 'user']

    def create(self, request):
        data = request.data['content'].file.read()
        if len(data)>150000:
            raise serializers.ValidationError(detail="size error")
        file_hash = hashlib.md5(data).hexdigest()
        if FileStorage.objects.filter(hash_content=file_hash, user=request.user):
            raise serializers.ValidationError(detail="file already exists")
        file = FileStorage(
            user=request.user,
            content=request.data['content'],
            hash_content=file_hash
        )
        file.save()
        return file
