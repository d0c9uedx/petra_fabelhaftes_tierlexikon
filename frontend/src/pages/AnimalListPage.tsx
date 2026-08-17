import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import { listAnimals } from "../api/animals";
import AnimalCard from "../components/AnimalCard";
import type { AnimalCategory, AnimalListItem } from "../types";

export default function AnimalListPage() {
  const { category } = useParams<{ category: AnimalCategory }>();
  const [animals, setAnimals] = useState<AnimalListItem[]>([]);

  useEffect(() => {
    if (category) listAnimals(category).then(setAnimals);
  }, [category]);

  return (
    <div>
      <p>
        <Link to="/">← Zurück zu den Kategorien</Link>
      </p>
      <h1>Tiere</h1>
      <div className="animal-grid">
        {animals.map((animal) => (
          <AnimalCard key={animal.id} animal={animal} />
        ))}
      </div>
      {animals.length === 0 && <p>Für diese Kategorie sind noch keine Tiere hinterlegt.</p>}
    </div>
  );
}
