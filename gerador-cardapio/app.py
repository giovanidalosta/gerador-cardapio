from flask import Flask, render_template, request, send_file
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
    if file and file.filename.endswith('.xlsx'):
        df = pd.read_excel(file, header=None)
        return generate_menu(df)
    return "Invalid file format", 400

def generate_menu(df):
    # Define your drawing logic here using the provided code
    # This is a placeholder for the actual image generation logic
    img = Image.new('RGB', (1200, 800), color='white')
    draw = ImageDraw.Draw(img)
    
    # Example of drawing text (you would replace this with your actual logic)
    draw.text((10, 10), "Menu", fill="black")
    
    # Save the image
    output_path = os.path.join('CardapiosGerados', 'generated_menu.png')
    img.save(output_path)
    
    return send_file(output_path, as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))