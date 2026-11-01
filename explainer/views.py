# views.py
from django.shortcuts import render
from .models import ExplanationLog, CodeSample
from .services import explain_code

def index(request):
    ctx = {"samples": CodeSample.objects.all()[:10]}
    if request.method == "POST":
        code = request.POST.get("code", "").strip()
        lang = request.POST.get("language", "python")
        if code:
            try:
                ctx["explanation"] = explain_code(code, lang)
                ExplanationLog.objects.create(language=lang, code=code, explanation=ctx["explanation"])
            except Exception as e:
                ctx["error"] = str(e)
        ctx["code"], ctx["language"] = code, lang
    return render(request, "explainer/index.html", ctx)