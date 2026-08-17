import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { getAnimal } from "../api/animals";
import AnimalProfile from "../components/AnimalProfile";
import type { Animal } from "../types";

export default function AnimalDetailPage() {
  const { id } = useParams<{ id: string }>();
  const [animal, setAnimal] = useState<Animal | null>(null);

  useEffect(() => {
    if (id) getAnimal(Number(id)).then(setAnimal);
  }, [id]);

  if (!animal) return <p>Lädt…</p>;
  return <AnimalProfile animal={animal} />;
}
