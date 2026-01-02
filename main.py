import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns  # Grafikler için
import string 

# NLP Kütüphaneleri
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from TurkishStemmer import TurkishStemmer

# Makine Öğrenmesi (Scikit-Learn)
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression  # Daha kararlı algoritma
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

# Gerekli indirmeler (Sadece ilk çalışmada indirir)
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)

# 1. ADIM: VERİ HAZIRLIĞI VE YÜKLEME
print("\n 1. Veri seti yükleniyor...")

dosya_adi = 'clickbait_dataset.csv'

try:
    df = pd.read_csv(dosya_adi)
    # Etiketleri Sayısal Hale Getirelim (Eğer metinse) veya tam tersi
    # Bizim CSV'de 1 ve 0 var. 1=Clickbait, 0=Normal
    print(f"Başarılı! Toplam {len(df)} satır veri okundu.")
    
    # Veri setinde boş veri var mı kontrol et ve temizle
    if df.isnull().sum().any():
        print("Boş satırlar bulundu, temizleniyor...")
        df = df.dropna()
        
except FileNotFoundError:
    print(f"HATA: '{dosya_adi}' bulunamadı! Lütfen önce veri üretici kodunu çalıştırın.")
    exit()

# 2. ADIM: METİN ÖN İŞLEME FONKSİYONU
print("2. Metinler temizleniyor (Stemming & Stopwords)...")

stop_words = set(stopwords.words('turkish'))
stemmer = TurkishStemmer()

def metni_temizle(metin):
    """
    Noktalama işaretlerini koruyarak temizlik yapar.
    Clickbait'ler genelde '!' ve '...' kullanır, bunları atmamalıyız.
    """
    metin = str(metin).lower()
    
    # Kelimelere ayır
    kelimeler = word_tokenize(metin)
    
    temiz_kelimeler = []
    for kelime in kelimeler:
        # Stop words temizliği yapalım ama noktalama işaretlerini KORUYALIM
        # isalpha() yerine, noktalama işaretiyse DE ekle diyoruz.
        if (kelime.isalpha() or kelime in string.punctuation) and kelime not in stop_words:
            try:
                # Sadece harf ise kök bul, noktalama ise dokunma
                if kelime.isalpha():
                    kok = stemmer.stem(kelime)
                    temiz_kelimeler.append(kok)
                else:
                    temiz_kelimeler.append(kelime)
            except:
                temiz_kelimeler.append(kelime)
            
    return " ".join(temiz_kelimeler)

# Tüm veri setine bu fonksiyonu uygula
df['islenmis_veri'] = df['baslik'].apply(metni_temizle)

# 3. ADIM: ÖZELLİK ÇIKARIMI VE BÖLÜMLEME
print("3. Yapay Zeka için veriler matematiğe dökülüyor (TF-IDF)...")

tfidf = TfidfVectorizer(ngram_range=(1, 3), min_df=1, max_features=3000, token_pattern=r'(?u)\S+')

X = tfidf.fit_transform(df['islenmis_veri']) # Giriş verisi (Başlıklar)
y = df['etiket'] # Çıkış verisi (0 veya 1)

# Veriyi %80 Eğitim, %20 Test olarak ayır
# stratify=y -> Eğitim ve test setinde clickbait oranını eşit tutar.
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# 4. ADIM: MODEL EĞİTİMİ (LOGISTIC REGRESSION)
print(" 4. Model eğitiliyor...")

# Naive Bayes yerine Logistic Regression kullanıyoruz.
# Çünkü olasılık (yüzde kaç clickbait?) hesabında daha iyidir.
model = LogisticRegression(random_state=42)
model.fit(X_train, y_train)

# Başarı Skorunu Hesapla
y_pred = model.predict(X_test)
basari = accuracy_score(y_test, y_pred)

print(f"\n EĞİTİM TAMAMLANDI!")
print(f"Model Doğruluk Oranı: %{basari * 100:.2f}")

# Detaylı Rapor
print("\n--- Detaylı Sınıflandırma Raporu ---")
print(classification_report(y_test, y_pred, target_names=['Normal', 'Clickbait']))

# 6. ADIM: İNTERAKTİF (CANLI) TEST MODU
print("\n" + "="*60)
print("SİSTEM HAZIR! (Çıkmak için 'q' yazın)")
print("Örnek: 'Şok şok şok bu kürü deneyen yandı' veya 'Yarın hava güneşli'")
print("="*60)

while True:
    giris = input("\n Başlık Girin: ")
    
    if giris.lower() in ['q', 'exit', 'çık']:
        print("Güle güle!")
        break
        
    if len(giris) < 5:
        print("Lütfen biraz daha uzun bir cümle girin.")
        continue

    # 1. Girilen veriyi temizle
    temiz_giris = metni_temizle(giris)
    
    # 2. Vektöre çevir (Daha önce eğitilen tfidf'i kullan)
    vektor = tfidf.transform([temiz_giris])
    
    # 3. Olasılık Hesapla (predict_proba)
    # Model bize [Normal_Olasılığı, Clickbait_Olasılığı] şeklinde iki sayı verir.
    olasiliklar = model.predict_proba(vektor)[0]
    clickbait_ihtimali = olasiliklar[1] # 2. sıradaki değer (Clickbait olma ihtimali)
    
    # 4. Ekrana Yazdır
    skor_yuzde = clickbait_ihtimali * 100
    
    print(f" Clickbait İhtimali: %{skor_yuzde:.1f}")
    
    if clickbait_ihtimali > 0.65:
        print("🚨 SONUÇ: TIK TUZAĞI (CLICKBAIT) TESPİT EDİLDİ!")
    else:
        print("✅ SONUÇ: GÜVENLİ (NORMAL HABER)")