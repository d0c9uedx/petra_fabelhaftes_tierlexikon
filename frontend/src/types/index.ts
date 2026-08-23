export type AnimalCategory =
  | "vogel"
  | "fisch"
  | "insekt"
  | "saeugetier"
  | "sonstiges_landtier";

export interface Category {
  value: AnimalCategory;
  label: string;
}

export interface AnimalListItem {
  id: number;
  name_de: string;
  image_url: string;
  category: AnimalCategory;
  seen: boolean;
}

export type RelationshipStatus = "monogam" | "wechselnde_liebhaber" | "harem";

export interface Animal {
  id: number;
  name_de: string;
  name_scientific: string;
  image_url: string;
  category: AnimalCategory;
  home_turf: string;
  conservation_status: string;
  reproduction_mode: "egg_laying" | "live_bearing";
  offspring_brood: string;
  baby_wait_time: string;
  favorite_food: string;
  arch_enemies: string;
  social_life: "solitary" | "herd";
  group_size: string | null;
  personality: string;
  fun_fact: string | null;
  superpower: string | null;
  mating_season: string | null;
  nest_building: string | null;
  courtship_dance: string | null;
  relationship_status: RelationshipStatus | null;
}

export interface User {
  id: number;
  username: string;
}

export interface CategoryProgress {
  category: AnimalCategory;
  seen_count: number;
  total_count: number;
}

export interface Progress {
  seen_count: number;
  total_count: number;
  by_category: CategoryProgress[];
}

export interface QuizAnimal {
  id: number;
  image_url: string;
  category: AnimalCategory;
}

export interface QuizOption {
  animal_id: number;
  name_de: string;
}

export interface QuizQuestion {
  animal: QuizAnimal;
  options: QuizOption[];
}

export interface QuizAnswerResult {
  correct: boolean;
  correct_animal_id: number;
  repetitions: number;
  interval_days: number;
  next_due_at: string;
}
