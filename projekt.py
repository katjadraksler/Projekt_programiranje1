import csv
import json
import os
import re
import sys

import requests


def pripravi_imenik(ime_datoteke):
    '''Če še ne obstaja, pripravi prazen imenik za dano datoteko.'''
    imenik = os.path.dirname(ime_datoteke)
    if imenik:
        os.makedirs(imenik, exist_ok=True)


def shrani_spletno_stran(url, ime_datoteke, vsili_prenos=False):
    '''Vsebino strani na danem naslovu shrani v datoteko z danim imenom.'''
    try:
        print('Shranjujem {} ...'.format(url), end='')
        sys.stdout.flush()
        if os.path.isfile(ime_datoteke) and not vsili_prenos:
            print('shranjeno že od prej!')
            return
        r = requests.get(url)
    except requests.exceptions.ConnectionError:
        print('stran ne obstaja!')
    else:
        pripravi_imenik(ime_datoteke)
        with open(ime_datoteke, 'w', encoding='utf-8') as datoteka:
            datoteka.write(r.text)
            print('shranjeno!')


def vsebina_datoteke(ime_datoteke):
    '''Vrne niz z vsebino datoteke z danim imenom.'''
    with open(ime_datoteke, encoding='utf-8') as datoteka:
        return datoteka.read()


def zapisi_csv(slovarji, imena_polj, ime_datoteke):
    '''Iz seznama slovarjev ustvari CSV datoteko z glavo.'''
    pripravi_imenik(ime_datoteke)
    with open(ime_datoteke, 'w', encoding='utf-8') as csv_datoteka:
        writer = csv.DictWriter(csv_datoteka, fieldnames=imena_polj)
        writer.writeheader()
        for slovar in slovarji:
            writer.writerow(slovar)


def zapisi_json(objekt, ime_datoteke):
    '''Iz danega objekta ustvari JSON datoteko.'''
    pripravi_imenik(ime_datoteke)
    with open(ime_datoteke, 'w', encoding='utf-8') as json_datoteka:
        json.dump(objekt, json_datoteka, indent=4, ensure_ascii=False)


vzorec = re.compile (
   r'<tr itemscope itemtype="http://schema.org/Book">.+?'
   r'<td valign="top" class="number">(.|..|...)</td>.+?'
   r'<div id="(?P<id>\d+)" class="u-anchorTarget"></div>.+?'
   r'<a title="(?P<naslov>.+?)" href.+?'
   r'<span itemprop="name">(?P<avtor>.+?)<.+?'
   r'</span></span> (?P<povprecna_ocena>.+?) avg rating &mdash;'
   r' (?P<st_ocen>.+?) ratings.+?'
   r'return false;">score: (?P<score>(\d\d|\d\d\d|\d)?,?(\d\d\d|\d\d|\d)?).+?',
   re.DOTALL)



def izloci_podatke_knjige(ujemanje_knjige):
    podatki_knjige = ujemanje_knjige.groupdict()
    podatki_knjige['avtor'] = podatki_knjige['avtor'].strip()
    podatki_knjige['naslov'] = podatki_knjige['naslov'].strip()
    podatki_knjige['naslov'] = podatki_knjige['naslov'].replace('&amp;','and')
    podatki_knjige['naslov'] = podatki_knjige['naslov'].replace('&#39;',"'")
    podatki_knjige['score'] = podatki_knjige['score'].replace(',', '.')
    podatki_knjige['st_ocen'] = podatki_knjige['st_ocen'].replace(',', '')
    return podatki_knjige


for i in range(1, 11):
    url = (
        'https://www.goodreads.com/list/show/7.'
        'Best_Books_of_the_21st_Century?page={}'
    ).format(i)
    shrani_spletno_stran(url, 'zajeti-podatki/najbolj-znane-knjige-21-stoletja-{}.html'.format(i))
    
for i in range(1, 11):
    url = (
        'https://www.goodreads.com/list/best_of_century/20th?id=6.'
        'Best_Books_of_the_20th_Century&page={}'
    ).format(i)
    shrani_spletno_stran(url, 'zajeti-podatki/najbolj-znane-knjige-20-stoletja-{}.html'.format(i))


podatki_knjig = []
vsebina1 = vsebina_datoteke('zajeti-podatki/najbolj-znane-knjige-21-stoletja-1.html')
vsebina2 = vsebina_datoteke('zajeti-podatki/najbolj-znane-knjige-21-stoletja-2.html')
vsebina3 = vsebina_datoteke('zajeti-podatki/najbolj-znane-knjige-21-stoletja-3.html')
vsebina4 = vsebina_datoteke('zajeti-podatki/najbolj-znane-knjige-21-stoletja-4.html')
vsebina5 = vsebina_datoteke('zajeti-podatki/najbolj-znane-knjige-21-stoletja-5.html')
vsebina6 = vsebina_datoteke('zajeti-podatki/najbolj-znane-knjige-21-stoletja-6.html')
vsebina7 = vsebina_datoteke('zajeti-podatki/najbolj-znane-knjige-21-stoletja-7.html')
vsebina8 = vsebina_datoteke('zajeti-podatki/najbolj-znane-knjige-21-stoletja-8.html')
vsebina9 = vsebina_datoteke('zajeti-podatki/najbolj-znane-knjige-21-stoletja-9.html')
vsebina10 = vsebina_datoteke('zajeti-podatki/najbolj-znane-knjige-21-stoletja-10.html')

for ujemanje_knjige in vzorec.finditer(vsebina1):
    podatki_knjig.append(izloci_podatke_knjige(ujemanje_knjige))
for ujemanje_knjige in vzorec.finditer(vsebina2):
    podatki_knjig.append(izloci_podatke_knjige(ujemanje_knjige))
for ujemanje_knjige in vzorec.finditer(vsebina3):
    podatki_knjig.append(izloci_podatke_knjige(ujemanje_knjige))
for ujemanje_knjige in vzorec.finditer(vsebina4):
    podatki_knjig.append(izloci_podatke_knjige(ujemanje_knjige))
for ujemanje_knjige in vzorec.finditer(vsebina5):
    podatki_knjig.append(izloci_podatke_knjige(ujemanje_knjige))
for ujemanje_knjige in vzorec.finditer(vsebina6):
    podatki_knjig.append(izloci_podatke_knjige(ujemanje_knjige))
for ujemanje_knjige in vzorec.finditer(vsebina7):
    podatki_knjig.append(izloci_podatke_knjige(ujemanje_knjige))
for ujemanje_knjige in vzorec.finditer(vsebina8):
    podatki_knjig.append(izloci_podatke_knjige(ujemanje_knjige))
for ujemanje_knjige in vzorec.finditer(vsebina9):
    podatki_knjig.append(izloci_podatke_knjige(ujemanje_knjige))
for ujemanje_knjige in vzorec.finditer(vsebina10):
    podatki_knjig.append(izloci_podatke_knjige(ujemanje_knjige))

podatki_knjig1 = []
vsebina10 = vsebina_datoteke('zajeti-podatki/najbolj-znane-knjige-20-stoletja-1.html')
vsebina20 = vsebina_datoteke('zajeti-podatki/najbolj-znane-knjige-20-stoletja-2.html')
vsebina30 = vsebina_datoteke('zajeti-podatki/najbolj-znane-knjige-20-stoletja-3.html')
vsebina40 = vsebina_datoteke('zajeti-podatki/najbolj-znane-knjige-20-stoletja-4.html')
vsebina50 = vsebina_datoteke('zajeti-podatki/najbolj-znane-knjige-20-stoletja-5.html')
vsebina60 = vsebina_datoteke('zajeti-podatki/najbolj-znane-knjige-20-stoletja-6.html')
vsebina70 = vsebina_datoteke('zajeti-podatki/najbolj-znane-knjige-20-stoletja-7.html')
vsebina80 = vsebina_datoteke('zajeti-podatki/najbolj-znane-knjige-20-stoletja-8.html')
vsebina90 = vsebina_datoteke('zajeti-podatki/najbolj-znane-knjige-20-stoletja-9.html')
vsebina100 = vsebina_datoteke('zajeti-podatki/najbolj-znane-knjige-20-stoletja-10.html')

for ujemanje_knjige in vzorec.finditer(vsebina10):
    podatki_knjig1.append(izloci_podatke_knjige(ujemanje_knjige))
for ujemanje_knjige in vzorec.finditer(vsebina20):
    podatki_knjig1.append(izloci_podatke_knjige(ujemanje_knjige))
for ujemanje_knjige in vzorec.finditer(vsebina30):
    podatki_knjig1.append(izloci_podatke_knjige(ujemanje_knjige))
for ujemanje_knjige in vzorec.finditer(vsebina40):
    podatki_knjig1.append(izloci_podatke_knjige(ujemanje_knjige))
for ujemanje_knjige in vzorec.finditer(vsebina50):
    podatki_knjig1.append(izloci_podatke_knjige(ujemanje_knjige))
for ujemanje_knjige in vzorec.finditer(vsebina60):
    podatki_knjig1.append(izloci_podatke_knjige(ujemanje_knjige))
for ujemanje_knjige in vzorec.finditer(vsebina70):
    podatki_knjig1.append(izloci_podatke_knjige(ujemanje_knjige))
for ujemanje_knjige in vzorec.finditer(vsebina80):
    podatki_knjig1.append(izloci_podatke_knjige(ujemanje_knjige))
for ujemanje_knjige in vzorec.finditer(vsebina90):
    podatki_knjig1.append(izloci_podatke_knjige(ujemanje_knjige))
for ujemanje_knjige in vzorec.finditer(vsebina100):
    podatki_knjig1.append(izloci_podatke_knjige(ujemanje_knjige))

zapisi_json(podatki_knjig, 'obdelani-podatki/vse-knjige-21-stoletja.json')
zapisi_csv(podatki_knjig, ['id', 'naslov' , 'avtor', 'povprecna_ocena', 'st_ocen', 'score'],
           'obdelani-podatki/vse-knjige-21-stoletja.csv')
zapisi_json(podatki_knjig1, 'obdelani-podatki/vse-knjige-20-stoletja.json')
zapisi_csv(podatki_knjig1, ['id', 'naslov' , 'avtor', 'povprecna_ocena', 'st_ocen', 'score'],
           'obdelani-podatki/vse-knjige-20-stoletja.csv')


