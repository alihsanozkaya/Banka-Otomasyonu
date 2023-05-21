import giris
import kayitOl

def anaEkran():
    print("1- Giriş")
    print("2- Kayıt ol")
    secim = int(input("Seçiminizi giriniz: "))
    anaMenu(secim)
    
def anaMenu(secim):
    if secim == 1:
        giris.girisYap()
    elif secim == 2:
        kayitOl.kayitOl()
    else:
        print("Geçersiz seçim")
        anaEkran()

anaEkran()