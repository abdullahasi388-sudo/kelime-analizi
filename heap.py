"""
Custom Heap Data Structure Implementation
Bu dosya, kelime analizi için özel tasarlanmış bir Max Heap yapısı içerir.
Heap, kelimeleri önce ilk harflerine (A-Z), sonra tekrar sayılarına göre sıralar.
"""

class WordNode:
    """
    Heap'te saklanacak kelime düğümü
    """
    def __init__(self, word, count=1):
        self.word = word.lower()  # Kelimeyi küçük harfe çevir
        self.count = count  # Tekrar sayısı
        self.first_letter = word[0].lower() if word else 'z'
    
    def __repr__(self):
        return f"WordNode('{self.word}', count={self.count})"


class CustomHeap:
    """
    Özel Max Heap implementasyonu
    Sıralama kuralları:
    1. İlk harfe göre A'dan Z'ye (alfabetik)
    2. Aynı harfle başlayanlar: En çok tekrar eden önce gelir
    """
    
    def __init__(self):
        self.heap = []  # Heap array'i
        self.word_map = {}  # Kelime -> index mapping (hızlı arama için)
    
    def size(self):
        """Heap'teki eleman sayısı"""
        return len(self.heap)
    
    def is_empty(self):
        """Heap boş mu?"""
        return len(self.heap) == 0
    
    def _parent_index(self, index):
        """Parent node'un index'ini döndür"""
        return (index - 1) // 2
    
    def _left_child_index(self, index):
        """Sol child'ın index'ini döndür"""
        return 2 * index + 1
    
    def _right_child_index(self, index):
        """Sağ child'ın index'ini döndür"""
        return 2 * index + 2
    
    def _has_parent(self, index):
        """Parent var mı?"""
        return self._parent_index(index) >= 0
    
    def _has_left_child(self, index):
        """Sol child var mı?"""
        return self._left_child_index(index) < len(self.heap)
    
    def _has_right_child(self, index):
        """Sağ child var mı?"""
        return self._right_child_index(index) < len(self.heap)
    
    def _compare(self, node1, node2):
        """
        İki node'u karşılaştır
        Return: True if node1 > node2 (heap property için)
        
        Sıralama mantığı:
        1. İlk harf küçük olanı önce (a < b < c ...)
        2. Aynı harfse, count büyük olanı önce
        """
        # İlk harfleri karşılaştır
        if node1.first_letter != node2.first_letter:
            return node1.first_letter < node2.first_letter
        
        # Aynı harfle başlıyorsa, count'a bak (büyük olan önce)
        return node1.count > node2.count
    
    def _swap(self, index1, index2):
        """İki elemanın yerini değiştir"""
        # Word map'i güncelle
        self.word_map[self.heap[index1].word] = index2
        self.word_map[self.heap[index2].word] = index1
        
        # Heap'te swap yap
        self.heap[index1], self.heap[index2] = self.heap[index2], self.heap[index1]
    
    def heapify_up(self, index):
        """
        Heap property'yi yukarı doğru düzelt
        Yeni eklenen eleman parent'ından büyükse yukarı çık
        """
        while self._has_parent(index):
            parent_idx = self._parent_index(index)
            
            # Eğer current node parent'tan büyükse (öncelikli ise)
            if self._compare(self.heap[index], self.heap[parent_idx]):
                self._swap(index, parent_idx)
                index = parent_idx
            else:
                break
    
    def heapify_down(self, index):
        """
        Heap property'yi aşağı doğru düzelt
        Root'tan başlayarak doğru pozisyona yerleştir
        """
        while self._has_left_child(index):
            # En büyük child'ı bul
            larger_child_idx = self._left_child_index(index)
            
            if self._has_right_child(index):
                right_idx = self._right_child_index(index)
                if self._compare(self.heap[right_idx], self.heap[larger_child_idx]):
                    larger_child_idx = right_idx
            
            # Eğer current node child'dan büyükse, heap property sağlanıyor
            if self._compare(self.heap[index], self.heap[larger_child_idx]):
                break
            
            # Değilse swap yap ve devam et
            self._swap(index, larger_child_idx)
            index = larger_child_idx
    
    def insert(self, word):
        """
        Yeni kelime ekle veya mevcut kelimenin count'unu artır
        """
        word_lower = word.lower()
        
        # Kelime zaten varsa count'unu artır
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
    
    def update_word(self, word):
        """
        Mevcut kelimenin count'unu artır ve heap'i yeniden düzenle
        """
        word_lower = word.lower()
        
        if word_lower not in self.word_map:
            return
        
        index = self.word_map[word_lower]
        self.heap[index].count += 1
        
        # Count arttığı için yukarı çıkabilir
        self.heapify_up(index)
    
    def extract_max(self):
        """
        En öncelikli elemanı çıkar ve döndür
        """
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
    
    def get_sorted_list(self):
        """
        Heap'teki tüm elemanları sıralı liste olarak döndür
        NOT: Bu işlem heap'i boşaltır!
        """
        sorted_list = []
        
        while not self.is_empty():
            node = self.extract_max()
            sorted_list.append({
                'word': node.word,
                'count': node.count,
                'first_letter': node.first_letter
            })
        
        return sorted_list
    
    def peek(self):
        """En öncelikli elemanı döndür (çıkarmadan)"""
        if self.is_empty():
            return None
        return self.heap[0]
    
    def get_all_words(self):
        """
        Tüm kelimeleri sıralı şekilde döndür (heap'i boşaltmadan)
        """
        # Heap'in kopyasını oluştur
        temp_heap = CustomHeap()
        temp_heap.heap = [WordNode(node.word, node.count) for node in self.heap]
        temp_heap.word_map = self.word_map.copy()
        
        # Kopyadan sıralı listeyi al
        return temp_heap.get_sorted_list()
    
    def get_statistics(self):
        """
        Heap hakkında istatistikler döndür
        """
        if self.is_empty():
            return {
                'total_words': 0,
                'unique_words': 0,
                'most_common': None,
                'total_occurrences': 0
            }
        
        total_occurrences = sum(node.count for node in self.heap)
        most_common = max(self.heap, key=lambda x: x.count)
        
        return {
            'total_words': total_occurrences,
            'unique_words': len(self.heap),
            'most_common': {
                'word': most_common.word,
                'count': most_common.count
            },
            'total_occurrences': total_occurrences
        }
    
    def get_heap_structure(self):
        """
        Heap'in tree yapısını görselleştirme için döndür
        """
        if self.is_empty():
            return []
        
        structure = []
        for i, node in enumerate(self.heap):
            node_data = {
                'id': i,
                'word': node.word,
                'count': node.count,
                'first_letter': node.first_letter,
                'parent': self._parent_index(i) if self._has_parent(i) else None,
                'left_child': self._left_child_index(i) if self._has_left_child(i) else None,
                'right_child': self._right_child_index(i) if self._has_right_child(i) else None
            }
            structure.append(node_data)
        
        return structure
