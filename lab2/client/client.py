import streamlit as st
import requests

BASE_URL = 'http://localhost:5000'

st.title("Управление людьми")

def get_persons():
    try:
        response = requests.get(f'{BASE_URL}/persons')
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Ошибка при выполнении GET-запроса: {e}")
        return []


def add_person(name, surname, email, age):
    data = {
        'name': name,
        'surname': surname,
        'email': email,
        'age': age
    }
    try:
        response = requests.post(f'{BASE_URL}/persons', json=data)
        response.raise_for_status()
        st.success(response.json().get('message', 'Человек успешно добавлен!'))
    except requests.exceptions.RequestException as e:
        st.error(f"Ошибка при выполнении POST-запроса: {e}")


with st.form("add_person_form"):
    st.write("Добавить нового человека")
    name = st.text_input("Имя")
    surname = st.text_input("Фамилия")
    email = st.text_input("Email")
    age = st.number_input("Возраст", min_value=1, max_value=99)
    submitted = st.form_submit_button("Добавить")
    if submitted:
        if name and surname and email and age:
            add_person(name, surname, email, age)
        else:
            st.warning("Все поля должны быть заполнены!")


if st.button("Получить список людей"):
    persons = get_persons()
    if persons:
        st.write("Список людей:")
        for person in persons:
            st.write(f"ID: {person[0]}, Имя: {person[1]}, Фамилия: {person[2]}, Email: {person[3]}, Возраст: {person[4]}")
    else:
        st.write("Список людей пуст.")