#!/usr/bin/env python3
"""
Rikasta asuntohintadata väestötiedoilla
=============================================
Hakee:
- Paavo-väestötiedot (Tilastokeskus)
- Etäisyydet keskustoihin
"""

import requests
import json
import time
from xml.etree import ElementTree as ET
from shapely.geometry import shape, Point
from shapely.ops import nearest_points
import math

def hae_paavo_data():
    """
    Hae Paavo-väestötiedot Tilastokeskuksen WFS-rajapinnasta
    Hakee aikasarjan vuosilta 2015-2026
    """
    print("Haetaan Paavo-väestötietoja (aikasarja 2015-2026)...")
    
    # Saatavilla olevat vuodet WFS-rajapinnasta
    vuodet = list(range(2015, 2027))  # 2015-2026
    
    # Paavo WFS-rajapinta
    url = "https://geo.stat.fi/geoserver/postialue/wfs"
    
    # Tallenna data postinumeroittain
    paavo_dict = {}
    
    for vuosi in vuodet:
        print(f"   Haetaan vuosi {vuosi}...", end=' ')
        
        params = {
            'service': 'WFS',
            'version': '2.0.0',
            'request': 'GetFeature',
            'typeName': f'postialue:pno_tilasto_{vuosi}',
            'outputFormat': 'application/json',
            'srsName': 'EPSG:4326'
        }
        
        max_yritykset = 3
        for yritys in range(max_yritykset):
            try:
                response = requests.get(url, params=params, timeout=180)
                response.raise_for_status()
                data = response.json()
                
                alueiden_lkm = 0
                for feature in data.get('features', []):
                    props = feature.get('properties', {})
                    # Vanhemmissa vuosissa kenttä on 'posti_alue', uudemmissa 'postinumeroalue'
                    postinumero = props.get('postinumeroalue') or props.get('posti_alue')
                    
                    if postinumero:
                        # Luo postinumeroalue jos ei vielä ole
                        if postinumero not in paavo_dict:
                            paavo_dict[postinumero] = {}
                        
                        # Tallenna vuoden tiedot
                        paavo_dict[postinumero][str(vuosi)] = {
                            'vaesto': props.get('he_vakiy') or 0,  # Väestömäärä
                            'keski_ika': props.get('he_kika') or 0,  # Keski-ikä
                            'tyolliset': props.get('pt_tyoll') or 0,  # Työlliset
                            'tyottomat': props.get('pt_tyott') or 0,  # Työttömät
                            'elakelaiset': props.get('pt_elakel') or 0,  # Eläkeläiset
                            'opiskelijat': props.get('pt_opisk') or 0,  # Opiskelijat
                            'keskitulo': props.get('hr_mtu') or 0,  # Asuntokuntien keskitulot
                            'koulutustaso': props.get('ko_ika18y') or 0,  # Korkea-aste
                            'asuntokuntia': props.get('te_as_valj') or 0,  # Asuntokuntien koko
                        }
                        
                        vuosi_data = paavo_dict[postinumero][str(vuosi)]
                        
                        # Laske työttömyysaste
                        tyossa = vuosi_data['tyolliset'] + vuosi_data['tyottomat']
                        if tyossa > 0:
                            vuosi_data['tyottomyysaste'] = (vuosi_data['tyottomat'] / tyossa * 100)
                        else:
                            vuosi_data['tyottomyysaste'] = 0
                        
                        # Laske väestötiheys (per km²)
                        pinta_ala_km2 = (props.get('pinta_ala') or 0) / 1_000_000
                        if pinta_ala_km2 > 0:
                            vuosi_data['vaestotiheys'] = (vuosi_data['vaesto'] / pinta_ala_km2)
                        else:
                            vuosi_data['vaestotiheys'] = 0
                        
                        alueiden_lkm += 1
                
                print(f"{alueiden_lkm} aluetta")
                time.sleep(2)  # Kohteliaisuus API:a kohtaan
                break  # Onnistui, siirry seuraavaan vuoteen
                
            except Exception as e:
                if yritys < max_yritykset - 1:
                    print(f"Yritys {yritys+1} epäonnistui, yritetään uudelleen...", end=' ')
                    time.sleep(5)
                else:
                    print(f"VIRHE: {e}")
                    # Jatka seuraavaan vuoteen virheen jälkeen
                    break
    
    print(f"\n   Yhteensä {len(paavo_dict)} postinumeroaluetta, {len(vuodet)} vuotta")
    return paavo_dict


def laske_etaisyys(lat1, lon1, lat2, lon2):
    """Laske etäisyys kahdel pisteen välillä (Haversine-kaava, km)"""
    R = 6371  # Maapallon säde km
    
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    
    a = (math.sin(dlat/2) * math.sin(dlat/2) +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
         math.sin(dlon/2) * math.sin(dlon/2))
    
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    
    return R * c


def laske_etaisyydet_keskustoihin(postinumerokoordinaatit):
    """
    Laske etäisyydet suurimpien kaupunkien keskustoihin
    """
    print("Lasketaan etäisyyksiä keskustoihin...")
    
    keskustat = {
        'Helsinki': (60.1699, 24.9384),
        'Espoo': (60.2055, 24.6559),
        'Vantaa': (60.2934, 25.0378),
        'Tampere': (61.4978, 23.7610),
        'Turku': (60.4518, 22.2666),
        'Oulu': (65.0121, 25.4651),
        'Kuopio': (62.8924, 27.6782),
        'Jyvaskyla': (62.2426, 25.7473),
        'Lahti': (60.9827, 25.6612),
        'Pori': (61.4847, 21.7972)
    }
    
    etaisyydet = {}
    
    for postinumero, coords in postinumerokoordinaatit.items():
        lat, lon = coords['lat'], coords['lon']
        
        # Laske etäisyys jokaiseen keskustaan
        etaisyys_keskustoihin = {}
        for kaupunki, (c_lat, c_lon) in keskustat.items():
            etaisyys = laske_etaisyys(lat, lon, c_lat, c_lon)
            etaisyys_keskustoihin[kaupunki.lower()] = round(etaisyys, 2)
        
        # Laske etäisyys lähimpään keskustaan
        lahin_etaisyys = min(etaisyys_keskustoihin.values())
        
        etaisyydet[postinumero] = {
            'lahin_keskusta_km': lahin_etaisyys,
            'keskustat': etaisyys_keskustoihin
        }
    
    print(f"   Laskettu etäisyydet {len(etaisyydet)} postinumeroalueelle")
    return etaisyydet


def main():
    print("="*60)
    print("RIKASTAN ASUNTOHINTADATAA")
    print("="*60)
    
    # 1. Hae Paavo-väestötiedot
    paavo_data = hae_paavo_data()
    
    # 2. Lataa postinumerokoordinaatit
    print("\nLadataan postinumerokoordinaatteja...")
    try:
        with open('postinumerokoordinaatit.json', 'r', encoding='utf-8') as f:
            koordinaatit_raw = json.load(f)
            
        # Muunna oikeaan muotoon
        postinumerokoordinaatit = {}
        for postinumero, coords in koordinaatit_raw.items():
            # Tarkista onko dict-muodossa (uusi) vai lista-muodossa (vanha)
            if isinstance(coords, dict) and 'lat' in coords and 'lon' in coords:
                # Uusi muoto: {"lat": ..., "lon": ...}
                postinumerokoordinaatit[postinumero] = coords
            elif isinstance(coords, list) and len(coords) == 2:
                # Vanha muoto: [lon, lat]
                postinumerokoordinaatit[postinumero] = {
                    'lat': coords[1],  # lat, lon järjestys
                    'lon': coords[0]
                }
        
        print(f"   Ladattu {len(postinumerokoordinaatit)} postinumeroalueen koordinaatit")
    except FileNotFoundError:
        print("   postinumerokoordinaatit.json ei löydy. Aja ensin lataa_postinumeroalueet.py")
        return
    
    # 3. Laske etäisyydet keskustoihin
    etaisyydet = laske_etaisyydet_keskustoihin(postinumerokoordinaatit)
    
    # 4. Yhdistä kaikki data
    rikastettu_data = {}
    
    for postinumero in paavo_data.keys():
        rikastettu_data[postinumero] = {
            'paavo': paavo_data.get(postinumero, {}),
            'etaisyydet': etaisyydet.get(postinumero, {})
        }
    
    # 5. Tallenna
    output_file = 'data/rikastettu_data.json'
    
    import os
    os.makedirs('data', exist_ok=True)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(rikastettu_data, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ Rikastettu data tallennettu: {output_file}")
    print(f"   Postinumeroalueita: {len(rikastettu_data)}")
    print(f"   - Paavo-tiedot: {len(paavo_data)}")
    print(f"   - Etäisyydet: {len(etaisyydet)}")
    print("="*60)


if __name__ == "__main__":
    main()
