#!/usr/bin/env python3
"""
Laske palveluindeksi uudelleen normalisoituna (tiheys/km² + log-skaalaus).
Ei tarvitse ajaa OSM-parsintaa uudelleen - käyttää olemassa olevia raakamääriä.
"""
import json
import math
from shapely.geometry import shape

print("Lasketaan palveluindeksi uudelleen normalisoituna...")

# Ladataan data
with open('postinumerot_hinnat.geojson', 'r', encoding='utf-8') as f:
    geojson = json.load(f)

with open('data/rikastettu_data.json', 'r', encoding='utf-8') as f:
    rikastettu = json.load(f)

# Laske pinta-alat (likimääräinen WGS84-pohjainen laskelma)
alueen_alat = {}
for feature in geojson.get('features', []):
    pno = feature['properties'].get('postinumer')
    if pno and 'geometry' in feature:
        geom = shape(feature['geometry'])
        centroid = geom.centroid
        lat_rad = math.radians(centroid.y)
        lat_factor = 111320  # m per degree lat
        lon_factor = 111320 * math.cos(lat_rad)
        area_km2 = geom.area * lat_factor * lon_factor / 1_000_000
        alueen_alat[pno] = max(area_km2, 0.01)

# Painot
painot = {
    'kaupat': 1.0,
    'koulut': 1.5,
    'paivakodit': 1.2,
    'liikuntapaikat': 0.8,
    'terveysasemat': 1.3,
    'julkinen_liikenne': 0.5,
    'ravintolat': 0.7,
    'kahvilat': 0.5,
    'puistot': 0.6,
    'kirjastot': 1.0,
    'apteekit': 1.1
}

# Laske uudet palveluindeksit
paivitetty = 0
for pno, data in rikastettu.items():
    palvelut = data.get('palvelut', {})
    if not palvelut or 'kaupat' not in palvelut:
        continue
    
    area = alueen_alat.get(pno, 1.0)
    
    # Uusi kaava: log(1 + palvelulkm/pinta-ala) * paino
    palveluindeksi = sum(
        math.log(1 + palvelut.get(k, 0) / area) * paino
        for k, paino in painot.items()
    )
    
    vanha = palvelut.get('palveluindeksi', 0)
    palvelut['palveluindeksi'] = round(palveluindeksi, 2)
    paivitetty += 1

# Tallenna
with open('data/rikastettu_data.json', 'w', encoding='utf-8') as f:
    json.dump(rikastettu, f, ensure_ascii=False, indent=2)

print(f"Päivitetty {paivitetty} alueen palveluindeksi")

# Tulosta top 15 tarkistukseksi
items = [(pno, data.get('palvelut', {}).get('palveluindeksi', 0)) 
         for pno, data in rikastettu.items() 
         if data.get('palvelut', {}).get('palveluindeksi', 0) > 0]
items.sort(key=lambda x: x[1], reverse=True)

print("\nTOP 15 normalisoitu palveluindeksi:")
for pno, idx in items[:15]:
    p = rikastettu[pno].get('palvelut', {})
    area = alueen_alat.get(pno, 0)
    print(f"  {pno}: idx={idx:.2f}, area={area:.1f}km², julk={p.get('julkinen_liikenne',0)}, kaupat={p.get('kaupat',0)}")

print(f"\n88900 Kuhmo: {rikastettu.get('88900', {}).get('palvelut', {}).get('palveluindeksi', 'N/A')}")
print(f"00100 Helsinki: {rikastettu.get('00100', {}).get('palvelut', {}).get('palveluindeksi', 'N/A')}")
