
Hisse Senedi Tahmin Uygulaması

Bu proje, kullanıcılara belirli bir hisse senedi için geçmiş verilere dayanarak LSTM (Uzun Kısa Süreli Bellek) modelini kullanarak fiyat tahmini yapan bir web uygulaması sağlar. Flask framework'ü üzerine inşa edilmiştir ve hisse senedi verilerini işleyip tahmin grafiklerini kullanıcıya sunar.

Proje Yapısı:

hisse_tahmin_projesi/
├── app.py                # Ana Flask uygulama dosyası
├── static/               # Statik dosyalar (CSS, tahmin grafiği vs.)
│   ├── style.css         # Sayfa düzeni için CSS dosyası
│   └── tahmin.png        # Dinamik olarak oluşturulan tahmin grafikleri
├── templates/            # HTML şablon dosyaları
│   ├── index.html        # Ana sayfa (hisse kodu girişi)
│   └── tahmin.html       # Tahmin sonuçlarını gösteren sayfa
├── README.md             # Proje hakkında bilgi
└── .gitignore            # Git için gerekli dosya


Gerekli Kurulumlar:

1. Python 3.x sürümünün sisteminizde kurulu olduğundan emin olun.
2. Aşağıdaki komutla gerekli Python kütüphanelerini yükleyin:
   
   pip install -r requirements.txt

3. Dosya yapısı:
   - Hisse senedi verilerini .csv formatında proje dizinine koyun. Örneğin, aapl.csv gibi. Dosya adları hisse kodlarıyla aynı olmalıdır.

Uygulamayı Çalıştırma:

1. app.py dosyasını çalıştırın:
   python app.py

2. Tarayıcınızdan aşağıdaki adrese gidin:
   http://127.0.0.1:5000

3. Hisse senedi kodunu girerek tahmin yapın.

Kullanılan Teknolojiler:

- Flask: Web arayüzü için
- Pandas: Veri işleme için
- LSTM (Keras): Fiyat tahmini için
- Matplotlib: Grafik çizimi için

Özellikler:

- Kullanıcılar, hisse senedi kodunu girerek fiyat tahmini alabilir.
- Tahmin sonuçları grafikle görselleştirilir ve sunulur.
- CSS ile şık ve basit bir kullanıcı arayüzü sağlanır.

Katkıda Bulunma:

Katkıda bulunmak isterseniz, lütfen bir pull request gönderin.

