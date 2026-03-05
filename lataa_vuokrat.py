#!/usr/bin/env python3
"""
Vuokradata Tilastokeskuksesta
==============================
Hakee postinumeroalueittain vuokratiedot taulukosta 13eb:
- Neliövuokrat (EUR/m²/kk)
- Vuokra-asuntojen lukumäärät
- Eriteltynä huoneluvun mukaan (yksiöt, kaksiot, kolmiot+)

Kvartaalidata (Q1-Q4) muunnetaan vuosikeskiarvoiksi.
Tilastokeskuksen StatFin-rajapinnasta (taulukko: asvu_13eb)
Vuodet: 2015-2025
"""

import requests
import json
import time
from datetime import datetime

BASE_URL = "https://statfin.stat.fi/PxWeb/api/v1/fi/StatFin"
TABLE = "asvu/statfin_asvu_pxt_13eb.px"

# Huoneluvut (vuokradata)
ROOM_TYPES = {
    "01": "Yksiot",
    "02": "Kaksiot",
    "03": "Kolmiot+"
}

# Mapping vuokradata -> asuntohintadata talotyypit
# Rent '01' (Yksiöt) -> Price '1' (Kerrostalo yksiöt)
# Rent '02' (Kaksiot) -> Price '2' (Kerrostalo kaksiot)  
# Rent '03' (Kolmiot+) -> Price '3' (Kerrostalo kolmiot+)
ROOM_TO_BUILDING_TYPE = {
    "01": "1",
    "02": "2",
    "03": "3"
}


def get_metadata():
    """Hae taulukon metatiedot"""
    url = f"{BASE_URL}/{TABLE}"
    response = requests.get(url, timeout=30)
    return response.json()


def fetch_rents():
    """Hae nelivuokrat ja lukumaarat postinumeroittain"""
    print("Haetaan metadataa (13eb)...")
    meta = get_metadata()

    # Hae kaikki kvartaalit
    all_quarters = meta['variables'][0]['values']
    print(f"Kvartaalit: {len(all_quarters)} ({all_quarters[0]}-{all_quarters[-1]})")

    # Kaikki postinumerot
    all_postcodes = meta['variables'][1]['values']
    print(f"Postinumerot: {len(all_postcodes)}")

    # Hae data erissa
    results = {}
    batch_size = 200

    for i in range(0, len(all_postcodes), batch_size):
        batch = all_postcodes[i:i+batch_size]
        print(f"  Haetaan postinumerot {i+1}-{min(i+batch_size, len(all_postcodes))}...")

        query = {
            "query": [
                {
                    "code": "Vuosinelj\u00e4nnes",
                    "selection": {"filter": "item", "values": all_quarters}
                },
                {
                    "code": "Postinumero",
                    "selection": {"filter": "item", "values": batch}
                },
                {
                    "code": "Huoneluku",
                    "selection": {"filter": "item", "values": list(ROOM_TYPES.keys())}
                },
                {
                    "code": "Tiedot",
                    "selection": {"filter": "item", "values": ["keskivuokra", "lkm_ptno"]}
                }
            ],
            "response": {"format": "json"}
        }

        url = f"{BASE_URL}/{TABLE}"
        response = requests.post(url, json=query, timeout=90)

        if response.status_code == 200:
            data = response.json()

            for item in data.get('data', []):
                quarter = item['key'][0]       # "2024Q3"
                postcode = item['key'][1]       # "00100"
                room_type = item['key'][2]      # "01"
                values_list = item['values']    # ["819", "29.66"]

                # Parse arvot (lkm, keskivuokra)
                lkm_raw = values_list[0]
                vuokra_raw = values_list[1]

                lkm = None
                vuokra = None

                if lkm_raw not in ['.', '..', '...', '']:
                    try:
                        lkm = int(float(lkm_raw))
                    except (ValueError, TypeError):
                        pass

                if vuokra_raw not in ['.', '..', '...', '']:
                    try:
                        vuokra = float(vuokra_raw)
                    except (ValueError, TypeError):
                        pass

                if vuokra is not None:
                    if postcode not in results:
                        results[postcode] = {}
                    if quarter not in results[postcode]:
                        results[postcode][quarter] = {}

                    results[postcode][quarter][room_type] = {
                        'keskivuokra': vuokra
                    }
                    if lkm is not None:
                        results[postcode][quarter][room_type]['lkm'] = lkm

        time.sleep(0.5)

    return results, meta, all_quarters


def aggregate_to_annual(quarterly_data, all_quarters):
    """
    Muunna kvartaalidata vuosikeskiarvoiksi.

    Strategia: Lasketaan aritmeettinen keskiarvo kaikista saatavilla
    olevista kvartaaleista per vuosi. Tama on paras tapa koska:
    - Tasaa kausivaihtelun (kesa vs. talvi)
    - Kayttaa kaiken saatavilla olevan datan
    - Yhteensopiva vuosittaisen asuntohintadatan kanssa
    """
    print("\nLasketaan vuosikeskiarvoja kvartaalidatasta...")

    # Selvita saatavilla olevat vuodet
    years = sorted(set(q[:4] for q in all_quarters))
    print(f"  Vuodet: {years[0]}-{years[-1]}")

    annual_data = {}

    for postcode, quarters in quarterly_data.items():
        annual_data[postcode] = {}

        for year in years:
            year_quarters = [f"{year}Q{q}" for q in range(1, 5)]

            for room_type in ROOM_TYPES.keys():
                vuokrat = []
                total_lkm = 0

                for q in year_quarters:
                    if q in quarters and room_type in quarters[q]:
                        q_data = quarters[q][room_type]
                        vuokrat.append(q_data['keskivuokra'])
                        total_lkm += q_data.get('lkm', 0)

                if vuokrat:
                    # Vuosikeskiarvo = aritmeettinen keskiarvo kvartaaleista
                    avg_vuokra = sum(vuokrat) / len(vuokrat)

                    if year not in annual_data[postcode]:
                        annual_data[postcode][year] = {}

                    # Kayta talotyyppi-koodia (1,2,3) yhteensopivuuden vuoksi
                    building_type = ROOM_TO_BUILDING_TYPE[room_type]
                    annual_data[postcode][year][building_type] = {
                        'keskivuokra': round(avg_vuokra, 2),
                        'lkm': total_lkm,
                        'kvartaaleja': len(vuokrat)
                    }

    # Lisaa "Kaikki"-kategoria (painotettu keskiarvo)
    for postcode in annual_data:
        for year in annual_data[postcode]:
            year_data = annual_data[postcode][year]
            total_weighted = 0
            total_count = 0

            for bt in ['1', '2', '3']:
                if bt in year_data:
                    lkm = year_data[bt].get('lkm', 0)
                    if lkm > 0:
                        total_weighted += year_data[bt]['keskivuokra'] * lkm
                        total_count += lkm

            if total_count > 0:
                year_data['0'] = {
                    'keskivuokra': round(total_weighted / total_count, 2),
                    'lkm': total_count
                }

    return annual_data, years


def export_to_json(annual_data, years, filename="data/vuokradata.json"):
    """Vie JSON:iin"""
    import os
    os.makedirs('data', exist_ok=True)

    output = {
        "metadata": {
            "source": "Tilastokeskus (StatFin) - Asuntojen vuokrat postinumeroalueittain",
            "table": "asvu_13eb",
            "description": "Vapaarahoitteisten vuokra-asuntojen nelivuokrat",
            "years": years,
            "room_types": ROOM_TYPES,
            "building_type_mapping": ROOM_TO_BUILDING_TYPE,
            "unit": "EUR/m2/kk (kuukausivuokra per neliometri)",
            "aggregation": "Vuosikeskiarvo kvartaalidatasta (Q1-Q4 aritmeettinen keskiarvo)",
            "last_updated": datetime.now().isoformat()
        },
        "data": annual_data
    }

    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    file_size_mb = len(json.dumps(output)) / (1024 * 1024)
    print(f"\n[OK] Vuokradata viety: {filename}")
    print(f"   Koko: {file_size_mb:.1f} MB")
    return output


def print_summary(annual_data, years):
    """Tulosta yhteenveto"""
    print("\n" + "=" * 60)
    print("V U O K R A D A T A   Y H T E E N V E T O")
    print("=" * 60)

    latest_year = years[-1]
    postcodes_with_data = 0
    vuokrat_yksiot = []
    vuokrat_kaksiot = []

    for postcode, year_data in annual_data.items():
        if latest_year in year_data:
            postcodes_with_data += 1
            if '1' in year_data[latest_year]:
                vuokrat_yksiot.append(year_data[latest_year]['1']['keskivuokra'])
            if '2' in year_data[latest_year]:
                vuokrat_kaksiot.append(year_data[latest_year]['2']['keskivuokra'])

    print(f"\nVuosi {latest_year}:")
    print(f"  Postinumeroalueita vuokradatalla: {postcodes_with_data}")

    if vuokrat_yksiot:
        print(f"  Yksiot:")
        print(f"    Keskivuokra: {sum(vuokrat_yksiot)/len(vuokrat_yksiot):.2f} EUR/m2/kk")
        print(f"    Min: {min(vuokrat_yksiot):.2f} EUR/m2/kk")
        print(f"    Max: {max(vuokrat_yksiot):.2f} EUR/m2/kk")

    if vuokrat_kaksiot:
        print(f"  Kaksiot:")
        print(f"    Keskivuokra: {sum(vuokrat_kaksiot)/len(vuokrat_kaksiot):.2f} EUR/m2/kk")
        print(f"    Min: {min(vuokrat_kaksiot):.2f} EUR/m2/kk")
        print(f"    Max: {max(vuokrat_kaksiot):.2f} EUR/m2/kk")

    # Top 5 kalleimmat (yksiot)
    if vuokrat_yksiot:
        top5_data = []
        for postcode, year_data in annual_data.items():
            if latest_year in year_data and '1' in year_data[latest_year]:
                top5_data.append((postcode, year_data[latest_year]['1']['keskivuokra']))

        top5 = sorted(top5_data, key=lambda x: x[1], reverse=True)[:5]
        print(f"\n  Kalleimmat vuokrat (yksiot):")
        for postcode, vuokra in top5:
            print(f"    {postcode}: {vuokra:.2f} EUR/m2/kk")

    print(f"\nVuodet: {years[0]}-{years[-1]} ({len(years)} vuotta)")
    print("=" * 60)


def main():
    print("=" * 60)
    print("VUOKRADATA POSTINUMEROALUEITTAIN")
    print("Tilastokeskus, taulukko 13eb (2015-2025)")
    print("=" * 60)

    # 1. Hae kvartaalidata
    quarterly_data, meta, all_quarters = fetch_rents()

    print(f"\nHaettu {len(quarterly_data)} postinumeroaluetta")

    # 2. Muunna vuosikeskiarvoiksi
    annual_data, years = aggregate_to_annual(quarterly_data, all_quarters)

    # 3. Vie
    export_to_json(annual_data, years)

    # 4. Yhteenveto
    print_summary(annual_data, years)

    return annual_data


if __name__ == "__main__":
    main()
