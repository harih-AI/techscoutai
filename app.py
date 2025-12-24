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
from core.logic import generate_questions, validate_answer, clean_tech_stack, extract_info_with_llm
from core.llm import call_llm

from core.prompts import *
from utils.validators import is_exit, is_valid, is_valid_email, is_valid_phone, extract_years
from utils.style_utils import inject_premium_css, render_sidebar_profile, render_message

# --- UI Config ---
st.set_page_config(page_title="TalentScout Pro", page_icon="🤖", layout="wide")

# Inject Global Premium CSS
inject_premium_css()

# Render Sidebar with Live Profile Card
render_sidebar_profile(st.session_state.get("profile", {}), st.session_state.get("stage", 0))

# Main Content Area
st.markdown("<h1 class='main-header neon-text-cyan'>🤖 TalentScout Pro AI</h1>", unsafe_allow_html=True)

init_state(st)

# Progress Bar
# --- Chat Logic & UI ---

if "history" not in st.session_state:
    st.session_state.history = []

def display_chat():
    for role, text in st.session_state.history:
        render_message(role, text)

def add_message(role, text):
    st.session_state.history.append((role, text))
    render_message(role, text)

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
        if is_valid_email(prompt):
            profile["email"] = prompt.strip()
            valid = True
        else:
            # Attempt LLM extraction for conversational input
            extracted = extract_info_with_llm("The user's email address", prompt)
            if extracted and is_valid_email(extracted):
                profile["email"] = extracted
                valid = True
            else:
                add_message("assistant", "That doesn't look like a valid email. Please share a valid email address (e.g., name@example.com).")
                valid = False
    elif stage == 2:
        if is_valid_phone(prompt):
            profile["phone"] = prompt.strip()
            valid = True
        else:
            extracted = extract_info_with_llm("The user's phone number", prompt)
            if extracted and is_valid_phone(extracted):
                profile["phone"] = extracted
                valid = True
            else:
                add_message("assistant", "Could you please provide a valid phone number? (Include country code if possible).")
                valid = False
    elif stage == 3:
        years = extract_years(prompt)
        if years:
            profile["experience"] = years
            valid = True
        else:
            extracted = extract_info_with_llm("Years of experience (number only)", prompt)
            if extracted and extracted.isdigit():
                profile["experience"] = extracted
                valid = True
            else:
                add_message("assistant", "Please specify your years of experience as a number (e.g., '5' or '3 years').")
                valid = False
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
            profile["tech_stack"] = clean_tech_stack(prompt)
            if not profile["tech_stack"]:
                add_message("assistant", "I couldn't identify any technologies in your input. Please list them separated by commas.")
                valid = False
            else:
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
        
        current_idx = st.session_state.current_tech
        tech, question = st.session_state.questions[current_idx]
        
        # 1. Validate Answer
        with st.spinner("Evaluating..."):
            feedback = validate_answer(tech, question, prompt)
        
        # 2. Add feedback to history so candidate sees it
        add_message("assistant", feedback)
        
        # 3. Store response
        st.session_state.responses.append({"question": question, "answer": prompt, "feedback": feedback})
        
        # 4. Move to next
        st.session_state.current_tech += 1
        time.sleep(1) # Tiny pause for UX
        
        if st.session_state.current_tech >= len(st.session_state.questions):
           st.session_state.stage += 1 # Move to closing
           st.rerun()
        else:
           # Stay in stage 7 but next question will render on rerun
           st.rerun()
        # Implicitly valid for tech questions flow control
        valid = False 
        
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
