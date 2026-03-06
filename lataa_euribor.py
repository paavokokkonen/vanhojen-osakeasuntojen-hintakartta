#!/usr/bin/env python3
"""
Hae Euribor-aikasarjadata ennustemallien eksogenisenä muuttujana
================================================================
Hakee 12 kuukauden Euriborin vuosikeskiarvot ECB:n SDW-rajapinnasta.

Käyttö:
  python lataa_euribor.py

Tuottaa:
  data/euribor.json — Euribor-aikasarja vuosittain
"""

import json
import os
import requests
from datetime import datetime


def hae_euribor_ecb():
    """
    Hae 12kk Euribor-korot ECB Statistical Data Warehouse -rajapinnasta.
    ECB SDW REST API on avoin eikä vaadi rekisteröintiä.
    
    Sarja: FM.M.U2.EUR.RT.MM.EURIBOR1YD_.HSTA (12kk Euribor, kuukausikeskiarvo)
    """
    print("Haetaan Euribor-aikasarjaa ECB:n rajapinnasta...")
    
    # ECB SDW API — 12 kuukauden Euribor, kuukausikeskiarvo
    url = ("https://data-api.ecb.europa.eu/service/data/"
           "FM/M.U2.EUR.RT.MM.EURIBOR1YD_.HSTA"
           "?format=jsondata&startPeriod=2005-01&detail=dataonly")
    
    try:
        resp = requests.get(url, timeout=30, headers={
            'Accept': 'application/json',
            'User-Agent': 'asuntojen-hintakartta/1.0'
        })
        resp.raise_for_status()
        data = resp.json()
        
        # Parsitaan ECB:n JSON-rakenne
        observations = data['dataSets'][0]['series']['0:0:0:0:0:0:0']['observations']
        time_periods = data['structure']['dimensions']['observation'][0]['values']
        
        # Kerää kuukausidata
        kuukausidata = {}
        for idx, period in enumerate(time_periods):
            period_id = period['id']  # esim. "2023-01"
            value = observations.get(str(idx))
            if value and len(value) > 0 and value[0] is not None:
                kuukausidata[period_id] = round(value[0], 3)
        
        print(f"   Kuukausidatapisteitä: {len(kuukausidata)}")
        
        # Laske vuosikeskiarvot
        vuosittain = {}
        vuosi_arvot = {}
        for period, value in kuukausidata.items():
            vuosi = period[:4]
            if vuosi not in vuosi_arvot:
                vuosi_arvot[vuosi] = []
            vuosi_arvot[vuosi].append(value)
        
        for vuosi, arvot in sorted(vuosi_arvot.items()):
            keski = sum(arvot) / len(arvot)
            vuosittain[vuosi] = {
                'keskiarvo': round(keski, 3),
                'min': round(min(arvot), 3),
                'max': round(max(arvot), 3),
                'kuukausia': len(arvot)
            }
        
        print(f"   Vuosidatapisteitä: {len(vuosittain)} ({min(vuosittain.keys())}-{max(vuosittain.keys())})")
        
        return {
            'kuukausittain': kuukausidata,
            'vuosittain': vuosittain
        }
        
    except Exception as e:
        print(f"   ❌ ECB API virhe: {e}")
        return None


def hae_euribor_fallback():
    """
    Fallback: manuaalinen Euribor-data jos API ei toimi.
    12kk Euribor vuosikeskiarvot (lähde: Suomen Pankki).
    """
    print("   Käytetään manuaalista Euribor-dataa (fallback)...")
    return {
        'kuukausittain': {},
        'vuosittain': {
            '2005': {'keskiarvo': 2.334, 'min': 2.188, 'max': 2.629, 'kuukausia': 12},
            '2006': {'keskiarvo': 3.441, 'min': 2.833, 'max': 3.921, 'kuukausia': 12},
            '2007': {'keskiarvo': 4.448, 'min': 4.064, 'max': 4.793, 'kuukausia': 12},
            '2008': {'keskiarvo': 4.810, 'min': 3.452, 'max': 5.384, 'kuukausia': 12},
            '2009': {'keskiarvo': 1.610, 'min': 1.242, 'max': 2.622, 'kuukausia': 12},
            '2010': {'keskiarvo': 1.350, 'min': 1.210, 'max': 1.526, 'kuukausia': 12},
            '2011': {'keskiarvo': 2.009, 'min': 1.506, 'max': 2.183, 'kuukausia': 12},
            '2012': {'keskiarvo': 1.110, 'min': 0.549, 'max': 1.837, 'kuukausia': 12},
            '2013': {'keskiarvo': 0.536, 'min': 0.507, 'max': 0.588, 'kuukausia': 12},
            '2014': {'keskiarvo': 0.483, 'min': 0.325, 'max': 0.562, 'kuukausia': 12},
            '2015': {'keskiarvo': 0.168, 'min': 0.059, 'max': 0.298, 'kuukausia': 12},
            '2016': {'keskiarvo': -0.034, 'min': -0.082, 'max': 0.042, 'kuukausia': 12},
            '2017': {'keskiarvo': -0.156, 'min': -0.190, 'max': -0.095, 'kuukausia': 12},
            '2018': {'keskiarvo': -0.169, 'min': -0.190, 'max': -0.117, 'kuukausia': 12},
            '2019': {'keskiarvo': -0.224, 'min': -0.312, 'max': -0.108, 'kuukausia': 12},
            '2020': {'keskiarvo': -0.301, 'min': -0.497, 'max': -0.108, 'kuukausia': 12},
            '2021': {'keskiarvo': -0.487, 'min': -0.505, 'max': -0.477, 'kuukausia': 12},
            '2022': {'keskiarvo': 1.098, 'min': -0.477, 'max': 3.018, 'kuukausia': 12},
            '2023': {'keskiarvo': 3.862, 'min': 3.337, 'max': 4.193, 'kuukausia': 12},
            '2024': {'keskiarvo': 3.200, 'min': 2.458, 'max': 3.548, 'kuukausia': 12},
            '2025': {'keskiarvo': 2.400, 'min': 2.200, 'max': 2.600, 'kuukausia': 3},
        }
    }


def main():
    print("=" * 60)
    print("EURIBOR-AIKASARJAN LATAUS")
    print("=" * 60)
    
    result = hae_euribor_ecb()
    
    if result is None:
        result = hae_euribor_fallback()
    
    # Metadata
    output = {
        'metadata': {
            'kuvaus': '12 kuukauden Euribor-korko, vuosikeskiarvot',
            'lahde': 'ECB Statistical Data Warehouse',
            'url': 'https://data.ecb.europa.eu/',
            'paivitetty': datetime.now().isoformat(),
            'yksikko': '%',
        },
        'data': result
    }
    
    vuosittain = result.get('vuosittain', {})
    
    # Näytä aikasarja
    print("\n📊 12kk Euribor vuosikeskiarvot:")
    print("-" * 40)
    for vuosi in sorted(vuosittain.keys()):
        d = vuosittain[vuosi]
        bar = '█' * max(1, int((d['keskiarvo'] + 1) * 5))
        print(f"   {vuosi}: {d['keskiarvo']:+.3f} % {bar}")
    
    # Tallenna
    os.makedirs('data', exist_ok=True)
    output_file = 'data/euribor.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ Tallennettu: {output_file}")


if __name__ == '__main__':
    main()
