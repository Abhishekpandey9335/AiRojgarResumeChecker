import { useState } from "react";
import { Link, NavLink } from "react-router-dom";
import Logo from "./Logo.jsx";
import { MAIN_SITE_URL } from "../config";

export default function Navbar() {
  const [open, setOpen] = useState(false);
  const close = () => setOpen(false);
  return (
    <header className="nav-wrap">
      <nav className="nav">
        <Logo />
        <button className="nav-toggle" onClick={() => setOpen(!open)} aria-label="Menu" aria-expanded={open}>
          <span /><span /><span />
        </button>
        <div className={`nav-links ${open ? "open" : ""}`}>
          <NavLink to="/" end onClick={close}>Home</NavLink>
          <NavLink to="/check" onClick={close}>Check Resume</NavLink>
          <Link to="/#branches" onClick={close}>Branches</Link>
          <Link to="/#how-it-works" onClick={close}>How It Works</Link>
          <a href={MAIN_SITE_URL} onClick={close}>Back to AiRojgar</a>
          <Link to="/check" className="btn btn-primary btn-sm nav-cta" onClick={close}>Check My Resume</Link>
        </div>
      </nav>
    </header>
  );
}
