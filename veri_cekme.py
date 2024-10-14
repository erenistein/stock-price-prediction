import yfinance as yf
import pandas as pd

# Kullanıcıdan hisse senedi simgesi alalım
hisse_simgesi = input("Hisse senedi simgesini girin (örneğin: AAPL, TUPRS): Borsa ıstanbuldan girilen hisseler icin lutfen sonuna .IS ekleyin ").upper()

# Hisse senedi verilerini yfinance ile çekme (son 10 yıl)
hisse = yf.Ticker(hisse_simgesi)
df = hisse.history(period="10y")

# Verileri kontrol edelim
if df.empty:
    print(f"{hisse_simgesi} için veri bulunamadı.")
else:
    # Dinamik dosya ismi oluşturma
    dosya_adi = f"{hisse_simgesi.lower()}.csv"
    
    # Verileri CSV dosyasına kaydetme
    df.to_csv(dosya_adi)
    
    print(f"{hisse_simgesi} hisse senedi verileri '{dosya_adi}' dosyasına kaydedildi.")
