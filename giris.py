import sqlite3
import kayitOl

def girisYap():
    baglan = sqlite3.connect("banka.db", uri=True)
    imlec = baglan.cursor()
    print("-----GİRİŞ EKRANI-----")
    tc = int(input("TC kimlik numaranızı giriniz: "))
    parola = input("Parolanızı giriniz: ")
    imlec.execute('SELECT * FROM musteriler WHERE TC = ?', (tc,))
    kullanici = imlec.fetchone()
    if kullanici and kullanici[1] == parola:
        menuGosterme(tc)
    else:
        print("Giriş bilgileri yanlış") 
        anaEkran()
    baglan.close()
def anaEkran():
    print("1- Giriş")
    print("2- Kayıt ol")
    secim = int(input("Seçiminizi giriniz: "))
    anaMenu(secim)
    
def anaMenu(secim):
    if secim == 1:
        girisYap()
    elif secim == 2:
        kayitOl.kayitOl()
    else:
        print("Geçersiz seçim")
                
def menuGosterme(tc):
    print("-----MENU-----")
    print("1- Göster")
    print("2- Nakit Ekle")
    print("3- Nakit Çek")
    print("4- Nakit Gönder")
    print("5- Çıkış")
    secim = int(input("Seçiminizi giriniz: "))
    menu(secim, tc)

def menu(secim, tc):
    if secim == 1:
        goster(tc)
    elif secim == 2:
        nakitEkle(tc)
    elif secim == 3:
        nakitCek(tc)
    elif secim == 4:
        nakitGonder(tc)
    elif secim == 5:
        print("Çıkış yapılıyor...")
        anaEkran()
    else:
        print("Geçersiz seçim")
        menuGosterme(tc)

def goster(tc):
    baglan = sqlite3.connect("banka.db", uri=True)
    imlec = baglan.cursor()
    imlec.execute("SELECT * FROM musteriler WHERE TC = ?", (tc,))
    kullanici = imlec.fetchone()
    bakiye = kullanici[2]
    print(f'Hesabınızdaki para {bakiye} TL')
    menuGosterme(tc)

def nakitEkle(tc):
    baglan = sqlite3.connect("banka.db", uri=True)
    imlec = baglan.cursor()
    eklenecek = input("Eklemek istediğiniz tutarı giriniz(Menüye geri dönmek için G ye basınız): ")
    if eklenecek == "g" or eklenecek == "G":
        menuGosterme(tc)
    else:
        eklenecek = int(eklenecek)
        imlec.execute(f'UPDATE musteriler SET bakiye = bakiye + {eklenecek} WHERE TC = ?', (tc,))    
        baglan.commit()
        
    baglan.close()
    menuGosterme(tc)

def nakitCek(tc):
    baglan = sqlite3.connect("banka.db", uri=True)
    imlec = baglan.cursor()
    imlec.execute('SELECT * FROM musteriler WHERE TC = ?', (tc,))
    kullanici = imlec.fetchone()
    bakiye = kullanici[2]
    
    cekilecek = input("Çekmek istediğiniz tutarı giriniz(Menüye geri dönmek için G ye basınız): ")
    
    if cekilecek == "g" or cekilecek == "G":
        menuGosterme(tc)
    else:
        cekilecek = int(cekilecek)
        if cekilecek <= bakiye:
            imlec.execute(f'UPDATE musteriler SET bakiye = bakiye - {cekilecek} WHERE TC = ?', (tc,))
            baglan.commit()
        else: 
            print(f"Bakiye yetersiz para çekilemez! En fazla çekebileceğiniz nakit tutarı {bakiye} TL")
    
    baglan.close()
    menuGosterme(tc)

def nakitGonder(tc):
    baglan = sqlite3.connect("banka.db", uri=True)
    imlec = baglan.cursor()
    imlec.execute('SELECT * FROM musteriler WHERE TC = ?', (tc,))
    kullanici = imlec.fetchone()
    bakiye = kullanici[2]
    
    aliciTC = int(input("Gönderilecek kişinin TC kimlik numarasını giriniz: "))
    imlec.execute('SELECT * FROM musteriler WHERE TC = ?', (aliciTC,))
    alici = imlec.fetchone()

    if alici is None:
        print("Alıcı bulunamadı.")
    else:
        tutar = input("Göndereceğiniz tutarı giriniz(Menüye geri dönmek için G ye basınız): ")
        if tutar == "g" or tutar == "G":
            menuGosterme(tc)
        else:
            tutar = int(tutar)
            if tutar <= bakiye:
                imlec.execute(f'UPDATE musteriler SET bakiye = bakiye - {tutar} WHERE TC = ?', (tc,))
                imlec.execute(f'UPDATE musteriler SET bakiye = bakiye + {tutar} WHERE TC = ?', (aliciTC,))
                baglan.commit()
            else:
                print(f"Bakiye yetersiz para gönderilemez! En fazla gönderebileceğiniz nakit tutarı {bakiye} TL")
    
    baglan.close()    
    menuGosterme(tc)