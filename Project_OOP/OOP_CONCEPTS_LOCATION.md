# 📍 LOKASI KONSEP OOP DALAM KODE

## 1. 🔒 ENKAPSULASI (Encapsulation)
**Definisi:** Menyembunyikan data/atribut dengan modifier akses (private/public)**

### Lokasi di rental_manager.py:
```python
class Kendaraan(ABC):
    def __init__(self, nopol, merk, harga_harian, is_listrik):
        # ❌ PRIVATE ATTRIBUTES (Enkapsulasi)
        self.__nopol = nopol              # ← Baris 12
        self.__merk = merk                # ← Baris 13
        self.__harga_harian = harga_harian # ← Baris 14
        self.__is_listrik = is_listrik    # ← Baris 15

    # ✅ PUBLIC GETTER METHODS (Akses terkontrol)
    def get_nopol(self):                  # ← Baris 17 (Enkapsulasi)
        return self.__nopol
    def get_merk(self):                   # ← Baris 18 (Enkapsulasi)
        return self.__merk
    def get_is_listrik(self):             # ← Baris 19 (Enkapsulasi)
        return self.__is_listrik
    def get_harga_harian(self):           # ← Baris 20 (Enkapsulasi)
        return self.__harga_harian
```

---

## 2. 🟦 ABSTRAKSI (Abstraction)
**Definisi:** Mendefinisikan interface/template tanpa implementasi detail**

### Lokasi di rental_manager.py:
```python
from abc import ABC, abstractmethod    # ← Import abstraction tools

# ❌ ABSTRACT CLASS (Abstraksi)
class Kendaraan(ABC):                  # ← Baris 5 (Abstraksi)
    @abstractmethod
    def get_jenis(self):               # ← Baris 26 (Abstraksi)
        pass                           # Method tanpa implementasi
```

**Penjelasan:**
- Class `Kendaraan` adalah **Abstract Class** yang tidak bisa diinstantiate langsung
- Method `get_jenis()` adalah **Abstract Method** yang harus di-override oleh class turunan
- Ini mendefinisikan "kontrak" apa yang harus dilakukan class turunan

---

## 3. 🔗 INHERITANCE (Pewarisan)
**Definisi:** Class turunan mewarisi properties & methods dari class induk**

### Lokasi di rental_manager.py:
```python
# ✅ INHERITANCE dari Kendaraan
class Mobil(Kendaraan):                # ← Baris 37 (Pewarisan)
    def get_jenis(self):
        return "Mobil"

class Motor(Kendaraan):                # ← Baris 40 (Pewarisan)
    def get_jenis(self):
        return "Motor"
```

**Penjelasan:**
- `Mobil` dan `Motor` mewarisi semua atribut & method dari `Kendaraan`
- Mereka punya akses ke: `get_nopol()`, `get_merk()`, `hitung_total_sewa()`, dll
- Mereka HARUS meng-override method abstrak `get_jenis()`

---

## 4. 🔄 POLIMORFISME (Polymorphism)
**Definisi:** Satu method nama, banyak implementasi berbeda**

### Lokasi di rental_manager.py:

#### ✅ POLIMORFISME TIPE 1: Method Overriding
```python
class Kendaraan(ABC):
    @abstractmethod
    def get_jenis(self):               # ← Template (Baris 26)
        pass

class Mobil(Kendaraan):
    def get_jenis(self):               # ← Override 1 (Baris 38)
        return "Mobil"

class Motor(Kendaraan):
    def get_jenis(self):               # ← Override 2 (Baris 41)
        return "Motor"
```

**Penjelasan:** Method `get_jenis()` sama nama, tapi return value BERBEDA tergantung class apa yang memanggilnya

#### ✅ POLIMORFISME TIPE 2: Conditional Logic (Runtime Behavior)
```python
def hitung_total_sewa(self, hari):     # ← Baris 28-31
    total = self.__harga_harian * hari
    # Behavior BERBEDA tergantung nilai __is_listrik
    if self.__is_listrik:              # ← Condition (Baris 31)
        total *= 0.9                   # Diskon 10% untuk listrik
    return total
```

**Penjelasan:** Method yang sama, tapi output bisa berbeda tergantung status kendaraan

#### ✅ POLIMORFISME TIPE 3: Duck Typing (dalam GUI)
```python
# Baris 52-53: Bisa memanggil method yang sama untuk object berbeda
self.daftar_kendaraan = [
    Mobil("B 1234 ABC", "Toyota Avanza", 300000, False),     # Object Mobil
    Motor("D 5678 XY", "Honda Vario", 75000, False),         # Object Motor
]

# Baris 63-64: Kedua object bisa memanggil method yang sama
[f"{v.get_jenis()} - {v.get_merk()}" for v in self.daftar_kendaraan]
# Mobil → "Mobil"
# Motor → "Motor"
```

---

## 📊 RINGKASAN LOKASI

| OOP Concept | File | Class | Baris | Keterangan |
|---|---|---|---|---|
| **Enkapsulasi** | rental_manager.py | Kendaraan | 12-20 | Private attributes + getter methods |
| **Abstraksi** | rental_manager.py | Kendaraan | 5, 26 | ABC + @abstractmethod |
| **Inheritance** | rental_manager.py | Mobil, Motor | 37, 40 | Extends Kendaraan |
| **Polymorphism** | rental_manager.py | Mobil, Motor | 38, 41, 28-31 | Override + conditional logic |

---

## 🎯 FLOW PENGGUNAAN 4 OOP CONCEPTS

```
1. ABSTRAKSI (ABC)
   ↓ Mendefinisikan template method get_jenis() & hitung_total_sewa()
   
2. ENKAPSULASI (__nopol, __merk, dll)
   ↓ Menyembunyikan data, akses via getter
   
3. INHERITANCE (Mobil extends Kendaraan, Motor extends Kendaraan)
   ↓ Mewarisi semua attributes & methods
   
4. POLYMORPHISM (Override get_jenis() berbeda, conditional di hitung_total_sewa())
   ↓ Method sama, behavior berbeda
   
RESULT: System rental yang fleksibel & maintainable ✅
```

---

## 💡 CONTOH PENGGUNAAN SEMUA KONSEP BERSAMAAN

```python
# Di file rental_manager.py baris 76-82
def proses_sewa(self):
    kendaraan = self.daftar_kendaraan[idx]  # Ambil Mobil atau Motor
    total = kendaraan.hitung_total_sewa(hari)  # ← POLYMORPHISM (behavior berbeda)
    
    # Semua object punya method ini karena INHERITANCE
    # Data aman karena ENKAPSULASI (via getter)
    # Template tercapai karena ABSTRAKSI (ABC)
```

**Penjelasan:**
- Kita ambil kendaraan (bisa Mobil atau Motor) → **INHERITANCE** sudah aktif
- Kita panggil `hitung_total_sewa()` → **POLYMORPHISM** berbeda output (ada diskon atau tidak)
- Kita akses data via `get_merk()` → **ENKAPSULASI** melindungi data
- Semua ini dimungkinkan karena **ABSTRAKSI** mendefinisikan kontrak

✅ **SEMUA 4 KONSEP BEKERJA BERSAMA!**
