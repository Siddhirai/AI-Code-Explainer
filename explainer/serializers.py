# serializers.py
from rest_framework import serializers
from .models import CodeSample, ExplanationLog

class ExplainRequestSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=5000)
    language = serializers.CharField(max_length=30, default="python")

class CodeSampleSerializer(serializers.ModelSerializer):
    class Meta:
        model = CodeSample
        fields = "__all__"

class ExplanationLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExplanationLog
        fields = "__all__"