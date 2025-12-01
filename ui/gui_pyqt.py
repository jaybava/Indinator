"""
PyQt5 GUI for Indinator with Akinator-style layout.
Run with:  python3 ui/gui_pyqt.py
"""

import sys
from pathlib import Path
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton,
    QVBoxLayout, QHBoxLayout, QMessageBox, QSizePolicy
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

# Make project root importable
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from indinator.ai_engine import AkinatorAI


class IndinatorGUI(QWidget):
    def __init__(self):
        super().__init__()

        # --- Window styling (Akinator-ish) ---
        self.setWindowTitle("Indinator")
        self.setGeometry(200, 200, 950, 550)
        self.setStyleSheet("""
            QWidget {
                background-color: #0d74a6;   /* blue background */
                color: #2b1b17;
                font-family: "Arial";
            }
            QPushButton {
                background-color: #f3b13c;
                border-radius: 10px;
                padding: 8px 16px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #ffc75a;
            }
            QPushButton:disabled {
                background-color: #b8b8b8;
                color: #eeeeee;
            }
        """)

        # --- AI instance ---
        self.ai = AkinatorAI(
            traits_file=str(PROJECT_ROOT / "data" / "traits_flat.json"),
            questions_file=str(PROJECT_ROOT / "data" / "questions.json"),
            characters_file=str(PROJECT_ROOT / "data" / "characters.json"),
            enable_learning=True,
        )

        # --- Game state ---
        self.current_question_idx = None
        self.questions_asked = 0
        self.pending_guess = None
        self.mode = "idle"  # "asking" / "confirming" / "finished"

        # --- Load character images ---
        assets_dir = PROJECT_ROOT / "assets"
        self.pix_happy = QPixmap(str(assets_dir / "char_happy.png"))
        self.pix_worried = QPixmap(str(assets_dir / "char_worried.png"))
        self.pix_thinking = QPixmap(str(assets_dir / "char_thinking.png"))
        self.pix_skeptical = QPixmap(str(assets_dir / "char_skeptical.png"))

        # --- Layout: character on left, speech card on right ---
        root_layout = QHBoxLayout()
        root_layout.setContentsMargins(20, 20, 20, 20)
        root_layout.setSpacing(25)

        # LEFT: character + title
        left_layout = QVBoxLayout()
        left_layout.setSpacing(15)

        self.title_label = QLabel("Indinator")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("""
            QLabel {
                font-size: 28px;
                font-weight: bold;
                color: #ffeecb;
            }
        """)
        left_layout.addWidget(self.title_label)

        self.char_label = QLabel()
        self.char_label.setAlignment(Qt.AlignCenter)
        self.char_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        left_layout.addWidget(self.char_label)

        # RIGHT: speech bubble + buttons + status
        right_layout = QVBoxLayout()
        right_layout.setSpacing(15)

        self.speech_label = QLabel("")
        self.speech_label.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.speech_label.setWordWrap(True)
        self.speech_label.setMargin(20)
        self.speech_label.setStyleSheet("""
            QLabel {
                background-color: #ffe8b0;
                border: 4px solid #c63f3f;
                border-radius: 18px;
                font-size: 18px;
            }
        """)
        self.speech_label.setMinimumHeight(220)
        right_layout.addWidget(self.speech_label)

        # Buttons row
        btn_row = QHBoxLayout()
        btn_row.setSpacing(12)

        self.yes_btn = QPushButton("Yes")
        self.no_btn = QPushButton("No")
        self.skip_btn = QPushButton("Don't Know")

        self.yes_btn.clicked.connect(lambda: self.on_answer(True))
        self.no_btn.clicked.connect(lambda: self.on_answer(False))
        self.skip_btn.clicked.connect(lambda: self.on_answer(None))

        for b in (self.yes_btn, self.no_btn, self.skip_btn):
            b.setFixedWidth(140)
            btn_row.addWidget(b)

        right_layout.addLayout(btn_row)

        # New game button centered
        self.new_game_btn = QPushButton("New Game")
        self.new_game_btn.setFixedWidth(160)
        self.new_game_btn.clicked.connect(self.start_new_game)
        right_layout.addWidget(self.new_game_btn, alignment=Qt.AlignCenter)

        # Status text (small)
        self.status_label = QLabel("Think of a character and click 'New Game'.")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("""
            QLabel {
                font-size: 13px;
                color: #f4f4f4;
            }
        """)
        right_layout.addWidget(self.status_label)

        root_layout.addLayout(left_layout, stretch=3)
        root_layout.addLayout(right_layout, stretch=4)
        self.setLayout(root_layout)

        self.update_button_state(active=False)
        self.set_expression("idle")

    # ------------ Character expression helpers ------------

    def set_expression(self, state: str):
        """
        Change character pose based on game state:
        - "idle" or "success" -> happy
        - "asking" -> thinking
        - "guessing" -> skeptical
        - "error" / wrong -> worried
        """
        if state in ("idle", "success"):
            pix = self.pix_happy
        elif state == "asking":
            pix = self.pix_thinking
        elif state == "guessing":
            pix = self.pix_skeptical
        elif state == "error":
            pix = self.pix_worried
        else:
            pix = self.pix_happy

        if not pix.isNull():
            scaled = pix.scaled(320, 320, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.char_label.setPixmap(scaled)

    # ------------ Game flow ------------

    def start_new_game(self):
        self.ai.reset()
        self.mode = "asking"
        self.questions_asked = 0
        self.pending_guess = None

        self.status_label.setText("Game started! Answer truthfully 🙂")
        self.speech_label.setText("I'm ready. Let's begin…")
        self.update_button_state(True)
        self.set_expression("asking")
        self.next_question()

    def update_button_state(self, active: bool):
        for b in (self.yes_btn, self.no_btn, self.skip_btn):
            b.setEnabled(active)

    def next_question(self):
        q_idx = self.ai.select_best_question(focus_top_n=10)
        if q_idx is None:
            self.make_guess()
            return

        self.current_question_idx = q_idx
        question = self.ai.questions[q_idx]["question"]
        self.speech_label.setText(f"❓ {question}")
        self.mode = "asking"
        self.set_expression("asking")

    def compute_threshold(self) -> float:
        q = self.questions_asked
        if q <= 5:
            return 0.75
        elif q <= 12:
            return 0.65
        elif q <= 18:
            return 0.55
        return 0.45

    def on_answer(self, ans):
        if self.mode == "asking":
            self.handle_question_answer(ans)
        elif self.mode == "confirming":
            self.handle_guess_confirmation(ans)
        elif self.mode == "finished":
            QMessageBox.information(self, "Indinator",
                                    "Game over. Click 'New Game' to play again.")

    def handle_question_answer(self, ans):
        if self.current_question_idx is None:
            return

        self.questions_asked += 1

        if ans is not None:
            self.ai.update_probabilities(self.current_question_idx, bool(ans))
            self.status_label.setText(f"Questions asked: {self.questions_asked}")
        else:
            self.status_label.setText(
                f"Skipped. Questions asked: {self.questions_asked}"
            )

        threshold = self.compute_threshold()
        if self.ai.should_make_guess(threshold=threshold):
            self.make_guess()
        else:
            self.next_question()

    def make_guess(self):
        character, prob = self.ai.get_best_guess()
        self.pending_guess = (character, prob)
        self.mode = "confirming"
        self.set_expression("guessing")

        percent = prob * 100
        self.speech_label.setText(
            f"🤔 I think your character is…\n\n"
            f"👉 {character}\n\n"
            f"(Confidence: {percent:.1f}%)\n\n"
            f"Am I right?"
        )
        self.status_label.setText("Confirm my guess with Yes / No / Don't know.")

    def handle_guess_confirmation(self, ans):
        if not self.pending_guess:
            return

        character, prob = self.pending_guess

        if ans is True:
            self.set_expression("success")
            QMessageBox.information(
                self, "Got it!",
                f"🎉 I guessed your character: {character}\n"
                f"In {self.questions_asked} questions."
            )
            self.finish_game()
            return

        if ans is False:
            # Penalize wrong guess lightly and try again
            try:
                self.ai.penalize_wrong_guess(character, penalty_factor=0.001)
            except Exception:
                pass

            self.set_expression("error")
            self.status_label.setText("Hmm, I was wrong. Let me think again…")

            if self.questions_asked >= 25:
                self.make_guess()
            else:
                self.next_question()
            return

        # Don't know / skip on guess
        self.status_label.setText("Okay, let's ask a few more questions.")
        self.set_expression("asking")
        self.next_question()

    def finish_game(self):
        self.mode = "finished"
        self.update_button_state(False)
        self.speech_label.setText(
            "That was fun! Click 'New Game' if you want to play again."
        )
        self.status_label.setText("Game finished.")


def main():
    app = QApplication(sys.argv)
    gui = IndinatorGUI()
    gui.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
