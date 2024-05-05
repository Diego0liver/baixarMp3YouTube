from app import app
from flask import render_template, request, current_app, send_file
from pytube import YouTube
import os

@app.route('/')
def index():
    return render_template('index.html')

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

if __name__ == '__main__':
    app.run(debug=True)