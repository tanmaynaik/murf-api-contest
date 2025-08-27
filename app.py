from flask import Flask, render_template, request
from flask_cors import CORS
from murf import Murf

client = Murf(
    api_key="ap2_54e91e5e-8ac8-4d96-ab04-cdae5ff7a0f3",
)

def translate_text(text, locale):
    response = client.text.translate(
        target_language=locale,
        texts=[text],
    )
    return response.translations[0].translated_text

app = Flask(__name__)
CORS(app)

@app.route('/')
def home_display():
    return render_template("index.html")

@app.route('/', methods=["POST"])
def submit():
    text = request.form.get('paragraph')
    locale = request.form.get('language')
    translated_text = translate_text(text, locale)
    return render_template("index.html", translated_text=translated_text)

if __name__ == "__main__":
    app.run(debug=True)
