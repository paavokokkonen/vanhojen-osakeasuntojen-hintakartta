#!/usr/bin/env python3
"""
Hae matka-ajat postinumeroalueilta lähimpään kaupungin keskustaan
================================================================
Käyttää Digitransit Routing API v2 (GraphQL) hakemaan julkisen liikenteen
matka-ajan jokaisen postinumeroalueen centroidista lähimpään suureen keskustaan.

Digitransit API vaatii rekisteröinnin:
  https://digitransit.fi/en/developers/api-registration/

Käyttö:
  set DIGITRANSIT_API_KEY=sinun-api-avain
  python lataa_matka_ajat.py

Tai suorita ilman API-avainta → käyttää laskennallista arviota (Haversine + kerroin).
"""

import json
import os
import time
import math
import requests

# Keskustat ja niiden koordinaatit
KESKUSTAT = {
    'Helsinki': (60.1699, 24.9384),
    'Tampere': (61.4978, 23.7610),
    'Turku': (60.4518, 22.2666),
    'Oulu': (65.0121, 25.4651),
    'Kuopio': (62.8924, 27.6782),
    'Jyvaskyla': (62.2426, 25.7473),
    'Lahti': (60.9827, 25.6612),
}

# Digitransit endpoints
ENDPOINTS = {
    'finland': 'https://api.digitransit.fi/routing/v2/finland/gtfs/v1',
}

GRAPHQL_QUERY = """
{
  planConnection(
    origin: {location: {coordinate: {latitude: %f, longitude: %f}}}
    destination: {location: {coordinate: {latitude: %f, longitude: %f}}}
    first: 3
    modes: {transit: {transit: [{mode: BUS}, {mode: RAIL}, {mode: TRAM}]}}
  ) {
    edges {
      node {
        duration
        walkDistance
        legs {
          mode
          duration
        }
      }
    }
  }
}
"""


def haversine_km(lat1, lon1, lat2, lon2):
    """Haversine-etäisyys km"""
    R = 6371
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat/2)**2 + 
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * 
         math.sin(dlon/2)**2)
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))


def lahin_keskusta(lat, lon):
    """Palauttaa lähimmän keskustan nimen ja etäisyyden km"""
    paras = None
    paras_km = float('inf')
    for nimi, (c_lat, c_lon) in KESKUSTAT.items():
        km = haversine_km(lat, lon, c_lat, c_lon)
        if km < paras_km:
            paras_km = km
            paras = nimi
    return paras, paras_km


def arvio_matka_aika(etaisyys_km):
    """
    Laskennallinen matka-aika-arvio (minuutteja) ilman API:a.
    Perustuu empiiriseen kaavaan: julkinen liikenne ~30 km/h kaupungissa,
    mutta sisältää odotus- ja vaihtoaikoja.
    
    Kaava: matka_aika = 10 + etaisyys * 2.5 (minuuttia)
    - 10 min: kävely pysäkille + odotus
    - 2.5 min/km: keskimääräinen julkisen liikenteen nopeus odotuksineen
    """
    if etaisyys_km < 0.5:
        return 5  # Alle 500m, kävelymatka
    return round(10 + etaisyys_km * 2.5)


def hae_digitransit_matka_aika(api_key, origin_lat, origin_lon, dest_lat, dest_lon):
    """
    Hae matka-aika Digitransit API:sta (minuutteja).
    Palauttaa None jos ei yhteyttä tai ei julkista liikennettä.
    """
    url = ENDPOINTS['finland']
    query = GRAPHQL_QUERY % (origin_lat, origin_lon, dest_lat, dest_lon)
    
    headers = {
        'Content-Type': 'application/graphql',
        'digitransit-subscription-key': api_key,
    }
    
    try:
        resp = requests.post(url, data=query, headers=headers, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        
        edges = data.get('data', {}).get('planConnection', {}).get('edges', [])
        if not edges:
            return None
        
        # Ota lyhin matka-aika
        durations = []
        for edge in edges:
            node = edge.get('node', {})
            duration_sec = node.get('duration')
            if duration_sec and duration_sec > 0:
                durations.append(duration_sec / 60)  # sekunnit → minuuttia
        
        return round(min(durations)) if durations else None
        
    except Exception as e:
        return None


def main():
    print("=" * 60)
    print("MATKA-AIKOJEN LASKENTA")
    print("=" * 60)
    
    api_key = os.environ.get('DIGITRANSIT_API_KEY', '')
    use_api = bool(api_key)
    
    if use_api:
        print(f"✅ Digitransit API-avain löytyy, käytetään reititys-API:a")
        print(f"   Endpoint: {ENDPOINTS['finland']}")
    else:
        print("⚠️  DIGITRANSIT_API_KEY ei asetettu")
        print("   Käytetään laskennallista matka-aika-arviota (Haversine × kerroin)")
        print("   Aseta API-avain: set DIGITRANSIT_API_KEY=sinun-avain")
        print("   Rekisteröidy: https://digitransit.fi/en/developers/api-registration/")
    
    # Lataa postinumerokoordinaatit
    print("\nLadataan postinumerokoordinaatteja...")
    try:
        with open('postinumerokoordinaatit.json', 'r', encoding='utf-8') as f:
            koordinaatit = json.load(f)
        print(f"   {len(koordinaatit)} postinumeroaluetta")
    except FileNotFoundError:
        print("❌ postinumerokoordinaatit.json ei löydy!")
        return
    
    matka_ajat = {}
    api_haut = 0
    api_virheet = 0
    
    total = len(koordinaatit)
    for i, (pno, coords) in enumerate(koordinaatit.items()):
        if isinstance(coords, dict):
            lat, lon = coords['lat'], coords['lon']
        elif isinstance(coords, list):
            lon, lat = coords[0], coords[1]
        else:
            continue
        
        keskusta, etaisyys_km = lahin_keskusta(lat, lon)
        keskusta_coords = KESKUSTAT[keskusta]
        
        matka_aika = None
        lahde = 'arvio'
        
        # Yritä Digitransit API:a jos avain on
        if use_api and etaisyys_km < 150:  # API vain < 150 km keskustasta
            matka_aika = hae_digitransit_matka_aika(
                api_key, lat, lon, keskusta_coords[0], keskusta_coords[1]
            )
            api_haut += 1
            
            if matka_aika is not None:
                lahde = 'digitransit'
            else:
                api_virheet += 1
            
            # API rate limiting
            if api_haut % 10 == 0:
                time.sleep(1)
            if api_haut % 100 == 0:
                print(f"   API-hakuja: {api_haut}, onnistuneet: {api_haut - api_virheet}")
        
        # Fallback: laskennallinen arvio
        if matka_aika is None:
            matka_aika = arvio_matka_aika(etaisyys_km)
            lahde = 'arvio'
        
        matka_ajat[pno] = {
            'matka_aika_min': matka_aika,
            'lahin_keskusta': keskusta,
            'etaisyys_km': round(etaisyys_km, 1),
            'lahde': lahde,
        }
        
        if (i + 1) % 500 == 0:
            print(f"   Käsitelty {i+1}/{total} aluetta...")
    
    # Tilastot
    arviot = sum(1 for v in matka_ajat.values() if v['lahde'] == 'arvio')
    api_ok = sum(1 for v in matka_ajat.values() if v['lahde'] == 'digitransit')
    matka_ajat_list = [v['matka_aika_min'] for v in matka_ajat.values() if v['matka_aika_min']]
    
    print(f"\n📊 Tulokset:")
    print(f"   Alueita yhteensä: {len(matka_ajat)}")
    if use_api:
        print(f"   Digitransit API: {api_ok} onnistunutta")
    print(f"   Laskennallinen arvio: {arviot}")
    if matka_ajat_list:
        print(f"   Matka-aika: min={min(matka_ajat_list)}, max={max(matka_ajat_list)}, "
              f"keskiarvo={sum(matka_ajat_list)/len(matka_ajat_list):.0f} min")
    
    # Tallenna
    output = {
        'metadata': {
            'lahde': 'digitransit' if use_api else 'laskennallinen_arvio',
            'keskustat': {k: {'lat': v[0], 'lon': v[1]} for k, v in KESKUSTAT.items()},
            'api_haut': api_haut,
            'api_onnistuneet': api_ok,
        },
        'data': matka_ajat
    }
    
    os.makedirs('data', exist_ok=True)
    output_file = 'data/matka_ajat.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ Tallennettu: {output_file}")


if __name__ == '__main__':
    main()
