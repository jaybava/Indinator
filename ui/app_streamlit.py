import streamlit as st
from indinator.kb_store import KBStore
from indinator.engine import Engine
from indinator.selection import select_next_question
from indinator.config import ANSWER_SET, MAX_QUESTIONS

kb = KBStore("data/questions.json", "data/entities.json", "data/kb.json")
if "engine" not in st.session_state:
    st.session_state.engine = Engine(kb.all_entities(), kb.all_questions(), kb.likelihood)

st.title("indinator-Style Guessing (Bayesian)")
eng = st.session_state.engine

if st.button("Reset"):
    eng.reset()

remaining = [q for q in kb.all_questions() if q not in eng.asked]
q_id = remaining[0] if not eng.asked else select_next_question(eng.pi, eng.entities, remaining, kb.likelihood)

st.subheader(f"Question: {q_id}")
cols = st.columns(len(ANSWER_SET))
for i, a in enumerate(ANSWER_SET):
    if cols[i].button(a.capitalize()):
        eng.update(q_id, a)

st.write("Top-5:")
for e, p in eng.top_k(5):
    st.write(f"- {e}: {p:.3f}")

t = len(eng.asked)
if eng.should_guess(t):
    e, p = eng.guess()
    st.success(f"Guess: **{e}** with confidence {p:.2f}")
