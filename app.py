import streamlit as st
import time
import os
from dotenv import load_dotenv

# Try to load .env, but don't crash if encoding is weird (common on Windows)
try:
    load_dotenv()
except Exception:
    pass

from core.state import init_state
from core.logic import generate_questions
from core.llm import call_llm

from core.prompts import *
from utils.validators import is_exit, is_valid

# --- UI Config ---
st.set_page_config(page_title="TalentScout AI", page_icon="🤖", layout="centered")

# Custom CSS for "Premium" look
st.markdown("""
    <style>
    .stApp {
        background-color: #0E1117;
        color: #FAFAFA;
    }
    .stTextInput > div > div > input {
        background-color: #262730;
        color: #FAFAFA;
    }
    .main-header {
        font-family: 'Helvetica Neue', sans-serif;
        font-weight: 700;
        color: #4F8BF9;
        text-align: center;
        margin-bottom: 2rem;
    }
    .chat-bubble {
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
    }
    .ai-bubble {
        background-color: #1E232F;
        border-left: 4px solid #4F8BF9;
    }
    .user-bubble {
        background-color: #2C333F;
        border-right: 4px solid #00C853;
        text-align: right;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='main-header'>🤖 TalentScout AI</h1>", unsafe_allow_html=True)

init_state(st)

# Progress Bar
# --- Chat Logic & UI ---

if "history" not in st.session_state:
    st.session_state.history = []

def display_chat():
    for role, text in st.session_state.history:
        with st.chat_message(role):
            st.markdown(text)

def add_message(role, text):
    st.session_state.history.append((role, text))
    with st.chat_message(role):
        st.markdown(text)

stage = st.session_state.get("stage", 0)
profile = st.session_state.profile

# --- Logic to Determine Current Question ---
current_question = ""
if stage == 0:
    current_question = "**Hello! I'm TalentScout.**\n\nI'm here to find your perfect tech role.\n\nFirst, what is your **full name**?"
elif stage == 1:
    current_question = f"Nice to meet you, **{profile.get('name', 'candidate')}**.\n\nWhat is your **email address**?"
elif stage == 2:
    current_question = "Got it.\n\nCould you please share your **phone number**?"
elif stage == 3:
    current_question = "Thanks.\n\nHow many **years of experience** do you have in the tech industry?"
elif stage == 4:
    current_question = "Understood.\n\nWhat specific **position(s)** are you interested in applying for?"
elif stage == 5:
    current_question = "Noted.\n\nWhat is your **current location**?"
elif stage == 6:
    current_question = "Great. Now for the technical part.\n\nPlease list your **Tech Stack** (languages, frameworks, tools), separated by commas."
elif stage == 7:
    idx = st.session_state.current_tech
    if "questions" in st.session_state and idx < len(st.session_state.questions):
        tech, qs = st.session_state.questions[idx]
        current_question = f"**Technical Challenge: {tech}**\n\n{qs}\n\n*Please type your answer below.*"
    else:
        pass

# Display all history FIRST
display_chat()

# Ensure the assistant asks the question for the current stage
if (not st.session_state.history or st.session_state.history[-1][0] == "user") and current_question:
    add_message("assistant", current_question)

# --- Input Handling ---
if prompt := st.chat_input("Type your answer here..."):
    # 1. User Message
    add_message("user", prompt)
    
    # Check Exit
    if is_exit(prompt):
        with st.spinner("Closing..."):
            msg = call_llm(SYSTEM_PROMPT, CLOSING_PROMPT)
        add_message("assistant", msg)
        st.stop()
        
    # 2. Process Input based on Stage
    valid = False
    
    if stage == 0:
        if is_valid(prompt):
            profile["name"] = prompt
            valid = True
    elif stage == 1:
        if is_valid(prompt):
            profile["email"] = prompt
            valid = True
    elif stage == 2:
        if is_valid(prompt):
            profile["phone"] = prompt
            valid = True
    elif stage == 3:
        if is_valid(prompt):
            profile["experience"] = prompt
            valid = True
    elif stage == 4:
        if is_valid(prompt):
            profile["position"] = prompt
            valid = True
    elif stage == 5:
        if is_valid(prompt):
            profile["location"] = prompt
            valid = True
    elif stage == 6:
        if is_valid(prompt):
            profile["tech_stack"] = [t.strip().title() for t in prompt.split(",")]
            # Generate Questions
            with st.spinner("Analyzing profile..."):
                try:
                    st.session_state.questions = generate_questions(profile["tech_stack"], profile["experience"])
                    valid = True
                except Exception as e:
                    add_message("assistant", f"Error generating questions: {e}")
                    valid = False
    elif stage == 7:
        # Answer to technical question
        if "responses" not in st.session_state:
            st.session_state.responses = []
        st.session_state.responses.append(prompt)
        
        st.session_state.current_tech += 1
        if st.session_state.current_tech >= len(st.session_state.questions):
           st.session_state.stage += 1 # Move to closing
           st.rerun()
        else:
           # Stay in stage 7 but next question will render on rerun
           st.rerun()
        # Implicitly valid for tech questions
        valid = False # We handled the move manually, don't auto-increment stage
        
    # 3. Transition
    if valid:
        st.session_state.stage += 1
        st.rerun()

    # 4. Fallback if invalid and not stage 7 special case
    if not valid and stage != 7:
         fallback_msg = call_llm(SYSTEM_PROMPT, FALLBACK_PROMPT)
         add_message("assistant", fallback_msg)

# Closing logic
if stage > 7:
    if "analysis" not in st.session_state:
        # Perform analysis appropriately but do not display it to the user if per instructions "Do not evaluate"
        # We can enable it for our internal log or if explicitly requested.
        # For strict compliance, we will just close.
        pass
            
    final_msg = call_llm(SYSTEM_PROMPT, CLOSING_PROMPT)
    # We only show the final message once
    if not st.session_state.get("closed", False):
         add_message("assistant", final_msg)
         st.session_state.closed = True
