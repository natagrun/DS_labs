from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__)

def load_words(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            words = [word.strip().lower() for word in f.readlines()]
        return words
    except FileNotFoundError:
        print(f"Ошибка: Файл {filepath} не найден.")
        return []
    except Exception as e:
        print(f"Ошибка при загрузке файла: {e}")
        return []


word_file = os.path.join(os.path.dirname(__file__), "words.txt")
words = load_words(word_file)


def autocomplete(query, words_list):
    query = query.lower()
    return [word for word in words_list if word.startswith(query)][:10]



@app.route('/')
def index():
    return render_template('index.html')


@app.route('/autocomplete')
def autocomplete_route():
    query = request.args.get('query', '')
    suggestions = autocomplete(query, words)
    return jsonify(suggestions)


if __name__ == '__main__':
    app.run(debug=True)