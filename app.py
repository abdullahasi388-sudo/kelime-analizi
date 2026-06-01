"""
Flask Backend - Kelime Analiz Sistemi
Bu uygulama TXT dosyalarındaki kelimeleri analiz eder ve Heap yapısı ile sıralar.
"""

from flask import Flask, render_template, request, jsonify
import os
import re
from heap import CustomHeap
from werkzeug.utils import secure_filename
from datetime import datetime
import json
from datetime import datetime
import json

app = Flask(__name__)

# Konfigürasyon
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['HISTORY_FOLDER'] = 'history'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
ALLOWED_EXTENSIONS = {'txt'}

# Klasörleri oluştur
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['HISTORY_FOLDER'], exist_ok=True)

# İşlem sayacı dosyası
COUNTER_FILE = os.path.join(app.config['HISTORY_FOLDER'], 'counter.txt')

def get_next_operation_number():
    """Sonraki işlem numarasını al"""
    if os.path.exists(COUNTER_FILE):
        with open(COUNTER_FILE, 'r') as f:
            counter = int(f.read().strip())
    else:
        counter = 0
    
    counter += 1
    
    with open(COUNTER_FILE, 'w') as f:
        f.write(str(counter))
    
    return counter

def save_operation_history(operation_number, text_content, statistics):
    """İşlem geçmişini kaydet"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # Metin dosyası olarak kaydet
    history_file = os.path.join(
        app.config['HISTORY_FOLDER'], 
        f'islem_{operation_number}.txt'
    )
    
    with open(history_file, 'w', encoding='utf-8') as f:
        f.write(f"{'='*70}\n")
        f.write(f"İŞLEM NUMARASI: {operation_number}\n")
        f.write(f"TARİH: {timestamp}\n")
        f.write(f"{'='*70}\n\n")
        
        f.write(f"İSTATİSTİKLER:\n")
        f.write(f"- Toplam Kelime: {statistics['total_words']}\n")
        f.write(f"- Benzersiz Kelime: {statistics['unique_words']}\n")
        if statistics['most_common']:
            f.write(f"- En Çok Kullanılan: {statistics['most_common']['word']} ({statistics['most_common']['count']} kez)\n")
        f.write(f"\n{'='*70}\n\n")
        
        f.write(f"ANALİZ EDİLEN METİN:\n")
        f.write(f"{'-'*70}\n")
        f.write(text_content)
        f.write(f"\n{'-'*70}\n")
    
    # JSON olarak da kaydet (isteğe bağlı)
    json_file = os.path.join(
        app.config['HISTORY_FOLDER'], 
        f'islem_{operation_number}.json'
    )
    
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump({
            'operation_number': operation_number,
            'timestamp': timestamp,
            'text': text_content,
            'statistics': statistics
        }, f, ensure_ascii=False, indent=2)

def allowed_file(filename):
    """Dosya uzantısı kontrolü"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def clean_word(word):
    """
    Kelimeyi temizle: noktalama işaretlerini kaldır, küçük harfe çevir
    """
    # Sadece harf ve rakamları tut
    cleaned = re.sub(r'[^a-zA-ZğüşıöçĞÜŞİÖÇ0-9]', '', word)
    return cleaned.lower()

def process_text_file(filepath):
    """
    TXT dosyasını oku ve kelimeleri analiz et
    """
    heap = CustomHeap()
    
    try:
        # Dosyayı farklı encoding'lerle dene
        encodings = ['utf-8', 'latin-1', 'cp1254', 'iso-8859-9']
        content = None
        
        for encoding in encodings:
            try:
                with open(filepath, 'r', encoding=encoding) as file:
                    content = file.read()
                break
            except UnicodeDecodeError:
                continue
        
        if content is None:
            return None, None, "Dosya okunamadı. Encoding hatası."
        
        # Kelimeleri ayır
        words = content.split()
        
        # Her kelimeyi temizle ve heap'e ekle
        for word in words:
            cleaned_word = clean_word(word)
            
            # Boş string veya sadece rakamlardan oluşan kelimeleri atla
            if cleaned_word and not cleaned_word.isdigit() and len(cleaned_word) > 1:
                heap.insert(cleaned_word)
        
        return heap, content, None
    
    except Exception as e:
        return None, None, f"Hata: {str(e)}"

@app.route('/')
def index():
    """Ana sayfa"""
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    """
    Dosya yükleme endpoint'i
    """
    # Dosya kontrolü
    if 'file' not in request.files:
        return jsonify({'error': 'Dosya bulunamadı'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'Dosya seçilmedi'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'error': 'Sadece .txt dosyaları yüklenebilir'}), 400
    
    try:
        # Dosyayı kaydet
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Dosyayı işle
        heap, text_content, error = process_text_file(filepath)
        
        if error:
            return jsonify({'error': error}), 500
        
        # İstatistikleri al
        statistics = heap.get_statistics()
        
        # İşlem numarasını al
        operation_number = get_next_operation_number()
        
        # Geçmişe kaydet
        save_operation_history(operation_number, text_content, statistics)
        
        # Sıralı kelime listesini al
        sorted_words = heap.get_all_words()
        
        # Heap yapısını al (görselleştirme için)
        heap_structure = heap.get_heap_structure()
        
        # Harf bazlı gruplandırma
        letter_groups = {}
        for word_data in sorted_words:
            letter = word_data['first_letter']
            if letter not in letter_groups:
                letter_groups[letter] = []
            letter_groups[letter].append(word_data)
        
        # En çok kullanılan 10 kelime
        top_10_words = sorted_words[:10] if len(sorted_words) >= 10 else sorted_words
        
        # Harf bazlı istatistikler (grafik için)
        letter_stats = {}
        for letter, words in letter_groups.items():
            letter_stats[letter] = {
                'count': len(words),
                'total_occurrences': sum(w['count'] for w in words)
            }
        
        # Dosyayı sil (güvenlik için)
        os.remove(filepath)
        
        return jsonify({
            'success': True,
            'operation_number': operation_number,
            'statistics': statistics,
            'words': sorted_words,
            'heap_structure': heap_structure,
            'letter_groups': letter_groups,
            'top_10_words': top_10_words,
            'letter_stats': letter_stats
        })
    
    except Exception as e:
        return jsonify({'error': f'Beklenmeyen hata: {str(e)}'}), 500

@app.route('/search', methods=['POST'])
def search_word():
    """
    Kelime arama endpoint'i
    """
    data = request.get_json()
    search_term = data.get('search_term', '').lower()
    words = data.get('words', [])
    
    if not search_term:
        return jsonify({'results': words})
    
    # Kelimeyi ara
    results = [w for w in words if search_term in w['word']]
    
    return jsonify({'results': results})

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    print("=" * 60)
    print("🚀 Kelime Analiz Sistemi Başlatılıyor...")
    print("=" * 60)
    print("📊 Heap Data Structure ile Kelime Frekans Analizi")
    print("🌐 Tarayıcınızda açın: http://localhost:5000")
    print("=" * 60)
    # Production ortamında debug=False olmalı
    debug_mode = os.environ.get('FLASK_ENV') != 'production'
    app.run(debug=debug_mode, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
