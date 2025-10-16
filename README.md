# Akinator-Style Bayesian Guessing Game

## Problem Statement
Build a 20Q-style engine that guesses a fictional character by asking informative yes/no/probably questions.  
Core ML: Bayesian posterior updates, info-gain question selection, online learning (Beta updates).

## Quickstart
```bash
# 1) create env
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# 2) validate starter data
python tools/validate_kb.py

# 3) run CLI demo
python ui/cli.py

# 4) run Streamlit app
streamlit run ui/app_streamlit.py