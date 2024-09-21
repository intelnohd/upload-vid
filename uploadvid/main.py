import os
import uuid
from flask import Flask, request, redirect, url_for, render_template, send_from_directory

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # Ограничение на размер файла (100 MB)

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# Главная страница с формой для загрузки видео
@app.route('/')
def index():
    return render_template('index.html')

# Загрузка видео
@app.route('/upload', methods=['POST'])
def upload_video():
    if 'video' not in request.files:
        return 'Нет видеофайла'
    file = request.files['video']
    if file.filename == '':
        return 'Файл не выбран'
    if file:
        filename = f"{uuid.uuid4().hex}_{file.filename}"
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return redirect(url_for('video', video_id=filename))

# Отображение видео по уникальной ссылке
@app.route('/video/<video_id>')
def video(video_id):
    return render_template('video.html', video_url=url_for('uploaded_file', filename=video_id))

# Обслуживание загруженных файлов
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)
