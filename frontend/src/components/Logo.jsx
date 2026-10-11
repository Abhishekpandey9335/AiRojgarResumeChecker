import { MAIN_SITE_URL } from "../config";

// Replace this SVG with your real AiRojgar logo file (put it in /public and use an <img>).
export default function Logo({ compact = false }) {
  return (
    <a className="logo" href={MAIN_SITE_URL} aria-label="AiRojgar home">
      <svg width="34" height="34" viewBox="0 0 64 64" aria-hidden="true">
        <defs>
          <linearGradient id="lg" x1="0" y1="0" x2="1" y2="1">
            <stop offset="0" stopColor="#4f46e5" />
            <stop offset="1" stopColor="#7c3aed" />
          </linearGradient>
        </defs>
        <rect width="64" height="64" rx="16" fill="url(#lg)" />
        <path d="M20 46 32 16l12 30M25 37h14" fill="none" stroke="#fff" strokeWidth="5" strokeLinecap="round" strokeLinejoin="round" />
      </svg>
      <span className="logo-text">
        <strong>AiRojgar</strong>
        {!compact && <small>Resume Checker</small>}
      </span>
    </a>
  );
}
