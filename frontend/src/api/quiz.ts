import { apiFetch } from "./client";
import type { QuizAnswerResult, QuizQuestion } from "../types";

export function getNextQuestion(): Promise<QuizQuestion> {
  return apiFetch<QuizQuestion>("/quiz/next");
}

export function submitAnswer(animalId: number, selectedAnimalId: number): Promise<QuizAnswerResult> {
  return apiFetch<QuizAnswerResult>("/quiz/answer", {
    method: "POST",
    body: { animal_id: animalId, selected_animal_id: selectedAnimalId },
  });
}
