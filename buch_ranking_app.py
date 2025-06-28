import streamlit as st

books = [
    "Air – Christian Kracht",
    "Menschenwerk – Han Kang",
    "Trophäe – Gaea Schoeters",
    "Leonard and Paul – Rónán Hession",
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

def init_sort_lists(items):
    return [[item] for item in items]

if "lists" not in st.session_state:
    st.session_state.lists = init_sort_lists(books)
    st.session_state.left = None
    st.session_state.right = None
    st.session_state.merged = []
    st.session_state.i = 0
    st.session_state.j = 0
    st.session_state.stage = "select_merge"

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

def do_compare(choice):
    if choice == "left":
        st.session_state.merged.append(st.session_state.left[st.session_state.i])
        st.session_state.i += 1
    else:
        st.session_state.merged.append(st.session_state.right[st.session_state.j])
        st.session_state.j += 1

    if st.session_state.i >= len(st.session_state.left):
        st.session_state.merged.extend(st.session_state.right[st.session_state.j:])
        st.session_state.lists.insert(0, st.session_state.merged)
        st.session_state.stage = "select_merge"
    elif st.session_state.j >= len(st.session_state.right):
        st.session_state.merged.extend(st.session_state.left[st.session_state.i:])
        st.session_state.lists.insert(0, st.session_state.merged)
        st.session_state.stage = "select_merge"

    st.rerun()

if st.session_state.stage == "finished":
    st.success("🎉 Das Ranking ist fertig!")
    for idx, book in enumerate(st.session_state.lists[0], 1):
        st.markdown(f"**{idx}.** {book}")
    if st.button("🔄 Neu starten"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

elif st.session_state.stage == "select_merge":
    if len(st.session_state.lists) == 1:
        st.session_state.stage = "finished"
        st.rerun()
    else:
        # Automatisch nächsten Merge starten
        start_next_merge()
        st.rerun()

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
