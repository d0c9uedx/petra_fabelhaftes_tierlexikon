import { useEffect, useState } from "react";
import { getDailyAnimal } from "../api/animals";
import AnimalProfile from "../components/AnimalProfile";
import type { Animal } from "../types";

export default function DailyAnimalPage() {
  const [animal, setAnimal] = useState<Animal | null>(null);

  useEffect(() => {
    getDailyAnimal().then(setAnimal);
  }, []);

  return (
    <div>
      <h1>Tier des Tages</h1>
      {animal ? <AnimalProfile animal={animal} /> : <p>Lädt…</p>}
    </div>
  );
}
