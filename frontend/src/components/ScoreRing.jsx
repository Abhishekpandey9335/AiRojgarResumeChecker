import { useEffect, useState } from "react";

export function scoreColor(score) {
  if (score >= 70) return "#16a34a";
  if (score >= 50) return "#f59e0b";
  return "#ef4444";
}

export default function ScoreRing({ score, size = 190, stroke = 14 }) {
  const [shown, setShown] = useState(0);
  useEffect(() => {
    let frame;
    const start = performance.now();
    const duration = 900;
    const tick = (now) => {
      const t = Math.min(1, (now - start) / duration);
      setShown(Math.round(score * (1 - Math.pow(1 - t, 3))));
      if (t < 1) frame = requestAnimationFrame(tick);
    };
    frame = requestAnimationFrame(tick);
    return () => cancelAnimationFrame(frame);
  }, [score]);

  const r = (size - stroke) / 2;
  const c = 2 * Math.PI * r;
  const color = scoreColor(score);
  return (
    <div className="score-ring" style={{ width: size, height: size }} role="img" aria-label={`Score ${score} out of 100`}>
      <svg width={size} height={size}>
        <circle cx={size / 2} cy={size / 2} r={r} fill="none" stroke="#e8e9fb" strokeWidth={stroke} />
        <circle
          cx={size / 2}
          cy={size / 2}
          r={r}
          fill="none"
          stroke={color}
          strokeWidth={stroke}
          strokeLinecap="round"
          strokeDasharray={c}
          strokeDashoffset={c * (1 - shown / 100)}
          transform={`rotate(-90 ${size / 2} ${size / 2})`}
        />
      </svg>
      <div className="score-ring-label">
        <strong style={{ color }}>{shown}</strong>
        <span>out of 100</span>
      </div>
    </div>
  );
}
