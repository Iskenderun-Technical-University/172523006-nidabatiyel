import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import tkinter as tk
from tkinter import messagebox
import joblib
import os

MODEL_PATH = "wine_quality_model.pkl"

# Modeli eğit veya kaydedilmiş modeli yükle
def model_yukle_veya_egit():
    if os.path.exists(MODEL_PATH):
        model = joblib.load(MODEL_PATH)
        print("Model dosyası yüklendi.")
    else:
        print("Model dosyası yok, eğitim başlıyor...")
        df = pd.read_csv("winequality-red.csv", sep=';')
        X = df.drop("quality", axis=1)
        y = df["quality"]
        model = RandomForestClassifier(random_state=42)
        model.fit(X, y)
        joblib.dump(model, MODEL_PATH)
        print("Model eğitildi ve kaydedildi.")
    return model

# Ortalama eksik değerler
ortalama = {
    "citric acid": 0.27,
    "free sulfur dioxide": 15.87,
    "total sulfur dioxide": 46.47,
    "density": 0.9967,
    "pH": 3.31,
    "sulphates": 0.66,
}

import customtkinter as ctk

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

def tahmin_et():
    try:
        # Kullanıcıdan girilen verileri oku
        fixed_acidity = float(entry_fixed_acidity.get())
        volatile_acidity = float(entry_volatile_acidity.get())
        citric_acid = float(entry_citric_acid.get())
        residual_sugar = float(entry_residual_sugar.get())
        chlorides = float(entry_chlorides.get())
        alcohol = float(entry_alcohol.get())
    except ValueError:
        popup_mesaj("Hata", "Lütfen tüm alanlara geçerli sayılar girin!")
        return
    
    # Basit bir kalite tahmini (örnek)
    puan = fixed_acidity * 0.1 + alcohol * 0.5 - volatile_acidity * 0.3
    if puan > 7:
        yorum = "İyi kalite"
        kalite = "İyi"
    elif puan > 5:
        yorum = "Orta kalite"
        kalite = "Orta"
    else:
        yorum = "Düşük kalite"
        kalite = "Kötü"
    
    popup_mesaj(f"Kalite: {kalite}", yorum)

def popup_mesaj(baslik, mesaj):
    popup = ctk.CTkToplevel(root)
    popup.title(baslik)
    popup.geometry("350x180")
    
    label_baslik = ctk.CTkLabel(popup, text=baslik, font=ctk.CTkFont(size=20, weight="bold"))
    label_baslik.pack(pady=(20,10))
    
    label_mesaj = ctk.CTkLabel(popup, text=mesaj, font=ctk.CTkFont(size=16))
    label_mesaj.pack(pady=10)
    
    btn = ctk.CTkButton(popup, text="Tamam", command=popup.destroy)
    btn.pack(pady=15, ipadx=10, ipady=5)

root = ctk.CTk()
root.title("Şarap Kalite Tahmin Robotu")

frame = ctk.CTkFrame(root)
frame.pack(padx=20, pady=20)

# Etiket ve giriş kutuları
labels = ["Fixed Acidity", "Volatile Acidity", "Citric Acid", "Residual Sugar", "Chlorides", "Alcohol"]
entries = []

for label_text in labels:
    label = ctk.CTkLabel(frame, text=label_text)
    label.pack(anchor="w", pady=(5,0))
    entry = ctk.CTkEntry(frame, width=200)
    entry.pack(pady=(0,5))
    entries.append(entry)

(entry_fixed_acidity, entry_volatile_acidity, entry_citric_acid,
 entry_residual_sugar, entry_chlorides, entry_alcohol) = entries

btn_tahmin = ctk.CTkButton(root, text="Tahmin Et", command=tahmin_et)
btn_tahmin.pack(pady=20, ipadx=10, ipady=5)

root.mainloop()



model = model_yukle_veya_egit()

pencere = tk.Tk()
pencere.title("Şarap Kalite Tahmin")

tk.Label(pencere, text="fixed acidity").pack()
entry_fixed = tk.Entry(pencere)
entry_fixed.pack()

tk.Label(pencere, text="volatile acidity").pack()
entry_volatile = tk.Entry(pencere)
entry_volatile.pack()

tk.Label(pencere, text="residual sugar").pack()
entry_residual = tk.Entry(pencere)
entry_residual.pack()

tk.Label(pencere, text="chlorides").pack()
entry_chlorides = tk.Entry(pencere)
entry_chlorides.pack()

tk.Label(pencere, text="alcohol").pack()
entry_alcohol = tk.Entry(pencere)
entry_alcohol.pack()

tk.Button(pencere, text="Tahmin Et", command=tahmin_et).pack()

pencere.mainloop()

