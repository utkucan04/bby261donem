import tkinter as tk
from tkinter import messagebox
import random
from PIL import Image, ImageTk
import os
from sorular import soru_verileri


GELISTIRILMIS_BOYUT = (400, 250)
SORU_SAYISI = 10   




skor = 0
soru_indeksi = 0
aktif_sorular = []       
mevcut_resim = None

kalan_sure = 0
zaman_after_id = None

pencere = tk.Tk()
pencere.title("Utkucan Yıkmaz'ın Bilgi Yarışması")



giris_cercevesi = tk.Frame(pencere)
quiz_cercevesi = tk.Frame(pencere)

# GİRİŞ SAYFASI 

giris_baslik = tk.Label(
    giris_cercevesi,
    text="Utkucan Yıkmaz'ın Bilgi Yarışmasına Hoş Geldin!",
    font=("Arial", 16, "bold"),
    pady=20
)
giris_aciklama = tk.Label(
    giris_cercevesi,
    text=f"Toplam {SORU_SAYISI} soru sorulacak.\nHer soru için 10 saniye süren var.\nHazırsan başla!\nBaşarılar😊. 🚀",
    font=("Arial", 12),
    pady=10
)

def baslat_oyun():
    global skor, soru_indeksi, aktif_sorular, kalan_sure, zaman_after_id

    skor = 0
    soru_indeksi = 0
    kalan_sure = 10
    zaman_after_id = None

    
    soru_adedi = min(SORU_SAYISI, len(soru_verileri))
    aktif_sorular = random.sample(soru_verileri, soru_adedi)

    skor_etiketi.config(text=f"Skor: {skor}")
    geri_bildirim_etiketi.config(text="")
    zaman_etiketi.config(text="Süre: 10 sn")
    soru_numara_etiketi.config(text="")

    giris_cercevesi.pack_forget()
    quiz_cercevesi.pack(pady=10, padx=10)

    sonraki_soruyu_yukle()

baslat_buton = tk.Button(
    giris_cercevesi,
    text="OYUNA BAŞLA",
    font=("Arial", 14, "bold"),
    bg="#4CAF50",
    fg="white",
    padx=20,
    pady=10,
    command=baslat_oyun
)

giris_baslik.pack()
giris_aciklama.pack()
baslat_buton.pack(pady=20)

giris_cercevesi.pack(fill="both", expand=True)



soru_etiketi = None
resim_etiketi = None
cevap_butonlari = []
skor_etiketi = None
soru_numara_etiketi = None
geri_bildirim_etiketi = None
zaman_etiketi = None

def butonlari_kilitle(state):
    for b in cevap_butonlari:
        b.config(state=state)

def zaman_say():
    
    global kalan_sure, zaman_after_id

    zaman_etiketi.config(text=f"Süre: {kalan_sure} sn")

    if kalan_sure > 0:
        kalan_sure -= 1
        zaman_after_id = pencere.after(1000, zaman_say)
    else:
        zaman_after_id = None
        zaman_asimi()

def zaman_asimi():
    
    global soru_indeksi

    butonlari_kilitle("disabled")
    mevcut_soru = aktif_sorular[soru_indeksi]

    geri_bildirim_etiketi.config(
        text=f"Süre doldu! Doğru cevap: {mevcut_soru['dogru_cevap']}",
        fg="orange"
    )
    messagebox.showwarning(
        "Süre Doldu!",
        f"Süre bitti!\nDoğru cevap: {mevcut_soru['dogru_cevap']}",
        parent=pencere
    )

    soru_indeksi += 1
    sonraki_soruyu_yukle()

def cevabi_kontrol_et(secilen_cevap):
    global skor, soru_indeksi, zaman_after_id

    
    if zaman_after_id is not None:
        pencere.after_cancel(zaman_after_id)
        zaman_after_id = None

    butonlari_kilitle("disabled")

    mevcut_soru = aktif_sorular[soru_indeksi]

    if secilen_cevap == mevcut_soru["dogru_cevap"]:
        skor += 1
        geri_bildirim_etiketi.config(text="Doğru cevap! 🎉", fg="green")
        messagebox.showinfo("Tebrikler!", "Doğru cevap!", parent=pencere)
    else:
        geri_bildirim_etiketi.config(
            text=f"Yanlış! Doğru cevap: {mevcut_soru['dogru_cevap']}",
            fg="red"
        )
        messagebox.showerror(
            "Yanlış!",
            f"Yanlış cevap. Doğru cevap: {mevcut_soru['dogru_cevap']}",
            parent=pencere
        )

    skor_etiketi.config(text=f"Skor: {skor}")

    soru_indeksi += 1
    sonraki_soruyu_yukle()

def sonraki_soruyu_yukle():
    global soru_indeksi, mevcut_resim, kalan_sure, zaman_after_id

    
    if zaman_after_id is not None:
        pencere.after_cancel(zaman_after_id)
        zaman_after_id = None
    
    geri_bildirim_etiketi.config(text="")

    if soru_indeksi >= len(aktif_sorular):
        oyunu_bitir()
        return

    mevcut_soru = aktif_sorular[soru_indeksi]

    soru_numara_etiketi.config(
        text=f"Soru: {soru_indeksi + 1} / {len(aktif_sorular)}"
    )
    soru_etiketi.config(text=mevcut_soru["soru"])

    
    karisik_siklar = mevcut_soru["siklar"][:]
    random.shuffle(karisik_siklar)

    
    try:
        dosya_yolu = os.path.join(os.path.dirname(__file__), mevcut_soru["resim_dosyasi"])
        pil_image = Image.open(dosya_yolu)
        pil_image = pil_image.resize(GELISTIRILMIS_BOYUT, Image.Resampling.LANCZOS)
        yeni_resim = ImageTk.PhotoImage(pil_image)
        mevcut_resim = yeni_resim

        resim_etiketi.config(image=mevcut_resim)
        resim_etiketi.config(text="")
        resim_etiketi.image = mevcut_resim
    except Exception as e:
        resim_etiketi.config(image="")
        resim_etiketi.config(
            text=f"RESİM HATASI: {mevcut_soru['resim_dosyasi']} bulunamadı!\nPillow kurulu mu, yol doğru mu?"
        )
        print(f"Görsel Yükleme HATASI ({mevcut_soru['resim_dosyasi']}): {e}")

   
    for i in range(len(cevap_butonlari)):
        sik_metni = karisik_siklar[i]
        buton = cevap_butonlari[i]
        buton.config(
            text=sik_metni,
            command=lambda c=sik_metni: cevabi_kontrol_et(c),
            state="normal"
        )

    
    kalan_sure = 10
    zaman_etiketi.config(text=f"Süre: {kalan_sure} sn")
    zaman_say()

def oyunu_bitir():
    final_penceresi = tk.Toplevel(pencere)
    final_penceresi.title("Oyun Bitti!")

    final_mesaj = f"Tebrikler! Oyunu tamamladın 🎉\nFinal Skorun: {skor} / {len(aktif_sorular)}"
    tk.Label(
        final_penceresi,
        text=final_mesaj,
        font=("Arial", 16, "bold"),
        padx=40,
        pady=40
    ).pack()

    def yeniden_oyna():
        final_penceresi.destroy()
        baslat_oyun()

    tk.Button(
        final_penceresi,
        text="Yeniden Oyna",
        command=yeniden_oyna
    ).pack(pady=6)

    tk.Button(
        final_penceresi,
        text="Kapat",
        command=final_penceresi.destroy,
        bg="#FF6347",
        fg="white",
        font=("Arial", 10)
    ).pack(pady=10)



skor_etiketi = tk.Label(quiz_cercevesi, text=f"Skor: {skor}", font=("Arial", 12), fg="#000080")
skor_etiketi.pack(pady=5)

zaman_etiketi = tk.Label(quiz_cercevesi, text="Süre: 10 sn", font=("Arial", 11), fg="#AA0000")
zaman_etiketi.pack()

soru_numara_etiketi = tk.Label(quiz_cercevesi, text="", font=("Arial", 11), fg="#555555")
soru_numara_etiketi.pack()

soru_etiketi = tk.Label(
    quiz_cercevesi,
    text="",
    font=("Arial", 14, "bold"),
    wraplength=450,
    padx=10,
    pady=10,
    fg="#333333"
)
soru_etiketi.pack(pady=10)

resim_etiketi = tk.Label(quiz_cercevesi)
resim_etiketi.pack(pady=10)
resim_etiketi.image = mevcut_resim

cevap_cercevesi = tk.Frame(quiz_cercevesi)
cevap_cercevesi.pack(pady=20, padx=10)

cevap_butonlari = []
for i in range(4):
    buton = tk.Button(
        cevap_cercevesi,
        text=f"Şık {i+1}",
        width=30,
        height=2,
        bg="#4CAF50",
        fg="white",
        font=("Arial", 10, "bold"),
        activebackground="#6CC06C"
    )
    row_num = i // 2
    col_num = i % 2
    buton.grid(row=row_num, column=col_num, padx=10, pady=10)
    cevap_butonlari.append(buton)

geri_bildirim_etiketi = tk.Label(quiz_cercevesi, text="", font=("Arial", 11, "italic"))
geri_bildirim_etiketi.pack(pady=5)

pencere.mainloop()
