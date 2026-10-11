"""Turn a job-description line into a label + list of skill keywords, and
match those keywords against resume text."""
import re
from functools import lru_cache

# Different ways people write the same skill. Key = canonical keyword (lower
# case) found in the JD, value = extra spellings that also count as a match.
ALIASES = {
    "node.js": ["nodejs", "node js", "node"],
    "react.js": ["reactjs", "react js", "react"],
    "next.js": ["nextjs", "next js"],
    "vue.js": ["vuejs", "vue"],
    "express": ["expressjs", "express.js"],
    "postgresql": ["postgres", "psql", "postgre sql"],
    "mongodb": ["mongo db", "mongo"],
    "mysql": ["my sql"],
    "scikit-learn": ["sklearn", "scikit learn"],
    "tensorflow": ["tensor flow", "keras"],
    "pytorch": ["torch"],
    "javascript es6+": ["javascript", "es6", "js"],
    "javascript": ["js", "es6"],
    "typescript": ["ts"],
    "html5": ["html"],
    "css3": ["css"],
    "ci/cd": ["cicd", "ci cd", "continuous integration", "continuous delivery", "continuous deployment"],
    "github actions": ["gh actions"],
    "github/gitlab": ["github", "gitlab"],
    "git": ["github", "gitlab", "version control"],
    "version control": ["git", "github", "gitlab"],
    "kubernetes": ["k8s"],
    "amazon web services": ["aws"],
    "aws": ["amazon web services"],
    "gcp": ["google cloud", "google cloud platform"],
    "azure": ["microsoft azure"],
    "machine learning": ["ml"],
    "deep learning": ["dl"],
    "natural language processing": ["nlp"],
    "large language models": ["llm", "llms"],
    "large language models (llms)": ["llm", "llms"],
    "llms": ["llm", "large language model"],
    "rest api": ["rest apis", "restful", "rest api design", "restful api", "restful apis"],
    "rest api design": ["rest api", "rest apis", "restful"],
    "graphql": ["graph ql"],
    "oauth 2.0": ["oauth", "oauth2"],
    "jwt": ["json web token"],
    "huggingface transformers": ["hugging face", "huggingface", "transformers"],
    "langchain": ["lang chain"],
    "llamaindex": ["llama index"],
    "chromadb": ["chroma"],
    "pinecone": ["pine cone"],
    "ms excel": ["excel", "microsoft excel"],
    "power bi": ["powerbi", "power-bi"],
    "ui/ux": ["ui ux", "ux", "ui"],
    "hr": ["human resources"],
    "kpi": ["kpis", "key performance indicator"],
    "roi": ["return on investment"],
    "seo": ["search engine optimization", "search engine optimisation"],
    "sem": ["search engine marketing"],
    "gmp": ["good manufacturing practice", "good manufacturing practices"],
    "glp": ["good laboratory practice", "good laboratory practices"],
    "gcp (good clinical practice)": ["good clinical practice", "ich-gcp", "ich gcp"],
    "pcr": ["polymerase chain reaction", "qpcr", "rt-pcr"],
    "hplc": ["high performance liquid chromatography"],
    "elisa": ["enzyme-linked immunosorbent assay"],
    "sop": ["sops", "standard operating procedure", "standard operating procedures"],
    "capa": ["corrective and preventive action"],
    "ngs": ["next generation sequencing", "next-generation sequencing"],
    "rna-seq": ["rna seq", "rnaseq"],
}

# Words that carry no skill meaning when they stand alone.
STOP_KEYWORDS = {
    "", "and", "or", "etc", "etc.", "e.g.", "e.g", "i.e.", "basics", "basic",
    "knowledge", "understanding", "experience", "skills", "tools", "including",
    "such as", "like", "other", "others", "various", "familiarity", "proficiency",
    "strong", "good", "excellent", "working", "ability", "of", "in", "with", "the",
    "a", "an", "for", "to", "using", "based", "related",
    "i", "ii", "iii", "iv", "v", "us", "eu", "r2", "r3", "criteria", "design",
}

# Terms that contain a slash but are ONE skill.
PROTECTED = ["CI/CD", "UI/UX", "TCP/IP", "A/B testing", "I/O", "S/4HANA"]

LEADING_FILLER = re.compile(
    r"^(?:knowledge of|understanding of|experience (?:with|in|of)|proficiency in|"
    r"familiarity with|expertise in|strong|good|basic|working knowledge of|hands-on(?: experience)? (?:with|in)|"
    r"ability to|skills? in|including|such as|e\.g\.,?|i\.e\.,?|and|or)\s+",
    re.I,
)


def _clean(token):
    token = token.strip().strip(".;:-–—•*").strip()
    token = re.sub(r"\s+", " ", token)
    token = LEADING_FILLER.sub("", token).strip()
    return token


def parse_line(line):
    """'Databases: MySQL, PostgreSQL (fast)' -> ('Databases', ['MySQL', 'PostgreSQL', 'fast'])"""
    line = line.strip().lstrip("-•* ").strip()
    if not line:
        return None
    label = ""
    body = line
    # label = text before the first colon (only if it is short, i.e. a heading)
    if ":" in line:
        head, tail = line.split(":", 1)
        if len(head) <= 60 and tail.strip():
            label, body = head.strip(), tail.strip()
    elif "(" in line:
        label = line.split("(", 1)[0].strip()

    # Protect slash-terms that are a single skill.
    protected = {}
    for i, term in enumerate(PROTECTED):
        token = f"@@P{i}@@"
        if term.lower() in body.lower():
            body = re.sub(re.escape(term), token, body, flags=re.I)
            protected[token] = term

    keywords = []
    outside = re.sub(r"\([^)]*\)", " ", body)
    parts = re.split(r"[,;]|\s&\s|\sand\s|\sor\s|/|\s[—–-]\s", outside)
    keywords.extend(parts)
    for inner in re.findall(r"\(([^)]*)\)", body):
        keywords.extend(re.split(r"[,;/]|\s&\s|\sand\s|\s[—–-]\s", inner))

    cleaned, seen = [], set()
    for kw in keywords:
        for token, term in protected.items():
            kw = kw.replace(token, term)
        kw = _clean(kw)
        low = kw.lower()
        if low in STOP_KEYWORDS or len(kw) < 2 or len(kw) > 60 or kw.isdigit():
            continue
        if low not in seen:
            seen.add(low)
            cleaned.append(kw)
    if not label:
        label = cleaned[0] if cleaned else line[:40]
    return label.strip(), cleaned


def split_description(text):
    """Split the Excel cell into requirement lines."""
    return [ln for ln in (l.strip() for l in text.splitlines()) if ln.lstrip("-•* ").strip()]


def _normalise(text):
    text = text.lower()
    text = text.replace("’", "'").replace("–", "-").replace("—", "-")
    text = re.sub(r"[ \t]+", " ", text)
    return text


@lru_cache(maxsize=4096)
def _pattern_for(variant, case_sensitive=False):
    """Regex that finds `variant` as a whole word/phrase."""
    esc = re.escape(variant)
    esc = esc.replace(r"\ ", r"[\s\-_]+")  # 'machine learning' == 'machine-learning'
    flags = 0 if case_sensitive else re.I
    plural = "" if case_sensitive else "(?:s|es)?"
    return re.compile(r"(?<![A-Za-z0-9+#])" + esc + plural + r"(?![A-Za-z0-9+#])", flags)


# alias -> canonical keys that list it (so "Postgres" in a JD also finds "PostgreSQL")
_REVERSE = {}
for _canon, _alts in ALIASES.items():
    for _alt in _alts:
        _REVERSE.setdefault(_alt, set()).add(_canon)


def variants_for(keyword):
    key = keyword.lower().strip()
    out = {key}
    out.update(ALIASES.get(key, []))
    out.update(_REVERSE.get(key, []))
    if key.endswith(".js"):
        base = key[:-3]
        out.update({base + "js", base + " js"})
    for suffix in (" basics", " fundamentals", " concepts", " principles"):
        if key.endswith(suffix):
            out.add(key[: -len(suffix)])
    return out


def keyword_in_text(keyword, raw_text, norm_text):
    """Short tokens (<= 3 chars: 'ML', 'JS', 'PF') must match in UPPER case so
    that ordinary words ('us', 'pf') do not give false matches."""
    for variant in variants_for(keyword):
        if not variant:
            continue
        if len(variant) <= 3 and not any(ch.isdigit() for ch in variant):
            if _pattern_for(variant.upper(), True).search(raw_text) or (
                keyword.strip() == keyword.strip().title()
                and _pattern_for(keyword.strip(), True).search(raw_text)
            ):
                return True
        elif _pattern_for(variant).search(norm_text):
            return True
    return False


def match_keywords(keywords, resume_text):
    norm = _normalise(resume_text)
    matched = [k for k in keywords if keyword_in_text(k, resume_text, norm)]
    missing = [k for k in keywords if k not in matched]
    return matched, missing
