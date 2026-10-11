const base = { width: 24, height: 24, viewBox: "0 0 24 24", fill: "none", stroke: "currentColor", strokeWidth: 2, strokeLinecap: "round", strokeLinejoin: "round" };

export const Icon = {
  code: (p) => <svg {...base} {...p}><path d="m16 18 6-6-6-6M8 6l-6 6 6 6" /></svg>,
  briefcase: (p) => <svg {...base} {...p}><rect x="2" y="7" width="20" height="14" rx="2" /><path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16" /></svg>,
  dna: (p) => <svg {...base} {...p}><path d="M4 4c0 6 16 6 16 16M20 4c0 6-16 6-16 16M7 7.5h10M7 16.5h10M12 12h0" /></svg>,
  flask: (p) => <svg {...base} {...p}><path d="M9 3h6M10 3v6L4.5 19a1.5 1.5 0 0 0 1.3 2.2h12.4a1.5 1.5 0 0 0 1.3-2.2L14 9V3M7.5 15h9" /></svg>,
  upload: (p) => <svg {...base} {...p}><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4M17 8l-5-5-5 5M12 3v12" /></svg>,
  file: (p) => <svg {...base} {...p}><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8zM14 2v6h6M8 13h8M8 17h5" /></svg>,
  target: (p) => <svg {...base} {...p}><circle cx="12" cy="12" r="10" /><circle cx="12" cy="12" r="6" /><circle cx="12" cy="12" r="2" /></svg>,
  brain: (p) => <svg {...base} {...p}><path d="M9.5 2A3.5 3.5 0 0 0 6 5.5a3 3 0 0 0-2 5 3.5 3.5 0 0 0 2 6 3.5 3.5 0 0 0 7 .5V4.5A2.5 2.5 0 0 0 9.5 2zM14.5 2A3.5 3.5 0 0 1 18 5.5a3 3 0 0 1 2 5 3.5 3.5 0 0 1-2 6 3.5 3.5 0 0 1-5 1.5" /></svg>,
  chart: (p) => <svg {...base} {...p}><path d="M3 3v18h18M7 14l4-4 3 3 5-6" /></svg>,
  bolt: (p) => <svg {...base} {...p}><path d="M13 2 3 14h9l-1 8 10-12h-9z" /></svg>,
  shield: (p) => <svg {...base} {...p}><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z" /><path d="m9 12 2 2 4-4" /></svg>,
  users: (p) => <svg {...base} {...p}><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2M9 11a4 4 0 1 0 0-8 4 4 0 0 0 0 8zM23 21v-2a4 4 0 0 0-3-3.9M16 3.1a4 4 0 0 1 0 7.8" /></svg>,
  check: (p) => <svg {...base} {...p}><path d="M20 6 9 17l-5-5" /></svg>,
  x: (p) => <svg {...base} {...p}><path d="M18 6 6 18M6 6l12 12" /></svg>,
  arrow: (p) => <svg {...base} {...p}><path d="M5 12h14M12 5l7 7-7 7" /></svg>,
  back: (p) => <svg {...base} {...p}><path d="M19 12H5M12 19l-7-7 7-7" /></svg>,
  alert: (p) => <svg {...base} {...p}><path d="M12 9v4M12 17h.01M10.3 3.9 1.8 18a2 2 0 0 0 1.7 3h17a2 2 0 0 0 1.7-3L13.7 3.9a2 2 0 0 0-3.4 0z" /></svg>,
  bulb: (p) => <svg {...base} {...p}><path d="M9 18h6M10 22h4M12 2a7 7 0 0 0-4 12.7c.6.5 1 1.2 1 2V18h6v-1.3c0-.8.4-1.5 1-2A7 7 0 0 0 12 2z" /></svg>,
  print: (p) => <svg {...base} {...p}><path d="M6 9V2h12v7M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2M6 14h12v8H6z" /></svg>,
  external: (p) => <svg {...base} {...p}><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6M15 3h6v6M10 14 21 3" /></svg>,
};

export function branchIcon(name, props) {
  const C = Icon[name] || Icon.file;
  return <C {...props} />;
}
