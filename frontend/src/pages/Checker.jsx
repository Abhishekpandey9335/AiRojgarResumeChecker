import { useEffect, useMemo, useRef, useState } from "react";
import { useNavigate, useSearchParams } from "react-router-dom";
import { analyzeResume, getBranches, getRole, getRoles } from "../api";
import { Icon, branchIcon } from "../components/Icons.jsx";
import { MAX_UPLOAD_MB } from "../config";

const ACCEPT = ".pdf,.docx,.txt";

function formatSize(bytes) {
  return bytes > 1024 * 1024 ? `${(bytes / 1024 / 1024).toFixed(1)} MB` : `${Math.max(1, Math.round(bytes / 1024))} KB`;
}

export default function Checker() {
  const navigate = useNavigate();
  const [params, setParams] = useSearchParams();
  const branch = params.get("branch") || "";

  const [branches, setBranches] = useState([]);
  const [roles, setRoles] = useState([]);
  const [roleId, setRoleId] = useState("");
  const [roleInfo, setRoleInfo] = useState(null);
  const [search, setSearch] = useState("");
  const [file, setFile] = useState(null);
  const [dragging, setDragging] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [loadError, setLoadError] = useState("");
  const inputRef = useRef(null);

  useEffect(() => {
    getBranches().then(setBranches).catch((e) => setLoadError(e.message));
  }, []);

  useEffect(() => {
    setRoles([]);
    setRoleId("");
    setRoleInfo(null);
    setSearch("");
    if (!branch) return;
    getRoles(branch).then(setRoles).catch((e) => setLoadError(e.message));
  }, [branch]);

  useEffect(() => {
    setRoleInfo(null);
    if (roleId) getRole(roleId).then(setRoleInfo).catch(() => {});
  }, [roleId]);

  const filteredRoles = useMemo(
    () => roles.filter((r) => r.name.toLowerCase().includes(search.trim().toLowerCase())),
    [roles, search]
  );

  function pickFile(f) {
    setError("");
    if (!f) return;
    const ok = /\.(pdf|docx|txt)$/i.test(f.name);
    if (!ok) return setError("Please upload a PDF, DOCX or TXT file.");
    if (f.size > MAX_UPLOAD_MB * 1024 * 1024) return setError(`File is too large. Maximum size is ${MAX_UPLOAD_MB} MB.`);
    setFile(f);
  }

  async function submit(e) {
    e.preventDefault();
    setError("");
    if (!branch) return setError("Please select your branch.");
    if (!roleId) return setError("Please select a job role.");
    if (!file) return setError("Please upload your resume.");
    setLoading(true);
    try {
      const result = await analyzeResume({ file, roleId, branch });
      navigate(`/result/${result.id}`, { state: { result } });
    } catch (err) {
      setError(err.message);
      setLoading(false);
    }
  }

  const step = !branch ? 1 : !roleId ? 2 : 3;

  return (
    <section className="container checker">
      <div className="page-head">
        <span className="pill">Resume Checker</span>
        <h1>Check your resume for a specific role</h1>
        <p className="muted">Choose your branch, pick the job role, upload your resume and get your score.</p>
      </div>

      {loadError && <div className="alert error"><Icon.alert width={18} height={18} /> {loadError}</div>}

      <form onSubmit={submit} className="checker-grid">
        <div className="panel">
          <div className="panel-title"><span className={`num ${step >= 1 ? "on" : ""}`}>1</span> Select your branch</div>
          <div className="branch-pick">
            {branches.map((b) => (
              <button
                type="button"
                key={b.code}
                className={`branch-option ${branch === b.code ? "selected" : ""}`}
                onClick={() => setParams({ branch: b.code })}
              >
                <span className="branch-icon">{branchIcon(b.icon, { width: 22, height: 22 })}</span>
                <span><b>{b.name}</b><small>{b.role_count} roles</small></span>
              </button>
            ))}
          </div>

          <div className="panel-title spaced"><span className={`num ${step >= 2 ? "on" : ""}`}>2</span> Select job role</div>
          {!branch ? (
            <p className="muted small">Select a branch first to see its job roles.</p>
          ) : (
            <>
              <input
                className="input"
                type="search"
                placeholder="Search job roles..."
                value={search}
                onChange={(e) => setSearch(e.target.value)}
              />
              <div className="role-list" role="radiogroup" aria-label="Job roles">
                {filteredRoles.map((r) => (
                  <button
                    type="button"
                    role="radio"
                    aria-checked={String(r.id) === String(roleId)}
                    key={r.id}
                    className={`role-option ${String(r.id) === String(roleId) ? "selected" : ""}`}
                    onClick={() => setRoleId(String(r.id))}
                  >
                    {r.name}
                  </button>
                ))}
                {filteredRoles.length === 0 && <p className="muted small">No roles match your search.</p>}
              </div>
            </>
          )}
        </div>

        <div className="panel">
          <div className="panel-title"><span className={`num ${step >= 3 ? "on" : ""}`}>3</span> Upload your resume</div>

          <div
            className={`dropzone ${dragging ? "drag" : ""} ${file ? "has-file" : ""}`}
            onDragOver={(e) => { e.preventDefault(); setDragging(true); }}
            onDragLeave={() => setDragging(false)}
            onDrop={(e) => { e.preventDefault(); setDragging(false); pickFile(e.dataTransfer.files[0]); }}
            onClick={() => inputRef.current?.click()}
            role="button"
            tabIndex={0}
            onKeyDown={(e) => (e.key === "Enter" || e.key === " ") && inputRef.current?.click()}
          >
            <input ref={inputRef} type="file" accept={ACCEPT} hidden onChange={(e) => pickFile(e.target.files[0])} />
            {file ? (
              <>
                <span className="drop-icon ok"><Icon.file width={30} height={30} /></span>
                <b>{file.name}</b>
                <small>{formatSize(file.size)} - click to change</small>
              </>
            ) : (
              <>
                <span className="drop-icon"><Icon.upload width={30} height={30} /></span>
                <b>Drag &amp; drop your resume here</b>
                <small>or click to browse. PDF, DOCX or TXT, up to {MAX_UPLOAD_MB} MB</small>
              </>
            )}
          </div>

          {roleInfo && (
            <div className="role-preview">
              <div className="rp-title"><Icon.target width={18} height={18} /> Skills we will look for: {roleInfo.name}</div>
              <ul>
                {roleInfo.skills.slice(0, 8).map((s) => (
                  <li key={s.label}><b>{s.label}</b><span>{s.keywords.slice(0, 5).join(", ")}</span></li>
                ))}
              </ul>
            </div>
          )}

          {error && <div className="alert error"><Icon.alert width={18} height={18} /> {error}</div>}

          <button className="btn btn-primary btn-lg btn-block" disabled={loading}>
            {loading ? (<><span className="spinner" /> Analysing your resume...</>) : (<>Check My Resume <Icon.arrow width={18} height={18} /></>)}
          </button>
          <p className="muted small center">Your file is read once to calculate the score and is not stored.</p>
        </div>
      </form>
    </section>
  );
}
