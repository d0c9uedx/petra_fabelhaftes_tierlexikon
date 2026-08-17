import { useEffect, useState } from "react";
import { listCategories, getProgress } from "../api/animals";
import CategoryTile from "../components/CategoryTile";
import type { Category, Progress } from "../types";

export default function CategoryOverviewPage() {
  const [categories, setCategories] = useState<Category[]>([]);
  const [progress, setProgress] = useState<Progress | null>(null);

  useEffect(() => {
    listCategories().then(setCategories);
    getProgress().then(setProgress);
  }, []);

  return (
    <div>
      <h1>Kategorien</h1>
      <div className="category-grid">
        {categories.map((category) => (
          <CategoryTile
            key={category.value}
            category={category}
            progress={progress?.by_category.find((p) => p.category === category.value)}
          />
        ))}
      </div>
    </div>
  );
}
