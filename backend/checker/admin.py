from django.contrib import admin

from .models import Branch, JobRole, ResumeAnalysis, RoleSkill


class RoleSkillInline(admin.TabularInline):
    model = RoleSkill
    extra = 0


@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ("name", "code", "sort_order")


@admin.register(JobRole)
class JobRoleAdmin(admin.ModelAdmin):
    list_display = ("name", "group")
    list_filter = ("group", "branches")
    search_fields = ("name",)
    inlines = [RoleSkillInline]


@admin.register(ResumeAnalysis)
class ResumeAnalysisAdmin(admin.ModelAdmin):
    list_display = ("role", "branch", "score", "filename", "created_at")
    list_filter = ("branch", "role")
