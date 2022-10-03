from rest_framework import serializers
from .models import Document, Announcement

class AnnouncementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Announcement
        fields = '__all__'

class DocumentSerializer(serializers.ModelSerializer):
    rel_post = AnnouncementSerializer(read_only=True)
    class Meta:
        model = Document
        fields = '__all__'
