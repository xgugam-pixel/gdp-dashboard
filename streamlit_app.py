import streamlit as st
import time
from google import genai
from google.genai import types

# Инициализация живого клиента Gemini через секреты хостинга
def get_gemini_client():
    try:
        api_key = st.secrets["GEMINI_API_KEY"]
        return genai.Client(api_key=api_key)
    except Exception:
        return None

# Скрипт запуска чата (эту функцию мы вызовем в главном файле)
def run_chat():
    st.title("🤖 Чит-код AI: База от экспертов")
    st.write("Спроси ИИ о любой сложной теме. Он переведет это на язык Сигм!")

    subject = st.selectbox("Выбери предмет для настройки ответа:", 
                           ["Математика", "Русский язык", "Физика", "История", "Химия"])

    # Показываем историю переписки лентой
    for role, text in st.session_state.chat_history:
        with st.chat_message(role):
            st.write(text)

    # Строка ввода сообщения внизу экрана
    user_input = st.chat_input("Напиши свой вопрос сюда...")

    if user_input:
        if not st.session_state.is_vip and st.session_state.user_iq <= 80:
            st.error("Твой IQ упал до 80! Иди апай рейтинг в Мемный Судья!")
        else:
            # Отображаем вопрос школьника
            with st.chat_message("user"):
                st.write(user_input)
            st.session_state.chat_history.append(("user", user_input))

            # Обращение к настоящему ИИ Gemini
            with st.spinner("ИИ думает над чит-кодом..."):
                client = get_gemini_client()
                if client:
                    try:
                        # Системная инструкция внутри запроса
                        prompt = f"Ты Чит-код AI для школьников. Объясни предмет {subject} на молодежном сленге (сигма, кринж, база, имба, масик). Пиши коротко, разбивай по строкам. Вопрос: {user_input}"
                        response = client.models.generate_content(
                            model='gemini-2.5-flash',
                            contents=prompt
                        )
                        answer = response.text
                    except Exception as e:
                        answer = f"Ошибка подключения к Gemini: {str(e)}"
                else:
                    # Утешительный ответ, если ключ еще не вставлен в настройки
                    answer = f"Бот-заглушка: Тема {subject} - это полная имба! Чтобы получить настоящий ответ от Gemini, добавь API-ключ в настройки Secrets."

            # Отображаем ответ ИИ
            with st.chat_message("assistant"):
                st.write(answer)
            st.session_state.chat_history.append(("assistant", answer))

            # Списание баллов за вопрос
            if not st.session_state.is_vip:
                st.session_state.user_iq = max(80, st.session_state.user_iq - 2)

            st.rerun()
