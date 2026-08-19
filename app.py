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
    except FileNotFoundError as error:
        return jsonify(error=str(error)), 500
    except Exception:
        app.logger.exception("Erro ao processar o arquivo Excel")
        return jsonify(error="Não foi possível processar essa planilha. Confira se ela é um arquivo .xlsx válido."), 500

def generate_menu(df):
    base_path = os.path.join(os.path.dirname(__file__), 'cardapio_base.jpg')
    if not os.path.isfile(base_path):
        raise FileNotFoundError('O arquivo cardapio_base.jpg não foi encontrado no projeto.')

    get = lambda row, column: '' if pd.isna(df.iloc[row, column]) else str(df.iloc[row, column])
    data_inicio = pd.to_datetime(df.iloc[1, 1])
    data_fim = pd.to_datetime(df.iloc[1, 5])
    periodo = f'{data_inicio:%d/%m} a {data_fim:%d/%m}'

    columns = range(1, 6)
    eventos = [texto_evento(get(2, column)) for column in columns]
    pratos = [[get(row, column) for row in (3, 4, 5, 6)] for column in columns]
    differe = get(12, 5)

    img = Image.open(base_path).convert('RGB')
    draw = ImageDraw.Draw(img)
    fonts_dir = os.path.join(os.path.dirname(__file__), 'fontes')
    fonte_periodo = load_font(os.path.join(fonts_dir, 'Exo-Bold.ttf'), 46)
    fonte_prato = load_font(os.path.join(fonts_dir, 'calibri.ttf'), 20)
    fonte_evento = load_font(os.path.join(fonts_dir, 'Exo-Bold.ttf'), 24)

    draw.text((1150, 90), periodo, fill='#13A8C8', font=fonte_periodo)
    coordenadas = (100, 375, 655, 930, 1205)
    linhas = (373, 465, 555, 655)
    for x, valores in zip(coordenadas, pratos):
        for y, texto in zip(linhas, valores):
            escrever_multilinha(draw, fonte_prato, x, y, texto)
    escrever_multilinha(draw, fonte_prato, 1205, 740, differe)
    for x, evento in zip(coordenadas, eventos):
        escrever_evento(draw, fonte_evento, x, 270, evento)

    output = BytesIO()
    img.save(output, format='PNG')
    output.seek(0)
    return send_file(output, mimetype='image/png', as_attachment=True, download_name=f'Cardapio_{data_inicio:%d-%m}_a_{data_fim:%d-%m}.png')


def texto_evento(texto):
    return 'Sabor da Casa' if texto.strip().lower() in {'segunda', 'terça', 'terca', 'quarta', 'quinta', 'sexta'} else texto


def quebrar_texto(draw, font, texto, largura_max):
    linhas = []
    linha = ''
    for palavra in str(texto).split():
        teste = f'{linha} {palavra}'.strip()
        if draw.textbbox((0, 0), teste, font=font)[2] <= largura_max:
            linha = teste
        else:
            if linha:
                linhas.append(linha)
            linha = palavra
    if linha:
        linhas.append(linha)
    return linhas or ['']


def escrever_multilinha(draw, font, x, y, texto):
    for index, linha in enumerate(quebrar_texto(draw, font, texto, 250)):
        draw.text((x, y + index * 24), linha, fill='#041621', font=font)


def escrever_evento(draw, font, x, y, texto):
    escrever_multilinha(draw, font, x, y, texto)


def load_font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.load_default()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))