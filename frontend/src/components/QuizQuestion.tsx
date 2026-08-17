import { useState } from "react";
import type { QuizAnswerResult, QuizQuestion as QuizQuestionType } from "../types";

export default function QuizQuestion({
  question,
  onAnswer,
}: {
  question: QuizQuestionType;
  onAnswer: (selectedAnimalId: number) => Promise<QuizAnswerResult>;
}) {
  const [result, setResult] = useState<QuizAnswerResult | null>(null);
  const [selectedId, setSelectedId] = useState<number | null>(null);

  async function handleSelect(optionId: number) {
    if (result) return; // schon beantwortet
    setSelectedId(optionId);
    const answer = await onAnswer(optionId);
    setResult(answer);
  }

  return (
    <div className="quiz-question">
      <img src={question.animal.image_url} alt="Welches Tier ist das?" className="quiz-question-image" />
      <p>Wie heißt dieses Tier?</p>
      <div className="quiz-options">
        {question.options.map((option) => {
          const isSelected = selectedId === option.animal_id;
          const isCorrectOption = result && option.animal_id === result.correct_animal_id;
          let className = "quiz-option";
          if (result && isCorrectOption) className += " quiz-option-correct";
          else if (result && isSelected && !isCorrectOption) className += " quiz-option-wrong";

          return (
            <button
              key={option.animal_id}
              className={className}
              disabled={!!result}
              onClick={() => handleSelect(option.animal_id)}
            >
              {option.name_de}
            </button>
          );
        })}
      </div>
      {result && (
        <p className="quiz-feedback">
          {result.correct ? "Richtig! 🎉" : "Leider falsch."} Nächste Abfrage in {result.interval_days} Tag
          {result.interval_days === 1 ? "" : "en"}.
        </p>
      )}
    </div>
  );
}
