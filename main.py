import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import SnowballStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score
from TurkishStemmer import TurkishStemmer

# Gerekli NLTK paketleri
nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('stopwords')

# --- ADIM 1: GÜÇLENDİRİLMİŞ VERİ SETİ (V2) ---
data = {
    'baslik': [
        # --- CLICKBAIT (20 Adet) ---
        "Bu yöntemi deneyenler gözlerine inanamadı!",
        "Sakın bu meyveyi kabuğuyla yemeyin!",
        "Ünlü oyuncunun son hali görenleri şok etti.",
        "Hayatınızı değiştirecek 5 mucizevi ipucu.",
        "Bunu yapmayan pişman oluyor hemen tıklayın!",
        "Ayrılık iddiası ortalığı karıştırdı, bakın kimmiş!",
        "Sosyal medya bu görüntüyü konuşuyor, skandal!",
        "Duyanlar kulaklarına inanamadı, dehşet verici olay.",
        "Zayıflamak isteyenler buraya, 3 günde 5 kilo!",
        "Flaş flaş flaş! O isim istifa etti.",
        "Kimsenin bilmediği sır ortaya çıktı.",
        "Bakın o ünlü isim aslında nereliymiş!",
        "Yürekleri ağza getiren anlar, saniye saniye kaydedildi.",
        "Uzmanlar uyardı: Sakın çöpe atmayın!",
        "Görenler dönüp bir daha baktı, inanılmaz değişim.",
        "Doktorlar bu kürü öneriyor, hemen deneyin!",
        "Mucize kurtuluş! İzleyenler dondu kaldı.",
        "Olay yerinden ilk görüntüler, kan dondurdu.",
        "Herkes bu sorunun cevabını merak ediyor.",
        "Paranız cebinizde kalsın, işte bedava yöntem.",
        
        # --- NORMAL HABER (20 Adet) ---
        "Merkez Bankası faiz kararını yarın açıklayacak.",
        "İstanbul'da yarın sağanak yağış bekleniyor.",
        "Fenerbahçe derbi hazırlıklarını tamamladı.",
        "Eğitim bakanlığı yeni müfredatı duyurdu.",
        "Dolar kuru haftaya yatay seyirle başladı.",
        "Belediye ekipleri asfalt çalışmalarına devam ediyor.",
        "Otobüs ve metro sefer saatlerinde düzenleme yapıldı.",
        "Cumhurbaşkanı kabine toplantısı sonrası konuştu.",
        "Süper Lig'de bu hafta oynanacak maçların hakemleri belli oldu.",
        "Sağlık bakanlığı günlük koronavirüs tablosunu paylaştı.",
        "Milli takım teknik direktörü basın toplantısı düzenledi.",
        "Benzin ve motorin fiyatlarına bu gece zam geliyor.",
        "Üniversite sınav sonuçları erişime açıldı.",
        "İzmir'de 4.2 büyüklüğünde deprem meydana geldi.",
        "Turizm gelirleri geçen yıla göre yüzde 20 arttı.",
        "Meteoroloji uyardı: Kar yağışı geliyor.",
        "Altın fiyatları güne yükselişle başladı.",
        "Meclis yeni yasama yılına başladı.",
        "Trafik kazasında 3 kişi yaralandı.",
        "Şehir hastanesi hasta kabulüne başladı."
    ],
    'etiket': ['CLICKBAIT'] * 20 + ['NORMAL'] * 20 # 20 tane Clickbait, 20 tane Normal
}
df = pd.DataFrame(data)

# --- ADIM 2: PREPROCESSING (Ön İşleme) ---

def metin_on_isleme(metin):
    # 1. Küçük harfe çevir
    metin = metin.lower()
    
    # 2. Tokenization
    kelimeler = word_tokenize(metin)
    
    # 3. Stop Words
    stop_words = set(stopwords.words('turkish'))
    
    # 4. STEMMING TANIMLAMASI
    # Bilgisayara "stemmer"ın ne olduğunu burada söylüyoruz:
    stemmer = TurkishStemmer()
    temiz_kelimeler = []
    for kelime in kelimeler:
        if kelime.isalpha() and kelime not in stop_words:
            # Kelimenin kökünü buluyoruz (örn: 'yaptı' -> 'yap')
            kok = stemmer.stem(kelime)
            temiz_kelimeler.append(kok)
            
    return " ".join(temiz_kelimeler)
# Veriyi temizle
df['temiz_baslik'] = df['baslik'].apply(metin_on_isleme)

print("--- Örnek Dönüşüm ---")
print(f"Orijinal: {df['baslik'][0]}")
print(f"İşlenmiş: {df['temiz_baslik'][0]}")
print("-" * 30)

# --- ADIM 3: TF-IDF VEKTÖRLEŞTİRME ---
# Kelime Frekansı (BoW) ve Belge Frekansı (IDF) hesaplanıyor.
tfidf_vectorizer = TfidfVectorizer()

# Modeli besleyeceğimiz X (Matematiksel Veri) ve y (Etiketler)
X = tfidf_vectorizer.fit_transform(df['temiz_baslik'])
y = df['etiket']

# --- ADIM 4: MODEL EĞİTİMİ ---
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

model = MultinomialNB() # Metin sınıflandırmada standart model
#Naive Bayes algoritmasının bir türüdür. Özellikle metin sınıflandırma (bir kelime kaç kere geçmiş, puanı neymiş) gibi işlerde çok başarılıdır ve hızlıdır.
model.fit(X_train, y_train)

# --- ADIM 5: TEST VE TAHMİN ---
# Modelin başarısı
y_pred = model.predict(X_test)
print(f"Model Doğruluğu: {accuracy_score(y_test, y_pred)}\n")

# Yeni başlıklarla deneme yapalım
yeni_basliklar = [
    "Doktorlar bu kürü öneriyor, hemen deneyin!", # Clickbait olmalı
    "Belediye otobüs sefer saatlerinde düzenleme yaptı." # Normal olmalı
]

print("--- TAHMİNLER ---")
for baslik in yeni_basliklar:
    temiz = metin_on_isleme(baslik) #temizleme
    vektor = tfidf_vectorizer.transform([temiz]) #sayıya çevirme
    sonuc = model.predict(vektor)[0] #tahmin etme
    print(f"Başlık: {baslik}")
    print(f"Tahmin: {sonuc}")
    print("-" * 20)

# --- ADIM 6: GÖRSELLEŞTİRME (Word Cloud) ---
import matplotlib.pyplot as plt
from wordcloud import WordCloud

# İki ayrı metin yığını oluşturuyoruz: Biri Clickbait'ler, biri Normaller için
clickbait_metinleri = " ".join(df[df['etiket'] == 'CLICKBAIT']['temiz_baslik'])
normal_metinleri = " ".join(df[df['etiket'] == 'NORMAL']['temiz_baslik'])

# 1. Clickbait Bulutu (Kırmızı Tonlar)
wc_clickbait = WordCloud(width=800, height=400, background_color='black', colormap='Reds').generate(clickbait_metinleri)

# 2. Normal Haber Bulutu (Mavi Tonlar)
wc_normal = WordCloud(width=800, height=400, background_color='white', colormap='Blues').generate(normal_metinleri)

# Çizdirme Ayarları
plt.figure(figsize=(14, 7))

# Sol Taraf: Clickbait
plt.subplot(1, 2, 1)
plt.imshow(wc_clickbait, interpolation='bilinear')
plt.title("CLICKBAIT KELİMELERİ (DİKKAT!)", fontsize=15, color='red')
plt.axis('off')

# Sağ Taraf: Normal
plt.subplot(1, 2, 2)
plt.imshow(wc_normal, interpolation='bilinear')
plt.title("NORMAL HABER KELİMELERİ", fontsize=15, color='blue')
plt.axis('off')

# Ekrana bas
plt.show()