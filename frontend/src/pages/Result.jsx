import { useEffect, useState } from "react";
import { Link, useLocation, useParams } from "react-router-dom";
import { getAnalysis } from "../api";
import { MAIN_SITE_URL } from "../config";
import { Icon } from "../components/Icons.jsx";
import ScoreRing, { scoreColor } from "../components/ScoreRing.jsx";

const PRIORITY_LABEL = { high: "High priority", medium: "Medium", low: "Nice to have" };

export default function Result() {
  const { id } = useParams();
  const location = useLocation();
  const [data, setData] = useState(location.state?.result || null);
  const [error, setError] = useState("");

  useEffect(() => {
    if (data && String(data.id) === String(id)) return;
    getAnalysis(id).then(setData).catch((e) => setError(e.message));
  }, [id]); // eslint-disable-line react-hooks/exhaustive-deps

  if (error) {
    return (
      <section className="container narrow">
        <div className="alert error"><Icon.alert width={18} height={18} /> {error}</div>
        <Link to="/check" className="btn btn-primary">Check a resume</Link>
      </section>
    );
  }
  if (!data) return <section className="container narrow center"><span className="spinner dark" /> Loading result...</section>;

  const missingTop = data.missing_skills.slice(0, 24);

  return (
    <section className="container result">
      <Link to="/check" className="back-link"><Icon.back width={16} height={16} /> Check another resume</Link>

      <div className="result-hero">
        <ScoreRing score={data.score} />
        <div className="result-summary">
          <span className="pill">{data.branch ? `${data.branch} - ` : ""}{data.role}</span>
          <h1>{data.rating} resume for this role</h1>
          <p className={`verdict ${data.verdict.shortlisted ? "ok" : "no"}`}>
            {data.verdict.shortlisted ? <Icon.check width={18} height={18} /> : <Icon.alert width={18} height={18} />}
            {data.verdict.text}
          </p>
          <p className="muted">
            Your resume matches <b>{data.skill_match_percent}%</b> of the skills required for {data.role}.
            File checked: {data.filename}
          </p>
          <div className="hero-actions">
            <button className="btn btn-light" onClick={() => window.print()}><Icon.print width={18} height={18} /> Print / Save as PDF</button>
            <a className="btn btn-light" href={MAIN_SITE_URL}><Icon.external width={18} height={18} /> Back to AiRojgar</a>
          </div>
        </div>
      </div>

      <div className="grid-2">
        <div className="panel">
          <h2 className="panel-h">Score breakdown</h2>
          {data.breakdown.map((b) => {
            const pct = Math.round((b.score / b.max) * 100);
            return (
              <div className="bar-row" key={b.key}>
                <div className="bar-label"><span>{b.label}</span><b>{Math.round(b.score)} / {b.max}</b></div>
                <div className="bar"><i style={{ width: `${pct}%`, background: scoreColor(pct) }} /></div>
              </div>
            );
          })}
        </div>

        <div className="panel">
          <h2 className="panel-h">Resume checklist</h2>
          <ul className="checklist">
            {data.sections.map((s) => (
              <li key={s.key} className={s.present ? "yes" : "no"}>
                {s.present ? <Icon.check width={16} height={16} /> : <Icon.x width={16} height={16} />} {s.label}
              </li>
            ))}
            <li className={data.contact.email ? "yes" : "no"}>{data.contact.email ? <Icon.check width={16} height={16} /> : <Icon.x width={16} height={16} />} Email address</li>
            <li className={data.contact.phone ? "yes" : "no"}>{data.contact.phone ? <Icon.check width={16} height={16} /> : <Icon.x width={16} height={16} />} Phone number</li>
            <li className={data.contact.linkedin ? "yes" : "no"}>{data.contact.linkedin ? <Icon.check width={16} height={16} /> : <Icon.x width={16} height={16} />} LinkedIn profile</li>
            <li className={data.contact.portfolio ? "yes" : "no"}>{data.contact.portfolio ? <Icon.check width={16} height={16} /> : <Icon.x width={16} height={16} />} GitHub / portfolio link</li>
          </ul>
        </div>
      </div>

      <div className="panel">
        <h2 className="panel-h"><Icon.bulb width={20} height={20} /> What to change (suggestions)</h2>
        {data.suggestions.length === 0 ? (
          <p className="muted">Great work! We have no major changes to suggest.</p>
        ) : (
          <ol className="tips">
            {data.suggestions.map((t, i) => (
              <li key={i} className={`tip ${t.priority}`}>
                <span className="tip-tag">{PRIORITY_LABEL[t.priority]} - {t.category}</span>
                <p>{t.text}</p>
              </li>
            ))}
          </ol>
        )}
      </div>

      <div className="grid-2">
        <div className="panel">
          <h2 className="panel-h ok-h"><Icon.check width={20} height={20} /> Skills found ({data.matched_skills.length})</h2>
          <div className="chips">
            {data.matched_skills.length ? data.matched_skills.map((s) => <span className="chip ok" key={s}>{s}</span>) : <p className="muted">No role skills were found.</p>}
          </div>
        </div>
        <div className="panel">
          <h2 className="panel-h bad-h"><Icon.x width={20} height={20} /> Skills missing ({data.missing_skills.length})</h2>
          <div className="chips">
            {missingTop.length ? missingTop.map((s) => <span className="chip bad" key={s}>{s}</span>) : <p className="muted">You cover every skill. Excellent!</p>}
          </div>
        </div>
      </div>

      <div className="panel">
        <h2 className="panel-h">Skill-by-skill match for {data.role}</h2>
        <div className="skill-table">
          {data.skill_details.map((d) => (
            <div className="skill-row" key={d.label}>
              <div className="sr-head">
                <b>{d.label}</b>
                <span style={{ color: scoreColor(d.score) }}>{d.score}%</span>
              </div>
              <div className="bar"><i style={{ width: `${d.score}%`, background: scoreColor(d.score) }} /></div>
              <div className="chips small">
                {d.matched.map((s) => <span className="chip ok" key={"m" + s}>{s}</span>)}
                {d.missing.map((s) => <span className="chip bad" key={"x" + s}>{s}</span>)}
              </div>
            </div>
          ))}
        </div>
      </div>

      <div className="cta-band">
        <div>
          <h2>Want to try another role?</h2>
          <p>Fix the points above, then check again to see your score go up.</p>
        </div>
        <Link to="/check" className="btn btn-white btn-lg">Check Again <Icon.arrow width={18} height={18} /></Link>
      </div>
    </section>
  );
}
