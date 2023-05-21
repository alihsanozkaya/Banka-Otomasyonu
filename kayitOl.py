import sqlite3, giris

def kayitOl():
    baglan = sqlite3.connect("banka.db", uri=True)
    imlec = baglan.cursor()
    imlec.execute("CREATE TABLE IF NOT EXISTS musteriler(TC INTEGER PRIMARY KEY, parola TEXT, bakiye INTEGER)")
    tc = input("TC kimlik numaranızı giriniz: ")
    parola = input("Parolanızı giriniz: ")
    bakiye = int(input("Bakiye giriniz: "))
    
    imlec.execute("SELECT * FROM musteriler WHERE TC=?", (tc,))
    kullanici = imlec.fetchone()
    if kullanici is not None:
        print("Bu TC numarası zaten kayıtlıdır. Lütfen farklı bir TC numarası girin.")
    elif len(tc) == 11:
        tc = int(tc)
        imlec.execute("INSERT INTO musteriler VALUES(?, ?, ?)", (tc, parola, bakiye))
        baglan.commit()
        print("Kayıt işlemi tamamlandı.")
        giris.menuGosterme(tc)
    else:
        print("TC kimlik numarası hatalı girildi")
        anaEkran()
    
    baglan.close()
    
def anaEkran():
    print("1- Giriş")
    print("2- Kayıt ol")
    secim = int(input("Seçiminizi giriniz: "))
    giris.anaMenu(secim)