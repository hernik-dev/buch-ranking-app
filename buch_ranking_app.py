import streamlit as st

# Liste der Bücher
books = [
    "Air – Christian Kracht",
    "Menschenwerk – Han Kang",
    "Trophäe – Gaea Schoeters",
    "The Rabbit Hutch – Tess Gunty",
    "I Know Why the Caged Bird Sings – Maya Angelou",
    "The Sound and the Fury – William Faulkner",
    "Die Jahre – Annie Ernaux",
    "A Visit from the Goon Squad – Jennifer Egan",
    "Elementarteilchen – Michel Houellebecq",
    "Der falsche Gruß – Maxim Biller",
    "Ein Tag im Leben des Iwan Denissowitsch – Alexander Solschenizyn",
    "Eurotrash – Christian Kracht",
    "Unterleuten – Juli Zeh",
    "Der Trafikant – Robert Seethaler",
    "Heart of Darkness – Joseph Conrad",
    "Möchte die Witwe ... – Saša Stanišić",
    "Die Möglichkeit von Glück – Anne Rabe",
    "Train Dreams – Denis Johnson"
]

st.title("📚 Das große Buch-Ranking ")

# ---------------------------
# Hilfsfunktionen
# ---------------------------

def merge_step(left, right):
    return {
        "left": left,
        "right": right,
        "result": [],
        "i": 0,
        "j": 0
    }

def prepare_merges(items):
    stack = [[item] for item in items]
    merges = []

    while len(stack) > 1:
        a = stack.pop()
        b = stack.pop()
        merges.append(merge_step(b, a))
        stack.append(b + a)

    return merges[::-1]  # erste Vergleiche zuerst

# ---------------------------
# Initialisierung
# ---------------------------

if "merges" not in st.session_state:
    st.session_state.merges = prepare_merges(books)
    st.session_state.current = None
    st.session_state.result = None
    st.session_state.finished = False
    st.session_state.count = 0

# ---------------------------
# Vergleichslogik
# ---------------------------

def do_choice(choice):
    op = st.session_state.current
    if choice == "left":
        op["result"].append(op["left"][op["i"]])
        op["i"] += 1
    else:
        op["result"].append(op["right"][op["j"]])
        op["j"] += 1

    st.session_state.count += 1

    # Wenn ein Teil aufgebraucht ist, Rest anhängen und nächsten Schritt laden
    if op["i"] >= len(op["left"]):
        op["result"].extend(op["right"][op["j"]:])
        st.session_state.current = None
    elif op["j"] >= len(op["right"]):
        op["result"].extend(op["left"][op["i"]:])
        st.session_state.current = None

# ---------------------------
# Merge-Schritt starten
# ---------------------------

if not st.session_state.finished:
    if st.session_state.current is None:
        if st.session_state.merges:
            st.session_state.current = st.session_state.merges.pop(0)
        else:
            st.session_state.finished = True
            st.session_state.result = st.session_state.current["result"] if st.session_state.current else []

# ---------------------------
# UI
# ---------------------------

if st.session_state.finished:
    st.success("🎉 Dein Ranking ist fertig!")
    for i, book in enumerate(st.session_state.result, 1):
        st.markdown(f"**{i}.** {book}")

    if st.button("🔁 Neu starten"):
        for key in ["merges", "current", "result", "finished", "count"]:
            del st.session_state[key]
        st.rerun()

elif st.session_state.current:
    op = st.session_state.current
    if op["i"] < len(op["left"]) and op["j"] < len(op["right"]):
        a = op["left"][op["i"]]
        b = op["right"][op["j"]]
        col1, col2 = st.columns(2)
        with col1:
            if st.button(a):
                do_choice("left")
                st.rerun()
        with col2:
            if st.button(b):
                do_choice("right")
                st.rerun()
        st.info(f"Vergleiche bisher: {st.session_state.count}")
    else:
        # Letzten Merge-Schritt beenden
        op["result"].extend(op["left"][op["i"]:])
        op["result"].extend(op["right"][op["j"]:])
        st.session_state.current = None

        if not st.session_state.merges:
            st.session_state.finished = True
            st.session_state.result = op["result"]
        st.rerun()
