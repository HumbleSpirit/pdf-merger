from flask import Flask, render_template, request, redirect, url_for, send_file, flash
import os
import PyPDF2
from werkzeug.utils import secure_filename
import uuid
import shutil
from io import BytesIO

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Ограничение размера файла: 16MB

# Проверка допустимых расширений файлов
ALLOWED_EXTENSIONS = {'pdf'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    # Очистка старых временных файлов
    for item in os.listdir(app.config['UPLOAD_FOLDER']):
        item_path = os.path.join(app.config['UPLOAD_FOLDER'], item)
        if os.path.isfile(item_path):
            os.remove(item_path)
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'files[]' not in request.files:
        flash('Файлы не были выбраны')
        return redirect(request.url)
    
    files = request.files.getlist('files[]')
    
    if not files or files[0].filename == '':
        flash('Файлы не были выбраны')
        return redirect(request.url)
    
    file_list = []
    
    for file in files:
        if file and allowed_file(file.filename):
            # Генерация уникального имени файла
            filename = secure_filename(file.filename)
            unique_filename = f"{uuid.uuid4()}_{filename}"
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
            file.save(filepath)
            
            # Получение количества страниц в PDF
            try:
                with open(filepath, 'rb') as f:
                    pdf = PyPDF2.PdfReader(f)
                    page_count = len(pdf.pages)
                
                file_list.append({
                    'original_name': filename,
                    'filename': unique_filename,
                    'pages': page_count
                })
            except Exception as e:
                os.remove(filepath)  # Удаляем файл, если не удалось обработать
                flash(f'Ошибка при обработке файла {filename}: {str(e)}')
        else:
            flash(f'Файл {file.filename} имеет недопустимое расширение. Разрешены только PDF-файлы.')
    
    if not file_list:
        flash('Не удалось обработать загруженные файлы')
        return redirect(url_for('index'))
    
    return render_template('arrange.html', files=file_list)

@app.route('/merge', methods=['POST'])
def merge_files():
    file_order = request.form.getlist('file_order')
    
    if not file_order:
        flash('Нет файлов для объединения')
        return redirect(url_for('index'))
    
    # Переменная для отслеживания, добавили ли мы хоть один файл
    any_files_merged = False
    
    # Используем try-except блок с более детальной обработкой ошибок
    try:
        merger = PyPDF2.PdfMerger(strict=False)  # Используем strict=False
        
        for filename in file_order:
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            try:
                # Сначала пробуем открыть и проверить файл
                with open(filepath, 'rb') as f:
                    pdf = PyPDF2.PdfReader(f, strict=False)
                    # Проверяем, что можем прочитать количество страниц
                    _ = len(pdf.pages)
                
                # Если всё в порядке, добавляем файл к объединению
                merger.append(filepath)
                any_files_merged = True  # Отмечаем, что добавили файл
            except Exception as file_error:
                flash(f'Пропущен файл {os.path.basename(filepath)}: {str(file_error)}')
                continue  # Пропускаем проблемный файл
        
        # Проверяем, были ли добавлены файлы для объединения
        if not any_files_merged:
            flash('Нет валидных файлов для объединения')
            return redirect(url_for('index'))
        
        # Сохранение объединенного PDF в памяти
        output_buffer = BytesIO()
        merger.write(output_buffer)
        output_buffer.seek(0)
        
        return send_file(
            output_buffer,
            mimetype='application/pdf',
            as_attachment=True,
            download_name='merged_document.pdf'
        )
    except Exception as e:
        flash(f'Ошибка при объединении файлов: {str(e)}')
        return redirect(url_for('index'))
    finally:
        if 'merger' in locals():
            merger.close()

if __name__ == '__main__':
    # Создание директории для загрузок, если её нет
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(host='0.0.0.0', debug=False)
    