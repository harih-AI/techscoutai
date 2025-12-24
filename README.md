# 🤖 TalentScout – AI Hiring Assistant

![Python](https://img.shields.io/badge/Python-3.9%2B-blue?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4-412991?style=for-the-badge&logo=openai&logoColor=white)

## 🚀 Overview
**TalentScout** is a cutting-edge, AI-powered hiring assistant designed to revolutionize initial candidate screening. By leveraging advanced LLMs, it conducts natural, context-aware interviews for technology roles, saving recruiters time while providing candidates with an engaging first touchpoint.

## ✨ Key Features

### 🧠 Context-Aware Conversations
Instead of rigid forms, TalentScout engages in **multi-step, natural dialogue**. It remembers context, handles interruptions smoothly, and guides the candidate through the screening process just like a human recruiter would.

### 📝 Smart Information Collection
Effortlessly captures essential candidate details without feeling like an interrogation:
- **Personal Profile**: Name, Email, Phone
- **Professional Background**: Years of Experience, Current Location
- **Career Goals**: Desired Position & Roles

### 💻 Dynamic Technical Challenge
TalentScout doesn't just ask generic questions. It dynamically generates **tech stack–specific questions** based on the candidate's actual expertise.
- **Adaptive Difficulty**: Questions scale in complexity based on the candidate's years of experience.
- **Scenario-Based**: Focuses on real-world problem solving rather than textbook definitions.

### 🛡️ Robust Fail-Safe Logic
- **Input Validation**: Intelligently handles unclear or invalid inputs by politely asking for clarification.
- **Graceful Exits**: Detects when a candidate wants to end the interview and closes with a professional summary.

---

## 🏗️ Architecture

Built for speed, simplicity, and privacy.

- **Frontend**: [Streamlit](https://streamlit.io/) for a responsive, interactive chat interface.
- **Core Logic**: Prompt-engineered system using OpenAI's GPT models for reasoning.
- **State Management**: Session-state based context handling ensures a smooth flow without complex database dependencies.

## 🔒 Data Privacy & Security

We prioritize candidate privacy by design.
- **No Persistent Storage**: No database is used. All conversation data exists only for the duration of the session.
- **Transient Memory**: Once the tab is closed, all data is wiped, making it inherently GDPR-compliant for initial screenings.

---

## 🛠️ Run Locally

Get TalentScout up and running in minutes.

1. **Clone the repository**
   ```bash
   git clone https://github.com/harih-AI/techscoutai.git
   cd techscoutai
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Environment**
   ```bash
   # Linux/Mac
   export OPENAI_API_KEY="your_api_key_here"
   
   # Windows (PowerShell)
   $env:OPENAI_API_KEY="your_api_key_here"
   ```

4. **Launch the App**
   ```bash
   streamlit run app.py
   ```

---

