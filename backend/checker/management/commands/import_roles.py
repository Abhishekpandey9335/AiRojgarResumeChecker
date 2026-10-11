"""Load branches, job roles and required skills from the Excel sheet.

Usage:  python manage.py import_roles
        python manage.py import_roles --file path/to/file.xlsx
Safe to run again: roles are updated, not duplicated.
"""
import openpyxl
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils.text import slugify

from checker.models import Branch, JobRole, RoleSkill
from checker.services.skills import parse_line, split_description

BRANCHES = [
    dict(code="cse-it", name="B.Tech CSE / IT", tagline="Computer Science & Information Technology",
         description="CSE, IT, BCA, MCA and allied branches (AI/ML, Data Science, Cybersecurity)", icon="code", sort_order=1),
    dict(code="mba", name="MBA", tagline="Business / HRD / Marketing / Finance",
         description="All MBA specialisations: HR, Finance, Marketing, Operations, IT", icon="briefcase", sort_order=2),
    dict(code="biotechnology", name="Biotechnology", tagline="Biotech, Pharma & Life Sciences",
         description="Research, bioinformatics, clinical research, regulatory and quality roles", icon="dna", sort_order=3),
    dict(code="biochemistry", name="Biochemistry", tagline="Biochemistry & Lab Sciences",
         description="Lab, quality, clinical, enzymology and food science roles", icon="flask", sort_order=4),
]

# Excel "Group" column -> branch codes that get those roles
GROUP_TO_BRANCHES = {
    "Group 1": ["cse-it"],
    "Group 2": ["mba"],
    "Group 3": ["biotechnology", "biochemistry"],
}


class Command(BaseCommand):
    help = "Import job roles and skills from the Excel file"

    def add_arguments(self, parser):
        parser.add_argument("--file", default=str(settings.EXCEL_DATA_FILE))

    @transaction.atomic
    def handle(self, *args, **options):
        path = options["file"]
        try:
            wb = openpyxl.load_workbook(path, data_only=True)
        except Exception as exc:
            raise CommandError(f"Cannot open {path}: {exc}")
        ws = wb.active

        branches = {}
        for cfg in BRANCHES:
            obj, _ = Branch.objects.update_or_create(code=cfg["code"], defaults={k: v for k, v in cfg.items() if k != "code"})
            branches[obj.code] = obj

        created = updated = 0
        for row in ws.iter_rows(min_row=2, values_only=True):
            group, name, description = (row + (None, None, None))[:3]
            if not group or not name or not description:
                continue  # header or group banner rows
            group = str(group).strip()
            if group not in GROUP_TO_BRANCHES:
                continue
            name = str(name).strip()
            slug = slugify(name)[:170]
            role, was_created = JobRole.objects.update_or_create(
                slug=slug, defaults={"name": name, "group": group, "description": str(description)}
            )
            role.branches.set([branches[c] for c in GROUP_TO_BRANCHES[group]])
            role.skills.all().delete()
            for order, line in enumerate(split_description(str(description))):
                parsed = parse_line(line)
                if not parsed or not parsed[1]:
                    continue
                label, keywords = parsed
                RoleSkill.objects.create(role=role, order=order, label=label[:200], raw_text=line, keywords=keywords)
            created += was_created
            updated += not was_created

        self.stdout.write(self.style.SUCCESS(
            f"Imported {created} new and updated {updated} roles for {len(branches)} branches."
        ))
