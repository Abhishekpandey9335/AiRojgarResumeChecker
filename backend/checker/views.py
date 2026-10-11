from django.conf import settings
from django.db.models import Count
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, throttle_classes
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle

from .models import Branch, JobRole, ResumeAnalysis
from .serializers import BranchSerializer, RoleDetailSerializer, RoleListSerializer
from .services.extractor import ALLOWED_EXTENSIONS, ResumeReadError, extract_text
from .services.scorer import analyze


@api_view(["GET", "HEAD"])
def health(request):
    return Response({"status": "ok"})


@api_view(["GET"])
def branch_list(request):
    qs = Branch.objects.annotate(role_count=Count("roles")).order_by("sort_order", "name")
    return Response(BranchSerializer(qs, many=True).data)


@api_view(["GET"])
def role_list(request):
    qs = JobRole.objects.prefetch_related("skills")
    branch = request.query_params.get("branch")
    if branch:
        qs = qs.filter(branches__code=branch)
    return Response(RoleListSerializer(qs.distinct(), many=True).data)


@api_view(["GET"])
def role_detail(request, pk):
    role = get_object_or_404(JobRole.objects.prefetch_related("skills"), pk=pk)
    return Response(RoleDetailSerializer(role).data)


class AnalyzeThrottle(AnonRateThrottle):
    rate = "30/hour"


@api_view(["POST"])
@throttle_classes([AnalyzeThrottle])
def analyze_resume(request):
    upload = request.FILES.get("resume")
    role_id = request.data.get("role_id")
    branch_code = request.data.get("branch")

    if not upload:
        return Response({"detail": "Please upload your resume file."}, status=400)
    if not role_id:
        return Response({"detail": "Please select a job role."}, status=400)

    name = upload.name or "resume"
    if not name.lower().endswith(ALLOWED_EXTENSIONS):
        return Response({"detail": "Unsupported file type. Please upload a PDF, DOCX or TXT resume."}, status=400)
    if upload.size > settings.MAX_UPLOAD_MB * 1024 * 1024:
        return Response({"detail": f"File is too large. Maximum size is {settings.MAX_UPLOAD_MB} MB."}, status=400)

    try:
        role = JobRole.objects.prefetch_related("skills").get(pk=int(role_id))
    except (ValueError, TypeError, JobRole.DoesNotExist):
        return Response({"detail": "Selected job role was not found."}, status=404)
    branch = Branch.objects.filter(code=branch_code).first() if branch_code else None

    try:
        text, pages = extract_text(name, upload.read())
    except ResumeReadError as exc:
        return Response({"detail": str(exc)}, status=422)

    role_skills = [{"label": s.label, "keywords": s.keywords} for s in role.skills.all()]
    result = analyze(role.name, role_skills, text, pages)
    result["branch"] = branch.name if branch else None
    result["filename"] = name

    # Only the scores are saved. The resume text and file are never stored.
    saved = ResumeAnalysis.objects.create(
        role=role, branch=branch, filename=name[:255], score=result["score"], result=result
    )
    result["id"] = saved.id
    return Response(result)


@api_view(["GET"])
def analysis_detail(request, pk):
    obj = get_object_or_404(ResumeAnalysis, pk=pk)
    data = dict(obj.result)
    data["id"] = obj.id
    return Response(data)
