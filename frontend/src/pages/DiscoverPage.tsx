import { useCallback, useEffect, useState } from "react";
import { nextDiscoverAnimal } from "../api/animals";
import AnimalProfile from "../components/AnimalProfile";
import type { Animal } from "../types";

export default function DiscoverPage() {
  const [animal, setAnimal] = useState<Animal | null>(null);

  const loadNext = useCallback(() => {
    nextDiscoverAnimal().then(setAnimal);
  }, []);

  useEffect(() => {
    loadNext();
  }, [loadNext]);

  return (
    <div>
      <h1>Entdecken</h1>
      {animal ? <AnimalProfile animal={animal} key={animal.id} /> : <p>Lädt…</p>}
      <button onClick={loadNext}>Nächstes Tier ➜</button>
    </div>
  );
}
