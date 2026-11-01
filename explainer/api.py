# api.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from .models import CodeSample, ExplanationLog
from .serializers import *
from .services import explain_code

class ExplainAPI(APIView):
    def post(self, request):
        s = ExplainRequestSerializer(data=request.data)
        s.is_valid(raise_exception=True)
        code, lang = s.validated_data["code"], s.validated_data["language"]
        try:
            text = explain_code(code, lang)
        except Exception as e:
            return Response({"error": str(e)}, status=502)
        ExplanationLog.objects.create(language=lang, code=code, explanation=text)
        return Response({"language": lang, "explanation": text})

class SamplesAPI(ListAPIView):
    queryset = CodeSample.objects.all()
    serializer_class = CodeSampleSerializer

class HistoryAPI(ListAPIView):
    queryset = ExplanationLog.objects.all()[:50]
    serializer_class = ExplanationLogSerializer