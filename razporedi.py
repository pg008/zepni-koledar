import pdfimpose
import pdfimpose.schema
import pdfimpose.schema.common
import pdfimpose.schema.perfect
import fitz
import os




vhodna_datoteka = "material/zepni_koledar_2022.pdf"

izhodna_datoteka = "material/zepni_koledar_2022_tisk.pdf"













# pretvori milimetre v pt, ki so privzeta enota za PDF
def mm_v_pt(milimetri):
    resolucija = 72.0 / 25.4
    return milimetri * resolucija

def pt_v_mm(pt):
    resolucija = 72.0 / 25.4
    return round(pt / resolucija, 3)


# vmesne datoteke
vhodna_datoteka_z_okvirji = os.path.splitext(vhodna_datoteka)[0] + "_okvirji.pdf"
izhodna_datoteka_s_pregibi = os.path.splitext(izhodna_datoteka)[0] + "_pregibi.pdf"

# notranji rob med pregibi
velikost_pole = (297, 210)
notranji_rob = mm_v_pt(4)
pregibi = "hvh"


# nariši okvir na vsako prvo stran na poli
# da vemo, kje moramo obrezati prepognjen list
dokument = fitz.Document(vhodna_datoteka)
trenutna_stran = 1
sirina_male_strani = dokument.load_page(0).cropbox[2]
visina_male_strani = dokument.load_page(0).cropbox[3]


for stran in dokument.pages():
    # nariši okvir na prvo stran vsakega zvežčka
    if trenutna_stran % (2*2**len(pregibi)) == 1:
        stran.draw_rect(fitz.Rect((0,0), (sirina_male_strani, visina_male_strani)), color=(0.9, 0.9, 0.9))

    # nariši črto za končni pregib
    if trenutna_stran % (2*2**len(pregibi)) == (2*2**len(pregibi))//2 + 1:
        stran.draw_line((0, visina_male_strani/4), (0, 3*visina_male_strani/4), color=(0.8, 0.8, 0.8))
    trenutna_stran += 1

dokument.save(vhodna_datoteka_z_okvirji)

# zunanji rob - skupaj z notranjim in širino strani mora priti za A4 ( 297 - 4*69 - 3 ) / 2 = 9
zunanji_rob_desno_levo = (mm_v_pt(velikost_pole[0]) - 2**pregibi.count('h')*sirina_male_strani - notranji_rob) / 2
zunanji_rob_gor_dol = (mm_v_pt(velikost_pole[1]) - 2**pregibi.count('v')*visina_male_strani - notranji_rob) / 2



strani_na_papir = 2**len(pregibi)*2

zunanji_robovi = pdfimpose.schema.common.Margins(zunanji_rob_desno_levo, zunanji_rob_desno_levo, zunanji_rob_gor_dol, zunanji_rob_gor_dol)






pdfimpose.schema.perfect.impose(files=[vhodna_datoteka_z_okvirji],
                                output=izhodna_datoteka_s_pregibi,
                                omargin=zunanji_robovi,
                                imargin=notranji_rob,
                                mark=["crop"],
                                folds=pregibi,
                                )

# nariši črte za pregibe

dokument2 = fitz.Document(izhodna_datoteka_s_pregibi)

for stran in dokument2.pages():
    sirina = stran.cropbox[2] - 2*zunanji_rob_desno_levo
    visina = stran.cropbox[3] - 2*zunanji_rob_gor_dol

    pregibov_h = pregibi[:-1].count('h')
    pregibov_v = pregibi[:-1].count('v')

    pregibov_h = 2**pregibov_h
    pregibov_v = 2**pregibov_v

    for i in range(1, pregibov_h):
        stran.draw_line((i*sirina/pregibov_h+zunanji_rob_desno_levo, 0), (i*sirina/pregibov_h+zunanji_rob_desno_levo, visina+2*zunanji_rob_gor_dol))
    for i in range(1, pregibov_v):
        stran.draw_line((0, i*visina/pregibov_v+zunanji_rob_gor_dol), (sirina+2*zunanji_rob_desno_levo, i*visina/pregibov_v+zunanji_rob_gor_dol))
    
dokument2.save(izhodna_datoteka)
os.remove(izhodna_datoteka_s_pregibi)
os.remove(vhodna_datoteka_z_okvirji)