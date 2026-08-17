import { Link } from "react-router-dom";
import type { AnimalListItem } from "../types";

export default function AnimalCard({ animal }: { animal: AnimalListItem }) {
  return (
    <Link to={`/tier/${animal.id}`} className={`animal-card${animal.seen ? " animal-card-seen" : ""}`}>
      <img src={animal.image_url} alt={animal.name_de} loading="lazy" />
      <span className="animal-card-name">{animal.name_de}</span>
      {animal.seen && <span className="animal-card-badge">gesehen</span>}
    </Link>
  );
}
