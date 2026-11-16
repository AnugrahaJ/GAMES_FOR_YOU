import random
import streamlit as st
from words_list import animals, countries, fruits_vegetables
from sounds import play_sound

st.set_page_config(page_title="Hangman", page_icon="🕵️")

categories = {
    "🐾 Animals": animals,
    "🌍 Countries": countries,
    "🍎 Fruits & Vegetables": fruits_vegetables,
}
max_wrong = 6

# ---------- Styling ----------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;800;900&display=swap');
    .stApp { background: linear-gradient(135deg, #a1c4fd 0%, #c2e9fb 50%, #fbc2eb 100%); }
    .stApp, .stApp p, .stApp div, .stApp span { font-family: 'Poppins', sans-serif !important; color: #1f2a44; }

    .stApp .huge-title, .stApp .huge-title * {
        text-align: center !important; font-size: 72px !important; font-weight: 900 !important;
        line-height: 1.1 !important; color: #2b1b6b !important;
        text-shadow: 3px 3px 0 rgba(255,255,255,0.7); margin: 6px 0 12px 0 !important;
    }
    @media (max-width: 640px) { .stApp .huge-title, .stApp .huge-title * { font-size: 48px !important; } }
    .center { text-align: center; }

    /* Big buttons (categories, play again) */
    div.stButton > button {
        background: linear-gradient(90deg, #ff7eb3, #7a5cff); border: none; border-radius: 24px;
        padding: 14px 10px; box-shadow: 0 6px 14px rgba(122,92,255,0.35); transition: transform 0.15s ease;
    }
    div.stButton > button p { color: white !important; font-size: 20px !important; font-weight: 700; }
    div.stButton > button:hover { transform: scale(1.05); }

    /* Keyboard buttons: smaller, round tiles */
    .st-key-keyboard div.stButton > button {
        padding: 6px 0; border-radius: 12px; min-height: 46px;
        background: linear-gradient(135deg, #7a5cff, #ff7eb3);
    }
    .st-key-keyboard div.stButton > button p { font-size: 20px !important; font-weight: 800; }
    .st-key-keyboard div.stButton > button:disabled { background: #c9c9d6; box-shadow: none; }
    .st-key-keyboard div.stButton > button:disabled p { color: #7c7c8a !important; }
    .st-key-keyboard [data-testid="stHorizontalBlock"] { gap: 6px; flex-wrap: nowrap; }
    .st-key-keyboard [data-testid="stColumn"] { min-width: 0 !important; }

    /* Letter tiles for the word */
    .tiles { display: flex; justify-content: center; flex-wrap: wrap; gap: 8px; margin: 14px 0; }
    .tile {
        width: 44px; height: 54px; border-radius: 10px; background: rgba(255,255,255,0.75);
        border-bottom: 4px solid #7a5cff; display: flex; align-items: center; justify-content: center;
        font-size: 30px; font-weight: 800; color: #2b1b6b !important; text-transform: uppercase;
    }
    .tile.missed { color: #d6336c !important; border-bottom-color: #d6336c; }

    .category-badge {
        display: inline-block; background: #7a5cff; border-radius: 16px; padding: 6px 20px;
        font-size: 20px; font-weight: 700; box-shadow: 0 6px 14px rgba(122,92,255,0.35);
    }
    .stApp .category-badge, .stApp .category-badge * { color: white !important; }
    .hearts { text-align: center; font-size: 28px; letter-spacing: 4px; margin: 6px 0; }

    .banner { text-align: center; border-radius: 20px; padding: 22px 10px; margin: 14px 0;
              box-shadow: 0 8px 20px rgba(0,0,0,0.15); }
    .banner .big { font-size: 44px; font-weight: 900; }
    .banner .small { font-size: 22px; }
    .win  { background: linear-gradient(90deg, #43e97b, #38f9d7); }
    .lose { background: linear-gradient(90deg, #ff9a9e, #fecfef); }
    .stApp .win, .stApp .win * { color: #0b3d2e !important; }
    .stApp .lose, .stApp .lose * { color: #5a0f1e !important; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------- Game state (survives reruns) ----------
defaults = {
    "hm_category": None,   # which category was picked
    "hm_answer": None,     # the secret word
    "hm_hint": [],         # list like ["-", "-", "a"]
    "hm_wrong": 0,         # wrong guesses so far
    "hm_guessed": set(),   # letters already used
    "hm_sound": None,      # sound to play on this rerun
    "hm_nonce": 0,         # counter so repeated sounds still replay
    "hm_sound_on": True,   # 🔊 / 🔇 toggle
}
for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


def start_game(category):
    """Your main() setup: pick a word and reset everything."""
    answer = random.choice(categories[category])
    st.session_state.hm_category = category
    st.session_state.hm_answer = answer
    st.session_state.hm_hint = ["-"] * len(answer)
    st.session_state.hm_wrong = 0
    st.session_state.hm_guessed = set()
    st.session_state.hm_sound = None


def make_guess(guess):
    """Your guessing logic, unchanged — just using session_state."""
    answer = st.session_state.hm_answer
    st.session_state.hm_guessed.add(guess)
    st.session_state.hm_nonce += 1

    if guess in answer:
        for i in range(len(answer)):
            if answer[i] == guess:
                st.session_state.hm_hint[i] = guess
        st.session_state.hm_sound = "correct"
    else:
        st.session_state.hm_wrong += 1
        st.session_state.hm_sound = "wrong"

    if "-" not in st.session_state.hm_hint:
        st.session_state.hm_sound = "win"
    elif st.session_state.hm_wrong >= max_wrong:
        st.session_state.hm_sound = "lose"


def draw_hangman(wrong, lost):
    """Gallows + figure. One more body part per wrong guess."""
    stroke = "#2b1b6b"
    parts = [
        '<circle cx="150" cy="70" r="20" />',                 # 1 head
        '<line x1="150" y1="90" x2="150" y2="150" />',        # 2 body
        '<line x1="150" y1="105" x2="122" y2="130" />',       # 3 left arm
        '<line x1="150" y1="105" x2="178" y2="130" />',       # 4 right arm
        '<line x1="150" y1="150" x2="126" y2="188" />',       # 5 left leg
        '<line x1="150" y1="150" x2="174" y2="188" />',       # 6 right leg
    ]
    body = "".join(parts[:wrong])
    face = ""
    if lost:  # sad X-eyes face
        face = ('<line x1="141" y1="63" x2="147" y2="69"/><line x1="147" y1="63" x2="141" y2="69"/>'
                '<line x1="153" y1="63" x2="159" y2="69"/><line x1="159" y1="63" x2="153" y2="69"/>'
                '<path d="M142 80 Q150 74 158 80" />')
    return f"""
    <div style="display:flex; justify-content:center;">
    <svg viewBox="0 0 220 230" width="230" height="240" fill="none" stroke="{stroke}"
         stroke-width="6" stroke-linecap="round" stroke-linejoin="round">
        <rect x="10" y="10" width="200" height="210" rx="20" fill="rgba(255,255,255,0.55)" stroke="none"/>
        <line x1="40" y1="205" x2="120" y2="205" stroke="#8b5a2b"/>
        <line x1="65" y1="205" x2="65" y2="30" stroke="#8b5a2b"/>
        <line x1="65" y1="30" x2="150" y2="30" stroke="#8b5a2b"/>
        <line x1="65" y1="60" x2="95" y2="30" stroke="#8b5a2b"/>
        <line x1="150" y1="30" x2="150" y2="50" stroke="#c9a46b" stroke-width="4"/>
        <g stroke="{'#d6336c' if lost else stroke}">{body}{face}</g>
    </svg></div>"""


# ---------- Header ----------
top_left, top_right = st.columns([4, 1])
with top_left:
    if st.button("🏠 Home"):
        st.switch_page("game_app.py")
with top_right:
    st.session_state.hm_sound_on = st.toggle(
        "🔊" if st.session_state.hm_sound_on else "🔇", value=st.session_state.hm_sound_on
    )

st.markdown('<div class="huge-title">🕵️ Hangman</div>', unsafe_allow_html=True)

# ---------- Screen 1: pick a category ----------
if st.session_state.hm_answer is None:
    st.markdown('<p class="center" style="font-size:22px;">Choose a category to start</p>',
                unsafe_allow_html=True)
    for category in categories:
        left, middle, right = st.columns([1, 3, 1])
        with middle:
            if st.button(category, use_container_width=True):
                start_game(category)
                st.rerun()
    st.stop()

# ---------- Screens 2 & 3: game and result ----------
answer = st.session_state.hm_answer
won = "-" not in st.session_state.hm_hint
lost = st.session_state.hm_wrong >= max_wrong

st.markdown(f'<div class="center"><span class="category-badge">{st.session_state.hm_category}</span></div>',
            unsafe_allow_html=True)

st.markdown(draw_hangman(st.session_state.hm_wrong, lost), unsafe_allow_html=True)

hearts = "❤️" * (max_wrong - st.session_state.hm_wrong) + "🤍" * st.session_state.hm_wrong
st.markdown(f'<div class="hearts">{hearts}</div>', unsafe_allow_html=True)

# Word tiles (on a loss, show the missed letters in red)
tiles = ""
for i, letter in enumerate(answer):
    if st.session_state.hm_hint[i] != "-":
        tiles += f'<div class="tile">{letter}</div>'
    elif lost:
        tiles += f'<div class="tile missed">{letter}</div>'
    else:
        tiles += '<div class="tile"></div>'
st.markdown(f'<div class="tiles">{tiles}</div>', unsafe_allow_html=True)

if won or lost:
    if won:
        st.balloons()
        st.markdown(f"""<div class="banner win"><div class="big">🎉 YOU WIN! 🎉</div>
            <div class="small">The word was <b>{answer.upper()}</b></div></div>""", unsafe_allow_html=True)
    else:
        st.markdown(f"""<div class="banner lose"><div class="big">😭 YOU LOSE 😭</div>
            <div class="small">The word was <b>{answer.upper()}</b></div></div>""", unsafe_allow_html=True)

    left, middle, right = st.columns([1, 2, 1])
    with middle:
        if st.button("Play again", use_container_width=True):
            start_game(st.session_state.hm_category)
            st.rerun()
        if st.button("Change category", use_container_width=True):
            st.session_state.hm_answer = None
            st.rerun()
else:
    st.markdown('<p class="center">👇 Tap a letter to guess</p>', unsafe_allow_html=True)
    letters = "abcdefghijklmnopqrstuvwxyz"
    rows = [letters[0:9], letters[9:18], letters[18:26]]
    with st.container(key="keyboard"):
        for row in rows:
            cols = st.columns(9)
            for col, letter in zip(cols, row):
                with col:
                    if st.button(letter.upper(), key=f"key_{letter}",
                                 disabled=letter in st.session_state.hm_guessed,
                                 use_container_width=True):
                        make_guess(letter)
                        st.rerun()

# Sound for the last action, played at the very bottom of the page so the
# tiny sound frame can't disturb the layout above. Cleared so it plays once.
if st.session_state.hm_sound and st.session_state.hm_sound_on:
    play_sound(st.session_state.hm_sound, st.session_state.hm_nonce)
st.session_state.hm_sound = None
