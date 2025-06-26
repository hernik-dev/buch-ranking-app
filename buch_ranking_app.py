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

st.title("📚 Buchclub: The Ranking")

# --- Hilfsfunktion: initiale Liste in Einzel-Listen packen ---
def init_sort_lists(items):
    return [[item] for item in items]

# --- State-Initialisierung ---
if "lists" not in st.session_state:
    st.session_state.lists = init_sort_lists(books)  # Liste von Listen (Teil-Sortierungen)
    st.session_state.left = None  # linke Liste zum Mergen
    st.session_state.right = None  # rechte Liste zum Mergen
    st.session_state.merged = []  # aktuell gemergte Liste
    st.session_state.i = 0  # Index in linker Liste
    st.session_state.j = 0  # Index in rechter Liste
    st.session_state.stage = "select_merge"  # Status: "select_merge", "compare", "finished"

# --- Hilfsfunktion: starte nächsten Merge Schritt ---
def start_next_merge():
    if len(st.session_state.lists) == 1:
        st.session_state.stage = "finished"
        return
    st.session_state.left = st.session_state.lists.pop(0)
    st.session_state.right = st.session_state.lists.pop(0)
    st.session_state.merged = []
    st.session_state.i = 0
    st.session_state.j = 0
    st.session_state.stage = "compare"

# --- Vergleich anzeigen und Ergebnis speichern ---
def do_compare(choice):
    if choice == "left":
        st.session_state.merged.append(st.session_state.left[st.session_state.i])
        st.session_state.i += 1
    else:
        st.session_state.merged.append(st.session_state.right[st.session_state.j])
        st.session_state.j += 1

    # Prüfen, ob linke oder rechte Liste erschöpft ist
    if st.session_state.i >= len(st.session_state.left):
        # Rest der rechten Liste anhängen
        st.session_state.merged.extend(st.session_state.right[st.session_state.j:])
        # Merge abgeschlossen, Ergebnis speichern
        st.session_state.lists.insert(0, st.session_state.merged)
        st.session_state.stage = "select_merge"
    elif st.session_state.j >= len(st.session_state.right):
        # Rest der linken Liste anhängen
        st.session_state.merged.extend(st.session_state.left[st.session_state.i:])
        # Merge abgeschlossen, Ergebnis speichern
        st.session_state.lists.insert(0, st.session_state.merged)
        st.session_state.stage = "select_merge"

    st.experimental_rerun()

# --- UI und Logik ---
if st.session_state.stage == "finished":
    st.success("🎉 Das Ranking ist fertig!")
    for idx, book in enumerate(st.session_state.lists[0], 1):
        st.markdown(f"**{idx}.** {book}")
    if st.button("🔄 Neu starten"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.experimental_rerun()

elif st.session_state.stage == "select_merge":
    if len(st.session_state.lists) == 1:
        # Fertig sortiert
        st.session_state.stage = "finished"
        st.experimental_rerun()
    else:
        st.write(f"🔄 Merge Schritt: {len(st.session_state.lists)} Teillisten zusammenführen")
        if st.button("Starte nächsten Merge"):
            start_next_merge()

elif st.session_state.stage == "compare":
    left_book = st.session_state.left[st.session_state.i]
    right_book = st.session_state.right[st.session_state.j]
    st.write("Welches Buch findest du besser?")
    col1, col2 = st.columns(2)
    with col1:
        if st.button(left_book):
            do_compare("left")
    with col2:
        if st.button(right_book):
            do_compare("right")
