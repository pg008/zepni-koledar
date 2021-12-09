import scribus

from datetime import date
import datetime
from shutil import copyfile
import os

# API: https://impagina.org/scribus-scripter-api/


prvi_dan = datetime.datetime(2022, 1, 1)
zadnji_dan = datetime.datetime(2023, 1, 31)


# Preverimo, da je trenutno odprt dokument
if not scribus.haveDoc():
     scribus.messageBox('Scribus - Script Error', "Ni odprtega dokumenta!", scribus.ICON_WARNING, scribus.BUTTON_OK)
     sys.exit(1)


# Slovenska imena mesecev - dobimo na ta način: meseci[datum.month]
meseci = [
    "Januar",
    "Februar",
    "Marec",
    "April",
    "Maj",
    "Junij",
    "Julij",
    "Avgust",
    "September",
    "Oktober",
    "November",
    "December"
    ]

# Seznam praznikov
prazniki = {
    "1.1.": "novo leto",
    "2.1.": "",
    "8.2.": "Prešernov dan",
    "27.4.": "dan upora proti okupatorju",
    "1.5.": "praznik dela",
    "2.5.": "",
    "25.6.": "dan državnosti",
    "1.11.": "dan spomina na mrtve",
    "26.12.": "dan samostojnosti in enotnosti",
    "15.8.": "Marijino vnebovzetje",
    "31.10.": "dan reformacije",
    "25.12.": "Božič",
    
}
# prazniki, ki nimajo fiksnega datuma
prazniki_2022 = {
    "17.4.": "velika noč",
    "18.4.": "velikonočni ponedeljek",
    "5.6.": "binkošti"
}
prazniki.update(prazniki_2022)











# Funkcije za spreminjanje dokumenta

# V izdelan koledar vstavimo neposodobljeno stran iz predloge
def vstavi_novo_stran_iz_predloge(predloga, stran):
    scribus.importPage(predloga, (stran,))


def seznam_predmetov_na_strani(stran):
    scribus.gotoPage(stran)
    return scribus.getPageItems()

# Scribus ob kopiranju doda "Copy of ", zato predmeta ne moremo iskati po celem imenu
def ime_elementa_ki_vsebuje_odsek(odsek, predmeti):
    ime_elementa = [s[0] for s in predmeti if odsek in s[0]]
    if len(ime_elementa) != 0:
        return ime_elementa[0]
    else:
        return False

def spremeni_besedilo(ime_elementa, besedilo):
    if not isinstance(besedilo, str):
        besedilo = str(besedilo)
    scribus.selectText(0,-1,ime_elementa)
    scribus.deleteText(ime_elementa)
    scribus.insertText(besedilo, 0, ime_elementa)







# Pot do dokumenta, ki je trenutno odprt
predloga = scribus.getDocName()


# Pot do izdelanega koledarja
nova_datoteka = os.path.splitext(predloga)[0] + "_izdelan.sla"

# Naredimo kopijo, da ne spreminjamo predloge
copyfile(predloga, nova_datoteka)

# Odpremo kopijo
scribus.openDoc(nova_datoteka)


trenutna_stran = 1

# Vedeti moramo, s katerim datumom začnemo teden
trenutni_ponedeljek = prvi_dan - datetime.timedelta(days=prvi_dan.weekday())



# Vstavljamo strani, dokler ne vstavimo vseh datumov
while trenutni_ponedeljek <= zadnji_dan:

    # Prvo stran že imamo
    if trenutna_stran != 1:
        vstavi_novo_stran_iz_predloge(predloga, 1)

    # V seznam shranimo vse predmete na trenutni strani
    predmeti = seznam_predmetov_na_strani(trenutna_stran)
    
    # Vstavimo datum za vsak dan v tednu
    for i in range(1, 8):

        # Kateri datum je ta dan
        datum_dneva = trenutni_ponedeljek + datetime.timedelta(days=i-1)

        # S tem imenom bomo poiskali ustrezen element
        ime_elementa_dan = "d" + str(i)
        celotno_ime_elementa_dan = ime_elementa_ki_vsebuje_odsek(ime_elementa_dan, predmeti)

        # preverimo, da element obstaja
        if celotno_ime_elementa_dan:
                ime_praznika = prazniki[datum_dneva_niz]
                
            spremeni_besedilo(celotno_ime_elementa_praznik, ime_praznika)
        

                ime_praznika = prazniki[datum_dneva_niz]
                
            spremeni_besedilo(celotno_ime_elementa_praznik, ime_praznika)
        

            # Posodobimo datum za današnji dan
            spremeni_besedilo(celotno_ime_elementa_dan, datum_dneva.day)
        

        # Če je danes praznik, vstavimo ime
        ime_elementa_praznik = "p" + str(i)
        celotno_ime_elementa_praznik = ime_elementa_ki_vsebuje_odsek(ime_elementa_praznik, predmeti)
        
        # Če element obstaja
        if celotno_ime_elementa_praznik:
        # Slovar praznikov uporablja nize, ne pravih datumov
            datum_dneva_niz = str(datum_dneva.day) + "." + str(datum_dneva.month) + "."

            ime_praznika = ""

            if datum_dneva_niz in prazniki:
                ime_praznika = prazniki[datum_dneva_niz]
                
            spremeni_besedilo(celotno_ime_elementa_praznik, ime_praznika)
        

    # Prestavimo se na naslednji teden
    trenutni_ponedeljek = trenutni_ponedeljek + datetime.timedelta(days=7)
    trenutna_stran += 1



# shrani pdf
pdf = scribus.PDFfile()
pdf.file = os.path.splitext(nova_datoteka)[0] + ".pdf"
pdf.save()




