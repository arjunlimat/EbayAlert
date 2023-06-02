from rest_framework import serializers
from .models import Alert
from datetime import datetime

class AlertSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Alert
        fields = ['id', 'search_phrase', 'email', 'frequency', 'created_at']

    def create(self, validated_data):
        validated_data['created_at'] = datetime.now()
        return super().create(validated_data)
