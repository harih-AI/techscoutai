# TalentScout – AI Hiring Assistant

## Overview
TalentScout is an AI-powered hiring assistant designed to automate initial candidate screening for technology roles.

## Features
- Context-aware multi-step conversation
- Candidate information collection
- Tech stack–based technical question generation
- Experience-aware difficulty
- Fallback and exit handling

## Architecture
- Streamlit frontend
- Prompt-driven LLM logic
- Session-based context handling
- No persistent storage

## Data Privacy
- No database used
- All data exists only during session
- GDPR-compliant by design

## Run Locally
```bash
pip install -r requirements.txt
export OPENAI_API_KEY="your_key"
streamlit run app.py
```
