import { useEffect, useState } from "react";
import { getProgress } from "../api/animals";
import { useAuth } from "../context/AuthContext";
import type { Progress } from "../types";

const CATEGORY_LABELS: Record<string, string> = {
  vogel: "Vögel",
  fisch: "Fische",
  insekt: "Käfer / Insekten",
  saeugetier: "Säugetiere",
  sonstiges_landtier: "Sonstige Landtiere",
};

export default function ProfilePage() {
  const { user } = useAuth();
  const [progress, setProgress] = useState<Progress | null>(null);

  useEffect(() => {
    getProgress().then(setProgress);
  }, []);

  return (
    <div>
      <h1>Profil von {user?.username}</h1>
      {progress ? (
        <>
          <p>
            Sammel-Fortschritt gesamt: {progress.seen_count} / {progress.total_count}
          </p>
          <ul className="progress-list">
            {progress.by_category.map((c) => (
              <li key={c.category}>
                {CATEGORY_LABELS[c.category] ?? c.category}: {c.seen_count} / {c.total_count}
              </li>
            ))}
          </ul>
        </>
      ) : (
        <p>Lädt…</p>
      )}
    </div>
  );
}
