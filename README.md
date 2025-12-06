# 🇹🇷 Turkish Clickbait Detection System

Bu proje, Türkçe haber başlıklarını analiz ederek **"Clickbait" (Tık Tuzağı)** veya **"Normal Haber"** olarak sınıflandıran bir Doğal Dil İşleme (NLP) uygulamasıdır.

## 🚀 Proje Özellikleri
* **Stemming Desteği:** `TurkishStemmer` kütüphanesi ile Türkçe kelime köklerini bulur (Örn: "yapıldı" -> "yap").
* **Görselleştirme:** Clickbait ve Normal haberlerde en sık geçen kelimeleri **WordCloud** ile görselleştirir.
* **Başarı Oranı:** Genişletilmiş veri seti ve stratify yöntemi ile yüksek doğruluk oranı hedeflenmiştir.

## 🛠️ Kurulum

1. Projeyi indirin.
2. Gerekli kütüphaneleri yükleyin:
   ```bash
   pip install -r requirements.txt