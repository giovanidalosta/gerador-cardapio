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

    days, menu_items = read_menu_data(data)
    width, height = 1365, 768
    img = Image.new('RGB', (width, height), '#06131f')
    draw = ImageDraw.Draw(img)
    fonts_dir = os.path.join(os.path.dirname(__file__), 'fontes')
    title_font = load_font(os.path.join(fonts_dir, 'Exo-Bold.ttf'), 51)
    day_font = load_font(os.path.join(fonts_dir, 'Exo-Bold.ttf'), 22)
    item_font = load_font(os.path.join(fonts_dir, 'Exo-Bold.ttf'), 18)
    footer_font = load_font(os.path.join(fonts_dir, 'Exo-Bold.ttf'), 21)

    for y in range(height):
        ratio = y / height
        color = (4, int(18 + 78 * ratio), int(30 + 110 * ratio))
        draw.line((0, y, width, y), fill=color)

    draw.text((78, 43), 'Cardápio', font=title_font, fill='#19a9ca')
    title_width = draw.textbbox((0, 0), 'Cardápio', font=title_font)[2]
    draw.text((88 + title_width, 49), 'Semanal', font=title_font, fill='#f2f6f8')

    card_left, card_top, card_width, card_height, gap = 76, 176, 237, 510, 8
    labels = ['De casa 1:', 'De casa 2', 'Acompanhamento', 'Levissimo']
    for day_index, day in enumerate(days):
        left = card_left + day_index * (card_width + gap)
        draw.rounded_rectangle((left, card_top, left + card_width, card_top + card_height), radius=18, fill='#d4edf4')
        draw.rectangle((left, card_top + 31, left + card_width - 22, card_top + 54), fill='#1aa7c7')
        draw.text((left + 11, card_top + 42), day, font=day_font, fill='#eaf8fc', anchor='lm')

        for item_index, label in enumerate(labels):
            y = card_top + 127 + item_index * 82
            value = menu_items[day_index][item_index]
            draw.text((left + 14, y), value or label, font=item_font, fill='#092031', anchor='lm')
            if item_index == 3:
                draw.rounded_rectangle((left + 7, y - 26, left + card_width - 12, y + 53), radius=12, fill='#84d3e2')
                draw.text((left + 14, y - 4), value or label, font=item_font, fill='#092031', anchor='lm')

    draw.text((76, 724), 'Cardápio sujeito a alterações', font=footer_font, fill='#f1f8fa')
    draw.text((1290, 724), 'ikatec', font=title_font, fill='#06131f', anchor='ra')
    draw.text((1290, 733), 'Tecnologia e Inovação', font=footer_font, fill='#06131f', anchor='ra')

    output = BytesIO()
    img.save(output, format='PNG')
    output.seek(0)
    return send_file(output, mimetype='image/png', as_attachment=True, download_name='Cardapio.png')


def read_menu_data(data):
    weekdays = ['segunda-feira', 'terça-feira', 'quarta-feira', 'quinta-feira', 'sexta-feira']
    rows = data.values.tolist()
    if len(data.columns) >= 5:
        first_row = [str(value).strip().lower() for value in rows[0]]
        has_day_header = any('segunda' in value or 'terça' in value or 'terca' in value for value in first_row)
        headers = [format_day(value, weekdays[index]) for index, value in enumerate(rows[0][:5])] if has_day_header else weekdays
        content = rows[1:] if has_day_header else rows
        items = [[str(row[index]).strip() if index < len(row) else '' for index in range(5)] for row in content[:4]]
        while len(items) < 4:
            items.append([''] * 5)
        return headers, [[items[row_index][day_index] for row_index in range(4)] for day_index in range(5)]
    raise ValueError('A planilha precisa ter pelo menos cinco colunas, uma para cada dia útil.')


def format_day(value, fallback):
    text = str(value).strip()
    return text if text else fallback


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