from io import BytesIO

from flask import Flask, jsonify, render_template, request, send_file
import os
import pandas as pd
from PIL import Image, ImageDraw

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file part", 400
    file = request.files['file']
    if file.filename == '':
        return "No selected file", 400
    if not file.filename.lower().endswith('.xlsx'):
        return jsonify(error="Envie um arquivo Excel no formato .xlsx."), 400

    try:
        df = pd.read_excel(file, header=None, engine='openpyxl')
        return generate_menu(df)
    except Exception:
        app.logger.exception("Erro ao processar o arquivo Excel")
        return jsonify(error="Não foi possível processar essa planilha. Confira se ela é um arquivo .xlsx válido."), 500

def generate_menu(df):
    img = Image.new('RGB', (1200, 800), color='white')
    draw = ImageDraw.Draw(img)
    draw.text((10, 10), "Menu", fill="black")

    output = BytesIO()
    img.save(output, format='PNG')
    output.seek(0)
    return send_file(output, mimetype='image/png', as_attachment=True, download_name='Cardapio.png')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))