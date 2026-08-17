import { Link } from "react-router-dom";
import type { Category, CategoryProgress } from "../types";

const CATEGORY_ICONS: Record<string, string> = {
  vogel: "🐦",
  fisch: "🐟",
  insekt: "🐞",
  saeugetier: "🦁",
  sonstiges_landtier: "🦎",
};

export default function CategoryTile({
  category,
  progress,
}: {
  category: Category;
  progress?: CategoryProgress;
}) {
  return (
    <Link to={`/kategorie/${category.value}`} className="category-tile">
      <span className="category-tile-icon">{CATEGORY_ICONS[category.value] ?? "🐾"}</span>
      <span className="category-tile-label">{category.label}</span>
      {progress && (
        <span className="category-tile-progress">
          {progress.seen_count} / {progress.total_count} gesehen
        </span>
      )}
    </Link>
  );
}
