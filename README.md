# 🇹🇷 Turkish Clickbait Detection System (Türkçe Tık Tuzağı Tespit Sistemi)

![Python](https://img.shields.io/badge/Python-3.x-blue.svg)
![NLP](https://img.shields.io/badge/NLP-Natural_Language_Processing-green.svg)
![Status](https://img.shields.io/badge/Status-Completed-success.svg)

## 📌 Proje Tanımı
Bu proje, Türkçe haber sitelerinde ve sosyal medyada sıkça karşılaşılan **"Clickbait" (Tık Tuzağı)** başlıklarını tespit etmek amacıyla geliştirilmiş bir **Makine Öğrenmesi (Machine Learning)** uygulamasıdır. 

Sistem, haber başlıklarını analiz eder ve metin madenciliği yöntemlerini kullanarak başlığın okuyucuyu kandırmaya yönelik olup olmadığını (**CLICKBAIT** veya **NORMAL**) sınıflandırır.

## ✨ Temel Özellikler
* **Türkçe Doğal Dil İşleme:** Türkçe'nin yapısına uygun metin işleme süreçleri.
* **Gelişmiş Kök Bulma (Stemming):** `TurkishStemmer` kütüphanesi kullanılarak kelimeler köklerine indirgenir (Örn: *"yapıldı", "yapıyor", "yapacak"* -> **"yap"**).
* **TF-IDF Vektörleştirme:** Kelimelerin önem derecesini matematiksel ağırlıklarla belirleme.
* **Kelime Bulutu (Word Cloud):** Clickbait ve Normal haberlerde en çok geçen kelimeleri görselleştirme.
* **Yüksek Doğruluk:** Stratified Sampling ve genişletilmiş veri seti ile **~%87.5** doğruluk oranı.

## 🧰 Kullanılan Teknolojiler ve Kütüphaneler

| Teknoloji | Amaç |
|---|---|
| **Python** | Ana programlama dili |
| **Scikit-learn** | Makine öğrenmesi (Naive Bayes, TF-IDF, Split) |
| **NLTK** | Metin ön işleme (Tokenization, Stopwords) |
| **TurkishStemmer** | Türkçe kelime köklerini bulma |
| **Pandas** | Veri manipülasyonu ve yönetimi |
| **WordCloud** | Veri görselleştirme |

## ⚙️ Kurulum ve Çalıştırma

Projeyi yerel bilgisayarınızda çalıştırmak için aşağıdaki adımları izleyin:

**1. Projeyi Klonlayın**
```bash
git clone [https://github.com/sudemkirmiz/Turkish-Clickbait-Detection.git](https://github.com/sudemkirmiz/Turkish-Clickbait-Detection.git)
cd Turkish-Clickbait-Detection

**2. Gerekli Kütüphaneleri Yükleyin**
```bash
pip install -r requirements.txt
```

**3. Uygulamayı Çalıştırın**
```bash
python main.py
```

🧠 Nasıl Çalışır? (İş Akışı)
Proje, ham metni alıp tahmin üretmek için şu boru hattını (pipeline) izler:

Veri Yükleme: Örnek haber başlıkları ve etiketleri yüklenir.

Ön İşleme (Preprocessing):

Küçük harfe çevirme.

Noktalama işaretlerini kaldırma.

Etkisiz kelimeleri (Stop Words) temizleme.

Stemming: Kelimeleri köküne indirgeme (TurkishStemmer ile).

Vektörleştirme: Metinler TF-IDF yöntemiyle sayısal vektörlere dönüştürülür.

Model Eğitimi: Multinomial Naive Bayes algoritması ile model eğitilir.

Tahmin: Yeni gelen başlık analiz edilir.

## 📊 Sonuçlar ve Örnekler

Model, genişletilmiş veri seti ve Türkçe kök bulma (stemming) işlemi sayesinde zorlu örnekleri başarıyla ayırt edebilmektedir.

Aşağıda modelin test kümesinden ve gerçek hayat senaryolarından elde ettiği bazı tahminler yer almaktadır:

| Haber Başlığı | Tahmin | Durum |
|---|---|---|
| *"Doktorlar bu kürü öneriyor, hemen deneyin!"* | 🔴 **CLICKBAIT** | ✅ Başarılı |
| *"Belediye otobüs sefer saatlerinde düzenleme yaptı."* | 🔵 **NORMAL** | ✅ Başarılı |
| *"Flaş flaş! Görenler gözlerine inanamadı."* | 🔴 **CLICKBAIT** | ✅ Başarılı |
| *"Merkez Bankası faiz kararını açıkladı."* | 🔵 **NORMAL** | ✅ Başarılı |
| *"Sakın bu meyveyi kabuğuyla yemeyin!"* | 🔴 **CLICKBAIT** | ✅ Başarılı |

> **Not:** Modelin doğruluk oranı (Accuracy) test veri setinde **%87.5** olarak ölçülmüştür.

📂 Klasör Yapısı
Turkish-Clickbait-Detection/
├── main.py              # Projenin ana kaynak kodu
├── requirements.txt     # Gerekli kütüphane listesi
├── .gitignore           # Gereksiz dosyaların yüklenmesini engeller
└── README.md            # Proje dokümantasyonu

Geliştirici: Sudem Kırmız. Bu proje NLP öğrenim sürecimin bir parçası olarak geliştirilmiştir