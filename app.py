from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import numpy as np
from statsmodels.tsa.arima.model import ARIMA
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)

def csv_dosyasini_yukle(hisse_kodu):
    dosya_adi = f"{hisse_kodu.lower()}.csv"
    try:
        df = pd.read_csv(dosya_adi)
        return df
    except FileNotFoundError:
        return None

def veri_on_isleme(df):
    df['Date'] = pd.to_datetime(df['Date'])
    df.set_index('Date', inplace=True)
    df_close = df[['Close']].dropna()
    return df_close

def create_dataset(data, time_step=1):
    X, y = [], []
    for i in range(len(data) - time_step - 1):
        X.append(data[i:(i + time_step), 0])
        y.append(data[i + time_step, 0])
    return np.array(X), np.array(y)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        hisse_kodu = request.form['hisse_kodu']
        return redirect(url_for('tahmin', hisse_kodu=hisse_kodu))
    return render_template('index.html')

@app.route('/tahmin/<hisse_kodu>')
def tahmin(hisse_kodu):
    df = csv_dosyasini_yukle(hisse_kodu)
    if df is None:
        return f"{hisse_kodu} dosyası bulunamadı."
    
    df_close = veri_on_isleme(df)

    # Veriyi normalize etme
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(df_close)

    # Eğitim ve test setine ayırma
    train_size = int(len(scaled_data) * 0.8)
    train_data = scaled_data[:train_size]
    test_data = scaled_data[train_size:]

    time_step = 60
    X_train, y_train = create_dataset(train_data, time_step)
    X_test, y_test = create_dataset(test_data, time_step)

    # Giriş verisini yeniden şekillendirme
    X_train = X_train.reshape(X_train.shape[0], X_train.shape[1], 1)
    X_test = X_test.reshape(X_test.shape[0], X_test.shape[1], 1)

    # LSTM Modeli
    lstm_model = Sequential()
    lstm_model.add(LSTM(50, return_sequences=True, input_shape=(time_step, 1)))
    lstm_model.add(LSTM(50))
    lstm_model.add(Dense(1))

    # Modeli derleme
    lstm_model.compile(optimizer='adam', loss='mean_squared_error')

    # LSTM modelini eğitme
    lstm_model.fit(X_train, y_train, epochs=5, batch_size=32)

    # LSTM tahminleri
    lstm_predictions = lstm_model.predict(X_test)
    lstm_predictions = scaler.inverse_transform(lstm_predictions)

    # Grafik oluşturma
    fig, ax = plt.subplots(figsize=(12, 6))
    if len(df_close.index[train_size + time_step:]) != len(lstm_predictions):
        min_len = min(len(df_close.index[train_size + time_step:]), len(lstm_predictions))
        ax.plot(df_close.index[train_size + time_step:][:min_len], lstm_predictions[:min_len], color='green', label='LSTM Tahminleri')
    else:
        ax.plot(df_close.index[train_size + time_step:], lstm_predictions, color='green', label='LSTM Tahminleri')

    ax.legend()
    ax.set_title(f'{hisse_kodu} Hisse Senedi Tahminleri')
    ax.set_xlabel('Tarih')
    ax.set_ylabel('Fiyat')

    # Grafiği kaydet ve HTML'e gönder
    plt.savefig('static/tahmin.png')
    return render_template('tahmin.html', hisse_kodu=hisse_kodu, tahmin_img='static/tahmin.png')

if __name__ == '__main__':
    app.run(debug=True)
