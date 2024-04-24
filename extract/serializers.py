from rest_framework import serializers
from extract.models import ExtractedText

class ExtractedTextSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExtractedText
        fields = ['id', 'file_name', 'extracted_text', 'created_by']