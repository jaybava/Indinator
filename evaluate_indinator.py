"""
Evaluation script for Ind-inator.

Simulates games in two modes:

1. ideal: perfect yes/no answers based on the target character's traits
2. human: "human-like" graded answers (Yes / Probably Yes / Maybe /
          Probably No / No) with some randomness

Outputs:
  - results/evaluation_results_ideal.csv
  - results/evaluation_results_human.csv
  - results/questions_distribution_ideal.png
  - results/accuracy_ideal.png
  - results/questions_distribution_human.png
  - results/accuracy_human.png
"""

from pathlib import Path
import csv
import random
import matplotlib.pyplot as plt
from indinator import AkinatorAI


# ==================== CONFIG ====================

NUM_GAMES = None            # number of games to simulate (set None to use all chars)
MAX_QUESTIONS = 25        # hard cap on questions per game
CONFIDENCE_THRESHOLD = 0.85


# ==================== UTILITIES ====================

"""
Generates a graded human-like answer code for a single trait.
Encodes skewed probabilities so "true" traits lean toward Yes/Probably Yes,
and absent traits lean toward No/Probably No, introducing variability versus
a perfect binary oracle.
"""
def sample_human_like_answer(has_trait: bool) -> int:
    """
    Sample a graded answer code in {-2,-1,0,1,2} that *roughly* mimics
    a human:

        2  -> Yes
        1  -> Probably Yes
        0  -> Maybe
       -1  -> Probably No
       -2  -> No

    When the character *has* the trait, Yes/Probably Yes are more likely.
    When the character *doesn't* have the trait, No/Probably No are more likely.
    """
    # Probabilities are deliberately asymmetric to bias toward the "true" side.
    if has_trait:
        codes   = [2, 1, 0, -1, -2]          # Yes, ProbYes, Maybe, ProbNo, No
        weights = [0.55, 0.25, 0.15, 0.03, 0.02]
    else:
        codes   = [2, 1, 0, -1, -2]
        weights = [0.02, 0.03, 0.15, 0.25, 0.55]

    return random.choices(codes, weights, k=1)[0]


"""
Turns the numeric graded code into a readable label that makes CSV output or
debug printing clearer, without changing the scoring.
"""
def code_to_label(code: int) -> str:
    """Convert numeric code to a human-readable label (for CSV/debug)."""
    mapping = {
        2: "Yes",
        1: "Probably Yes",
        0: "Maybe",
        -1: "Probably No",
        -2: "No",
    }
    return mapping.get(code, "Unknown")


# ==================== SIMULATION MODES ====================

"""
Simulates a game where answers are perfectly aligned to the target's traits.
This is the upper-bound performance benchmark since every reply is "correct"
with no randomness.
"""
def simulate_game_ideal(ai: AkinatorAI, target_char: str) -> dict:
    """
    Perfect oracle: answers Yes if the target has the trait, else No.
    """
    ai.reset()

    target_traits = ai.traits[target_char]   # dict[trait_name] -> 0/1
    num_questions = 0
    prob_trace = []

    for _ in range(MAX_QUESTIONS):
        q_idx = ai.select_best_question()
        if q_idx is None:
            break

        question = ai.questions[q_idx]
        trait = question.get("trait", "")

        has_trait = target_traits.get(trait, 0) == 1
        user_answer_bool = bool(has_trait)

        ai.update_probabilities(q_idx, user_answer=user_answer_bool)

        num_questions += 1
        prob_trace.append(max(ai.probabilities))

        if ai.should_make_guess(threshold=CONFIDENCE_THRESHOLD):
            guess, final_prob = ai.get_best_guess()
            return {
                "target": target_char,
                "guess": guess,
                "correct": guess == target_char,
                "questions": num_questions,
                "final_prob": final_prob,
                "prob_trace": prob_trace,
                "mode": "ideal",
            }

    guess, final_prob = ai.get_best_guess()
    return {
        "target": target_char,
        "guess": guess,
        "correct": guess == target_char,
        "questions": num_questions,
        "final_prob": final_prob,
        "prob_trace": prob_trace,
        "mode": "ideal",
    }


"""
Simulates a noisy human by sampling graded answers, then translating them into
yes/no/skip for the binary update API. This exposes the model to uncertainty
while still measuring how quickly it can guess.
"""
def simulate_game_human_like(ai: AkinatorAI, target_char: str) -> dict:
    """
    Human-like oracle: samples graded answers
    (Yes / Probably Yes / Maybe / Probably No / No),
    but internally maps them to yes-like / no-like / skip
    for the existing boolean-based update_probabilities API.
    """
    ai.reset()

    target_traits = ai.traits[target_char]
    num_questions = 0
    prob_trace = []

    for _ in range(MAX_QUESTIONS):
        q_idx = ai.select_best_question()
        if q_idx is None:
            break

        question = ai.questions[q_idx]
        trait = question.get("trait", "")

        has_trait = target_traits.get(trait, 0) == 1

        # Sample a graded answer code in {-2,-1,0,1,2}
        answer_code = sample_human_like_answer(has_trait)
        answer_label = code_to_label(answer_code)

        # Map graded answer → behaviour for the engine:
        #   >0 : yes-like     → user_answer = True
        #   <0 : no-like      → user_answer = False
        #    0 : "Maybe"      → skip update (but still counts as a question)
        if answer_code > 0:
            # Yes / Probably Yes
            user_answer_bool = True
            ai.update_probabilities(q_idx, user_answer=user_answer_bool)
        elif answer_code < 0:
            # No / Probably No
            user_answer_bool = False
            ai.update_probabilities(q_idx, user_answer=user_answer_bool)
        else:
            # Maybe → no update, but the AI still "used up" a question
            pass

        num_questions += 1
        prob_trace.append(max(ai.probabilities))

        if ai.should_make_guess(threshold=CONFIDENCE_THRESHOLD):
            guess, final_prob = ai.get_best_guess()
            return {
                "target": target_char,
                "guess": guess,
                "correct": guess == target_char,
                "questions": num_questions,
                "final_prob": final_prob,
                "prob_trace": prob_trace,
                "mode": "human",
                # optional: last_answer=answer_label,
            }

    guess, final_prob = ai.get_best_guess()
    return {
        "target": target_char,
        "guess": guess,
        "correct": guess == target_char,
        "questions": num_questions,
        "final_prob": final_prob,
        "prob_trace": prob_trace,
        "mode": "human",
    }

# ==================== RUN + PLOTS ====================

"""
Drives a batch of simulated games for a given mode, logs aggregate stats,
persists the per-game results, and emits simple plots for question counts and
accuracy to compare modes visually.
"""
def run_experiments(mode: str, results_path_prefix: str):
    """
    mode: "ideal" or "human"
    results_path_prefix: e.g. "evaluation_results_ideal"
    """
    root = Path(__file__).resolve().parent
    data_dir = root / "data"

    traits_file = data_dir / "traits_flat.json"
    questions_file = data_dir / "questions.json"
    characters_file = data_dir / "characters.json"

    ai = AkinatorAI(
        traits_file=str(traits_file),
        questions_file=str(questions_file),
        characters_file=str(characters_file),
        enable_learning=False,
    )

    characters = ai.characters[:]  # list of character names

    if NUM_GAMES is None or NUM_GAMES >= len(characters):
        targets = characters
    else:
        targets = random.sample(characters, NUM_GAMES)  # sample to keep runs quick

    print(f"\n=== Running {mode.upper()} mode on {len(targets)} games ===")

    results = []
    for i, target in enumerate(targets, start=1):
        if mode == "ideal":
            res = simulate_game_ideal(ai, target)
        else:
            res = simulate_game_human_like(ai, target)

        results.append(res)
        print(
            f"[{i}/{len(targets)}] Target: {res['target']:<20} "
            f"Guess: {res['guess']:<20} "
            f"Correct: {res['correct']}  "
            f"Questions: {res['questions']}"
        )

    # Aggregate stats for logs and plots
    n = len(results)
    num_correct = sum(1 for r in results if r["correct"])
    accuracy = num_correct / n if n > 0 else 0.0
    avg_questions = sum(r["questions"] for r in results) / n if n > 0 else 0.0

    print(f"\n[{mode}] Games: {n}")
    print(f"[{mode}] Correct: {num_correct}")
    print(f"[{mode}] Accuracy: {accuracy * 100:.2f}%")
    print(f"[{mode}] Avg questions: {avg_questions:.2f}")

    # Save CSV for later analysis / plotting
    csv_path = root / f"{results_path_prefix}.csv"
    fieldnames = ["target", "guess", "correct", "questions", "final_prob", "mode"]
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(results)

    print(f"[{mode}] Saved results to {csv_path}")

    # Plots
    questions_list = [r["questions"] for r in results]
    correct_count = num_correct
    incorrect_count = n - num_correct

    # Histogram of questions
    plt.figure(figsize=(6, 4))
    plt.hist(questions_list, bins=10)
    plt.xlabel("Number of Questions")
    plt.ylabel("Frequency")
    plt.title(f"Questions per Game ({mode} responses)")
    # Show the average questions as a vertical marker to give quick context.
    plt.axvline(avg_questions, color="red", linestyle="--", linewidth=1)
    ylim = plt.ylim()
    plt.text(
        avg_questions,
        ylim[1] * 0.9,
        f"Avg: {avg_questions:.2f}",
        color="red",
        ha="center",
    )
    plt.tight_layout()
    hist_path = root / f"results/questions_distribution_{mode}.png"
    plt.savefig(hist_path, dpi=200)
    plt.close()
    print(f"[{mode}] Saved histogram to {hist_path}")

    # Violin plot for distribution shape
    plt.figure(figsize=(6, 4))
    plt.violinplot(questions_list, showmeans=True, showextrema=True)
    plt.ylabel("Number of Questions")
    plt.title(f"Question Count Distribution ({mode} responses)")
    plt.xticks([1], ["All games"])
    plt.tight_layout()
    violin_path = root / f"results/questions_violin_{mode}.png"
    plt.savefig(violin_path, dpi=200)
    plt.close()
    print(f"[{mode}] Saved violin plot to {violin_path}")

    # Accuracy bar chart
    plt.figure(figsize=(6, 4))
    plt.bar(["Correct", "Incorrect"], [correct_count, incorrect_count])
    plt.xlabel("Outcome")
    plt.ylabel("Count")
    plt.title(f"Guess Accuracy ({mode} responses)")
    # Add a caption with overall accuracy and average questions for quick reading.
    y_max = max(correct_count, incorrect_count)
    plt.text(
        0.5,
        y_max * 0.85 if y_max > 0 else 0.1,
        f"Accuracy: {accuracy * 100:.1f}%\nAvg Q: {avg_questions:.2f}",
        ha="center",
    )
    plt.tight_layout()
    acc_path = root / f"results/accuracy_{mode}.png"
    plt.savefig(acc_path, dpi=200)
    plt.close()
    print(f"[{mode}] Saved accuracy plot to {acc_path}")

    # Probability convergence curve (average of top probability across questions)
    prob_traces = [r.get("prob_trace", []) for r in results if r.get("prob_trace")]
    if prob_traces:
        max_len = max(len(t) for t in prob_traces)
        avg_curve = []
        for i in range(max_len):
            vals = [t[i] for t in prob_traces if len(t) > i]
            avg_curve.append(sum(vals) / len(vals))

        plt.figure(figsize=(7, 4))
        plt.plot(range(1, len(avg_curve) + 1), avg_curve, marker="o")
        plt.xlabel("Question #")
        plt.ylabel("Avg top probability")
        plt.ylim(0, 1.05)
        plt.title(f"Probability Convergence ({mode} responses)")
        plt.grid(alpha=0.3)
        plt.tight_layout()
        prob_path = root / f"results/probability_convergence_{mode}.png"
        plt.savefig(prob_path, dpi=200)
        plt.close()
        print(f"[{mode}] Saved probability convergence curve to {prob_path}")

    # Confusion matrix for wrong guesses
    wrong_pairs = [(r["target"], r["guess"]) for r in results if not r["correct"]]
    if wrong_pairs:
        actual_labels = sorted({a for a, _ in wrong_pairs})
        guess_labels = sorted({g for _, g in wrong_pairs})
        actual_idx = {a: i for i, a in enumerate(actual_labels)}
        guess_idx = {g: j for j, g in enumerate(guess_labels)}

        matrix = [[0 for _ in guess_labels] for _ in actual_labels]
        for actual, guess in wrong_pairs:
            matrix[actual_idx[actual]][guess_idx[guess]] += 1

        plt.figure(figsize=(max(6, len(guess_labels) * 0.4), max(4, len(actual_labels) * 0.4)))
        plt.imshow(matrix, cmap="Blues")
        plt.colorbar(label="Count")
        plt.xticks(range(len(guess_labels)), guess_labels, rotation=45, ha="right")
        plt.yticks(range(len(actual_labels)), actual_labels)
        plt.xlabel("Guessed")
        plt.ylabel("Actual")
        plt.title(f"Confusion Matrix of Wrong Guesses ({mode} responses)")
        plt.tight_layout()
        cm_path = root / f"results/confusion_matrix_wrong_{mode}.png"
        plt.savefig(cm_path, dpi=200)
        plt.close()
        print(f"[{mode}] Saved confusion matrix to {cm_path}")


"""
Entry point that runs both modes back-to-back so their metrics and plots are
produced in a single invocation.
"""
def main():
    # Run both modes so you can compare ideal vs human-like.
    run_experiments(mode="ideal",  results_path_prefix="results/evaluation_results_ideal")
    run_experiments(mode="human",  results_path_prefix="results/evaluation_results_human")


if __name__ == "__main__":
    main()
