import streamlit as st

st.set_page_config(page_title="Game Coder", page_icon="🎮")

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;800;900&display=swap');
    .stApp { background: linear-gradient(135deg, #a1c4fd 0%, #c2e9fb 50%, #fbc2eb 100%); }
    .stApp, .stApp p, .stApp div, .stApp span { font-family: 'Poppins', sans-serif !important; color: #1f2a44; }

    .stApp .huge-title, .stApp .huge-title * {
        text-align: center !important; font-size: 84px !important; font-weight: 900 !important;
        line-height: 1.1 !important; color: #2b1b6b !important;
        text-shadow: 3px 3px 0 rgba(255,255,255,0.7); margin: 10px 0 8px 0 !important;
    }
    @media (max-width: 640px) { .stApp .huge-title, .stApp .huge-title * { font-size: 52px !important; } }
    .subtitle { text-align: center; font-size: 22px; margin-bottom: 30px; }

    div.stButton > button {
        background: linear-gradient(90deg, #ff7eb3, #7a5cff); border: none; border-radius: 24px;
        padding: 28px 10px; box-shadow: 0 8px 18px rgba(122,92,255,0.35); transition: transform 0.15s ease;
    }
    div.stButton > button p { color: white !important; font-size: 26px !important; font-weight: 800; }
    div.stButton > button:hover { transform: scale(1.05); }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="huge-title">🎮 Game Coder</div>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Pick a game and have fun!</p>', unsafe_allow_html=True)

# One button per game. To add a new game later: add a file in pages/ and a line here.
games = [
    ("🎯 Number Guessing", "pages/1_Number_Guessing.py"),
    ("🕵️ Hangman", "pages/2_Hangman.py"),
]

for label, page in games:
    left, middle, right = st.columns([1, 3, 1])
    with middle:
        if st.button(label, use_container_width=True):
            st.switch_page(page)
