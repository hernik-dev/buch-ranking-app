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
    return {
        "type": "merge",
        "left": left,
        "right": right,
        "result": [],
        "i": 0,
        "j": 0
    }

def init_sort(lst):
    stack = []
    for book in lst:
        stack.append([book])
    ops = []
    while len(stack) > 1:
        a = stack.pop()
        b = stack.pop()
        ops.append(merge(b, a))  # Reihenfolge beachten
    return ops[::-1]  # umgekehrte Reihenf
