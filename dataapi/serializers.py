from rest_framework import serializers

from .models import UploadedFile


class UploadedFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadedFile
        fields = ['id', 'file_name', 'uploaded_at', 'column_info', 'file']


class AllDataSerializer(serializers.Serializer):
    file_id = serializers.IntegerField()
    columns = serializers.ListField(child=serializers.CharField(), required=False)
