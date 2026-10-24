import random
import streamlit as st

highest = 100
lowest = 1
max_guesses = 8

st.set_page_config(page_title="Number Guessing Game", page_icon="🎯")

# ---------- Styling ----------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;800&display=swap');

    .stApp {
        background: linear-gradient(135deg, #a1c4fd 0%, #c2e9fb 50%, #fbc2eb 100%);
    }
    .stApp, .stApp p, .stApp label, .stApp span, .stApp div, .stApp h1, .stApp h2, .stApp h3 {
        font-family: 'Poppins', sans-serif !important;
        color: #1f2a44;
    }

    /* Title and subtitle */
    .game-title {
        text-align: center;
        font-size: 46px;
        font-weight: 800;
        margin-bottom: 0;
    }
    .game-subtitle {
        text-align: center;
        font-size: 22px;
        margin-top: 4px;
        margin-bottom: 24px;
    }

    /* Bigger input label and number box */
    .stNumberInput label p {
        font-size: 20px !important;
        font-weight: 600;
    }
    .stNumberInput input {
        font-size: 22px !important;
        text-align: center;
    }

    /* Centred, attractive buttons */
    div.stButton {
        display: flex;
        justify-content: center;
    }
    div.stButton > button {
        background: linear-gradient(90deg, #ff7eb3, #7a5cff);
        color: white !important;
        border: none;
        border-radius: 30px;
        padding: 12px 48px;
        font-size: 20px;
        font-weight: 600;
        box-shadow: 0 6px 14px rgba(122, 92, 255, 0.35);
        transition: transform 0.15s ease;
    }
    div.stButton > button p {
        color: white !important;
        font-size: 20px !important;
        font-weight: 600;
    }
    div.stButton > button:hover {
        transform: scale(1.06);
        color: white !important;
    }

    /* Too high / too low feedback */
    .hint {
        text-align: center;
        font-size: 26px;
        font-weight: 600;
        background: rgba(255, 255, 255, 0.6);
        border-radius: 14px;
        padding: 10px;
        margin: 12px 0;
    }

    /* Big winning banner */
    .win-banner {
        text-align: center;
        background: linear-gradient(90deg, #43e97b, #38f9d7);
        border-radius: 20px;
        padding: 26px 10px;
        margin: 16px 0;
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.15);
    }
    .win-banner .big {
        font-size: 44px;
        font-weight: 800;
        color: #0b3d2e !important;
    }
    .win-banner .small {
        font-size: 22px;
        color: #0b3d2e !important;
    }

    /* Guess history */
    .history-title {
        font-size: 24px;
        font-weight: 700;
        margin-top: 28px;
    }
    .guess-item {
        font-size: 19px;
        background: rgba(255, 255, 255, 0.55);
        border-radius: 10px;
        padding: 6px 14px;
        margin: 6px 0;
    }
    .guess-correct {
        font-size: 30px;
        font-weight: 800;
        background: #43e97b;
        color: #0b3d2e !important;
        border-radius: 12px;
        padding: 12px 16px;
        margin: 10px 0;
        text-align: center;
    }

    /* Huge title */
    .stApp .huge-title, .stApp .huge-title * {
        text-align: center !important;
        font-size: 84px !important;
        font-weight: 900 !important;
        line-height: 1.1 !important;
        color: #2b1b6b !important;
        text-shadow: 3px 3px 0 rgba(255, 255, 255, 0.7);
        margin: 10px 0 18px 0 !important;
    }
    @media (max-width: 640px) {
        .stApp .huge-title, .stApp .huge-title * { font-size: 52px !important; }
    }

    /* Range badge with white text */
    .stApp .range-badge, .stApp .range-badge * {
        color: #ffffff !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------- Game state (survives reruns) ----------
if "answer" not in st.session_state:
    st.session_state.answer = random.randint(lowest, highest)
    st.session_state.guesses = 0
    st.session_state.won = False
    st.session_state.lost = False
    st.session_state.history = []

# ---------- Header ----------
st.markdown(
    """
    <div class="huge-title">🎯 Number Guessing Game</div>
    """,
    unsafe_allow_html=True,
)
st.markdown(
    f"""
    <div style="text-align:center; margin: 6px 0 24px 0;">
        <div style="font-size:20px; margin-bottom:10px;">Pick a number between</div>
        <span class="range-badge" style="background:#7a5cff; font-size:30px; font-weight:800;
                     padding:8px 26px; border-radius:16px; box-shadow:0 6px 14px rgba(122,92,255,0.35);">
            {lowest} &nbsp;–&nbsp; {highest}
        </span>
        <div style="font-size:17px; margin-top:14px;">You have <b>{max_guesses}</b> guesses</div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------- Game ----------
if not st.session_state.won and not st.session_state.lost:
    guess = st.number_input("Enter your guess:", min_value=lowest, max_value=highest, step=1)
    st.markdown(
        '<p style="text-align:center; font-size:16px;">👉 Type your number, then click the <b>Guess</b> button</p>',
        unsafe_allow_html=True,
    )

    left, middle, right = st.columns([1, 1, 1])
    with middle:
        guess_clicked = st.button("Guess", use_container_width=True)

    if guess_clicked:
        st.session_state.guesses += 1
        if guess > st.session_state.answer:
            st.session_state.history.append((guess, "TOO HIGH ⬆️"))
            st.markdown('<div class="hint">TOO HIGH ⬆️</div>', unsafe_allow_html=True)
        elif guess < st.session_state.answer:
            st.session_state.history.append((guess, "TOO LOW ⬇️"))
            st.markdown('<div class="hint">TOO LOW ⬇️</div>', unsafe_allow_html=True)
        else:
            st.session_state.history.append((guess, "CORRECT"))
            st.session_state.won = True
            st.rerun()

        if not st.session_state.won and st.session_state.guesses >= max_guesses:
            st.session_state.lost = True
            st.rerun()

    remaining = max_guesses - st.session_state.guesses
    st.markdown(
        f'<p style="text-align:center; font-size:18px;">Guesses left: <b>{remaining}</b> of {max_guesses}</p>',
        unsafe_allow_html=True,
    )
elif st.session_state.lost:
    st.markdown(
        f"""
        <div class="win-banner" style="background: linear-gradient(90deg, #ff9a9e, #fecfef);">
            <div class="big" style="color:#5a0f1e !important;">😭 You lost, sorry! 😭</div>
            <div class="small" style="color:#5a0f1e !important;">You used all 8 guesses. The number was <b>{st.session_state.answer}</b></div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    left, middle, right = st.columns([1, 1, 1])
    with middle:
        try_again = st.button("Play again", use_container_width=True)

    if try_again:
        del st.session_state.answer
        st.rerun()
else:
    st.balloons()
    st.markdown(
        f"""
        <div class="win-banner">
            <div class="big">🎉 {st.session_state.answer} is CORRECT! 🎉</div>
            <div class="small">You got it in <b>{st.session_state.guesses}</b> guesses</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    left, middle, right = st.columns([1, 1, 1])
    with middle:
        play_again = st.button("Play again", use_container_width=True)

    if play_again:
        del st.session_state.answer
        st.rerun()

# ---------- Previous guesses ----------
if st.session_state.history:
    st.markdown('<p class="history-title">Your previous guesses</p>', unsafe_allow_html=True)
    for i, (num, result) in enumerate(st.session_state.history, start=1):
        if result == "CORRECT":
            st.markdown(
                f'<div class="guess-correct">✅ {num} — CORRECT!</div>',
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f'<div class="guess-item">{i}. {num} → {result}</div>',
                unsafe_allow_html=True,
            )
