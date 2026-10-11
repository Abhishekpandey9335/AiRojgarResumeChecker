import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { getBranches } from "../api";
import { Icon, branchIcon } from "../components/Icons.jsx";

const FALLBACK_BRANCHES = [
  { code: "cse-it", name: "B.Tech CSE / IT", tagline: "Computer Science & Information Technology", icon: "code" },
  { code: "mba", name: "MBA", tagline: "Business / HRD / Marketing / Finance", icon: "briefcase" },
  { code: "biotechnology", name: "Biotechnology", tagline: "Biotech, Pharma & Life Sciences", icon: "dna" },
  { code: "biochemistry", name: "Biochemistry", tagline: "Biochemistry & Lab Sciences", icon: "flask" },
];

const STEPS = [
  { icon: "upload", title: "Upload Resume", text: "Upload your resume in PDF or DOCX format." },
  { icon: "file", title: "Select Role", text: "Choose your branch and the job role you want." },
  { icon: "brain", title: "Smart Analysis", text: "We match your resume with the skills that role needs." },
  { icon: "chart", title: "Get Your Score", text: "See your score out of 100 and what to improve." },
];

const BENEFITS = [
  { icon: "bolt", title: "Save Time", text: "Get your result in seconds." },
  { icon: "target", title: "Improve Chances", text: "Know exactly which skills are missing." },
  { icon: "shield", title: "Private & Safe", text: "Your resume file is never stored." },
  { icon: "users", title: "Built for Students", text: "Made for CSE/IT, MBA and Life Science students." },
];

export default function Home() {
  const [branches, setBranches] = useState(FALLBACK_BRANCHES);

  useEffect(() => {
    getBranches().then(setBranches).catch(() => {});
  }, []);

  return (
    <>
      <section className="hero">
        <div className="container hero-grid">
          <div className="hero-copy">
            <span className="pill">AI-Powered Resume Checker</span>
            <h1>
              Check Your Resume for the <span className="grad">Right Job Role</span>
            </h1>
            <p className="lead">
              Upload your resume, pick the job role you want, and get a score out of 100 with a clear list of
              missing skills and exact changes to make. Free, fast and built for students.
            </p>
            <div className="hero-actions">
              <Link to="/check" className="btn btn-primary btn-lg">
                <Icon.upload width={20} height={20} /> Upload Your Resume <Icon.arrow width={18} height={18} />
              </Link>
              <Link to="/#how-it-works" className="btn btn-light btn-lg">How It Works</Link>
            </div>
            <ul className="ticks">
              <li><Icon.check width={16} height={16} /> Fast &amp; Accurate</li>
              <li><Icon.check width={16} height={16} /> Role-Based Matching</li>
              <li><Icon.check width={16} height={16} /> 4 Student Branches</li>
            </ul>
          </div>

          <div className="hero-art" aria-hidden="true">
            <div className="float-card fc-1"><Icon.brain width={18} height={18} /> <div><b>Role Skill Match</b><small>Based on real job needs</small></div></div>
            <div className="float-card fc-2"><Icon.target width={18} height={18} /> <div><b>Score out of 100</b><small>Know where you stand</small></div></div>
            <div className="float-card fc-3"><Icon.bulb width={18} height={18} /> <div><b>Smart Suggestions</b><small>What to add or change</small></div></div>
            <div className="resume-mock">
              <div className="rm-head"><span className="rm-avatar" /><div><i className="w60" /><i className="w40" /></div></div>
              <i className="w90" /><i className="w80" /><i className="w70" />
              <div className="rm-sep" />
              <i className="w50 strong" /><i className="w90" /><i className="w60" />
              <div className="rm-sep" />
              <i className="w50 strong" /><i className="w80" /><i className="w90" />
              <div className="rm-badge"><strong>86</strong><span>/100</span></div>
            </div>
            <div className="verdict-card ok"><span className="vc-icon"><Icon.check width={18} height={18} /></span><div><b>Shortlist-ready</b><small>Your resume matches the role.</small></div></div>
            <div className="verdict-card bad"><span className="vc-icon"><Icon.x width={18} height={18} /></span><div><b>Needs improvement</b><small>Add the missing skills.</small></div></div>
          </div>
        </div>
      </section>

      <section className="container" id="branches">
        <div className="branches-box">
          <div className="branches-intro">
            <h2>Supported Student Branches</h2>
            <p className="muted">Multiple domains. One platform. Get matched with your dream role.</p>
          </div>
          <div className="branch-grid">
            {branches.map((b) => (
              <Link key={b.code} to={`/check?branch=${b.code}`} className={`branch-card bc-${b.code}`}>
                <span className="branch-icon">{branchIcon(b.icon, { width: 26, height: 26 })}</span>
                <b>{b.name}</b>
                <small>{b.tagline}</small>
                {b.role_count ? <em>{b.role_count} job roles</em> : null}
              </Link>
            ))}
          </div>
        </div>
      </section>

      <section className="container section" id="how-it-works">
        <h2 className="center">How It Works</h2>
        <p className="muted center">Simple steps to find out how strong your resume is</p>
        <div className="steps">
          {STEPS.map((s, i) => {
            const C = Icon[s.icon];
            return (
              <div className="step" key={s.title}>
                <div className="step-top"><span className="step-num">{i + 1}</span><span className="step-icon"><C width={22} height={22} /></span></div>
                <b>{s.title}</b>
                <p className="muted">{s.text}</p>
              </div>
            );
          })}
        </div>
      </section>

      <section className="container">
        <div className="benefits">
          {BENEFITS.map((b) => {
            const C = Icon[b.icon];
            return (
              <div className="benefit" key={b.title}>
                <span className="benefit-icon"><C width={22} height={22} /></span>
                <div><b>{b.title}</b><small>{b.text}</small></div>
              </div>
            );
          })}
        </div>
      </section>

      <section className="container section">
        <div className="cta-band">
          <div>
            <h2>Ready to see your resume score?</h2>
            <p>It takes less than a minute. No sign-up needed.</p>
          </div>
          <Link to="/check" className="btn btn-white btn-lg">Check My Resume <Icon.arrow width={18} height={18} /></Link>
        </div>
      </section>
    </>
  );
}
