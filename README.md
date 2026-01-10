# 🇹🇷 Türkçe RAG (Retrieval-Augmented Generation) Asistanı

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![AI](https://img.shields.io/badge/AI-RAG-orange)
![Ollama](https://img.shields.io/badge/LLM-Local-green)

Bu proje, **Doğal Dil İşleme (NLP)** ve **Üretken Yapay Zeka (Generative AI)** tekniklerini kullanarak, Türkçe dokümanlar (PDF) üzerinden soru-cevap yapabilen, yerel (local) çalışan akıllı bir asistandır.

Proje, **YZT | MEVZUU** takımı kapsamında geliştirilmiştir.

## 🚀 Proje Hakkında

Bu sistem, klasik anahtar kelime aramasının ötesine geçerek **Anlamsal Arama (Semantic Search)** yapar. Kullanıcı bir soru sorduğunda, sistem dokümanı okur, sorunun cevabının bulunduğu paragrafı bulur ve **LLM (Büyük Dil Modeli)** kullanarak insan benzeri bir cevap üretir.

### Temel Özellikler
* **📄 Doküman İşleme:** PDF dosyalarını okuma ve parçalama.
* **🧹 Gelişmiş Preprocessing:** Türkçe'ye özel Stemming (Kök bulma), Stop-word temizliği ve Tokenization.
* **🧠 Vektör Veritabanı:** `ChromaDB` ve `Sentence Transformers` kullanılarak verilerin anlamsal olarak saklanması.
* **🤖 RAG Mimarisi:** Retrieval (Bilgi Getirme) + Generation (Cevap Üretme) entegrasyonu.
* **💬 Prompt Engineering:** Zero-shot, One-shot ve Few-shot tekniklerinin karşılaştırmalı uygulaması.
* **🔒 Anti-Hallucination:** Modelin uydurmasını engelleyen "Grounding" mekanizması.

---

## 🛠️ Mimari ve Teknolojiler

Proje 4 ana modülden oluşmaktadır:

| Modül | Açıklama | Kullanılan Teknoloji |
| :--- | :--- | :--- |
| **NLP Motoru** | Metin temizleme ve kök bulma işlemleri. | `NLTK`, `TurkishStemmer` |
| **Retrieval (Klasik)** | İstatistiksel kelime eşleştirme (Baseline). | `Scikit-learn (TF-IDF)` |
| **Vector DB** | Metinleri vektör uzayına gömme ve anlamsal arama. | `ChromaDB`, `BERT (Turkish)` |
| **Generator** | Cevap üretme ve akıl yürütme. | `Ollama`, `gpt-oss:120b-cloud` |

---

## ⚙️ Kurulum ve Çalıştırma

Projeyi kendi bilgisayarınızda çalıştırmak için aşağıdaki adımları sırasıyla uygulayın.

### Ön Gereksinimler
* Python 3.10 veya üzeri
* Git
* [Ollama](https://ollama.com/) (Yerel LLM sunucusu için)

### 1. Depoyu Klonlayın
```bash
git clone [https://github.com/uludagai-club/YZT-MEVZUU-2026.git](https://github.com/uludagai-club/YZT-MEVZUU-2026.git)
cd YZT-MEVZUU-2026
```
### 2. Sanal Ortamı Kurun (Önerilen)
```bash
# Windows için:
python -m venv venv
.\venv\Scripts\activate

# Mac/Linux için:
python3 -m venv venv
source venv/bin/activate
```
### 3. Kütüphaneleri Yükleyin
```bash
pip install -r requirements.txt
```
### 4. Ollama Modelini Hazırlayın
Projenin kullandığı modeli yerel sunucunuza çekin:
```bash
ollama pull gpt-oss:120b-cloud
```
(Eğer bu özel model erişilebilir değilse, ollama pull llama3 veya gemma komutlarını kullanabilir ve kodda model ismini güncelleyebilirsiniz.)

## ▶️ Kullanım

Proje iki aşamada çalışır: **Öğrenme** ve **Sorgulama**.

### Adım 1: Hafızayı Oluşturma (İndeksleme)
PDF dosyasını analiz edip Vektör Veritabanına kaydetmek için:
```bash
python vector_db.py
```
(Bu işlem sadece yeni bir PDF eklendiğinde bir kez yapılır.)

### Adım 2: Asistanı Başlatma
Sistemi interaktif modda çalıştırmak için:
```bash
python main.py
```
Program açıldığında sorularınızı yöneltebilir ve Zero-shot / Few-shot modları arasında seçim yapabilirsiniz.

## 📊 Deneysel Sonuçlar ve Gözlemler

Proje geliştirme sürecinde yapılan testlerde (Örn: *Küçük Prens* kitabı üzerinde) şu kritik gözlemler yapılmıştır:

1.  **Anlamsal Arama Başarısı (Semantic Search):**
    * Klasik TF-IDF yöntemi kelime eşleşmesine dayalı olduğu için "duygusal bağ" sorgusunda sonuç veremezken, geliştirdiğimiz **Embedding tabanlı RAG mimarisi** bu sorguyu kitabın "evcilleştirmek" (bağ kurmak) ile ilgili bölümüyle (Sayfa 62) başarıyla eşleştirmiştir.

2.  **Prompt Tekniklerinin Etkisi:**
    * **Zero-shot:** Model daha özgür, detaylı ve edebi bir dil kullanma eğilimindedir. (Örn: Tilki'nin sırrını açıklarken metaforlar kullanması).
    * **One-shot / Few-shot:** Modele örnek verildiğinde cevaplar daha yapılandırılmış, net ve doğrudan sonuca odaklı hale gelmiştir.

3.  **Halüsinasyon Engelleme (Anti-Hallucination):**
    * Sisteme veri setinde bulunmayan tuzak sorular (Örn: *"Küçük Prens İstanbul'a ne zaman gitti?"*) sorulduğunda, model dış dünyadaki bilgilerini karıştırmadan **"Metinde bu bilgi yer almamaktadır"** yanıtını vermiştir. Bu, `main.py` içindeki sistem prompt'unun ("Sadece verilen metne bağlı kal") başarıyla çalıştığını kanıtlar.

4.  **Muhakeme (Reasoning) Yeteneği:**
    * Karmaşık tarihsel anlatımlarda (Örn: Gökbilimcinin keşif tarihi 1909 vs 1920), Zero-shot tekniğinin bazen detayları karıştırabildiği, ancak Few-shot tekniği ile modelin dikkatinin arttırılabildiği gözlemlenmiştir.

## 📂 Proje Yapısı

```text
YZT_RAG_PROJE/
├── 📂 chroma_db/        # Oluşturulan Vektör Veritabanı (Otomatik oluşur)
├── 📂 venv/             # Python Sanal Ortam klasörü
├── 📂 __pycache__/      # Python derleme önbelleği (Otomatik oluşur)
├── 📄 .gitignore        # Git tarafından yok sayılacak dosyalar
├── 📄 kucuk_prens.pdf   # Analiz edilen kaynak PDF dokümanı
├── 📄 main.py           # PROJE GİRİŞİ: RAG Asistanı ve LLM sorgulama kodu
├── 📄 pdf_search.py     # Klasik TF-IDF arama motoru (Baz karşılaştırma için)
├── 📄 preprocessing.py  # Türkçe NLP kütüphanesi (Stemming ve temizlik işlemleri)
├── 📄 README.md         # Proje raporu ve kullanım dokümanı
├── 📄 requirements.txt  # Gerekli Python kütüphaneleri listesi
└── 📄 vector_db.py      # Embedding ve vektör veritabanı kurulum kodu
```

---

## 📧 İletişim

**Geliştirici:** Sudem Kırmız
**Takım:** YZT | MEVZUU
**GitHub:** [https://github.com/sudemkirmiz](https://github.com/sudemkirmiz)
