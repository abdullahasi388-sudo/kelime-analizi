# 📊 Kelime Analiz Sistemi - Heap Data Structure

Modern bir kelime frekans analiz sistemi. TXT dosyalarındaki kelimeleri **sıfırdan yazılmış Heap Data Structure** kullanarak analiz eder.

## 🎯 Proje Amacı

Bir TXT dosyasındaki tüm kelimeleri okuyup, kelimelerin kaç kez geçtiğini hesaplamak ve bunları **özel Heap yapısı** ile sıralamak.

## ✨ Özellikler

### Teknik Özellikler
- ✅ **Sıfırdan yazılmış Heap Data Structure** (hazır kütüphane kullanılmadı)
- ✅ **Max Heap** implementasyonu
- ✅ Özel sıralama kuralları:
  - Kelimenin ilk harfine göre (A-Z)
  - Aynı harfle başlayan kelimelerde tekrar sayısına göre (çoktan aza)
- ✅ `heapify_up()` ve `heapify_down()` fonksiyonları
- ✅ `insert()`, `extract_max()`, `update_word()` operasyonları

### Arayüz Özellikleri
- ✅ Modern Dashboard tasarımı
- ✅ İki giriş seçeneği:
  - Dosya yükleme (Drag & Drop)
  - Doğrudan metin yazma
- ✅ Dark Mode / Light Mode
- ✅ Responsive tasarım
- ✅ Glassmorphism efektleri

### Görselleştirme
- ✅ İstatistik kartları
- ✅ Kelime arama
- ✅ Sıralı kelime tablosu
- ✅ **Heap Tree görselleştirmesi** (D3.js)
- ✅ **Chart.js grafikleri**:
  - En çok kullanılan 10 kelime
  - Harf dağılımı
  - Harf bazlı istatistikler

## 🏗️ Proje Yapısı

```
project/
│
├── app.py                      # Flask backend
├── heap.py                     # Custom Heap Data Structure
├── requirements.txt            # Python bağımlılıkları
├── sample_text.txt            # Örnek test dosyası
├── README.md                  # Bu dosya
├── HEAP_ALGORITMA_ACIKLAMASI.md  # Heap algoritması detayları
│
├── templates/
│   └── index.html             # Ana HTML sayfası
│
├── static/
│   ├── css/
│   │   └── style.css          # Modern CSS tasarımı
│   └── js/
│       └── script.js          # JavaScript kodları
│
└── uploads/                   # Yüklenen dosyalar (otomatik oluşur)
```

## 🚀 Kurulum ve Çalıştırma

### 1. Gereksinimler
- Python 3.8 veya üzeri
- pip (Python paket yöneticisi)

### 2. Bağımlılıkları Yükleyin

```bash
pip install -r requirements.txt
```

### 3. Uygulamayı Başlatın

```bash
python app.py
```

### 4. Tarayıcıda Açın

```
http://localhost:5000
```

## 📖 Kullanım

### Yöntem 1: Dosya Yükleme
1. Ana sayfada "Dosya Yükle" seçeneğini seçin
2. Bir TXT dosyası sürükleyip bırakın veya "Dosya Seç" butonuna tıklayın
3. Sistem otomatik olarak dosyayı analiz eder

### Yöntem 2: Metin Yazma
1. "Metin Yaz" seçeneğine tıklayın
2. Metninizi yazın veya yapıştırın (minimum 10 kelime)
3. "Analiz Et" butonuna tıklayın

### Sonuçları Görüntüleme
- **İstatistikler**: Genel bilgiler
- **Kelime Listesi**: Heap'e göre sıralanmış tüm kelimeler
- **Heap Yapısı**: Binary tree görselleştirmesi
- **Grafikler**: Çeşitli istatistiksel grafikler

## 🧮 Heap Data Structure Detayları

### Heap Kuralları

1. **İlk Harf Sıralaması**: Kelimeler önce ilk harflerine göre A'dan Z'ye sıralanır
2. **Tekrar Sayısı**: Aynı harfle başlayan kelimeler, en çok tekrar edenden en az tekrar edene doğru sıralanır
3. **Max Heap Property**: Parent node, child node'lardan her zaman daha önceliklidir

### Heap Fonksiyonları

#### `insert(word)`
Yeni kelime ekler veya mevcut kelimenin count'unu artırır.

#### `heapify_up(index)`
Heap property'yi yukarı doğru düzeltir.

#### `heapify_down(index)`
Heap property'yi aşağı doğru düzeltir.

#### `extract_max()`
En öncelikli elemanı çıkarır ve döndürür.

### Karmaşıklık Analizi

- **Insert**: O(log n)
- **Extract Max**: O(log n)
- **Heapify Up**: O(log n)
- **Heapify Down**: O(log n)
- **Search**: O(1) - HashMap kullanımı sayesinde

## 🎨 Teknolojiler

### Backend
- **Python 3.x**: Ana programlama dili
- **Flask**: Web framework
- **Custom Heap**: Sıfırdan yazılmış veri yapısı

### Frontend
- **HTML5**: Yapı
- **CSS3**: Modern tasarım ve animasyonlar
- **JavaScript (ES6+)**: İnteraktif özellikler
- **Chart.js**: Grafik görselleştirme
- **D3.js**: Heap tree görselleştirme
- **Font Awesome**: İkonlar

## 📊 Örnek Çıktı

### Heap Sıralaması Örneği
```
1. algoritma (a) - 5 kez
2. analiz (a) - 3 kez
3. bilimi (b) - 4 kez
4. başlangıç (b) - 2 kez
5. çok (ç) - 8 kez
```

## 🎓 Önemli Notlar

- **Sıfırdan Heap**: Hiçbir hazır kütüphane kullanılmadı (`heapq` ❌, `sort()` ❌)
- **İki Anahtarlı Sıralama**: İlk harf + tekrar sayısı
- **Verimli**: O(log n) operasyonlar
- **Görsel**: D3.js ile tree görselleştirme

## 📝 Detaylı Dokümantasyon

Heap algoritmasının detaylı açıklaması için `HEAP_ALGORITMA_ACIKLAMASI.md` dosyasına bakın.

---

**Proje tamamen tamamlanmıştır ve kullanıma hazırdır!** 🚀
