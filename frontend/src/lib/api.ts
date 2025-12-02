// API service for backend communication

export interface GameState {
  question: { id: number; text: string } | null;
  questionIndex: number | null;
  questionNumber: number;
  entropy: number;
  topCandidates: Array<{ name: string; probability: number }>;
  guess: { name: string; probability: number } | null;
}

export interface ApiError {
  error: string;
}

const API_BASE = "/api";

/**
 * Map frontend answer values to backend format
 */
const mapAnswerToBackend = (answer: string): string => {
  const mapping: Record<string, string> = {
    "yes": "yes",
    "probably-yes": "probably_yes",
    "maybe": "unknown",
    "probably-no": "probably_no",
    "no": "no",
  };
  return mapping[answer] || "unknown";
};

/**
 * Helper to parse JSON response with better error handling
 */
async function parseJsonResponse<T>(response: Response): Promise<T> {
  const text = await response.text();
  
  if (!text) {
    throw new Error(`Empty response from server (status: ${response.status}). Is the backend server running?`);
  }
  
  try {
    return JSON.parse(text) as T;
  } catch (e) {
    throw new Error(`Invalid JSON response: ${text.substring(0, 100)}`);
  }
}

/**
 * Start a new game
 */
export const startGame = async (): Promise<GameState> => {
  try {
    const response = await fetch(`${API_BASE}/start`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
    });

    if (!response.ok) {
      const error = await parseJsonResponse<ApiError>(response).catch(() => ({
        error: `Server error (${response.status}): ${response.statusText}`,
      }));
      throw new Error(error.error || "Failed to start game");
    }

    return parseJsonResponse<GameState>(response);
  } catch (error) {
    if (error instanceof TypeError && error.message.includes("fetch")) {
      throw new Error("Cannot connect to backend server. Make sure it's running on http://localhost:5000");
    }
    throw error;
  }
};

/**
 * Submit an answer to the current question
 */
export const submitAnswer = async (
  questionId: number,
  answer: string
): Promise<GameState> => {
  const backendAnswer = mapAnswerToBackend(answer);

  const response = await fetch(`${API_BASE}/answer`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      questionId,
      answer: backendAnswer,
    }),
  });

  if (!response.ok) {
    const error = await parseJsonResponse<ApiError>(response).catch(() => ({
      error: `Server error (${response.status}): ${response.statusText}`,
    }));
    throw new Error(error.error || "Failed to submit answer");
  }

  return parseJsonResponse<GameState>(response);
};

/**
 * Get the next question (after wrong guess)
 */
export const getNextQuestion = async (): Promise<GameState> => {
  const response = await fetch(`${API_BASE}/next-question`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
  });

  if (!response.ok) {
    const error = await parseJsonResponse<ApiError>(response).catch(() => ({
      error: `Server error (${response.status}): ${response.statusText}`,
    }));
    throw new Error(error.error || "Failed to get next question");
  }

  return parseJsonResponse<GameState>(response);
};

/**
 * Submit feedback on a guess
 */
export const submitGuessFeedback = async (
  correct: boolean
): Promise<{ ok: boolean; message: string }> => {
  const response = await fetch(`${API_BASE}/guess-feedback`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ correct }),
  });

  if (!response.ok) {
    const error = await parseJsonResponse<ApiError>(response).catch(() => ({
      error: `Server error (${response.status}): ${response.statusText}`,
    }));
    throw new Error(error.error || "Failed to submit feedback");
  }

  return parseJsonResponse<{ ok: boolean; message: string }>(response);
};

