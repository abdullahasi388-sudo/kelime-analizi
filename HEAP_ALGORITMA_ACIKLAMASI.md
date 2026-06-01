# 🔧 Heap Algoritması Detaylı Açıklama

## 📚 Heap Nedir?

Heap, **complete binary tree** (tam ikili ağaç) yapısında özel bir veri yapısıdır. Bu projede **Max Heap** kullanılmıştır.

### Heap Özellikleri
1. **Complete Binary Tree**: Her seviye soldan sağa dolu, son seviye hariç
2. **Heap Property**: Parent node, child node'lardan önceliklidir
3. **Array Representation**: Tree yapısı array ile temsil edilir

## 🎯 Bu Projedeki Özel Heap

### Sıralama Kuralları
Bu projede heap, **iki anahtara** göre sıralama yapar:

1. **Birincil Anahtar**: Kelimenin ilk harfi (A-Z)
2. **İkincil Anahtar**: Tekrar sayısı (çoktan aza)

### Karşılaştırma Fonksiyonu

```python
def _compare(self, node1, node2):
    """
    node1 > node2 ise True döner (heap property için)
    """
    # 1. İlk harfleri karşılaştır
    if node1.first_letter != node2.first_letter:
        return node1.first_letter < node2.first_letter  # a < b < c
    
    # 2. Aynı harfse, count'a bak
    return node1.count > node2.count  # Büyük count önce
```

### Örnek Sıralama

Kelimeler:
- apple: 5 kez
- banana: 3 kez
- apricot: 7 kez
- cherry: 4 kez
- avocado: 2 kez

Heap sıralaması:
1. **apricot** (a, 7) - İlk harf 'a', en çok tekrar
2. **apple** (a, 5) - İlk harf 'a', ikinci en çok
3. **avocado** (a, 2) - İlk harf 'a', en az
4. **banana** (b, 3) - İlk harf 'b'
5. **cherry** (c, 4) - İlk harf 'c'

## 🔄 Heap Operasyonları

### 1. INSERT (Ekleme)

**Algoritma:**
1. Yeni elemanı array'in sonuna ekle
2. `heapify_up()` ile yukarı çıkar

**Kod:**
```python
def insert(self, word):
    word_lower = word.lower()
    
    # Kelime varsa count'u artır
    if word_lower in self.word_map:
        self.update_word(word_lower)
        return
    
    # Yeni kelime ekle
    new_node = WordNode(word_lower)
    self.heap.append(new_node)
    new_index = len(self.heap) - 1
    self.word_map[word_lower] = new_index
    
    # Heap property'yi düzelt
    self.heapify_up(new_index)
```

**Örnek:**
```
Başlangıç:
        [apple:5]
       /         \
   [banana:3]   [cherry:4]

"date:6" ekle:

Adım 1: Sona ekle
        [apple:5]
       /         \
   [banana:3]   [cherry:4]
   /
[date:6]

Adım 2: heapify_up
        [apple:5]
       /         \
   [date:6]     [cherry:4]
   /
[banana:3]
```

**Karmaşıklık:** O(log n)

### 2. HEAPIFY_UP (Yukarı Düzeltme)

**Algoritma:**
1. Current node'u parent ile karşılaştır
2. Current > parent ise swap yap
3. Root'a ulaşana kadar tekrarla

**Kod:**
```python
def heapify_up(self, index):
    while self._has_parent(index):
        parent_idx = self._parent_index(index)
        
        # Current node parent'tan büyükse
        if self._compare(self.heap[index], self.heap[parent_idx]):
            self._swap(index, parent_idx)
            index = parent_idx
        else:
            break
```

**Görsel Örnek:**
```
Başlangıç:
        [apple:5]
       /         \
   [banana:3]   [cherry:4]
   /
[apricot:7]  <- Yeni eklendi

Adım 1: apricot vs banana
        [apple:5]
       /         \
   [apricot:7]  [cherry:4]
   /
[banana:3]

Adım 2: apricot vs apple
        [apricot:7]
       /           \
   [apple:5]      [cherry:4]
   /
[banana:3]
```

**Karmaşıklık:** O(log n)

### 3. EXTRACT_MAX (En Büyüğü Çıkar)

**Algoritma:**
1. Root'u kaydet (return edilecek)
2. Son elemanı root'a taşı
3. `heapify_down()` ile aşağı indir

**Kod:**
```python
def extract_max(self):
    if self.is_empty():
        return None
    
    # Root'u al
    max_node = self.heap[0]
    del self.word_map[max_node.word]
    
    if len(self.heap) == 1:
        self.heap.pop()
        return max_node
    
    # Son elemanı root'a taşı
    last_node = self.heap.pop()
    self.heap[0] = last_node
    self.word_map[last_node.word] = 0
    
    # Heap property'yi düzelt
    self.heapify_down(0)
    
    return max_node
```

**Görsel Örnek:**
```
Başlangıç:
        [apricot:7]
       /           \
   [apple:5]      [cherry:4]
   /
[banana:3]

Adım 1: Root'u çıkar, son elemanı root'a taşı
        [banana:3]
       /           \
   [apple:5]      [cherry:4]

Adım 2: heapify_down
        [apple:5]
       /         \
   [banana:3]   [cherry:4]
```

**Karmaşıklık:** O(log n)

### 4. HEAPIFY_DOWN (Aşağı Düzeltme)

**Algoritma:**
1. Current node'u child'lar ile karşılaştır
2. En büyük child'ı bul
3. Current < child ise swap yap
4. Leaf'e ulaşana kadar tekrarla

**Kod:**
```python
def heapify_down(self, index):
    while self._has_left_child(index):
        # En büyük child'ı bul
        larger_child_idx = self._left_child_index(index)
        
        if self._has_right_child(index):
            right_idx = self._right_child_index(index)
            if self._compare(self.heap[right_idx], self.heap[larger_child_idx]):
                larger_child_idx = right_idx
        
        # Current node child'dan büyükse, tamam
        if self._compare(self.heap[index], self.heap[larger_child_idx]):
            break
        
        # Swap yap ve devam et
        self._swap(index, larger_child_idx)
        index = larger_child_idx
```

**Görsel Örnek:**
```
Başlangıç:
        [banana:3]
       /           \
   [apple:5]      [cherry:4]

Adım 1: banana vs apple, cherry
        [apple:5]
       /         \
   [banana:3]   [cherry:4]
```

**Karmaşıklık:** O(log n)

### 5. UPDATE_WORD (Kelime Güncelle)

**Algoritma:**
1. Kelimeyi HashMap'te bul
2. Count'u artır
3. `heapify_up()` ile yukarı çıkar (count arttığı için)

**Kod:**
```python
def update_word(self, word):
    word_lower = word.lower()
    
    if word_lower not in self.word_map:
        return
    
    index = self.word_map[word_lower]
    self.heap[index].count += 1
    
    # Count arttığı için yukarı çıkabilir
    self.heapify_up(index)
```

**Karmaşıklık:** O(log n)

## 📊 Array Representation

Heap, array ile temsil edilir. Index hesaplamaları:

```python
# Parent index
parent_index = (index - 1) // 2

# Left child index
left_child_index = 2 * index + 1

# Right child index
right_child_index = 2 * index + 2
```

**Örnek:**
```
Tree:
        [0]
       /   \
     [1]   [2]
     / \   / \
   [3][4][5][6]

Array: [0, 1, 2, 3, 4, 5, 6]

Index 1'in:
- Parent: (1-1)//2 = 0
- Left child: 2*1+1 = 3
- Right child: 2*1+2 = 4
```

## 🎯 Karmaşıklık Analizi

| Operasyon | Zaman Karmaşıklığı | Açıklama |
|-----------|-------------------|----------|
| Insert | O(log n) | heapify_up çağrısı |
| Extract Max | O(log n) | heapify_down çağrısı |
| Heapify Up | O(log n) | Tree yüksekliği |
| Heapify Down | O(log n) | Tree yüksekliği |
| Update Word | O(log n) | heapify_up çağrısı |
| Search | O(1) | HashMap kullanımı |
| Peek | O(1) | Root'a erişim |

**Not:** Tree yüksekliği = log₂(n)

## 🔍 HashMap Kullanımı

Heap'te kelime aramayı hızlandırmak için HashMap kullanılır:

```python
self.word_map = {}  # word -> index mapping

# Ekleme
self.word_map[word] = index

# Arama
if word in self.word_map:
    index = self.word_map[word]

# Silme
del self.word_map[word]
```

**Avantaj:** O(n) yerine O(1) arama

## 🎨 Görselleştirme

### Complete Binary Tree
```
Level 0:        [1]
Level 1:      /     \
            [2]     [3]
Level 2:   /  \    /  \
         [4] [5] [6] [7]
```

### Max Heap Property
```
Parent >= Children

        [10]
       /    \
     [8]    [9]
    /  \   /  \
  [5] [6][7] [4]
```

### Bu Projedeki Heap
```
        [apricot:7]  (a, 7)
       /            \
   [apple:5]      [banana:3]
   (a, 5)         (b, 3)
    /    \
[avocado:2] [cherry:4]
(a, 2)      (c, 4)
```

## 💡 Neden Heap?

### Avantajlar
1. **Verimli sıralama**: O(log n) insert
2. **Dinamik**: Sürekli güncelleme yapılabilir
3. **Öncelik kuyrukları**: En öncelikli eleman hızlıca bulunur
4. **Bellek verimli**: Array ile temsil

### Alternatifler ve Karşılaştırma

| Veri Yapısı | Insert | Search | Sort |
|-------------|--------|--------|------|
| Array + Sort | O(1) | O(n) | O(n log n) |
| Heap | O(log n) | O(1)* | O(n log n) |
| BST | O(log n) | O(log n) | O(n) |

*HashMap ile

## 🎓 Sunum İçin Önemli Noktalar

1. **Heap Property**: Parent > Children
2. **Complete Binary Tree**: Soldan sağa dolu
3. **Array Representation**: Index formülleri
4. **İki Anahtarlı Sıralama**: İlk harf + count
5. **O(log n) Operasyonlar**: Verimli
6. **HashMap Optimizasyonu**: O(1) arama
7. **Heapify Up/Down**: Heap property'yi koruma

## 📝 Örnek Senaryo

### Kelimeler
```
python: 5
flask: 3
heap: 4
python: 1 (güncelleme)
algorithm: 2
```

### Heap Oluşumu

**1. "python:5" ekle**
```
[python:5]
```

**2. "flask:3" ekle**
```
    [flask:3]
    /
[python:5]
```
(f < p, flask yukarı)

**3. "heap:4" ekle**
```
    [flask:3]
    /        \
[heap:4]  [python:5]
```

**4. "python" güncelle (5→6)**
```
    [flask:3]
    /        \
[heap:4]  [python:6]
```
heapify_up çağrılır, ama p > h, değişiklik yok

**5. "algorithm:2" ekle**
```
        [algorithm:2]
       /             \
    [flask:3]      [heap:4]
    /
[python:6]
```
(a < f, algorithm yukarı çıkar)

**Final Heap:**
```
        [algorithm:2]
       /             \
    [flask:3]      [heap:4]
    /
[python:6]
```

**Sıralı Liste:**
1. algorithm: 2
2. flask: 3
3. heap: 4
4. python: 6

---

**Bu açıklama, heap algoritmasının nasıl çalıştığını detaylı bir şekilde göstermektedir. Sunum sırasında bu örnekleri kullanabilirsiniz! 🚀**
