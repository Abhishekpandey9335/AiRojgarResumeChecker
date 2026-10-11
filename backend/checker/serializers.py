from rest_framework import serializers

from .models import Branch, JobRole, RoleSkill


class BranchSerializer(serializers.ModelSerializer):
    role_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Branch
        fields = ["code", "name", "tagline", "description", "icon", "role_count"]


class RoleListSerializer(serializers.ModelSerializer):
    skill_count = serializers.SerializerMethodField()

    class Meta:
        model = JobRole
        fields = ["id", "name", "slug", "group", "skill_count"]

    def get_skill_count(self, obj):
        return sum(len(s.keywords) for s in obj.skills.all())


class RoleSkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoleSkill
        fields = ["label", "keywords"]


class RoleDetailSerializer(serializers.ModelSerializer):
    skills = RoleSkillSerializer(many=True, read_only=True)

    class Meta:
        model = JobRole
        fields = ["id", "name", "slug", "group", "skills"]
