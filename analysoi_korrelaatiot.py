#!/usr/bin/env python3
"""
Analysoi korrelaatiot asuntohintojen ja muiden muuttujien välillä
==================================================================
"""

import json
import warnings
import numpy as np
from scipy import stats
import pandas as pd

warnings.filterwarnings('ignore', category=stats.ConstantInputWarning)

def laske_korrelaatiot(asuntohinnat, rikastettu_data):
    """
    Laske Pearsonin korrelaatiokertoimet asuntohintojen ja eri muuttujien välillä
    """
    print("Lasketaan korrelaatioita...")
    
    # Kerää data listiksi
    data_list = []
    
    for postinumero, hinta_data in asuntohinnat['data'].items():
        # Ota viimeisin vuosi (2025)
        if '2025' not in hinta_data['data']:
            continue
        
        if '0' not in hinta_data['data']['2025']:  # "Kaikki" kategoria
            continue
        
        hinta_info = hinta_data['data']['2025']['0']
        hinta = hinta_info.get('keskihinta_aritm_nw')
        kaupat = hinta_info.get('lkm_julk20')
        
        if not hinta or hinta == 0:
            continue
        
        # Hae rikastettu data
        rikastettu = rikastettu_data.get(postinumero, {})
        paavo_vuodet = rikastettu.get('paavo', {})
        etaisyydet = rikastettu.get('etaisyydet', {})
        palvelut = rikastettu.get('palvelut', {})
        
        # Paavo-data on vuositasolla — hae uusin vuosi
        if not paavo_vuodet:
            continue
        
        # Valitse uusin vuosi jossa on dataa
        paavo = {}
        for v in sorted(paavo_vuodet.keys(), reverse=True):
            if isinstance(paavo_vuodet[v], dict) and paavo_vuodet[v].get('vaesto'):
                paavo = paavo_vuodet[v]
                break
        
        if not paavo:
            continue
        
        data_point = {
            'postinumero': postinumero,
            'hinta': hinta,
            'kaupat': kaupat or 0,
            'vaesto': paavo.get('vaesto', 0),
            'keski_ika': paavo.get('keski_ika', 0),
            'keskitulo': paavo.get('keskitulo', 0),
            'koulutustaso': paavo.get('koulutustaso', 0),
            'tyottomyysaste': paavo.get('tyottomyysaste', 0),
            'vaestotiheys': paavo.get('vaestotiheys', 0),
            'lahin_keskusta_km': etaisyydet.get('lahin_keskusta_km', 0),
            'palveluindeksi': palvelut.get('palveluindeksi', 0),
            'kaupat_lkm': palvelut.get('kaupat', 0),
            'koulut_lkm': palvelut.get('koulut', 0),
            'julkinen_liikenne_lkm': palvelut.get('julkinen_liikenne', 0)
        }
        
        data_list.append(data_point)
    
    print(f"   Datapisteitä: {len(data_list)}")
    
    if len(data_list) < 10:
        print("   Liian vähän dataa korrelaatioiden laskemiseen")
        return {}
    
    # Muunna pandas DataFrameksi
    df = pd.DataFrame(data_list)
    
    # Määrittele muuttujat joiden korrelaatiot lasketaan
    muuttujat = {
        'keskitulo': 'Keskitulo (€/kk)',
        'koulutustaso': 'Koulutustaso (%)',
        'tyottomyysaste': 'Työttömyysaste (%)',
        'vaestotiheys': 'Väestötiheys (as/km²)',
        'lahin_keskusta_km': 'Etäisyys keskustaan (km)',
        'palveluindeksi': 'Palveluindeksi',
        'kaupat_lkm': 'Kauppojen määrä',
        'koulut_lkm': 'Koulujen määrä',
        'julkinen_liikenne_lkm': 'Julkisen liikenteen pysäkit',
        'vaesto': 'Väestömäärä',
        'keski_ika': 'Keski-ikä (vuotta)'
    }
    
    korrelaatiot = {}
    
    for muuttuja, label in muuttujat.items():
        # Poista rivit joissa on puuttuvia arvoja tai nollia
        valid_data = df[['hinta', muuttuja]].dropna()
        valid_data = valid_data[valid_data[muuttuja] != 0]
        
        if len(valid_data) < 10:
            continue
        
        # Ohita vakioarvoiset sarakkeet
        if valid_data[muuttuja].std() == 0:
            continue
        
        # Laske Pearsonin korrelaatiokerroin
        r, p_value = stats.pearsonr(valid_data['hinta'], valid_data[muuttuja])
        
        # Ohita jos tulos on nan (esim. vakioarvoinen sarake)
        if np.isnan(r):
            continue
        
        # Luokittele voimakkuus
        abs_r = abs(r)
        if abs_r >= 0.7:
            voimakkuus = 'Vahva'
        elif abs_r >= 0.4:
            voimakkuus = 'Kohtalainen'
        elif abs_r >= 0.2:
            voimakkuus = 'Heikko'
        else:
            voimakkuus = 'Ei merkittävää'
        
        # Määrittele suunta
        if r > 0:
            suunta = 'positiivinen'
        elif r < 0:
            suunta = 'negatiivinen'
        else:
            suunta = 'ei suuntaa'
        
        korrelaatiot[muuttuja] = {
            'label': label,
            'r': round(float(r), 3),
            'p_value': round(float(p_value), 6) if p_value is not None else None,
            'merkitseva': bool(p_value < 0.05) if p_value is not None else False,
            'voimakkuus': voimakkuus,
            'suunta': suunta,
            'kuvaus': f"{voimakkuus} {suunta}",
            'n': len(valid_data)
        }
    
    return korrelaatiot, df


def luo_scatterplot_data(df, muuttuja):
    """Luo data scatterplot-visualisointia varten"""
    valid_data = df[['postinumero', 'hinta', muuttuja]].dropna()
    
    scatter_data = []
    for _, row in valid_data.iterrows():
        scatter_data.append({
            'x': float(row[muuttuja]),
            'y': float(row['hinta']),
            'postinumero': row['postinumero']
        })
    
    return scatter_data


def main():
    print("="*60)
    print("KORRELAATIOANALYYSI")
    print("="*60)
    
    # Lataa asuntohintadata
    print("\nLadataan asuntohintadataa...")
    try:
        with open('asuntohinnat.json', 'r', encoding='utf-8') as f:
            asuntohinnat = json.load(f)
        print(f"   Ladattu {len(asuntohinnat['data'])} postinumeroalueen hintatiedot")
    except FileNotFoundError:
        print("   asuntohinnat.json ei löydy. Aja ensin asuntohinnat.py")
        return
    
    # Lataa rikastettu data
    print("Ladataan rikastettua dataa...")
    try:
        with open('data/rikastettu_data.json', 'r', encoding='utf-8') as f:
            rikastettu_data = json.load(f)
        print(f"   Ladattu {len(rikastettu_data)} postinumeroalueen rikastettu data")
    except FileNotFoundError:
        print("   data/rikastettu_data.json ei löydy. Aja ensin rikasta_data.py")
        return
    
    # Laske korrelaatiot
    korrelaatiot, df = laske_korrelaatiot(asuntohinnat, rikastettu_data)
    
    if not korrelaatiot:
        print("Ei voitu laskea korrelaatioita")
        return
    
    # Tulosta tulokset
    print("\nKORRELAATIOT ASUNTOHINTOJEN KANSSA (2025, Kaikki):")
    print("-" * 80)
    print(f"{'Muuttuja':<40} {'r':<8} {'p':<10} {'Kuvaus':<20}")
    print("-" * 80)
    
    # Järjestä korrelaatiot abs(r):n mukaan
    sorted_korr = sorted(korrelaatiot.items(), key=lambda x: abs(x[1]['r']), reverse=True)
    
    for muuttuja, stats_info in sorted_korr:
        r = stats_info['r']
        p = stats_info['p_value']
        kuvaus = stats_info['kuvaus']
        merkki = '***' if stats_info['merkitseva'] else ''
        
        print(f"{stats_info['label']:<40} {r:>7.3f} {p:>9.6f} {kuvaus:<20} {merkki}")
    
    print("-" * 80)
    print("*** = Tilastollisesti merkitsevä (p < 0.05)")
    
    # Luo scatterplot-data jokaiselle muuttujalle
    scatter_plots = {}
    for muuttuja in korrelaatiot.keys():
        scatter_plots[muuttuja] = luo_scatterplot_data(df, muuttuja)
    
    # Tallenna tulokset
    output = {
        'korrelaatiot': korrelaatiot,
        'scatter_data': scatter_plots,
        'metadata': {
            'datapisteet': len(df),
            'laskettu': '2026-03-02',
            'vuosi': '2025',
            'huoneistotyyppi': 'Kaikki'
        }
    }
    
    output_file = 'data/korrelaatiot.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ Korrelaatiot tallennettu: {output_file}")
    print("="*60)


if __name__ == "__main__":
    main()
