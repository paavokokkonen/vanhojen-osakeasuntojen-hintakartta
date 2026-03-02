#!/usr/bin/env python3
"""
Analysoi hintatrendejä ja luo yksinkertaisia tunnuslukuja
olemassa olevasta asuntohintadatasta
"""

import json
import statistics

def laske_trendianalyysi(asuntohinnat_file='asuntohinnat.json'):
    """
    Laske trendianalyysi olemassa olevasta datasta:
    - Hinnan muutos viimeisen 5 vuoden aikana (%)
    - Kauppojen määrän trendi
    - Markkinan likviditeetti (kauppoja/vuosi keskimäärin)
    """
    print("=" * 60)
    print("TRENDIANALYYSI")
    print("=" * 60)
    
    with open(asuntohinnat_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    analyysit = {}
    
    # Analysoi jokaiselle postinumeroalueelle
    for postcode, info in data['data'].items():
        vuosidata = info['data']
        
        # Analysoi "Kaikki"-kategorialle (building_type='0')
        hinnat_vuosittain = []
        kaupat_vuosittain = []
        
        # Kerää viimeisen 5 vuoden data (2021-2025)
        vuodet = ['2021', '2022', '2023', '2024', '2025']
        
        for vuosi in vuodet:
            if vuosi in vuosidata and '0' in vuosidata[vuosi]:
                hinta = vuosidata[vuosi]['0'].get('keskihinta_aritm_nw')
                kaupat = vuosidata[vuosi]['0'].get('lkm_julk20')
                
                if hinta:
                    hinnat_vuosittain.append({'vuosi': vuosi, 'hinta': hinta})
                if kaupat:
                    kaupat_vuosittain.append({'vuosi': vuosi, 'kaupat': kaupat})
        
        if len(hinnat_vuosittain) < 2:
            continue  # Ei tarpeeksi dataa
        
        # Laske hinnan muutos 5 vuoden aikana
        alku_hinta = hinnat_vuosittain[0]['hinta']
        loppu_hinta = hinnat_vuosittain[-1]['hinta']
        hinta_muutos_prc = round(((loppu_hinta - alku_hinta) / alku_hinta) * 100, 1)
        
        # Laske keskimääräinen kauppamäärä
        if kaupat_vuosittain:
            keskim_kaupat = round(statistics.mean([k['kaupat'] for k in kaupat_vuosittain]))
        else:
            keskim_kaupat = 0
        
        # Laske volatiliteetti (hintojen keskihajonta)
        if len(hinnat_vuosittain) >= 3:
            hinnat = [h['hinta'] for h in hinnat_vuosittain]
            volatiliteetti = round(statistics.stdev(hinnat), 2)
        else:
            volatiliteetti = 0
        
        # Luokittele markkinan aktiivisuus
        if keskim_kaupat > 200:
            aktiivisuus = "Erittäin aktiivinen"
        elif keskim_kaupat > 100:
            aktiivisuus = "Aktiivinen"
        elif keskim_kaupat > 50:
            aktiivisuus = "Kohtalainen"
        elif keskim_kaupat > 20:
            aktiivisuus = "Hiljainen"
        else:
            aktiivisuus = "Erittäin hiljainen"
        
        # Luokittele hintatrendi
        if hinta_muutos_prc > 20:
            trendi = "Vahva nousu"
        elif hinta_muutos_prc > 10:
            trendi = "Nousu"
        elif hinta_muutos_prc > 0:
            trendi = "Lievä nousu"
        elif hinta_muutos_prc > -10:
            trendi = "Lievä lasku"
        elif hinta_muutos_prc > -20:
            trendi = "Lasku"
        else:
            trendi = "Vahva lasku"
        
        analyysit[postcode] = {
            'hinta_muutos_5v': hinta_muutos_prc,
            'keskim_kaupat_vuosi': keskim_kaupat,
            'volatiliteetti': volatiliteetti,
            'aktiivisuus': aktiivisuus,
            'trendi': trendi,
            'nykyinen_hinta': loppu_hinta,
            'datapisteet': len(hinnat_vuosittain)
        }
    
    print(f"\nAnalysoitu {len(analyysit)} postinumeroaluetta")
    print(f"Aikajakso: 2021-2025 (5 vuotta)")
    
    # Tilastot
    kaikki_muutokset = [a['hinta_muutos_5v'] for a in analyysit.values()]
    print(f"\nHinnan muutos 5 vuodessa:")
    print(f"  Keskiarvo: {statistics.mean(kaikki_muutokset):.1f}%")
    print(f"  Mediaani: {statistics.median(kaikki_muutokset):.1f}%")
    print(f"  Min: {min(kaikki_muutokset):.1f}%")
    print(f"  Max: {max(kaikki_muutokset):.1f}%")
    
    # Tallenna
    output = {
        'metadata': {
            'kuvaus': 'Trendianalyysi asuntohinnoista 2021-2025',
            'aikajakso': '2021-2025',
            'mittarit': {
                'hinta_muutos_5v': 'Hinnan muutos 5 vuodessa (%)',
                'keskim_kaupat_vuosi': 'Keskimääräinen kauppamäärä per vuosi',
                'volatiliteetti': 'Hintojen keskihajonta (volatiliteetti)',
                'aktiivisuus': 'Markkinan aktiivisuus',
                'trendi': 'Hintatrendi'
            }
        },
        'analyysit': analyysit
    }
    
    with open('data/trendianalyysi.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ Trendianalyysi tallennettu: data/trendianalyysi.json")
    print("=" * 60)
    
    return analyysit


if __name__ == "__main__":
    laske_trendianalyysi()
