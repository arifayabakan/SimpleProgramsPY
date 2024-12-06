import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
#%%
# Kullanıcı girdileri
isim = input("İsim bilgisi giriniz: ")
while True:
    try:
        input_kg = float(input("Vücut ağırlığı bilgisi giriniz (kg): "))
        break
    except ValueError:
        print("Lütfen geçerli bir sayı giriniz.")
        
while True:
    try:
        input_boy = float(input("Boy bilgisi giriniz (m): "))
        break
    except ValueError:
        print("Lütfen geçerli bir sayı giriniz.")

# Tarih seçimi
while True:
    try:
        tarih_input = input("Veri hangi gün için girilecek? (YYYY-MM-DD formatında): ")
        tarih = datetime.strptime(tarih_input, "%Y-%m-%d").strftime("%Y-%m-%d")
        break
    except ValueError:
        print("Lütfen geçerli bir tarih giriniz (YYYY-MM-DD formatında).")

su_bardak = float(input("Bugün kaç bardak su içtiniz? (Bardak kapasitesi 200 ml): "))
su_sise = float(input("Bugün kaç şişe su içtiniz? (Şişe kapasitesi 500 ml): "))

# Vücut kitle endeksi hesaplama
vke = input_kg / (input_boy ** 2)
vke_alt_sinir = 18.5
vke_ust_sinir = 24.9
sisman_ust_sinir = 29.9
obez_ust_sinir = 39.9

if vke < vke_alt_sinir:
    output_durum = "Zayıf"
elif vke <= vke_ust_sinir:
    output_durum = "Sağlıklı"
elif vke <= sisman_ust_sinir:
    output_durum = "Şişman"
elif vke <= obez_ust_sinir:
    output_durum = "Obez"
else:
    output_durum = "Morbid"

# Su miktarını hesaplama
su_miktari = su_bardak * 0.2 + su_sise * 0.5
ideal_su = input_kg * 0.03  # Minimum su miktarı (litre cinsinden)

# Hedefler
hedef_su = float(input("Günlük su tüketim hedefiniz (L) nedir? "))
hedef_kilo = float(input("Hedef kilonuz nedir (kg)? "))

# Su ve kilo hedeflerinin durumu
if su_miktari < hedef_su:
    print(f"Hedefinize {hedef_su - su_miktari:.2f} L su daha içmeniz gerekiyor.")
else:
    print(f"Tebrikler! Bugün hedef su tüketiminizi geçtiniz!")

if input_kg > hedef_kilo:
    print(f"Hedef kilonuza {input_kg - hedef_kilo:.2f} kg kaldı!")
else:
    print(f"Hedef kilonuza ulaştınız ya da geçtiniz!")

# Veriyi hazırlama
yeni_veri = {
    "Tarih": [tarih],
    "İsim": [isim],
    "Ağırlık (kg)": [input_kg],
    "Boy (m)": [input_boy],
    "Vücut Kitle Endeksi": [vke],
    "Durum": [output_durum],
    "Tüketilen Su Miktarı (L)": [su_miktari],
    "Hafta No": [datetime.now().isocalendar()[1]],  # Haftanın numarası
    "Ay": [datetime.now().strftime("%B")],  # Ay adı
    "Kullanıcı ID": [isim.lower().replace(" ", "_")]  # Kullanıcı ID
}

# Excel dosyasını işleme
dosya_adi = "gunluk_veriler.xlsx"

try:
    # Dosya mevcutsa, oku ve yeni veriyi ekle
    df = pd.read_excel(dosya_adi, index_col=0)
    df = pd.concat([df, pd.DataFrame(yeni_veri)], ignore_index=True)
except FileNotFoundError:
    # Dosya yoksa, yeni bir DataFrame oluştur
    df = pd.DataFrame(yeni_veri)

# Güncellenmiş tabloyu kaydet
df.to_excel(dosya_adi)

# Veriyi görselleştirme (Su Tüketimi ve Kilo Grafikleri)
fig, ax1 = plt.subplots(figsize=(10, 6))

# Su tüketimi grafiği
ax1.plot(df["Tarih"], df["Tüketilen Su Miktarı (L)"], marker='o', label="Su Tüketimi", color='b')
ax1.axhline(y=ideal_su, color='r', linestyle='--', label="İdeal Su Seviyesi")
ax1.set_xlabel("Tarih")
ax1.set_ylabel("Su Miktarı (L)", color='b')
ax1.tick_params(axis='y', labelcolor='b')
ax1.legend(loc='upper left')

# Kilo grafiği için ikinci bir eksen
ax2 = ax1.twinx()
ax2.plot(df["Tarih"], df["Ağırlık (kg)"], marker='s', label="Vücut Ağırlığı", color='g')
ax2.set_ylabel("Ağırlık (kg)", color='g')
ax2.tick_params(axis='y', labelcolor='g')
ax2.legend(loc='upper right')

plt.title("Günlük Su Tüketimi ve Kilo Değişimi")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Haftalık rapor (toplam kilo yerine sadece ortalama)
hafta_df = df[df['Hafta No'] == datetime.now().isocalendar()[1]]
ortalama_su_hafta = hafta_df["Tüketilen Su Miktarı (L)"].mean()
ortalama_kilo_hafta = hafta_df["Ağırlık (kg)"].mean()

print(f"\nBu hafta ortalama su tüketimin: {ortalama_su_hafta:.2f} L")
print(f"Haftalık ortalama kilo: {ortalama_kilo_hafta:.2f} kg")

# Genel ilerleme raporu
ilk_kilo = df["Ağırlık (kg)"].iloc[0]  # İlk günün kilosu
son_kilo = df["Ağırlık (kg)"].iloc[-1]  # Son günün kilosu

agirlik_degisim = son_kilo - ilk_kilo  # Ağırlık değişimi

toplam_su = df["Tüketilen Su Miktarı (L)"].sum()
ortalama_su = df["Tüketilen Su Miktarı (L)"].mean()
ortalama_kilo = df["Ağırlık (kg)"].mean()

print(f"\nToplam su tüketimin: {toplam_su:.2f} L")
print(f"Günlük ortalama su tüketimin: {ortalama_su:.2f} L")
print(f"Ağırlık değişimin: {agirlik_degisim:.2f} kg")
print(f"Günlük ortalama ağırlık: {ortalama_kilo:.2f} kg")
print(f"{tarih} tarihli veriniz başarıyla kaydedildi!")

#%%
