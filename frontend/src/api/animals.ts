import { apiFetch } from "./client";
import type { Animal, AnimalCategory, AnimalListItem, Category, Progress } from "../types";

export function listCategories(): Promise<Category[]> {
  return apiFetch<Category[]>("/categories");
}

export function listAnimals(category?: AnimalCategory): Promise<AnimalListItem[]> {
  const query = category ? `?category=${category}` : "";
  return apiFetch<AnimalListItem[]>(`/animals${query}`);
}

export function getAnimal(id: number): Promise<Animal> {
  return apiFetch<Animal>(`/animals/${id}`);
}

export function markAnimalSeen(id: number): Promise<void> {
  return apiFetch<void>(`/animals/${id}/seen`, { method: "POST" });
}

export function nextDiscoverAnimal(): Promise<Animal> {
  return apiFetch<Animal>("/discover/next");
}

export function getDailyAnimal(): Promise<Animal> {
  return apiFetch<Animal>("/daily-animal");
}

export function getProgress(): Promise<Progress> {
  return apiFetch<Progress>("/progress");
}
