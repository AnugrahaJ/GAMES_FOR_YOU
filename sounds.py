"""Browser-generated sound effects shared by all games. No sound files needed."""
import streamlit as st

_SCRIPTS = {
    "correct": """
        // Cheerful little blip
        const o = ctx.createOscillator(), g = ctx.createGain();
        o.type = 'sine'; o.frequency.value = 660;
        const t = ctx.currentTime;
        g.gain.setValueAtTime(0.2, t);
        g.gain.exponentialRampToValueAtTime(0.001, t + 0.15);
        o.connect(g); g.connect(ctx.destination); o.start(t); o.stop(t + 0.2);
    """,
    "wrong": """
        // Low buzz
        const o = ctx.createOscillator(), g = ctx.createGain();
        o.type = 'sawtooth'; o.frequency.value = 160;
        const t = ctx.currentTime;
        g.gain.setValueAtTime(0.2, t);
        g.gain.exponentialRampToValueAtTime(0.001, t + 0.25);
        o.connect(g); g.connect(ctx.destination); o.start(t); o.stop(t + 0.3);
    """,
    "win": """
        // Triumphant fanfare: layered trumpet-style arpeggio + final chord
        const melody = [[523,0.18],[659,0.18],[784,0.18],[1047,0.45]];
        let t = ctx.currentTime + 0.05;
        for (const [f,d] of melody) {
            for (const [type, vol, detune] of [['square',0.12,0],['triangle',0.2,3]]) {
                const o = ctx.createOscillator(), g = ctx.createGain();
                o.type = type; o.frequency.value = f; o.detune.value = detune;
                g.gain.setValueAtTime(0.0001, t);
                g.gain.exponentialRampToValueAtTime(vol, t + 0.03);
                g.gain.exponentialRampToValueAtTime(0.001, t + d);
                o.connect(g); g.connect(ctx.destination); o.start(t); o.stop(t + d + 0.05);
            }
            t += d * 0.82;
        }
        // Closing major chord with shimmer
        for (const f of [523, 659, 784, 1047]) {
            const o = ctx.createOscillator(), g = ctx.createGain();
            o.type = 'triangle'; o.frequency.value = f;
            g.gain.setValueAtTime(0.0001, t);
            g.gain.exponentialRampToValueAtTime(0.14, t + 0.04);
            g.gain.exponentialRampToValueAtTime(0.001, t + 1.4);
            o.connect(g); g.connect(ctx.destination); o.start(t); o.stop(t + 1.5);
        }
    """,
    "lose": """
        // Classic sad trombone: four descending notes with a droopy slide on each
        const notes = [[233,0.4],[220,0.4],[207,0.4],[185,1.1]];
        let t = ctx.currentTime + 0.05;
        for (const [f,d] of notes) {
            const o = ctx.createOscillator(), g = ctx.createGain();
            o.type = 'sawtooth';
            o.frequency.setValueAtTime(f * 1.04, t);
            o.frequency.exponentialRampToValueAtTime(f * 0.93, t + d);  // the "wah" droop
            const lp = ctx.createBiquadFilter();
            lp.type = 'lowpass'; lp.frequency.value = 900;
            g.gain.setValueAtTime(0.0001, t);
            g.gain.exponentialRampToValueAtTime(0.22, t + 0.05);
            g.gain.exponentialRampToValueAtTime(0.001, t + d);
            o.connect(lp); lp.connect(g); g.connect(ctx.destination);
            o.start(t); o.stop(t + d + 0.05);
            t += d + 0.07;
        }
    """,
}


def play_sound(kind, nonce):
    """Play one sound. `nonce` must change on every call (a counter works):
    if two identical sounds are sent in a row, Streamlit sees identical
    content and skips re-running it — the nonce makes each one unique,
    which is what keeps the beeps consistent."""
    st.iframe(
        f"""<html><body><!-- {nonce} --><script>
        const ctx = new (window.AudioContext || window.webkitAudioContext)();
        {_SCRIPTS[kind]}
        </script></body></html>""",
        height=1,
    )
