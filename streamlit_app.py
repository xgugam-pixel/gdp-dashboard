import streamlit as st
import random
import time

st.set_page_config(page_title="Cheat Code AI")

if "user_iq" not in st.session_state:
    st.session_state.user_iq = 100
if "skins" not in st.session_state:
    st.session_state.skins = ["Дефолтный Штрих"]
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

def ask_gemini_mock(subject, user_question):
    mock_responses = {
        "Математика": ["Теорема Пифагора полная имба! Гипотенуза в квадрате равна сумме катетов в квадрате."],
        "Русский язык": ["Чувак, запятые это база. Ставь щит из запятой перед что, чтобы и потому что."],
        "Физика": ["Сила трения буквально контрит твое движение, как замедление от Спайка в Бравле."]
    }
    responses = mock_responses.get(subject, [f"Про {user_question} поясняем: это имба! Главное не ловить кринж."])
    return random.choice(responses)

def get_korpus_info(iq):
    if iq >= 140: return "Корпус А (Сигмы)", 1.0, "Ты на вершине! Настоящий гигачад."
    elif iq >= 120: return "Корпус Б (Масики)", (iq - 120) / 20, f"До Корпуса А осталось {140 - iq} IQ!"
    elif iq >= 100: return "Корпус В (Челики)", (iq - 100) / 20, f"До Корпуса Б осталось {120 - iq} IQ!"
    else: return "Корпус Г (Двоечники)", (iq - 80) / 20, f"Срочно апай IQ! До Корпуса В осталось {100 - iq} IQ!"

st.sidebar.title("Профиль")
korpus_title, korpus_pct, korpus_text = get_korpus_info(st.session_state.user_iq)
st.sidebar.metric("Твой IQ Рейтинг", f"{st.session_state.user_iq} PTS")
st.sidebar.info(f"Твой Сезон: {korpus_title}")
st.sidebar.write("Прогресс Сезона:")
st.sidebar.progress(korpus_pct)
st.sidebar.caption(korpus_text)

page = st.sidebar.radio("Куда летим?", ["Чат по предметам", "Мемный Судья", "Мегаящик", "Мои Скины"])

if page == "Чат по предметам":
    st.title("🤖 Чит-код AI: База от экспертов")
    subject = st.selectbox("Выбери предмет:", ["Математика", "Русский язык", "Физика"])
    for role, text in st.session_state.chat_history:
        with st.chat_message(role): st.write(text)
    user_input = st.chat_input("Напиши свой вопрос сюда...")
    if user_input:
        with st.chat_message("user"): st.write(user_input)
        st.session_state.chat_history.append(("user", user_input))
        with st.spinner("ИИ переводит параграф учебника..."):
            time.sleep(1)
            answer = ask_gemini_mock(subject, user_input)
        with st.chat_message("assistant"): st.write(answer)
        st.session_state.chat_history.append(("assistant", answer))
        st.session_state.user_iq = max(80, st.session_state.user_iq - 2)
        st.rerun()

# СЮДА ВСТАВЛЯЙ ВТОРУЮ ЧАСТЬ
elif page == "Мемный Судья":
    st.title("⚖️ Мемный Экзамен: Тест на Сигму")
    quiz_questions = [
        {"q": "Твой тиммейт на Эдгаре прыгает в толпу врагов с 10 банками за 2 секунды до конца матча. Что это?", "a": ["Чистая база и красивый уход", "КРИНЖ и слив кубков", "Закон Архимеда в действии"], "right": "КРИНЖ и слив кубков"},
        {"q": "Учитель кричит: Убираем телефоны, внезапная летучка!. Твоё главное оружие?", "a": ["Резко притвориться спящим NPC", "Открыть ГДЗ быстрее всех", "Громко заплакать"], "right": "Открыть ГДЗ быстрее всех"},
        {"q": "Ты зашел в класс с каменным лицом, ни с кем не поздоровался и смотришь в стену. Кто ты?", "a": ["Грустный тюбик", "Зомби после Доты", "Абсолютный Сигма-гигачад"], "right": "Абсолютный Сигма-гигачад"}
    ]
    if "quiz_step" not in st.session_state: st.session_state.quiz_step = 0
    if "quiz_score" not in st.session_state: st.session_state.quiz_score = 0
    
    step = st.session_state.quiz_step
    if step >= len(quiz_questions):
        st.subheader("🏁 Экзамен окончен!")
        correct = st.session_state.quiz_score
        st.write(f"Правильных ответов: {correct} из {len(quiz_questions)}")
        earned_iq = (correct * 10) - ((len(quiz_questions) - correct) * 5)
        st.session_state.user_iq = max(80, st.session_state.user_iq + earned_iq)
        st.write(f"Рейтинг изменился на: {earned_iq} IQ PTS!")
        if correct == len(quiz_questions):
            st.balloons()
            loot = ["Скин: Золотой Сигма Леон", "Скин: Гигачад Мортис", "Скин: Меха-Альтушка Эдгар"]
            won = random.choice(loot)
            if won not in st.session_state.skins: st.session_state.skins.append(won)
            st.write(f"🎉 БОНУС за 3 из 3! Выпал {won}!")
        if st.button("Пройти заново 🔄"):
            st.session_state.quiz_step = 0
            st.session_state.quiz_score = 0
            st.rerun()
    else:
        current_q = quiz_questions[step]
        st.progress(step / len(quiz_questions))
        st.subheader(f"Вопрос {step + 1}: {current_q['q']}")
        for option in current_q['a']:
            if st.button(option, key=f"btn_{step}_{option}"):
                if option == current_q['right']:
                    st.session_state.quiz_score += 1
                    st.toast("База! Правильно.")
                else:
                    st.toast("Кринж! Ошибка.")
                st.session_state.quiz_step += 1
                time.sleep(0.3)
                st.rerun()

elif page == "Мегаящик":
    st.title("🎁 Симулятор Мегаящика")
    st.write("Слей 20 IQ ради крутого скина! Испытай удачу!")
    st.audio("https://soundboard.com", format="audio/mp3", loop=True)
    if st.button("Открыть Мегаящик (Цена: 20 IQ)"):
        st.session_state.user_iq = max(80, st.session_state.user_iq - 20)
        with st.spinner("Ящик трясется... Внутри что-то мигает..."): time.sleep(1.5)
        loot_pool = ["Скин: Золотой Сигма Леон", "Скин: Масик Эль Примо", "Скин: Альтушка Нани", "Скин: Тюбик Поко", "Скин: Гигачад Мортис"]
        won_skin = random.choice(loot_pool)
        if won_skin not in st.session_state.skins: st.session_state.skins.append(won_skin)
        st.balloons()
        st.write(f"🎉 ПРЕДМЕТОВ: 1! Тебе выпал {won_skin}!")
        time.sleep(1)
        st.rerun()

elif page == "Мои Скины":
    st.title("👕 Твой гардероб для флекса")
    st.write("Все твои открытые скины из Мегаящика и Экзаменов:")
    for skin in st.session_state.skins:
        st.write(f"- {skin}")
