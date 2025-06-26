import streamlit as st

# Bücherliste
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

st.title("📚 Effizientes Buch-Ranking per interaktivem Sortieren")

# -------------------------------------------
# Merge-Sort als Stack-basierte Simulation
# -------------------------------------------

def merge(left, right):
    return {"type": "merge", "left": left, "right": right, "result": [], "i": 0, "j": 0}

def init_sort(lst):
    stack = []
    for book in lst:
        stack.append([book])
    ops = []
    while len(stack) > 1:
        a = stack.pop()
        b = stack.pop()
        ops.append(merge(b, a))  # Reihenfolge beachten
    return ops[::-1]  # umgekehrte Reihenfolge, damit man mit pop() von vorne beginnt

# ----------------------------
# Initialisierung in Session
# ----------------------------

if "ops" not in st.session_state:
    st.session_state.ops = init_sort(books)
    st.session_state.current = None
    st.session_state.finished = False
    st.session_state.history = []
    st.session_state.result = None
    st.session_state.decision_count = 0

# --------------------------------------
# Weiterverarbeitung nach Benutzerwahl
# --------------------------------------

def process_choice(choice):
    op = st.session_state.current
    if choice == "left":
        op["result"].append(op["left"][op["i"]])
        op["i"] += 1
    elif choice == "right":
        op["result"].append(op["right"][op["j"]])
        op["j"] += 1

    # Wenn ein Teil aufgebraucht ist, Rest anhängen
    if op["i"] >= len(op["left"]):
        op["result"].extend(op["right"][op["j"]:])
        st.session_state.ops.append(op["result"])
        st.session_state.current = None
    elif op["j"] >= len(op["right"]):
        op["result"].extend(op["left"][op["i"]:])
        st.session_state.ops.append(op["result"])
        st.session_state.current = None

    st.session_state.decision_count += 1

# --------------------------------------
# Hauptlogik
# --------------------------------------

# Wenn gerade kein aktiver Vergleich läuft
if not st.session_state.current and len(st.session_state.ops) > 1:
