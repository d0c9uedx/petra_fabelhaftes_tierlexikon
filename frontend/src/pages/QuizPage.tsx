import { useCallback, useEffect, useState } from "react";
import { getNextQuestion, submitAnswer } from "../api/quiz";
import QuizQuestionComponent from "../components/QuizQuestion";
import { ApiError } from "../api/client";
import type { QuizQuestion } from "../types";

export default function QuizPage() {
  const [question, setQuestion] = useState<QuizQuestion | null>(null);
  const [noneDue, setNoneDue] = useState(false);

  const loadNext = useCallback(() => {
    setNoneDue(false);
    setQuestion(null);
    getNextQuestion()
      .then(setQuestion)
      .catch((err) => {
        if (err instanceof ApiError && err.status === 404) setNoneDue(true);
        else throw err;
      });
  }, []);

  useEffect(() => {
    loadNext();
  }, [loadNext]);

  if (noneDue) {
    return (
      <div>
        <h1>Quiz</h1>
        <p>Aktuell ist keine Frage fällig — schau später wieder vorbei! 🎉</p>
      </div>
    );
  }

  return (
    <div>
      <h1>Quiz</h1>
      {question ? (
        <>
          <QuizQuestionComponent
            key={question.animal.id}
            question={question}
            onAnswer={(selectedId) => submitAnswer(question.animal.id, selectedId)}
          />
          <button className="quiz-next-button" onClick={loadNext}>
            Nächste Frage ➜
          </button>
        </>
      ) : (
        <p>Lädt…</p>
      )}
    </div>
  );
}
