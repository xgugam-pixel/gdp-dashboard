import streamlit as st
import random

st.set_page_config(page_title="Cheat Code AI")

if "user_iq" not in st.session_state:
    st.session_state.user_iq = 100
if "skins" not in st.session_state:
    st.session_state.skins = ["Defolt"]

st.sidebar.title("Profil")
st.sidebar.write(f"IQ: {st.session_state.user_iq} PTS")

page = st.sidebar.radio("Menu", ["Chat", "Test", "Box", "Skins"])

if page == "Chat":
    st.title("Chat s II")
    user_input = st.text_input("Vopros:")
    if st.button("Otvetit"):
        if user_input:
            st.write(f"II: Pro {user_input} - eto baza! Glavnoe ne lovit krizh.")
            st.session_state.user_iq = max(80, st.session_state.user_iq - 2)

elif page == "Test":
    st.title("Test na Sigmu")
    st.write("Edgar prygaet v tolpu s 10 bankami. Chto eto?")
    if st.button("Eto BAZA"):
        st.session_state.user_iq += 10
        st.success("Pravilno! +10 IQ")
    if st.button("Eto KRINZH"):
        st.session_state.user_iq = max(80, st.session_state.user_iq - 5)
        st.error("Oshibka! -5 IQ")

elif page == "Box":
    st.title("Megabox")
    if st.button("Открыть за 20 IQ"):
        if st.session_state.user_iq - 20 < 80:
            st.error("Malo IQ! Minimum 80.")
        else:
            st.session_state.user_iq -= 20
            loot = ["Sigma Leon", "Masik Primo", "Altushka Nani", "Gigachad Mortis"]
            won = random.choice(loot)
            if won not in st.session_state.skins:
                st.session_state.skins.append(won)
            st.balloons()
            st.success(f"Vypal skin: {won}!")

elif page == "Skins":
    st.title("Tvoi Skins")
    for s in st.session_state.skins:
        st.write(f"- {s}")
