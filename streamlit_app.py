import streamlit as st
import random
import time

# Инициализация сессии (stateless-вайб для каждого игрока)
if "user_iq" not in st.session_state:
    st.session_state.user_iq = 100
if "is_vip" not in st.session_state:
    st.session_state.is_vip = False
if "skins" not in st.session_state:
    st.session_state.skins = ["Дефолтный Штрих"]
if "auth" not in st.session_state:
    st.session_state.auth = False

# Функция-заглушка для теста интерфейса
def ask_gemini_mock(subject: str, user_question: str) -> str:
    mock_responses = {
        "Математика": [
            "Слушай сюда, эта теорема — полная имба. Пифагор просто затащил катку в геометрии. Короче, гипотенуза в квадрате — это как прокачанный Шелли на ульте, равна сумме катетов в квадрате!",
            "Твой x и y — это как масик и тюбик, вечно ищут точки пересечения. Дискриминант больше нуля? Значит у тебя два сочных корня, катка выиграна, апнули IQ."
        ],
        "Русский язык": [
            "Чувак, ставить запятые — это база. Если ты их ливаешь из текста, твоя учительница ловит жесткий кринж. Запомни: перед 'что', 'чтобы' и 'потому что' всегда ставим щит из запятой.",
            "Жи-Ши пиши с буквой И. Кто пишет с Ы — тот официально забанен в Корпусе А. Это правило жесткое, как баланс бравлеров в новом сезоне."
        ],
        "Физика": [
            "Сила трения — это когда ты пытаешься флексить новыми кроссами, но физика говорит 'не в эту смену'. Она буквально контрит твое движение, как замедление от Спайка.",
            "Гравитация — это жесткий притягательный вайб Земли. Ты прыгаешь, но планета говорит: 'Куда намылился?' и притягивает тебя обратно со скоростью 9.8 м/с²."
        ]
    }
    responses = mock_responses.get(subject, [
        f"Ну ты выдал, конечно! Запрос про '{user_question}' — это мощно. Короче, тут всё просто: апаешь щиты и сдаешь домашку вовремя. Чистый флекс!",
        f"По поводу '{user_question}': эксперты из Корпуса А поясняют, что это полная имба, если юзать с умом."
    ])
    return random.choice(responses)

# Логика определения Корпуса (Сезона)
def get_korpus(iq):
    if iq >= 140: return "Корпус А (Сигмы) 👑"
    elif iq >= 120: return "Корпус Б (Масики) 🔥"
    elif iq >= 100: return "Корпус В (Челики) 😐"
    else: return "Корпус Г (Двоечники) 💀"

# Окно авторизации (st.dialog)
@st.dialog("Вход в Чит-код AI 🕶️")
def login_dialog():
    st.write("Добро пожаловать в ИИ-приложение для школьников!")
    username = st.text_input("Введи свой никнейм из Brawl Stars:")
    if st.button("Затащить в катку 🚀"):
        if username:
            st.session_state.username = username
            st.session_state.auth = True
            st.rerun()
        else:
            st.error("Без ника не пустим, чувак!")

# Проверка авторизации
if not st.session_state.auth:
    st.title("🤖 Чит-код AI")
    st.write("Для старта нужно пройти быструю верификацию.")
    if st.button("Открыть окно входа"):
        login_dialog()
    st.stop()

# --- ОСНОВНОЙ ИНТЕРФЕЙС ПРИЛОЖЕНИЯ ---
st.sidebar.title(f"Профиль: {st.session_state.username}")
korpus_now = get_korpus(st.session_state.user_iq)
st.sidebar.metric("Твой IQ Рейтинг 📊", f"{st.session_state.user_iq} PTS")
st.sidebar.info(f"🏫 Твой Сезон: {korpus_now}")

if st.sidebar.toggle("🔥 Активировать VIP (199р/мес)"):
    st.session_state.is_vip = True
    st.sidebar.success("VIP Статус: АКТИВЕН (Безлимитный ИИ)")
else:
    st.session_state.is_vip = False

page = st.sidebar.radio("Куда летим?", ["Чат по /предметам", "Мемный Судья (Фарм IQ)", "Мегаящик 🎰", "Мои Скины 👑"])

# 1. ЧАТ С ИИ
if page == "Чат по /предметам":
    st.title("🤖 Чит-код AI: Объяснение на пальцах")
    subject = st.selectbox("Выбери предмет:", ["Математика", "Русский язык", "Физика", "История", "Химия"])
    user_input = st.text_input("Что тебе непонятно? (Например: Объясни теорему Пифагора)")
    
    if st.button("Сгенерировать Чит-Код 🚀"):
        if user_input:
            if not st.session_state.is_vip and st.session_state.user_iq <= 80:
                st.error("⚠️ Кринж! Твой IQ упал до 80! Ниже падать нельзя. Иди апай IQ в Мемного Судью или купи VIP!")
            else:
                with st.spinner("ИИ переводит учебник на язык штрихов..."):
                    time.sleep(1) # Имитация загрузки
                    answer = ask_gemini_mock(subject, user_input)
                
                if not st.session_state.is_vip:
                    st.session_state.user_iq = max(80, st.session_state.user_iq - 2)
                    st.toast("⚡ -2 IQ за запрос (С VIP было бы бесплатно)")
                
                st.chat_message("user").write(user_input)
                st.chat_message("assistant").write(answer)

# 2. МЕМНЫЙ СУДЬЯ
elif page == "Мемный Судья (Фарм IQ)":
    st.title("⚖️ Мемный Судья: База или Кринж?")
    st.write("Быстро оценивай ситуации и зарабатывай IQ!")
    
    memes = [
        "Учительница ставит 5 за то, что ты принес ей мем про Brawl Stars.",
        "Твой друг списал домашку у ChatGPT, но забыл стереть фразу 'Как искусственный интеллект, я...'",
        "Ты апнул Корпус А (Сигмы) за первую неделю учебы.",
        "Ученик ливнул с контрольной по физике через окно первого этажа."
    ]
    
    if "current_meme" not in st.session_state:
        st.session_state.current_meme = random.choice(memes)
        
    st.info(f"Ситуация: {st.session_state.current_meme}")
    
    col1, col2 = st.columns(2)
    if col1.button("🟢 БАЗА (+5 IQ)"):
        st.session_state.user_iq += 5
        st.success("Правильно! Это чистая база.")
        st.session_state.current_meme = random.choice(memes)
        time.sleep(0.5)
        st.rerun()
        
    if col2.button("🔴 КРИНЖ (+5 IQ)"):
        st.session_state.user_iq += 5
        st.success("Согласны, это полный кринж!")
        st.session_state.current_meme = random.choice(memes)
        time.sleep(0.5)
        st.rerun()

# 3. МЕГАЯЩИК
elif page == "Мегаящик 🎰":
    st.title("🎁 Симулятор Мегаящика")
    st.write("Слей 20 IQ ради крутого скина! Испытай удачу!")
    
    if st.button("Открыть Мегаящик (Цена: 20 IQ) 💥"):
        if st.session_state.user_iq - 20 < 80:
            st.error("⚠️ Недостаточно IQ! Минимальный порог 80 очков, чтобы никто не обиделся. Иди фарми рейтинг!")
        else:
            st.session_state.user_iq -= 20
            with st.spinner("Ящик трясется... Внутри что-то мигает..."):
                time.sleep(1.5)
            
            loot_pool = ["Скин: Золотой Сигма Леон 🦁", "Скин: Масик Эль Примо 🌹", "Скин: Альтушка Нани 💅", "Скин: Тюбик Поко 💀"]
            won_skin = random.choice(loot_pool)
            
            if won_skin not in st.session_state.skins:
                st.session_state.skins.append(won_skin)
            
            st.balloons() # Салют st.balloons прямо на лету!
            st.success(f"🎉 ПРЕДМЕТОВ: 1! Тебе выпал {won_skin}!")

# 4. МОИ СКИНЫ
elif page == "Мои Скины 👑":
    st.title("👕 Твой гардероб для флекса")
    st.write("Все твои открытые скины из Мегаящика:")
    for skin in st.session_state.skins:
        st.write(f"- {skin}")
