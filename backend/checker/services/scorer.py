"""Scores a resume out of 100 for one job role.

Score breakdown
---------------
  Skill match for the role ........ 60 points  (the role's required skills, line by line)
  Resume sections ................. 15 points  (summary, education, skills, projects, ...)
  Content quality ................. 15 points  (length, action verbs, numbers/impact)
  Contact & profile links ......... 10 points  (email, phone, LinkedIn, GitHub/portfolio)
"""
import math
import re

from .skills import match_keywords

SKILL_WEIGHT = 60
SECTION_WEIGHT = 15
CONTENT_WEIGHT = 15
CONTACT_WEIGHT = 10

SECTIONS = {
    "summary": {
        "label": "Professional summary / objective",
        "pattern": r"\b(summary|objective|profile|about me|career objective)\b",
        "weight": 2,
        "tip": "Add a 2-3 line professional summary at the top that names the role you are applying for.",
    },
    "education": {
        "label": "Education",
        "pattern": r"\b(education|academic|qualification|b\.?tech|m\.?tech|b\.?sc|m\.?sc|mba|bca|mca|university|college)\b",
        "weight": 3,
        "tip": "Add an Education section with degree, college, year and CGPA/percentage.",
    },
    "skills": {
        "label": "Skills",
        "pattern": r"\b(skills|technical skills|key skills|core competencies|tools|technologies)\b",
        "weight": 3,
        "tip": "Add a clear Skills section so recruiters and ATS software can find your skills quickly.",
    },
    "projects": {
        "label": "Projects",
        "pattern": r"\b(projects?|academic projects?|personal projects?|dissertation|thesis|research work)\b",
        "weight": 3,
        "tip": "Add a Projects section (or thesis / research work) with what you built and the tools you used.",
    },
    "experience": {
        "label": "Experience / internships",
        "pattern": r"\b(experience|internships?|work history|employment|training|apprenticeship)\b",
        "weight": 2,
        "tip": "Add internships, training or work experience, even short or unpaid ones.",
    },
    "certifications": {
        "label": "Certifications / achievements",
        "pattern": r"\b(certifications?|certificates?|achievements?|awards?|courses?|publications?|honou?rs)\b",
        "weight": 2,
        "tip": "Add relevant certifications, courses, publications or achievements.",
    },
}

ACTION_VERBS = [
    "developed", "built", "designed", "implemented", "created", "led", "managed", "analyzed",
    "analysed", "optimized", "optimised", "improved", "automated", "deployed", "launched",
    "engineered", "delivered", "achieved", "increased", "reduced", "conducted", "coordinated",
    "executed", "performed", "established", "trained", "researched", "evaluated", "streamlined",
    "collaborated", "published", "validated", "monitored", "prepared", "organized", "organised",
    "negotiated", "generated", "maintained", "migrated", "integrated", "tested", "documented",
]

WEAK_PHRASES = ["responsible for", "worked on", "helped with", "duties included", "hard working", "hardworking"]

EMAIL_RE = re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+")
PHONE_CANDIDATE_RE = re.compile(r"\+?\d[\d\s\-().]{8,16}\d")
LINKEDIN_RE = re.compile(r"linkedin\.com/|\blinkedin\b", re.I)
GITHUB_RE = re.compile(r"github\.com/|gitlab\.com/|\bgithub\b|portfolio|behance\.net|kaggle\.com|researchgate|orcid|scholar\.google", re.I)
NUMBER_IMPACT_RE = re.compile(r"\d+(?:\.\d+)?\s?(?:%|x\b|\+|k\b|lakh|crore|million|users|clients|hours|days|projects|samples|models|patients|sites|members|candidates)", re.I)


def _rating(score):
    if score >= 80:
        return "Excellent"
    if score >= 65:
        return "Good"
    if score >= 45:
        return "Average"
    return "Needs work"


def _verdict(score):
    if score >= 70:
        return {"shortlisted": True, "text": "Likely to be shortlisted for this role"}
    if score >= 50:
        return {"shortlisted": False, "text": "Close, but a few improvements are needed to get shortlisted"}
    return {"shortlisted": False, "text": "Not shortlist-ready yet. Follow the suggestions below"}


def score_skills(role_skills, resume_text):
    """role_skills: list of dicts {label, keywords}. Returns (points, details)."""
    details = []
    total_line_score = 0.0
    counted = 0
    for item in role_skills:
        keywords = item["keywords"]
        if not keywords:
            continue
        matched, missing = match_keywords(keywords, resume_text)
        # A resume rarely lists every tool in a line. Matching half of the keywords
        # in a line already earns full marks for that line.
        needed = max(1, math.ceil(len(keywords) * 0.5))
        line_score = min(1.0, len(matched) / needed)
        total_line_score += line_score
        counted += 1
        details.append(
            {
                "label": item["label"],
                "matched": matched,
                "missing": missing,
                "score": round(line_score * 100),
            }
        )
    points = (total_line_score / counted) * SKILL_WEIGHT if counted else 0
    return points, details


def score_sections(text):
    lowered = text.lower()
    found, earned, possible = {}, 0, 0
    for key, cfg in SECTIONS.items():
        present = bool(re.search(cfg["pattern"], lowered))
        found[key] = present
        possible += cfg["weight"]
        if present:
            earned += cfg["weight"]
    points = earned / possible * SECTION_WEIGHT
    return points, found


def score_content(text, pages):
    lowered = text.lower()
    words = re.findall(r"[A-Za-z0-9+#.]+", text)
    word_count = len(words)
    notes = []

    # Length (6 pts): 250-900 words is a healthy resume.
    if 250 <= word_count <= 900:
        length_pts = 6
    elif 150 <= word_count < 250 or 900 < word_count <= 1200:
        length_pts = 3.5
        notes.append("short" if word_count < 250 else "long")
    else:
        length_pts = 1.5
        notes.append("too_short" if word_count < 150 else "too_long")

    # Action verbs (5 pts)
    verbs_used = sorted({v for v in ACTION_VERBS if re.search(rf"\b{v}\b", lowered)})
    verb_pts = min(5, len(verbs_used) / 6 * 5)

    # Numbers / measurable impact (4 pts)
    impact_hits = len(NUMBER_IMPACT_RE.findall(text))
    impact_pts = min(4, impact_hits / 3 * 4)

    weak = [p for p in WEAK_PHRASES if p in lowered]
    penalty = min(2, len(weak) * 0.7)

    points = max(0, min(CONTENT_WEIGHT, length_pts + verb_pts + impact_pts - penalty))
    return points, {
        "word_count": word_count,
        "pages": pages,
        "action_verbs": verbs_used,
        "impact_numbers": impact_hits,
        "weak_phrases": weak,
        "length_note": notes[0] if notes else "ok",
    }


def score_contact(text):
    has_email = bool(EMAIL_RE.search(text))
    has_phone = any(
        10 <= len(re.sub(r"\D", "", m.group())) <= 13 for m in PHONE_CANDIDATE_RE.finditer(text)
    )
    has_linkedin = bool(LINKEDIN_RE.search(text))
    has_profile = bool(GITHUB_RE.search(text))
    points = has_email * 3 + has_phone * 2.5 + has_linkedin * 2.5 + has_profile * 2
    return points, {
        "email": has_email,
        "phone": has_phone,
        "linkedin": has_linkedin,
        "portfolio": has_profile,
    }


def build_suggestions(role_name, skill_details, sections, content, contact, skill_pct):
    tips = []

    # ---- skills: biggest impact first
    gaps = sorted((d for d in skill_details if d["score"] < 100), key=lambda d: (d["score"], -len(d["missing"])))
    for d in gaps[:6]:
        if not d["missing"]:
            continue
        shown = ", ".join(d["missing"][:5])
        priority = "high" if d["score"] < 40 else "medium"
        if d["matched"]:
            msg = f"Strengthen \"{d['label']}\": you already show {', '.join(d['matched'][:3])}. Also add {shown} if you have worked with them."
        else:
            msg = f"Add \"{d['label']}\" skills to your resume. Learn and mention: {shown}."
        tips.append({"priority": priority, "category": "Skills", "text": msg})

    if skill_pct < 40:
        tips.insert(0, {
            "priority": "high",
            "category": "Skills",
            "text": f"Your resume matches only {round(skill_pct)}% of the skills required for {role_name}. Build 2-3 projects using the missing skills and list them under Projects.",
        })

    # ---- sections
    for key, present in sections.items():
        if not present:
            tips.append({"priority": "medium", "category": "Structure", "text": SECTIONS[key]["tip"]})

    # ---- content
    note = content["length_note"]
    if note in ("too_short", "short"):
        tips.append({"priority": "medium", "category": "Content", "text": f"Your resume has only {content['word_count']} words. Add more detail about projects, internships and results (aim for 300-800 words)."})
    elif note in ("too_long", "long"):
        tips.append({"priority": "medium", "category": "Content", "text": f"Your resume has {content['word_count']} words. Trim it to 1-2 pages and keep only relevant points."})
    if len(content["action_verbs"]) < 5:
        tips.append({"priority": "medium", "category": "Content", "text": "Start bullet points with strong action verbs such as Developed, Built, Analyzed, Led, Optimized."})
    if content["impact_numbers"] < 2:
        tips.append({"priority": "medium", "category": "Content", "text": "Add measurable results, for example \"improved accuracy by 12%\" or \"handled 40+ samples per week\"."})
    if content["weak_phrases"]:
        tips.append({"priority": "low", "category": "Content", "text": f"Replace weak phrases ({', '.join(content['weak_phrases'])}) with specific achievements."})

    # ---- contact
    if not contact["email"]:
        tips.append({"priority": "high", "category": "Contact", "text": "Add a professional email address at the top of your resume."})
    if not contact["phone"]:
        tips.append({"priority": "high", "category": "Contact", "text": "Add your phone number so recruiters can reach you."})
    if not contact["linkedin"]:
        tips.append({"priority": "low", "category": "Contact", "text": "Add your LinkedIn profile link."})
    if not contact["portfolio"]:
        tips.append({"priority": "low", "category": "Contact", "text": "Add a GitHub, portfolio, Kaggle or ORCID link that shows your work."})

    order = {"high": 0, "medium": 1, "low": 2}
    tips.sort(key=lambda t: order[t["priority"]])
    return tips[:14]


def analyze(role_name, role_skills, text, pages=None):
    skill_pts, skill_details = score_skills(role_skills, text)
    section_pts, sections = score_sections(text)
    content_pts, content = score_content(text, pages)
    contact_pts, contact = score_contact(text)

    total = round(skill_pts + section_pts + content_pts + contact_pts)
    total = max(0, min(100, total))
    skill_pct = skill_pts / SKILL_WEIGHT * 100

    matched_all = sorted({k for d in skill_details for k in d["matched"]}, key=str.lower)
    missing_all = []
    for d in sorted(skill_details, key=lambda d: d["score"]):
        for k in d["missing"]:
            if k not in missing_all:
                missing_all.append(k)

    return {
        "score": total,
        "rating": _rating(total),
        "verdict": _verdict(total),
        "role": role_name,
        "breakdown": [
            {"key": "skills", "label": "Role skill match", "score": round(skill_pts, 1), "max": SKILL_WEIGHT},
            {"key": "sections", "label": "Resume sections", "score": round(section_pts, 1), "max": SECTION_WEIGHT},
            {"key": "content", "label": "Content quality", "score": round(content_pts, 1), "max": CONTENT_WEIGHT},
            {"key": "contact", "label": "Contact & links", "score": round(contact_pts, 1), "max": CONTACT_WEIGHT},
        ],
        "skill_match_percent": round(skill_pct),
        "skill_details": skill_details,
        "matched_skills": matched_all,
        "missing_skills": missing_all[:40],
        "sections": [
            {"key": k, "label": SECTIONS[k]["label"], "present": v} for k, v in sections.items()
        ],
        "content": content,
        "contact": contact,
        "suggestions": build_suggestions(role_name, skill_details, sections, content, contact, skill_pct),
    }
