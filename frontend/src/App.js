import React, { useState, useEffect } from "react";
import axios from "axios";

const App = () => {
  const [topic, setTopic] = useState("");
  const [numEasy, setNumEasy] = useState(0);
  const [numMedium, setNumMedium] = useState(0);
  const [numHard, setNumHard] = useState(0);
  const [questions, setQuestions] = useState([]);
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [answers, setAnswers] = useState([]);
  const [score, setScore] = useState(0);
  const [showResult, setShowResult] = useState(false);

  const handleSubmitForm = async () => {
    try {
      const response = await axios.post("http://localhost:8000/generate-quiz", {
        topic,
        numEasy,
        numMedium,
        numHard,
      });

      setQuestions(response.data.questions);
      setAnswers(new Array(response.data.questions.length).fill(null));
      setCurrentQuestionIndex(0);
      setScore(0);
      setShowResult(false);

      console.log("Received questions from backend:", response.data.questions);
    } catch (error) {
      console.error("Error fetching quiz:", error.response ? error.response.data : error.message);
      alert(`Error fetching quiz: ${error.response ? JSON.stringify(error.response.data) : error.message}`);
    }
  };

  const handleAnswerChange = (value) => {
    const updatedAnswers = [...answers];
    updatedAnswers[currentQuestionIndex] = value;
    setAnswers(updatedAnswers);
  };

  const handleNextQuestion = () => {
    if (currentQuestionIndex < questions.length - 1) {
      setCurrentQuestionIndex(currentQuestionIndex + 1);
    } else {
      calculateScore();
      setShowResult(true);
    }
  };

  const calculateScore = () => {
    let calculatedScore = 0;

    questions.forEach((question, index) => {
      if (answers[index] === question.answer) {
        calculatedScore += 1;
      }
    });

    setScore(calculatedScore);
  };

  const renderQuestionResult = (question, index) => {
    const userAnswer = answers[index];
    const correctAnswer = question.answer;
    console.log(question.answer);
    console.log(correctAnswer);
    const isCorrect = userAnswer === correctAnswer;

    return (
      <div
        key={index}
        className={`border rounded-lg p-4 mb-4 ${
          isCorrect ? "bg-green-50 border-green-400" : "bg-red-50 border-red-400"
        }`}
      >
        <p className="text-lg font-semibold">Q{index + 1}: {question.question}</p>
        <p className="mt-2">Your Answer: <span className={`font-medium ${isCorrect ? "text-green-600" : "text-red-600"}`}>{question.options[userAnswer]}</span></p>
        <p className="mt-1">Correct Answer: <span className="font-medium text-blue-600">{question.options[correctAnswer]}</span></p>
        <p className="mt-1 text-indigo-600">Marks Awarded: {isCorrect ? 1 : 0}</p>
      </div>
    );
  };

  return (
    <div className="min-h-screen bg-gray-100 flex flex-col items-center py-10 px-4">
      <div className="w-full max-w-3xl bg-white shadow-lg rounded-lg p-6">
        <h1 className="text-3xl font-bold text-center mb-6">Interactive Quiz Application</h1>

        {/* Quiz Configuration Form */}
        {!questions.length && !showResult && (
          <div>
            <h2 className="text-2xl font-semibold mb-4">Configure Your Quiz</h2>
            <div className="space-y-4">
              <div>
                <label className="block text-lg font-medium">Topic</label>
                <input
                  type="text"
                  value={topic}
                  onChange={(e) => setTopic(e.target.value)}
                  className="w-full border rounded-lg px-3 py-2 mt-1"
                />
              </div>
              <div>
                <label className="block text-lg font-medium">Number of Easy Questions</label>
                <input
                  type="number"
                  value={numEasy}
                  onChange={(e) => setNumEasy(Number(e.target.value))}
                  className="w-full border rounded-lg px-3 py-2 mt-1"
                />
              </div>
              <div>
                <label className="block text-lg font-medium">Number of Medium Questions</label>
                <input
                  type="number"
                  value={numMedium}
                  onChange={(e) => setNumMedium(Number(e.target.value))}
                  className="w-full border rounded-lg px-3 py-2 mt-1"
                />
              </div>
              <div>
                <label className="block text-lg font-medium">Number of Hard Questions</label>
                <input
                  type="number"
                  value={numHard}
                  onChange={(e) => setNumHard(Number(e.target.value))}
                  className="w-full border rounded-lg px-3 py-2 mt-1"
                />
              </div>
            </div>
            <button
              onClick={handleSubmitForm}
              className="w-full bg-blue-600 text-white rounded-lg px-4 py-2 mt-6 hover:bg-blue-700 transition"
            >
              Generate Quiz
            </button>
          </div>
        )}

        {/* Quiz Question Section */}
        {questions.length > 0 && !showResult && (
          <div>
            <h2 className="text-2xl font-semibold mb-4">
              Question {currentQuestionIndex + 1} of {questions.length}
            </h2>
            <p className="text-lg mb-6">{questions[currentQuestionIndex].question}</p>
            <div className="space-y-4">
              {Object.entries(questions[currentQuestionIndex].options).map(([key, value]) => (
                <label
                  key={key}
                  className={`block border rounded-lg px-4 py-2 cursor-pointer ${
                    answers[currentQuestionIndex] === key ? "bg-blue-100 border-blue-500" : "border-gray-300"
                  }`}
                >
                  <input
                    type="radio"
                    name={`question-${currentQuestionIndex}`}
                    value={key}
                    checked={answers[currentQuestionIndex] === key}
                    onChange={(e) => handleAnswerChange(e.target.value)}
                    className="hidden"
                  />
                  {value}
                </label>
              ))}
            </div>
            <button
              onClick={handleNextQuestion}
              className="w-full bg-green-600 text-white rounded-lg px-4 py-2 mt-6 hover:bg-green-700 transition"
              disabled={answers[currentQuestionIndex] === null}
            >
              {currentQuestionIndex === questions.length - 1 ? "Finish Quiz" : "Next Question"}
            </button>
          </div>
        )}

        {/* Quiz Results Section */}
        {showResult && (
          <div>
            <h2 className="text-3xl font-bold mb-6">Quiz Results</h2>
            <p className="text-lg font-medium mb-4">
              Your Score: <span className="text-green-600">{score}</span> / {questions.length}
            </p>
            <div className="space-y-4">
              {questions.map((question, index) => renderQuestionResult(question, index))}
            </div>
            <button
              onClick={() => {
                setQuestions([]);
                setAnswers([]);
                setTopic("");
                setNumEasy(0);
                setNumMedium(0);
                setNumHard(0);
                setScore(0);
                setShowResult(false);
              }}
              className="w-full bg-blue-600 text-white rounded-lg px-4 py-2 mt-6 hover:bg-blue-700 transition"
            >
              Restart Quiz
            </button>
          </div>
        )}
      </div>
    </div>
  );
};

export default App;
