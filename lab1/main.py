from flask import Flask, render_template, request
import re

app = Flask(__name__)


@app.route('/lab1', methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
        name = request.form['name']
        age_str = request.form['age']
        email = request.form['email']
        msisdn = request.form['msisdn']

        is_valid = True
        errors = {}

        if not name:
            is_valid = False
            errors['name'] = 'Имя не может быть пустым.'
        try:
            age = int(age_str)
            if age <= 0:
                is_valid = False
                errors['age'] = 'Возраст должен быть положительным числом.'
        except ValueError:
            is_valid = False
            errors['age'] = 'Возраст должен быть числом.'
        else:
            age = int(age_str)

        if not email:
            is_valid = False
            errors['email'] = 'Email не может быть пустым.'
        elif not re.match(r"^[\w\.-]+@[\w\.-]+\.\w{2,4}$", email):
            is_valid = False
            errors['email'] = 'Email имеет неверный формат.'

        if not msisdn:
            is_valid = False
            errors['msisdn'] = 'Номер телефона не может быть пустым.'
        elif not re.match(r"^\+7\d{10}$", msisdn):
            is_valid = False
            errors['msisdn'] = 'Номер телефона имеет неверный формат.'

        if is_valid:
            return render_template('result.html', name=name, age=age, email=email, msisdn=msisdn)
        else:
            return render_template('form.html', errors=errors)

    return render_template('form.html')


if __name__ == '__main__':
    app.run(debug=True)