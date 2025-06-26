import streamlit as st

books = [
    "Air – Christian Kracht",
    "Menschenwerk – Han Kang",
    "Trophäe – Gaea Schoeters",
    "The Rabbit Hutch – Tess Gunty",
]

def merge_step(left, right):
    return {"left": left, "right": right, "result": [], "i": 0, "j": 0}

def prepare_merges(items):
    stack = [[item] for item in items]
    merges = []
    while len(stack) > 1:
        a = stack.pop()
        b = stack.pop()
        merges.append(merge_step(b, a))
        stack.append(b + a)
    return merges[::-1]

if "merges" not in st.session_state:
    st.session_state.merges = prepare_merges(books)
    st.session_state.current = None
    st.session_state.result = []
    st.session_state.finished = False
    st.session_state.count = 0

def do_choice(choice):
    op = st.session_state.current
    if choice == "left":
        op["result"].append(op["left"][op["i"]])
        op["i"] += 1
    else:
        op["result"].append(op["right"][op["j"]])
        op["j"] += 1
    st.session_state.count += 1
    if op["i"] >= len(op["left"]):
        op["result"].extend(op["right"][op["j"]:])
        st.session_state.current = None
    elif op["j"] >= len(op["right"]):
        op["result"].extend(op["left"][op["i"]:])
        st.session_state.current = None

if not st.session_state.finished:
    if st.session_state.current is None:
        if st.session_state.merges:
            st.session_state.current = st.session_state.merges.pop(0)
        else:
            st.session_state.finished = True
            # Wenn current None, dann result bleibt so
            if st.session_state.current is not None:
                st.session_state.result = st.session_state.current["result"]

if st.session_state.finished:
    st.success("🎉 Dein Ranking ist fertig!")
    for i, book in enumerate(st.session_state.result, 1):
        st.markdown(f"**{i}.** {book}")
    if st.button("🔁 Neu starten"):
        for key in ["merges", "current", "result", "finished", "count"]:
            del st.session_state[key]
        st.experimental_rerun()
elif st.session_state.current:
    op = st.session_state.current
    if op["i"] < len(op["left"]) and op["j"] < len(op["right"]):
        a = op["left"][op["i"]]
        b = op["right"][op["j"]]
        col1, col2 = st.columns(2)
        with col1:
            if st.button(a):
                do_choice("left")
                st.experimental_rerun()
        with col2:
            if st.button(b):
                do_choice("right")
                st.experimental_rerun()
        st.info(f"Vergleiche bisher: {st.session_state.count}")
    else:
        op["result"].extend(op["left"][op["i"]:])
        op["result"].extend(op["right"][op["j"]:])
        st.session_state.result = op["result"]  # Wichtig!
        st.session_state.current = None
        if not st.session_state.merges:
            st.session_state.finished = True
        st.experimental_rerun()
