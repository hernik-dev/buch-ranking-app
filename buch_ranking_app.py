import streamlit as st
import random

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

st.set_page_config(page_title="Buch-Ranking", layout="centered")
st.title("📚 Dein persönliches Buch-Ranking")

# Initialisierung
if "candidates" not in st.session_state:
    st.session_state.candidates = books.copy()
    random.shuffle(st.session_state.candidates)
    st.session_state.ranked = []

# Vergleichsfunktion mit einfachem Bubble-Sort-Ansatz
def compare_next():
    if len(st.session_state.candidates) <= 1:
        st.session_state.ranked = st.session_state.candidates + st.session_state.ranked
        st.session_state.candidates = []

if len(st.session_state.candidates) >= 2:
    book1 = st.session_state.candidates[0]
    book2 = st.session_state.candidates[1]

    st.write("Welches Buch gefällt dir besser?")
    col1, col2 = st.columns(2)

    with col1:
        if st.button(book1):
            st.session_state.ranked.append(book1)
            # Der Verlierer kommt zurück ans Ende der Liste
            st.session_state.candidates = st.session_state.candidates[2:] + [book2]
            st.rerun()

    with col2:
        if st.button(book2):
            st.session_state.ranked.append(book2)
            st.session_state.candidates = st.session_state.candidates[2:] + [book1]
            st.rerun()
else:
    # Falls 1 Buch übrig ist, hänge es ans Ende
    if len(st.session_state.candidates) == 1:
        st.session_state.ranked.append(st.session_state.candidates[0])
        st.session_state.candidates = []

    st.success("🎉 Dein Ranking ist fertig!")
    st.subheader("📊 Dein Buch-Ranking:")
    for i, book in enumerate(st.session_state.ranked, 1):
        st.markdown(f"**{i}.** {book}")

    if st.button("🔄 Neu starten"):
        del st.session_state["candidates"]
        del st.session_state["ranked"]
        st.rerun()
