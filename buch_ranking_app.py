import streamlit as st

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

st.title("📚 Buch-Ranking mit möglichst wenig Vergleichen")

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

    # Rest anhängen
    if op["i"] >= len(op["left"]):
        op["result"].extend(op["right"][op["j"]:])
        st.session_state.current = None
    elif op["j"] >= len(op["right"]):
        op["result"].extend(op["left"][op["i"]:])
        st.session_state.current = None

# ---------------------------
# Merge Schritt fortsetzen
# ---------------------------

if not st.session_state.finished:
    if st.session_state.current is None and st.session_state.
