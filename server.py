import os
import requests
from pathlib import Path
from dotenv import load_dotenv
from flask import Flask, render_template, request, url_for, flash, redirect

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('FLASK_KEY')

BASE_URL = 'https://morse-code-parser-and-generator-apiverve.p.rapidapi.com/v1'
API_HEADERS = headers = {
                'x-rapidapi-key': os.getenv('API_KEY'),
                'x-rapidapi-host': 'morse-code-parser-and-generator-apiverve.p.rapidapi.com',
                'Content-Type': 'application/json'
            }

BASE_DIR = Path(__file__).resolve().parent
TtM_path = BASE_DIR / 'utilities' / 'TtM.json'
MtT_path = BASE_DIR / 'utilities' / 'MtT.json'

@app.route('/', methods=['GET', 'POST'])
def render():
    if request.method == 'POST':
        translation_type = request.form.get('translationType')
        translation_content = request.form.get('translationContent')

        translation = ''

        if translation_type == 'MtT':

            payload = {
                'morse': translation_content
            }

            res = requests.post(f'{BASE_URL}/decodemorsecode', headers=headers, json=payload)
            res.raise_for_status()
            translation_json = res.json()

            translation = translation_json['data']['text']

        elif translation_type == "TtM":

            payload = {
                'text': translation_content
            }

            res = requests.post(f'{BASE_URL}/encodemorsecode', headers=headers, json=payload)
            res.raise_for_status()
            translation_json = res.json()

            translation = translation_json['data']['morse']

        else:
            return render_template('error.html')
        
        if translation == ' ':
            flash('Please enter a valid input for the translation type')
            return redirect(url_for('render'))

        return render_template('results.html', translation=translation)
    return render_template('index.html')

if __name__ == "__main__":
    app.run()