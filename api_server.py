# api_server.py
"""
Simple Flask API for the Indinator web UI.
Run with:  python api_server.py
"""

from pathlib import Path
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS

from indinator import AkinatorAI

# --- Setup --------------------------------------------------------------------

project_root = Path(__file__).parent
data_dir = project_root / "data"

app = Flask(__name__, static_folder="ui", static_url_path="")
CORS(app)  # Enable CORS for all routes

# Create a single AI engine instance (single-user / local use case)
ai = None
last_guess_name = None  # track last guess for feedback

try:
    print("[INIT] Initializing AI engine...")
    ai = AkinatorAI(
        traits_file=str(data_dir / "traits_flat.json"),
        questions_file=str(data_dir / "questions.json"),
        characters_file=str(data_dir / "characters.json"),
        enable_learning=False,  # keep web version simple & fast
    )
    print("[OK] AI engine ready!")
except Exception as e:
    print(f"[ERROR] Error initializing AI engine: {e}")
    import traceback
    traceback.print_exc()
    # ai will remain None, routes will check for this


# --- Helpers ------------------------------------------------------------------


def build_state(allow_guess: bool = True):
    """
    Build the JSON state returned to the frontend.
    Includes: next question (if any), entropy, top candidates, and guess (if ready).
    """
    global last_guess_name

    try:
        # Basic stats
        entropy = ai.entropy(ai.probabilities)
        top_candidates = [
            {"name": name, "probability": float(prob)}
            for name, prob in ai.get_top_characters(8)
        ]

        # Decide whether to guess
        guess = None
        last_guess_name = None
        if allow_guess and ai.should_make_guess(threshold=0.85):
            name, prob = ai.get_best_guess()
            guess = {"name": name, "probability": float(prob)}
            last_guess_name = name

        # If we're not making a guess (or want to keep asking), pick the next question
        question = None
        question_idx = None
        if guess is None:
            q_idx = ai.select_best_question()
            if q_idx is not None:
                # Validate question index
                if 0 <= q_idx < len(ai.questions):
                    q_obj = ai.questions[q_idx]
                    question = {
                        "id": q_idx,
                        "text": q_obj.get("question", ""),
                    }
                    question_idx = q_idx
                else:
                    print(f"Warning: Invalid question index {q_idx} (total questions: {len(ai.questions)})")

        # Question number = asked so far + 1 if we're presenting a new one
        questions_asked = len(ai.asked_questions)
        question_number = questions_asked + (1 if question is not None else 0)

        return {
            "question": question,             # {id, text} or null
            "questionIndex": question_idx,    # same as id; included for clarity
            "questionNumber": question_number,
            "entropy": float(entropy),
            "topCandidates": top_candidates,
            "guess": guess,                   # {name, probability} or null
        }
    except Exception as e:
        print(f"Error in build_state: {e}")
        import traceback
        traceback.print_exc()
        raise


# --- Routes -------------------------------------------------------------------


@app.route("/")
def index():
    """Serve the main UI page."""
    return send_from_directory(app.static_folder, "index.html")


@app.post("/api/start")
def api_start():
    """Start a new game (or restart) and return the initial state."""
    if ai is None:
        return jsonify({"error": "AI engine not initialized. Check server logs."}), 500
    
    try:
        ai.reset()
        state = build_state(allow_guess=False)  # never guess immediately
        return jsonify(state)
    except Exception as e:
        print(f"Error in api_start: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": f"Failed to start game: {str(e)}"}), 500


@app.post("/api/answer")
def api_answer():
    """
    Submit an answer to the current question.
    Body: { "questionId": int, "answer": "yes" | "no" | "probably_yes" | ... }
    """
    if ai is None:
        return jsonify({"error": "AI engine not initialized. Check server logs."}), 500
    
    try:
        data = request.get_json(force=True) or {}

        if "questionId" not in data or "answer" not in data:
            return jsonify({"error": "Missing 'questionId' or 'answer'"}), 400

        q_idx = int(data["questionId"])
        answer_code = str(data["answer"])

        # Map UI answers to (bool, likelihoods)
        if answer_code == "yes":
            ans_bool = True
            lk_correct, lk_incorrect = 0.95, 0.05
        elif answer_code == "probably_yes":
            ans_bool = True
            lk_correct, lk_incorrect = 0.75, 0.25
        elif answer_code == "no":
            ans_bool = False
            lk_correct, lk_incorrect = 0.95, 0.05
        elif answer_code == "probably_no":
            ans_bool = False
            lk_correct, lk_incorrect = 0.75, 0.25
        elif answer_code == "unknown":
            ans_bool = None  # skip: don't update probabilities
        else:
            return jsonify({"error": f"Invalid answer '{answer_code}'"}), 400

        # Update probabilities only if the user gave a directional answer
        if ans_bool is not None:
            ai.update_probabilities(
                q_idx,
                ans_bool,
                likelihood_correct=lk_correct,
                likelihood_incorrect=lk_incorrect,
            )

        state = build_state(allow_guess=True)
        return jsonify(state)
    except Exception as e:
        print(f"Error in api_answer: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": f"Failed to process answer: {str(e)}"}), 500


@app.post("/api/next-question")
def api_next_question():
    """
    Get the next question without changing probabilities.
    Used after a wrong guess (penalty already applied).
    """
    if ai is None:
        return jsonify({"error": "AI engine not initialized. Check server logs."}), 500
    
    try:
        state = build_state(allow_guess=True)
        return jsonify(state)
    except Exception as e:
        print(f"Error in api_next_question: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": f"Failed to get next question: {str(e)}"}), 500


@app.post("/api/guess-feedback")
def api_guess_feedback():
    """
    Receive feedback on the last guess.
    Body: { "correct": bool }
    If incorrect, penalize that character so we don't repeat the same wrong guess.
    """
    if ai is None:
        return jsonify({"error": "AI engine not initialized. Check server logs."}), 500
    
    try:
        global last_guess_name

        data = request.get_json(force=True) or {}
        correct = bool(data.get("correct", False))

        if last_guess_name is None:
            return jsonify({"error": "No active guess to score"}), 400

        if correct:
            # Boost the correct character's probability (optional)
            ai.boost_character(last_guess_name, boost_factor=1000.0)
            msg = "Great! I'll remember that."
        else:
            # Strongly penalize the wrong guess and continue
            ai.penalize_wrong_guess(last_guess_name, penalty_factor=0.001)
            msg = "Got it — updating my beliefs and continuing."

        # Clear stored guess
        last_guess_name = None

        return jsonify({"ok": True, "message": msg})
    except Exception as e:
        print(f"Error in api_guess_feedback: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": f"Failed to process feedback: {str(e)}"}), 500


if __name__ == "__main__":
    # Listen on all interfaces to handle both IPv4 and IPv6 connections
    app.run(host="0.0.0.0", port=5000, debug=True)
