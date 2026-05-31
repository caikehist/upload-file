import os
from flask import Flask, render_template, request, redirect, send_from_directory, url_for

app = Flask(__name__)

# Pasta onde os arquivos serão salvos (será criada automaticamente)
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'arquivos_servidos')
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# Define um limite de tamanho se quiser (ex: 16MB)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 

# 1. Endpoint Principal: Lista os arquivos
@app.route('/')
def index():
    # Lista todos os arquivos da pasta, ignorando arquivos ocultos
    files = [f for f in os.listdir(app.config['UPLOAD_FOLDER']) if not f.startswith('.')]
    return render_template('index.html', files=files)

# 2. Endpoint de Upload
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(url_for('index'))
    
    file = request.files['file']
    
    if file.filename == '':
        return redirect(url_for('index'))
    
    if file:
        # Salva o arquivo com o nome original
        # Para sistemas antigos/internos, mantemos o nome original. 
        # Caso vá para a web, use secure_filename da Werkzeug.
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        
    return redirect(url_for('index'))

# 3. Endpoint de Download
@app.route('/download/<filename>')
def download_file(filename):
    # as_attachment=True força o navegador antigo a baixar em vez de tentar renderizar
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

# 4. Endpoint de Exclusão (Usando POST nativo do formulário HTML)
@app.route('/delete/<filename>', methods=['POST'])
def delete_file(filename):
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if os.path.exists(filepath):
        os.remove(filepath)
    return redirect(url_for('index'))

if __name__ == '__main__':
    # Roda o servidor acessível por qualquer dispositivo na mesma rede (0.0.0.0) na porta 5000
    app.run(host='0.0.0.0', port=5000, debug=True)