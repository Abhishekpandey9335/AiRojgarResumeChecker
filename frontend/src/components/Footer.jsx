import { Link } from "react-router-dom";
import Logo from "./Logo.jsx";
import { MAIN_SITE_URL } from "../config";

export default function Footer() {
  return (
    <footer className="footer">
      <div className="container footer-inner">
        <div>
          <Logo />
          <p className="muted footer-text">
            Resume Checker is a free tool by AiRojgar. We compare your resume with the skills employers ask for and
            show you exactly what to improve.
          </p>
        </div>
        <div className="footer-links">
          <Link to="/check">Check Resume</Link>
          <Link to="/#how-it-works">How It Works</Link>
          <a href={MAIN_SITE_URL}>airojgar.in</a>
        </div>
      </div>
      <div className="container footer-bottom">
        <span>&copy; {new Date().getFullYear()} AiRojgar. All rights reserved.</span>
        <span>Your resume is analysed instantly and is never stored.</span>
      </div>
    </footer>
  );
}
