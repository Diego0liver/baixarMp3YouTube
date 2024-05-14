from app import app
from flask import render_template, request, current_app, send_file, send_from_directory
from pytube import YouTube
import pyshorteners
import os
import qrcode
from datetime import datetime

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/baixarVideo')
def baixarYoutube():
    return render_template('baixarYoutube.html')

@app.route('/baixarMp3', methods=['POST'])
def baixarMp3():
    url = request.form['urlMp3']
    pasta = current_app.root_path
    
    yt = YouTube(url)
    titulo_video = yt.title

    caracteres_invalidos = r'<>:"/\|?*'
    for char in caracteres_invalidos:
        titulo_video = titulo_video.replace(char, '')

    nome_arquivo = titulo_video + ".mp3"

    audio = yt.streams.filter(only_audio=True).first()

    arquivo_destino = os.path.join(pasta, nome_arquivo)

    audio.download(output_path=pasta, filename=nome_arquivo)

    os.rename(os.path.join(pasta, nome_arquivo), arquivo_destino)
    
    return send_file(arquivo_destino, as_attachment=True)

@app.route('/baixarMp4', methods=['POST'])
def baixarMp4():
    url = request.form['urlMp4']
    pasta = current_app.root_path
    
    yt = YouTube(url)
    titulo_video = yt.title
    resolucao = '720p'
    caracteres_invalidos = r'<>:"/\|?*'
    for char in caracteres_invalidos:
        titulo_video = titulo_video.replace(char, '')

    video = yt.streams.filter(res=resolucao, file_extension='mp4').first()
    nome_arquivo = titulo_video + ".mp4"

    arquivo_destino = os.path.join(pasta, nome_arquivo)

    video.download(output_path=pasta, filename=nome_arquivo)

    os.rename(os.path.join(pasta, nome_arquivo), arquivo_destino)

    return send_file(arquivo_destino, as_attachment=True)

@app.route('/encurtarLink', methods=['GET', 'POST'])
def encurtarLink():
    new_link = None
    if request.method == 'POST':
        url = request.form['url']
        shortener = pyshorteners.Shortener()
        new_link = shortener.tinyurl.short(url)
    return render_template('encurtarLink.html', new_link=new_link)

@app.route('/gerarQrCode', methods=['GET', 'POST'])
def gerarQrCode():
    if request.method == 'POST':
        url = request.form['linkQr']
        img = qrcode.make(url)
        now = datetime.now()
        pasta_destino = 'app/static/img/qrcode'
        os.makedirs(pasta_destino, exist_ok=True)
        timestamp = now.strftime("%Y-%m-%d_%H-%M-%S-%f")    
        nome_arquivo = f"qrcodes_{timestamp}.png"
        img.save(os.path.join(pasta_destino, nome_arquivo))
        return send_file(pasta_destino, as_attachment=True)
    return render_template('gerarQrCode.html')

if __name__ == '__main__':
    app.run(debug=True)