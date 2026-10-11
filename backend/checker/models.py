from django.db import models


class Branch(models.Model):
    code = models.SlugField(unique=True)
    name = models.CharField(max_length=100)
    tagline = models.CharField(max_length=200, blank=True)
    description = models.CharField(max_length=300, blank=True)
    icon = models.CharField(max_length=30, blank=True)
    sort_order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["sort_order", "name"]

    def __str__(self):
        return self.name


class JobRole(models.Model):
    name = models.CharField(max_length=150)
    slug = models.SlugField(max_length=170, unique=True)
    group = models.CharField(max_length=20)
    branches = models.ManyToManyField(Branch, related_name="roles")
    description = models.TextField(blank=True, help_text="Raw job description from the Excel sheet")

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class RoleSkill(models.Model):
    """One requirement line of a role, e.g. 'Databases: MySQL, PostgreSQL'."""

    role = models.ForeignKey(JobRole, on_delete=models.CASCADE, related_name="skills")
    order = models.PositiveSmallIntegerField(default=0)
    label = models.CharField(max_length=200)
    raw_text = models.TextField()
    keywords = models.JSONField(default=list)

    class Meta:
        ordering = ["role_id", "order"]

    def __str__(self):
        return f"{self.role.name}: {self.label}"


class ResumeAnalysis(models.Model):
    """Result of one check. The resume file/text itself is NOT stored."""

    role = models.ForeignKey(JobRole, on_delete=models.CASCADE, related_name="analyses")
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True, related_name="analyses")
    filename = models.CharField(max_length=255)
    score = models.PositiveSmallIntegerField()
    result = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.role.name} - {self.score}/100"
