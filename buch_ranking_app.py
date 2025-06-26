import streamlit as st

# Liste deiner Bücher
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

# ---------------------
# Interaktiver MergeSort
# ---------------------

def merge_sort(lst):
    if len(lst) <= 1:
        return lst
    mid = len(lst) // 2
    left = merge_sort(lst[:mid])
    right = merge_sort(lst[mid:])
    return list(merge_gen(left, right))

def merge_gen(left, right):
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        yield ("compare", left[i], right[j])
        response = yield
        if response == "left":
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    yield ("merged", result)

# ---------------------
# Streamlit UI
# ---------------------

st.title("📚 Effizientes Buch-Ranking per interaktivem Sortieren")

# Initialisierung
if "sort_stack" not in st.session_state:
    st.session_state.original_books = books.copy()
    st.session_state.generator_stack = merge_gen(books[:len(books)//2], books[len(books)//2:])
    st.session_state.merge_result = []
    st.session_state.last_pair = None
    st.session_state.decision_count = 0

# Merge-Schritt
gen = st.session_state.generator_stack

# Vorschlag anzeigen
try:
    if st.session_state.last_pair is None:
        instruction = next(gen)
        if instruction[0] == "compare":
            st.session_state.last_pair = (instruction[1], instruction[2])
        elif instruction[0] == "merged":
            st.session_state.merge_result = instruction[1]
            st.session_state.last_pair = None
except StopIteration:
    pass

# Vergleichsanzeige
if st.session_state.last_pair:
    a, b = st.session_state.last_pair
    col1, col2 = st.columns(2)

    with col1:
        if st.button(a):
            try:
                gen.send("left")
                st.session_state.last_pair = None
                st.session_state.decision_count += 1
                st.rerun()
            except StopIteration:
                pass

    with col2:
        if st.button(b):
            try:
                gen.send("right")
                st.session_state.last_pair = None
                st.session_state.decision_count += 1
                st.rerun()
            except StopIteration:
                pass

    st.info(f"Vergleiche abgeschlossen: {st.session_state.decision_count}")

# Fertiges Ranking anzeigen
elif st.session_state.merge_result:
    st.success("🎉 Ranking abgeschlossen!")
    st.subheader("📊 Dein Ranking:")
    for i, book in enumerate(st.session_state.merge_result, 1):
        st.markdown(f"**{i}.** {book}")

    if st.button("🔄 Neu starten"):
        for key in ["sort_stack", "merge_result", "last_pair", "decision_count", "original_books", "generator_stack"]:
            if key in st.session_state:
                del st.session_state[key]
        st.rerun()
