import streamlit as st

def inject_premium_css():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap');

        /* Global Overrides */
        .stApp {
            background: radial-gradient(circle at top right, #1a1c2c, #0b0f19);
            color: #FAFAFA;
            font-family: 'Outfit', sans-serif;
        }

        /* Glassmorphism Sidebar */
        [data-testid="stSidebar"] {
            background-color: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(15px);
            border-right: 1px solid rgba(255, 255, 255, 0.1);
        }

        /* Glass Card Utility */
        .glass-card {
            background: rgba(255, 255, 255, 0.05);
            border-radius: 15px;
            padding: 20px;
            border: 1px solid rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
            margin-bottom: 15px;
        }

        /* Neon Text/Accents */
        .neon-text-cyan { color: #00F2FF; text-shadow: 0 0 10px rgba(0, 242, 255, 0.5); }
        .neon-text-green { color: #39FF14; text-shadow: 0 0 10px rgba(57, 255, 20, 0.5); }
        
        .stProgress > div > div > div {
            background: linear-gradient(90deg, #00F2FF, #4F8BF9);
        }

        /* Premium Chat Bubbles */
        .chat-bubble-container {
            display: flex;
            margin-bottom: 20px;
            animation: fadeIn 0.5s ease-in-out;
        }
        
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .bubble {
            max-width: 80%;
            padding: 15px 20px;
            border-radius: 20px;
            font-size: 1rem;
            line-height: 1.5;
            position: relative;
        }

        .ai-bubble-v2 {
            background: rgba(79, 139, 249, 0.15);
            border: 1px solid rgba(79, 139, 249, 0.3);
            color: #E0E7FF;
            border-bottom-left-radius: 5px;
        }

        .user-bubble-v2 {
            background: rgba(57, 255, 20, 0.1);
            border: 1px solid rgba(57, 255, 20, 0.2);
            color: #DCFCE7;
            border-bottom-right-radius: 5px;
            margin-left: auto;
        }
        
        /* Floating Input Area */
        .stChatInput {
            border-radius: 30px !important;
            background: rgba(255, 255, 255, 0.05) !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            backdrop-filter: blur(10px);
        }

        /* Hide default Streamlit elements for cleaner look */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        </style>
    """, unsafe_allow_html=True)

def render_sidebar_profile(profile, stage):
    with st.sidebar:
        st.markdown("<h2 class='neon-text-cyan'>⚡ TalentScout Pro</h2>", unsafe_allow_html=True)
        
        # Progress
        progress_per = (stage / 8)
        st.write(f"**Interview Progress**: {int(progress_per*100)}%")
        st.progress(progress_per)
        
        st.markdown("---")
        
        st.markdown("### 👤 Profile Summary")
        with st.container():
            st.markdown(f"""
            <div class="glass-card">
                <p><b>Name:</b> {profile.get('name') or '---'}</p>
                <p><b>Email:</b> {profile.get('email') or '---'}</p>
                <p><b>Experience:</b> {profile.get('experience') or '---'} yrs</p>
                <p><b>Role:</b> {profile.get('position') or '---'}</p>
            </div>
            """, unsafe_allow_html=True)
            
        if profile.get('tech_stack'):
            st.markdown("### 🛠️ Tech Stack")
            tech_html = "".join([f"<span style='background:rgba(0,242,255,0.1); border:1px solid #00F2FF; border-radius:15px; padding:2px 10px; margin:3px; display:inline-block; font-size:0.8rem;'>{t}</span>" for t in profile['tech_stack']])
            st.markdown(f"<div>{tech_html}</div>", unsafe_allow_html=True)

def render_message(role, text):
    if role == "assistant":
        st.markdown(f"""
            <div class="chat-bubble-container">
                <div class="bubble ai-bubble-v2">{text}</div>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
            <div class="chat-bubble-container">
                <div class="bubble user-bubble-v2">{text}</div>
            </div>
        """, unsafe_allow_html=True)
