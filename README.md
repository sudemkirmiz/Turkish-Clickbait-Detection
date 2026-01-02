# 🇹🇷 Turkish Clickbait Detection System (Türkçe Tık Tuzağı Tespit Sistemi)

![Python](https://img.shields.io/badge/Python-3.x-blue.svg)
![NLP](https://img.shields.io/badge/NLP-Natural_Language_Processing-green.svg)
![Algorithm](https://img.shields.io/badge/Model-Logistic_Regression-orange.svg)
![Status](https://img.shields.io/badge/Status-Active-success.svg)

## 📌 Proje Tanımı
Bu proje, Türkçe haber sitelerinde, sosyal medyada ve video platformlarında sıkça karşılaşılan **"Clickbait" (Tık Tuzağı)** başlıklarını tespit etmek amacıyla geliştirilmiş ileri seviye bir **Doğal Dil İşleme (NLP)** projesidir.

Sistemin önceki versiyonlarından en büyük farkı; sadece kelimelere değil, **cümlenin bağlamına (context)**, **kelime öbeklerine (n-grams)** ve **noktalama işaretlerinin kullanım şekline** (Örn: "!!!", "...") odaklanmasıdır. Model, bir dedektif gibi davranarak hem dil bilgisel hem de görsel ipuçlarını analiz eder.

## ✨ Temel Özellikler (YENİ)
* **🕵️‍♀️ Akıllı Noktalama Analizi:** Standart NLP süreçlerinin aksine, bu model noktalama işaretlerini silmez. Ünlem (`!`), üç nokta (`...`) ve soru işaretlerini (`?`) birer "duygu belirteci" olarak analiz eder.
* **🔗 N-Gram Analizi (1-3):** Kelimelere tek tek bakmak yerine 3'lü gruplar halinde bakar. (Örn: *"Şok"* kelimesi yerine *"Şok şok şok"* kalıbını ayırt eder).
* **🇹🇷 Türkçe Stemming:** `TurkishStemmer` ile kelimeler köklerine indirgenir ancak özel kalıplar ve noktalama işaretleri korunur.
* **🧠 Logistic Regression:** Olasılık tabanlı sınıflandırma ile daha kararlı sonuçlar üretir (`predict_proba` yeteneği sayesinde güven skoru verir).
* **📊 Görsel Analiz:** Modelin performansını ölçmek için **Confusion Matrix (Hata Matrisi)** ısı haritası oluşturur.

## 🧰 Kullanılan Teknolojiler ve Kütüphaneler

| Teknoloji | Amaç |
|---|---|
| **Python** | Ana programlama dili |
| **Scikit-learn** | Makine öğrenmesi (Logistic Regression, TF-IDF, Metrics) |
| **NLTK** | Metin ön işleme (Tokenization, Stopwords) |
| **TurkishStemmer** | Türkçe kelime köklerini bulma |
| **Pandas** | Veri manipülasyonu ve yönetimi |

## ⚙️ Kurulum ve Çalıştırma

Projeyi yerel bilgisayarınızda çalıştırmak için aşağıdaki adımları sırasıyla izleyin:

**1. Projeyi Bilgisayarınıza İndirin (Clone)**
Terminali açın ve aşağıdaki komutu yazarak projeyi bilgisayarınıza çekin:
```bash
git clone [https://github.com/sudemkirmiz/Turkish-Clickbait-Detection.git](https://github.com/sudemkirmiz/Turkish-Clickbait-Detection.git)
cd Turkish-Clickbait-Detection
```
**2. Sanal Ortamı Oluşturun (Önerilen) Kütüphanelerin çakışmaması için sanal ortam (virtual environment) oluşturmanız tavsiye edilir:**
```bash
# Windows için:
python -m venv venv
.\venv\Scripts\activate
```
```bash
# Mac/Linux için:
python3 -m venv venv
source venv/bin/activate
```
**3. Gerekli Kütüphaneleri Yükleyin Projenin çalışması için gereken paketleri yükleyin:**
```bash
pip install -r requirements.txt
# Veya manuel olarak:
pip install pandas numpy nltk TurkishStemmer scikit-learn
```
**4. Uygulamayı Çalıştırın Kurulum tamamlandıktan sonra projeyi başlatın:**
```bash
python main.py
```

## 🧠 Nasıl Çalışır? (Teknik İş Akışı)

Proje, metni ham halden alıp sonuca ulaştırmak için aşağıdaki "Pipeline" (Boru Hattı) adımlarını izler:

1.  **Veri Yükleme:** `clickbait_dataset.csv` dosyasından haber başlıkları ve etiketleri (0: Normal, 1: Clickbait) yüklenir.
2.  **Akıllı Ön İşleme (Smart Preprocessing):**
    * Metin küçük harfe çevrilir.
    * Etkisiz kelimeler (Stop Words) temizlenir.
    * **ÖNEMLİ:** Standart temizliğin aksine, ünlem (`!`), soru işareti (`?`) ve üç nokta (`...`) **silinmez**, korunur.
    * Kelimeler `TurkishStemmer` ile köklerine indirgenir.
3.  **Vektörleştirme (TF-IDF):**
    * Metinler matematiksel vektörlere dönüştürülür.
    * `token_pattern=r'(?u)\S+'` ayarı ile noktalama işaretleri de birer kelime gibi işlenir.
    * `ngram_range=(1, 3)` kullanılarak kelime grupları (Örn: "şok şok şok") analiz edilir.
4.  **Model Eğitimi:** `Logistic Regression` algoritması, verideki bu desenleri ve olasılıkları öğrenir.
5.  **Canlı Test:** Kullanıcıdan alınan metin aynı işlemlerden geçirilip % (yüzde) olasılık skoru ile değerlendirilir.

## 📊 Örnek Senaryolar

Yeni modelin "noktalama duyarlılığı" ve "bağlam analizi" sayesinde yakaladığı bazı kritik farklar aşağıdadır:

| Haber Başlığı | Tahmin | Neden? |
|---|---|---|
| *"Doktorlar bu kürü öneriyor..."* | 🔴 **CLICKBAIT** | "Bu kür" kelimesi ve "..." (merak boşluğu) kullanımı tespit edildi. |
| *"Böyle kar görülmedi!!"* | 🔴 **CLICKBAIT** | Aşırı ünlem (`!!`) kullanımı yapay heyecan olarak algılandı. |
| *"Böyle kar görülmedi"* | 🔵 **NORMAL** | Aynı cümle, noktalama normal olduğu için güvenli bulundu. |
| *"Merkez Bankası faiz kararını açıkladı."* | 🔵 **NORMAL** | Bilgi verici, duygusal manipülasyon yok. |
| *"Sakın çöpe atmayın! Meğer..."* | 🔴 **CLICKBAIT** | "Sakın", "Meğer" kelimeleri ve ünlem kombinasyonu yakalandı. |

> **Not:** Model, %65 ve üzeri olasılık değerlerini "Clickbait" olarak işaretleyecek şekilde hassas ayarlanmıştır.

## 📂 Klasör Yapısı

```text
Turkish-Clickbait-Detection/
├── assets/
│   └── wordcloud.png    # Proje çıktısı (Kelime Bulutu görseli)
├── main.py              # Projenin ana kaynak kodu
├── requirements.txt     # Gerekli kütüphane listesi
├── .gitignore           # Gereksiz dosyaların yüklenmesini engeller
└── README.md            # Proje dokümantasyonu
```
>Geliştirici: Sudem Kırmız. Bu proje NLP öğrenim sürecimin bir parçası olarak geliştirilmiştir