import streamlit as st

# Liste deiner Bücher (kann erweitert/geändert werden)
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

# Initialisierung
if "rounds" not in st.session_state:
    st.session_state.remaining = [(a, b) for i, a in enumerate(books) for b in books[i+1:]]
    st.session_state.scores = {book: 0 for book in books}
    st.session_state.rounds = 0

st.title("📚 Buch-Ranking per Paarvergleich")
st.write("Vergleiche jeweils zwei Bücher und wähle deinen Favoriten. So entsteht ein konsistentes Ranking aller Bücher.")

if st.session_state.remaining:
    book1, book2 = st.session_state.remaining[0]
    col1, col2 = st.columns(2)

    with col1:
        if st.button(book1):
            st.session_state.scores[book1] += 1
            st.session_state.remaining.pop(0)
            st.session_state.rounds += 1
            st.rerun()

    with col2:
        if st.button(book2):
            st.session_state.scores[book2] += 1
            st.session_state.remaining.pop(0)
            st.session_state.rounds += 1
            st.rerun()

    st.info(f"Vergleiche abgeschlossen: {st.session_state.rounds} / {len(books) * (len(books) - 1) // 2}")
else:
    st.success("🎉 Alle Vergleiche abgeschlossen!")
    st.subheader("📊 Dein Ranking:")
    sorted_books = sorted(st.session_state.scores.items(), key=lambda x: x[1], reverse=True)
    for i, (book, score) in enumerate(sorted_books, 1):
        st.markdown(f"**{i}.** {book} ({score} Punkte)")

    if st.button("🔄 Neu starten"):
        for key in ["remaining", "scores", "rounds"]:
            del st.session_state[key]
        st.rerun()
