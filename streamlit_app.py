import streamlit as st
import random
import time

st.set_page_config(page_title="Cheat Code AI")

# Инициализация памяти игрока
if "user_iq" not in st.session_state:
    st.session_state.user_iq = 100
if "is_vip" not in st.session_state:
    st.session_state.is_vip = False
if "skins" not in st.session_state:
    st.session_state.skins = ["Дефолтный Штрих"]
if "auth" not in st.session_state:
    st.session_state.auth = False
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Локальная заглушка ИИ на чистом русском языке
def ask_gemini_mock(subject, user_question):
    mock_responses = {
        "Математика": [
            "Слушай сюда, эта теорема полная имба. Пифагор просто затащил катку в геометрии. Короче, гипотенуза в квадрате равна сумме катетов в квадрате!",
            "Твой x и y это как масик и тюбик, вечно ищут точки пересечения. Дискриминант больше нуля? Значит у тебя два сочных корня, катка выиграна."
        ],
        "Русский язык": [
            "Чувак, ставить запятые это база. Если ты их ливаешь из текста, твоя учительница ловит жесткий кринж. Запомни: перед что, чтобы и потому что всегда ставим щит из запятой.",
            "Жи-Ши пиши с буквой И. Кто пишет с Ы тот официально забанен в Корпусе А. Это правило жесткое, как баланс бравлеров в новом сезоне."
        ],
        "Физика": [
            "Сила трения это когда ты пытаешься флексить новыми кроссами, но физика говорит не в эту смену. Она буквально контрит твое движение, как замедление от Спайка.",
            "Гравитация это жесткий притягательный вайб Земли. Ты прыгаешь, но планета притягивает тебя обратно со скоростью 9.8 метров в секунду."
        ]
    }
    responses = mock_responses.get(subject, [
        f"Ну ты выдал, конечно! Запрос про {user_question} это мощно. Короче, тут все просто: апаешь щиты и сдаешь домашку вовремя. Чистый флекс!",
        f"По поводу {user_question}: эксперты из Корпуса А поясняют, что это полная имба, если юзать с умом."
    ])
    return random.choice(responses)

# Расчет Корпуса и шкалы прогресса
def get_korpus_info(iq):
    if iq >= 140: 
        return "Корпус А (Сигмы)", 1.0, "Ты на вершине! Настоящий гигачад."
    elif iq >= 120: 
        progress = (iq - 120) / (140 - 120)
        return "Корпус Б (Масики)", min(1.0, max(0.0, progress)), f"До Корпуса А осталось {140 - iq} IQ!"
    elif iq >= 100: 
        progress = (iq - 100) / (120 - 100)
        return "Корпус В (Челики)", min(1.0, max(0.0, progress)), f"До Корпуса Б осталось {120 - iq} IQ!"
    else: 
        progress = (iq - 80) / (100 - 80)
        return "Корпус Г (Двоечники)", min(1.0, max(0.0, progress)), f"Срочно апай IQ! До Корпуса В осталось {100 - iq} IQ!"

# Окно авторизации
@st.dialog("Вход в Чит-код AI")
def login_dialog():
    st.write("Добро пожаловать в ИИ-приложение для школьников!")
    username = st.text_input("Введи свой никнейм из Brawl Stars:")
    if st.button("Затащить в катку"):
        if username:
            st.session_state.username = username
            st.session_state.auth = True
            st.rerun()
        else:
            st.error("Без ника не пустим, чувак!")

# Проверка входа
if not st.session_state.auth:
    st.title("🤖 Чит-код AI")
    st.write("Для старта нужно пройти быструю верификацию.")
    if st.button("Открыть окно входа"):
        login_dialog()
    st.stop()

# --- БОКОВОЕ МЕНЮ (SIDEBAR) ---
st.sidebar.title(f"Профиль: {st.session_state.username}")
korpus_title, korpus_pct, korpus_text = get_korpus_info(st.session_state.user_iq)

st.sidebar.metric("Твой IQ Рейтинг", f"{st.session_state.user_iq} PTS")
st.sidebar.info(f"Твой Сезон: {korpus_title}")

st.sidebar.write("Прогресс Сезона:")
st.sidebar.progress(korpus_pct)
st.sidebar.caption(korpus_text)

if st.sidebar.toggle("Активировать VIP"):
    st.session_state.is_vip = True
    st.sidebar.success("VIP Статус: АКТИВЕН")
else:
    st.session_state.is_vip = False

page = st.sidebar.radio("Куда летим?", ["Чат по предметам", "Мемный Судья", "Мегаящик", "Мои Скины"])


# --- СТРАНИЦЫ ИГРЫ ---

# 1. ЧАТ ПО ПРЕДМЕТАМ
if page == "Чат по предметам":
    st.title("🤖 Чит-код AI: База от экспертов")
    st.write("Спроси ИИ о любой сложной теме из учебника. Он переведет это на язык Сигм!")

    subject = st.selectbox("Выбери предмет для кастомизации ответа:", 
                           ["Математика", "Русский язык", "Физика", "История", "Химия"])

    for role, text in st.session_state.chat_history:
        with st.chat_message(role):
            st.write(text)

    user_input = st.chat_input("Напиши свой вопрос сюда...")

    if user_input:
        if not st.session_state.is_vip and st.session_state.user_iq <= 80:
            st.error("Твой IQ упал до 80! Ниже нельзя. Иди апай рейтинг в Экзамен!")
        else:
            with st.chat_message("user"):
                st.write(user_input)
            st.session_state.chat_history.append(("user", user_input))

            with st.spinner("ИИ переводит параграф учебника..."):
                time.sleep(1) 
                answer = ask_gemini_mock(subject, user_input)

            with st.chat_message("assistant"):
                st.write(answer)
            st.session_state.chat_history.append(("assistant", answer))

            if not st.session_state.is_vip:
                st.session_state.user_iq = max(80, st.session_state.user_iq - 2)
                st.toast("Минус 2 IQ за запрос к ИИ")

            st.rerun()


# 2. МЕМНЫЙ ЭКЗАМЕН (КВИЗ)
elif page == "Мемный Судья":
    st.title("⚖️ Мемный Экзамен: Тест на Сигму")
    
    quiz_questions = [
        {
            "q": "Твой тиммейт на Эдгаре прыгает в толпу врагов с 10 банками за 2 секунды до конца матча. Что это?",
            "a": ["Чистая база и красивый уход", "КРИНЖ и слив кубков", "Закон Архимеда в действии", "Тактический мув из киберспорта"],
            "right": "КРИНЖ и слив кубков"
        },
        {
            "q": "Учитель кричит: Убираем телефоны, внезапная летучка!. Твоё главное оружие?",
            "a": ["Резко притвориться спящим NPC", "Открыть ГДЗ быстрее всех", "Громко заплакать", "Сдать чистый лист с автографом"],
            "right": "Открыть ГДЗ быстрее всех"
        },
        {
            "q": "Ты зашел в класс с каменным лицом, ни с кем не поздоровался и смотришь в стену. Кто ты?",
            "a": ["Грустный тюбик", "Зомби после Доты", "Абсолютный Сигма-гигачад", "NPC, у которого завис скрипт"],
            "right": "Абсолютный Сигма-гигачад"
        },
        {
            "q": "Что делать на экзамене, если ты вообще не знаешь ответ на вопрос?",
            "a": ["Написать смешной мем в бланке ответов", "Уверенно ливнуть через окно", "Налить столько воды, чтобы комиссия утонула", "Ждать, пока ОГЭ отменят по радио"],
            "right": "Налить столько воды, чтобы комиссия утонула"
        },
        {
            "q": "Какой Корпус считается самым имбовым в нашей школе?",
            "a": ["Корпус Г (Двоечники)", "Корпус В (Челики)", "Корпус Б (Масики)", "Корпус А (Сигмы)"],
            "right": "Корпус А (Сигмы)"
        }
    ]

    if "quiz_step" not in st.session_state:
        st.session_state.quiz_step = 0
    if "quiz_score" not in st.session_state:
        st.session_state.quiz_score = 0
    if "quiz_active" not in st.session_state:
        st.session_state.quiz_active = True

    if not st.session_state.quiz_active:
        st.write("Ты уже прошел этот экзамен!")
        if st.button("Пройти пересдачу"):
            st.session_state.quiz_step = 0
            st.session_state.quiz_score = 0
            st.session_state.quiz_active = True
            st.rerun()
    else:
        step = st.session_state.quiz_step
        
        if step >= len(quiz_questions):
            st.subheader("🏁 Экзамен окончен! Твои результаты:")
            correct_answers = st.session_state.quiz_score
            st.write(f"Правильных ответов: {correct_answers} из 5")
            
            earned_iq = (correct_answers * 10) - ((5 - correct_answers) * 5)
            st.session_state.user_iq = max(80, st.session_state.user_iq + earned_iq)
            
            if earned_iq >= 0:
                st.write(f"Твой рейтинг изменился на: +{earned_iq} IQ PTS!")
            else:
                st.write(f"Твой рейтинг изменился на: {earned_iq} IQ PTS! Иди учи уроки.")
                
            if correct_answers == 5:
                st.balloons()
                loot_pool = ["Скин: Золотой Сигма Леон", "Скин: Гигачад Мортис", "Скин: Меха-Альтушка Эдгар"]
                won_skin = random.choice(loot_pool)
                if won_skin not in st.session_state.skins:
                    st.session_state.skins.append(won_skin)
                st.write(f"🎉 МЕГА-БОНУС за идеальную сдачу! Тебе выпадает редчайший {won_skin}!")
                
            st.session_state.quiz_active = False
            st.button("Зафиксировать результат")
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


# 3. СИМУЛЯТОР МЕГAЯЩИКА
elif page == "Мегаящик":
    st.title("🎁 Симулятор Мегаящика")
    st.write("Слей 20 IQ ради крутого скина! Испытай удачу!")
    
    st.audio("https://soundboard.com", format="audio/mp3", loop=True)
    
    if st.button("Открыть Мегаящик (Цена: 20 IQ)"):
