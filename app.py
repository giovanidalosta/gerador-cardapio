from io import BytesIO

from flask import Flask, jsonify, render_template, request, send_file
import os
import pandas as pd
from PIL import Image, ImageDraw, ImageFont

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
    data = df.fillna('').astype(str)
    data = data.loc[(data != '').any(axis=1), (data != '').any(axis=0)]
    if data.empty:
        raise ValueError('A planilha não possui dados preenchidos.')

    width, height = 1200, 800
    img = Image.new('RGB', (width, height), '#081b2a')
    draw = ImageDraw.Draw(img)
    fonts_dir = os.path.join(os.path.dirname(__file__), 'fontes')
    title_font = load_font(os.path.join(fonts_dir, 'Exo-Bold.ttf'), 42)
    header_font = load_font(os.path.join(fonts_dir, 'Exo-Bold.ttf'), 20)
    body_font = load_font(os.path.join(fonts_dir, 'calibri.ttf'), 20)

    draw.rectangle((0, 0, width, 115), fill='#123d52')
    draw.text((60, 28), 'CARDÁPIO', font=title_font, fill='#f1fbff')
    draw.text((width - 60, 43), 'Gerado automaticamente', font=body_font, fill='#9fd3df', anchor='ra')

    left, top = 60, 160
    table_width = width - 120
    columns = len(data.columns)
    column_width = table_width // columns
    row_height = min(62, max(42, (height - top - 55) // (len(data) + 1)))

    for row_index, row in enumerate(data.itertuples(index=False, name=None)):
        y = top + row_index * row_height
        is_header = row_index == 0 and len(data) > 1
        fill = '#1b5368' if is_header else ('#102f42' if row_index % 2 else '#0d2637')
        draw.rounded_rectangle((left, y, left + table_width, y + row_height - 4), radius=8, fill=fill)
        font = header_font if is_header else body_font
        for column_index, value in enumerate(row):
            x = left + column_index * column_width + 18
            text = shorten_text(value, column_width - 32)
            draw.text((x, y + row_height // 2 - 2), text, font=font, fill='#f0f8fc', anchor='lm')

    output = BytesIO()
    img.save(output, format='PNG')
    output.seek(0)
    return send_file(output, mimetype='image/png', as_attachment=True, download_name='Cardapio.png')


def load_font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.load_default()


def shorten_text(value, max_width):
    text = str(value).strip()
    while text and ImageFont.load_default().getlength(text) > max_width:
        text = text[:-1]
    return text if text == str(value).strip() else text.rstrip() + '...'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))