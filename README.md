# AiRojgar Resume Checker

A sub-website of **airojgar.in**. A student picks a branch and a job role (for example AI / ML Engineer),
uploads a resume (PDF, DOCX or TXT), and gets:

- a **score out of 100**
- skills found and **skills missing** for that role
- a skill-by-skill match, a resume checklist, and a prioritised list of **suggested changes**

**Tech stack:** React (Vite) + Django REST + PostgreSQL + Python text analysis (pypdf, python-docx).

Branches: B.Tech CSE / IT (incl. BCA, MCA, allied), MBA, Biotechnology, Biochemistry. 33 job roles are loaded
from `backend/data/Job_Roles_and_Skills_by_Department.xlsx`.

## Folder structure

```
airojgar-resume-checker/
  backend/                      Django project
    config/                     settings, urls
    checker/
      models.py                 Branch, JobRole, RoleSkill, ResumeAnalysis
      views.py, urls.py         REST API
      services/
        extractor.py            reads PDF / DOCX / TXT
        skills.py               parses the Excel job description + skill matching (aliases)
        scorer.py               the 100-point scoring and suggestions
      management/commands/import_roles.py   loads the Excel file into PostgreSQL
    data/Job_Roles_and_Skills_by_Department.xlsx
    requirements.txt, .env.example
  frontend/                     React app (Vite)
    src/pages/  Home, Checker, Result
    src/components/, src/styles/global.css
```

## Setup (open the `airojgar-resume-checker` folder in VS Code)

You need: Python 3.10+, Node.js 18+, PostgreSQL 14+.

### 1. Database
Create an empty database (pgAdmin or psql):
```sql
CREATE DATABASE airojgar_resume_checker;
```

### 2. Backend (Terminal 1)
```bash
cd backend
python -m venv venv
venv\Scripts\activate            # Windows   (Mac/Linux: source venv/bin/activate)
pip install -r requirements.txt
copy .env.example .env           # Mac/Linux: cp .env.example .env  -> put your PostgreSQL password in .env
python manage.py migrate
python manage.py import_roles    # loads branches, roles and skills from the Excel file
python manage.py runserver       # http://127.0.0.1:8000
```
Optional admin panel: `python manage.py createsuperuser`, then open http://127.0.0.1:8000/admin

### 3. Frontend (Terminal 2)
```bash
cd frontend
npm install
npm run dev                      # http://localhost:5173
```
Open http://localhost:5173. In development Vite forwards `/api` calls to Django automatically.

## How the score is calculated (out of 100)

| Part | Points | What is checked |
|---|---|---|
| Role skill match | 60 | Every requirement line of the role is checked. Matching about half the keywords of a line gives full marks for that line. Aliases are understood (Postgres = PostgreSQL, sklearn = Scikit-learn, K8s = Kubernetes, ML = Machine Learning). |
| Resume sections | 15 | Summary, Education, Skills, Projects, Experience, Certifications |
| Content quality | 15 | Length (250-900 words), action verbs, measurable results, weak phrases |
| Contact and links | 10 | Email, phone, LinkedIn, GitHub / portfolio |

70+ is shown as "likely to be shortlisted", 50-69 as "close", below 50 as "needs work".

## Changing roles or skills
- Edit the Excel file (keep the columns: Group, Job Role, Required Skills; one skill line per row in the form
  `- Heading: skill, skill, skill`) and run `python manage.py import_roles` again. Re-running updates, it does not duplicate.
- Add spelling variants in `backend/checker/services/skills.py` (`ALIASES`).
- Change score weights at the top of `backend/checker/services/scorer.py`.
- Group 1 roles go to CSE/IT, Group 2 to MBA, Group 3 to both Biotechnology and Biochemistry
  (`GROUP_TO_BRANCHES` in `import_roles.py`).

## API
| Method | URL | Purpose |
|---|---|---|
| GET | `/api/branches/` | branches with role counts |
| GET | `/api/roles/?branch=cse-it` | roles of a branch |
| GET | `/api/roles/<id>/` | role with its required skills |
| POST | `/api/analyze/` | form-data: `resume` (file), `role_id`, `branch` |
| GET | `/api/analyses/<id>/` | a saved result |

## Linking from your main AiRojgar website
Link to the deployed frontend URL, for example `<a href="https://resume.airojgar.in">Resume Checker</a>`.
Deep links work too: `https://resume.airojgar.in/check?branch=mba`.
Set `VITE_MAIN_SITE_URL` in `frontend/.env` so the logo and "Back to AiRojgar" buttons go to your main site.
Replace the SVG in `frontend/src/components/Logo.jsx` with your real logo image if you want.

## Deployment notes
- Backend: set `DJANGO_DEBUG=False`, a long random `DJANGO_SECRET_KEY`, your real `DJANGO_ALLOWED_HOSTS`
  and `CORS_ALLOWED_ORIGINS` (the frontend URL), then run with gunicorn (`pip install gunicorn && gunicorn config.wsgi`).
- Frontend: set `VITE_API_URL` to the backend URL, run `npm run build`, and host the `dist` folder.
- Privacy: only the scores and suggestions are saved. The resume file and its text are never stored.
- Scanned (image-only) PDFs cannot be read. Users get a clear message asking for a text-based PDF or DOCX.
