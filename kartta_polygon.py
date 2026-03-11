#!/usr/bin/env python3
"""
Asuntojen hintakartta - Polygon-versio
- Vuodet 2009-2025
- Talotyypit (kerrostalot, rivi/ketjutalot, pientalot, kaikki)
- Mittarit (hinnat, kauppojen lukum.)
- Vuosimuutokset
"""

import json

print("Ladataan dataa...")

# Lataa asuntohintadata
with open('asuntohinnat.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Lataa GeoJSON
with open('postinumerot_hinnat.geojson', 'r', encoding='utf-8') as f:
    geojson_data = json.load(f)

# Lataa trendianalyysi (jos saatavilla)
try:
    with open('data/trendianalyysi.json', 'r', encoding='utf-8') as f:
        trendianalyysi = json.load(f)['analyysit']
    print(f"  Trendianalyysi: {len(trendianalyysi)} aluetta")
except FileNotFoundError:
    trendianalyysi = {}
    print("  Trendianalyysi: Ei saatavilla")

# Lataa rikastettu data (Paavo-väestötiedot)
try:
    with open('data/rikastettu_data.json', 'r', encoding='utf-8') as f:
        rikastettu_data = json.load(f)
    print(f"  Väestötiedot: {len(rikastettu_data)} aluetta")
except FileNotFoundError:
    rikastettu_data = {}
    print("  Väestötiedot: Ei saatavilla")

# Lataa ennustemallit (Linear, ARIMA, Exponential Smoothing)
try:
    with open('data/ennusteet_mallit.json', 'r', encoding='utf-8') as f:
        ennusteet_mallit = json.load(f)
    model_counts = {}
    for pc_data in ennusteet_mallit.values():
        for bt_data in pc_data.values():
            for model in bt_data.keys():
                model_counts[model] = model_counts.get(model, 0) + 1
    print(f"  Ennustemallit: {', '.join(f'{k}={v}' for k, v in model_counts.items())}")
except FileNotFoundError:
    ennusteet_mallit = {}
    print("  Ennustemallit: Ei saatavilla (aja: python laske_ennusteet.py)")

# Lataa vuokradata (Tilastokeskus 13eb)
try:
    with open('data/vuokradata.json', 'r', encoding='utf-8') as f:
        vuokradata = json.load(f)
    vuokra_years = vuokradata['metadata']['years']
    vuokra_postcodes = len(vuokradata['data'])
    print(f"  Vuokradata: {vuokra_postcodes} aluetta, {vuokra_years[0]}-{vuokra_years[-1]}")
except FileNotFoundError:
    vuokradata = {'data': {}}
    print("  Vuokradata: Ei saatavilla (aja: python lataa_vuokrat.py)")

# Lataa matka-ajat (Digitransit / laskennallinen)
try:
    with open('data/matka_ajat.json', 'r', encoding='utf-8') as f:
        matka_ajat_data = json.load(f)
    matka_ajat = matka_ajat_data.get('data', {})
    print(f"  Matka-ajat: {len(matka_ajat)} aluetta ({matka_ajat_data.get('metadata', {}).get('lahde', '?')})")
except FileNotFoundError:
    matka_ajat = {}
    print("  Matka-ajat: Ei saatavilla (aja: python lataa_matka_ajat.py)")

# Lataa Euribor-aikasarja
try:
    with open('data/euribor.json', 'r', encoding='utf-8') as f:
        euribor_data = json.load(f)
    euribor_vuosittain = euribor_data.get('data', {}).get('vuosittain', {})
    print(f"  Euribor: {len(euribor_vuosittain)} vuotta ({min(euribor_vuosittain.keys())}-{max(euribor_vuosittain.keys())})")
except FileNotFoundError:
    euribor_data = {'data': {'vuosittain': {}}}
    euribor_vuosittain = {}
    print("  Euribor: Ei saatavilla (aja: python lataa_euribor.py)")

# Hae metatiedot
available_years = sorted(data['metadata']['years'])
building_types = data['metadata']['building_types']
latest_year = available_years[-2]  # 2025 - viimeisin datavuosi (ei ennuste)

print(f"  Vuodet: {len(available_years)} ({min(available_years)}-{max(available_years)})")
print(f"  Talotyypit: {len(building_types)}")
print(f"  Postinumeroalueita: {len(geojson_data['features'])}")

# Lisää hintadata GeoJSON-featureisiin
print("Yhdistetään dataa...")
for feature in geojson_data['features']:
    postcode = feature['properties']['postinumer']
    feature['properties']['data'] = {}
    
    # Lisää hintadata jos postinumero löytyy
    if postcode in data['data']:
        feature['properties']['data'] = data['data'][postcode]['data']
        # data-rakenne: {year: {building_type: {keskihinta_aritm_nw, lkm_julk20}}}
    
    # Lisää trendianalyysi jos saatavilla
    if postcode in trendianalyysi:
        feature['properties']['analyysi'] = trendianalyysi[postcode]
    
    # Lisää Paavo-tiedot jos saatavilla (aikasarjadata 2015-2026)
    if postcode in rikastettu_data:
        paavo_aikasarja = rikastettu_data[postcode].get('paavo', {})
        
        # Valitse viimeisin saatavilla oleva vuosi väestötiedoista
        # Suosi vuotta jolla on myös työpaikkatietoja (tp_tyopy > 0)
        if paavo_aikasarja:
            vuodet_jarj = sorted(paavo_aikasarja.keys(), reverse=True)
            viimeisin_vuosi = vuodet_jarj[0]
            # Etsi viimeisin vuosi jolla tp_tyopy > 0 (työpaikkatilasto julkaistu)
            for v in vuodet_jarj:
                if paavo_aikasarja[v].get('tp_tyopy', 0) > 0:
                    viimeisin_vuosi = v
                    break
            feature['properties']['paavo'] = paavo_aikasarja[viimeisin_vuosi]
            feature['properties']['paavo_aikasarja'] = paavo_aikasarja
        else:
            feature['properties']['paavo'] = None
            feature['properties']['paavo_aikasarja'] = {}
        
        # Lisää palvelutiedot jos saatavilla
        palvelut = rikastettu_data[postcode].get('palvelut', {})
        feature['properties']['palvelut'] = palvelut if palvelut else {}
    
    # Lisää vuokradata jos saatavilla
    if postcode in vuokradata.get('data', {}):
        feature['properties']['vuokra'] = vuokradata['data'][postcode]
    else:
        feature['properties']['vuokra'] = {}
    
    # Lisää matka-aika jos saatavilla
    if postcode in matka_ajat:
        feature['properties']['matka_aika'] = matka_ajat[postcode]
    else:
        feature['properties']['matka_aika'] = {}

# Luo JavaScript-muuttujat
years_json = json.dumps(available_years)
building_types_json = json.dumps(building_types)
geojson_json = json.dumps(geojson_data)
ennusteet_mallit_json = json.dumps(ennusteet_mallit)
euribor_json = json.dumps(euribor_vuosittain)

# Laske oletustilastot (viimeisin vuosi, Kaikki-kategoria, hinnat)
default_prices = []
for feature in geojson_data['features']:
    if latest_year in feature['properties'].get('data', {}):
        if '0' in feature['properties']['data'][latest_year]:
            if 'keskihinta_aritm_nw' in feature['properties']['data'][latest_year]['0']:
                default_prices.append(feature['properties']['data'][latest_year]['0']['keskihinta_aritm_nw'])

avg_price = int(sum(default_prices) / len(default_prices)) if default_prices else 0
max_price = int(max(default_prices)) if default_prices else 0
min_price = int(min(default_prices)) if default_prices else 0

# Kerää kuntalista hakutyökalua varten
kunnat_set = set()
for feature in geojson_data['features']:
    city_name = feature['properties'].get('city', '')
    if city_name:
        kunnat_set.add(city_name)
kunnat_sorted = sorted(kunnat_set)
kunnat_options = chr(10).join(f'                <option value="{k}">{k}</option>' for k in kunnat_sorted)
kunnat_json = json.dumps(kunnat_sorted)

html = f'''<!DOCTYPE html>
<html lang="fi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Asuntojen hintakartta 2009-{latest_year}</title>
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
    <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.7/dist/chart.umd.min.js"></script>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; }}
        
        #header {{
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            color: white;
            padding: 20px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.2);
            position: relative;
        }}
        #header h1 {{ font-size: 24px; margin-bottom: 5px; }}
        #header p {{ opacity: 0.8; font-size: 14px; }}
        #header .forecast-note {{ opacity: 0.7; font-size: 12px; font-style: italic; margin-top: 5px; }}
        
        #mobile-menu-toggle {{
            display: none;
            position: absolute;
            top: 15px;
            right: 15px;
            z-index: 1001;
            background: rgba(255,255,255,0.2);
            border: 2px solid white;
            color: white;
            font-size: 24px;
            width: 40px;
            height: 40px;
            border-radius: 6px;
            cursor: pointer;
            align-items: center;
            justify-content: center;
            transition: all 0.3s;
        }}
        #mobile-menu-toggle:active {{
            background: rgba(255,255,255,0.3);
        }}
        
        #controls {{
            background: #2a5298;
            padding: 15px 20px;
            color: white;
            display: flex;
            gap: 20px;
            align-items: center;
            flex-wrap: wrap;
        }}
        #controls label {{ font-size: 13px; font-weight: 500; margin-right: 5px; }}
        #controls select {{
            padding: 6px 10px;
            border-radius: 4px;
            border: 1px solid #ddd;
            font-size: 14px;
        }}
        #controls .control-group {{
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        
        #stats {{
            display: flex;
            gap: 15px;
            padding: 15px 20px;
            background: #f8f9fa;
            flex-wrap: wrap;
        }}
        .stat-box {{
            background: white;
            padding: 10px 20px;
            border-radius: 8px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }}
        .stat-box .label {{ font-size: 12px; color: #666; }}
        .stat-box .value {{ font-size: 20px; font-weight: bold; }}
        
        #map {{ height: calc(100vh - 270px); width: 100%; }}
        
        .legend {{
            background: white;
            padding: 15px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.2);
            line-height: 1.8;
        }}
        .legend h4 {{ margin-bottom: 10px; }}
        .legend-item {{ display: flex; align-items: center; gap: 8px; }}
        .legend-color {{
            width: 20px;
            height: 20px;
            border-radius: 4px;
            border: 1px solid #ccc;
        }}
        
        .popup-content {{ min-width: 220px; }}
        .popup-content h3 {{ margin-bottom: 10px; color: #1e3c72; }}
        .popup-content .price {{ font-size: 24px; font-weight: bold; color: #27ae60; }}
        .popup-content .details {{ margin-top: 10px; font-size: 12px; color: #666; }}
        
        #search-box {{
            position: absolute;
            top: 10px;
            right: 10px;
            z-index: 1000;
            background: white;
            padding: 10px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.2);
        }}
        #search-box input {{
            padding: 8px 12px;
            border: 1px solid #ddd;
            border-radius: 4px;
            width: 200px;
            font-size: 14px;
        }}
        
        .city-buttons {{
            position: absolute;
            top: 250px;
            left: 10px;
            z-index: 1000;
            display: flex;
            flex-direction: column;
            gap: 5px;
        }}
        .city-buttons button {{
            padding: 6px 12px;
            background: white;
            border: 1px solid #ddd;
            border-radius: 4px;
            cursor: pointer;
            box-shadow: 0 2px 5px rgba(0,0,0,0.2);
            font-size: 13px;
            white-space: nowrap;
        }}
        .city-buttons button:hover {{
            background: #f0f0f0;
        }}
        
        /* Mobiili */
        @media (max-width: 768px) {{
            #header {{
                padding: 10px 15px;
            }}
            #header h1 {{
                font-size: 16px;
                margin-bottom: 0;
                padding-right: 50px;
            }}
            #header p {{
                display: none;
            }}
            #header .forecast-note {{
                display: none;
            }}
            
            #mobile-menu-toggle {{
                display: flex;
            }}
            
            #controls {{
                display: none;
                padding: 10px 15px;
                gap: 10px;
                max-height: 0;
                overflow: hidden;
                transition: max-height 0.3s ease-out;
            }}
            #controls.mobile-menu-open {{
                display: flex;
                max-height: 500px;
            }}
            #controls .control-group {{
                flex-basis: 100%;
                gap: 5px;
            }}
            #controls select {{
                font-size: 13px;
                padding: 5px 8px;
                width: 100%;
            }}
            #controls label {{
                font-size: 12px;
            }}
            
            #stats {{
                position: absolute;
                top: 50px;
                left: 0;
                right: 0;
                z-index: 999;
                padding: 8px 10px;
                gap: 8px;
                background: rgba(255, 255, 255, 0.95);
                box-shadow: 0 2px 8px rgba(0,0,0,0.15);
                transition: opacity 0.3s;
            }}
            #controls.mobile-menu-open ~ #stats {{
                opacity: 0;
                pointer-events: none;
            }}
            .stat-box {{
                padding: 6px 10px;
                flex: 1;
                min-width: 70px;
            }}
            .stat-box .label {{
                font-size: 9px;
            }}
            .stat-box .value {{
                font-size: 14px;
            }}
            
            #map {{
                height: calc(100vh - 50px);
            }}
            
            .city-buttons {{
                display: none;
            }}
            #search-box {{
                display: none;
            }}
            
            .popup-content {{
                min-width: 180px;
            }}
            .popup-content h3 {{
                font-size: 16px;
            }}
            .popup-content .price {{
                font-size: 20px;
            }}
            #timeseries-panel {{
                width: 100%;
            }}
        }}
        
        /* Aikasarjakaavio-modal */
        #timeseries-modal {{
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            z-index: 2000;
            background: rgba(0,0,0,0.5);
        }}
        #timeseries-panel {{
            position: absolute;
            top: 0;
            right: 0;
            width: 650px;
            height: 100%;
            background: white;
            overflow-y: auto;
            box-shadow: -4px 0 20px rgba(0,0,0,0.3);
            padding: 25px;
            animation: slideIn 0.3s ease-out;
        }}
        @keyframes slideIn {{
            from {{ transform: translateX(100%); }}
            to {{ transform: translateX(0); }}
        }}
        #timeseries-panel .ts-close-btn {{
            position: sticky;
            top: 0;
            float: right;
            font-size: 28px;
            cursor: pointer;
            color: #666;
            z-index: 10;
            background: white;
            border: none;
            padding: 0 5px;
            line-height: 1;
        }}
        #timeseries-panel .ts-close-btn:hover {{
            color: #333;
        }}
        #timeseries-panel h2 {{
            color: #1e3c72;
            margin-bottom: 5px;
            font-size: 22px;
        }}
        #timeseries-panel .ts-area-name {{
            color: #666;
            margin-bottom: 20px;
            font-size: 14px;
        }}
        .ts-chart-section {{
            margin-bottom: 30px;
            padding-bottom: 15px;
            border-bottom: 1px solid #eee;
        }}
        .ts-chart-section:last-child {{
            border-bottom: none;
        }}
        .ts-chart-section h3 {{
            color: #2a5298;
            margin-bottom: 10px;
            font-size: 15px;
        }}
        .ts-chart-section canvas {{
            max-height: 280px;
        }}
        .ts-btn {{
            background: #1e3c72;
            color: white;
            border: none;
            padding: 6px 14px;
            border-radius: 4px;
            cursor: pointer;
            font-size: 12px;
            margin-top: 10px;
            display: block;
            width: 100%;
        }}
        .ts-btn:hover {{
            background: #2a5298;
        }}
        
        /* Top 10 -paneeli */
        #top10-toggle {{
            position: absolute;
            bottom: 30px;
            left: 10px;
            z-index: 1000;
            background: white;
            border: 2px solid #1e3c72;
            color: #1e3c72;
            font-weight: bold;
            padding: 8px 14px;
            border-radius: 8px;
            cursor: pointer;
            box-shadow: 0 2px 8px rgba(0,0,0,0.2);
            font-size: 13px;
        }}
        #top10-toggle:hover {{ background: #f0f4ff; }}
        #top10-panel {{
            display: none;
            position: absolute;
            top: 0;
            left: 0;
            width: 370px;
            height: 100%;
            background: white;
            z-index: 1500;
            box-shadow: 4px 0 20px rgba(0,0,0,0.3);
            overflow-y: auto;
            animation: top10SlideIn 0.3s ease-out;
        }}
        @keyframes top10SlideIn {{
            from {{ transform: translateX(-100%); }}
            to {{ transform: translateX(0); }}
        }}
        #top10-panel .top10-header {{
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            color: white;
            padding: 15px 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            position: sticky;
            top: 0;
            z-index: 10;
        }}
        #top10-panel .top10-header h2 {{ font-size: 18px; margin: 0; }}
        #top10-panel .top10-close {{
            background: none;
            border: none;
            color: white;
            font-size: 24px;
            cursor: pointer;
        }}
        .top10-tabs {{
            display: flex;
            flex-wrap: wrap;
            gap: 5px;
            padding: 10px 15px;
            background: #f8f9fa;
            border-bottom: 1px solid #ddd;
            position: sticky;
            top: 52px;
            z-index: 9;
        }}
        .top10-tab {{
            padding: 5px 10px;
            border: 1px solid #ddd;
            border-radius: 15px;
            background: white;
            cursor: pointer;
            font-size: 11px;
            white-space: nowrap;
        }}
        .top10-tab.active {{
            background: #1e3c72;
            color: white;
            border-color: #1e3c72;
        }}
        .top10-list {{
            padding: 10px 15px;
        }}
        .top10-item {{
            display: flex;
            align-items: center;
            padding: 10px;
            border-bottom: 1px solid #f0f0f0;
            cursor: pointer;
            transition: background 0.2s;
        }}
        .top10-item:hover {{ background: #f0f4ff; }}
        .top10-rank {{
            font-weight: bold;
            color: #1e3c72;
            width: 30px;
            font-size: 16px;
        }}
        .top10-info {{ flex: 1; }}
        .top10-info .top10-zip {{ font-weight: bold; color: #333; font-size: 14px; }}
        .top10-info .top10-name {{ font-size: 11px; color: #888; }}
        .top10-value {{
            text-align: right;
            font-weight: bold;
            font-size: 14px;
        }}
        @media (max-width: 768px) {{
            #top10-panel {{ width: 100%; }}
            #top10-toggle {{ bottom: 15px; left: 5px; padding: 6px 10px; font-size: 12px; }}
            #finder-toggle {{ bottom: 15px; left: 95px; padding: 6px 10px; font-size: 12px; }}
            #finder-panel {{ width: 100%; }}
        }}
        
        /* Paras alue -hakutyökalu */
        #finder-toggle {{
            position: absolute;
            bottom: 30px;
            left: 120px;
            z-index: 1000;
            background: white;
            border: 2px solid #27ae60;
            color: #27ae60;
            font-weight: bold;
            padding: 8px 14px;
            border-radius: 8px;
            cursor: pointer;
            box-shadow: 0 2px 8px rgba(0,0,0,0.2);
            font-size: 13px;
        }}
        #finder-toggle:hover {{ background: #f0fff4; }}
        #finder-panel {{
            display: none;
            position: absolute;
            top: 0;
            right: 0;
            width: 380px;
            height: 100%;
            background: white;
            z-index: 1500;
            box-shadow: -4px 0 20px rgba(0,0,0,0.3);
            overflow-y: auto;
            animation: finderSlideIn 0.3s ease-out;
        }}
        @keyframes finderSlideIn {{
            from {{ transform: translateX(100%); }}
            to {{ transform: translateX(0); }}
        }}
        .finder-header {{
            background: linear-gradient(135deg, #27ae60 0%, #2ecc71 100%);
            color: white;
            padding: 15px 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            position: sticky;
            top: 0;
            z-index: 10;
        }}
        .finder-header h2 {{ font-size: 18px; margin: 0; }}
        .finder-close {{
            background: none;
            border: none;
            color: white;
            font-size: 24px;
            cursor: pointer;
        }}
        .finder-form {{
            padding: 15px;
        }}
        .finder-group {{
            margin-bottom: 14px;
        }}
        .finder-group label {{
            display: block;
            font-weight: bold;
            font-size: 13px;
            color: #333;
            margin-bottom: 5px;
        }}
        .finder-group select,
        .finder-group input[type="range"] {{
            width: 100%;
        }}
        .finder-group select {{
            padding: 8px;
            border: 1px solid #ddd;
            border-radius: 5px;
            font-size: 13px;
        }}
        .finder-range-value {{
            text-align: center;
            font-weight: bold;
            color: #27ae60;
            font-size: 15px;
            margin-top: 3px;
        }}
        .finder-checks {{
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
        }}
        .finder-check {{
            display: flex;
            align-items: center;
            gap: 4px;
            font-size: 12px;
            background: #f8f9fa;
            padding: 4px 8px;
            border-radius: 12px;
            border: 1px solid #ddd;
        }}
        .finder-check input {{ margin: 0; }}
        .finder-btn {{
            background: linear-gradient(135deg, #27ae60 0%, #2ecc71 100%);
            color: white;
            border: none;
            padding: 12px;
            border-radius: 8px;
            cursor: pointer;
            font-size: 14px;
            font-weight: bold;
            width: 100%;
            margin-top: 5px;
        }}
        .finder-btn:hover {{ opacity: 0.9; }}
        .finder-reset {{
            background: #f8f9fa;
            color: #666;
            border: 1px solid #ddd;
            padding: 8px;
            border-radius: 8px;
            cursor: pointer;
            font-size: 12px;
            width: 100%;
            margin-top: 8px;
        }}
        .finder-reset:hover {{ background: #eee; }}
        .finder-results {{
            padding: 0 15px 15px;
        }}
        .finder-results-header {{
            font-weight: bold;
            font-size: 14px;
            color: #333;
            padding: 10px 0;
            border-bottom: 2px solid #27ae60;
            margin-bottom: 5px;
        }}
        .finder-result-item {{
            display: flex;
            align-items: center;
            padding: 10px 5px;
            border-bottom: 1px solid #f0f0f0;
            cursor: pointer;
            transition: background 0.2s;
        }}
        .finder-result-item:hover {{ background: #f0fff4; }}
        .finder-result-rank {{
            font-weight: bold;
            color: #27ae60;
            width: 30px;
            font-size: 14px;
        }}
        .finder-result-info {{ flex: 1; }}
        .finder-result-info .fr-zip {{ font-weight: bold; color: #333; font-size: 13px; }}
        .finder-result-info .fr-name {{ font-size: 11px; color: #888; }}
        .finder-result-info .fr-city {{ font-size: 10px; color: #27ae60; }}
        .finder-result-value {{
            text-align: right;
            font-size: 12px;
            line-height: 1.4;
        }}
        .finder-result-value .fr-price {{ font-weight: bold; color: #1e3c72; }}
        .finder-result-value .fr-services {{ font-size: 10px; color: #888; }}

        /* Mobiili-alapaneeli popupin sijaan */
        #mobile-info-panel {{
            display: none;
            position: fixed;
            bottom: 0;
            left: 0;
            right: 0;
            z-index: 1500;
            background: white;
            border-radius: 16px 16px 0 0;
            box-shadow: 0 -4px 20px rgba(0,0,0,0.25);
            max-height: 55vh;
            overflow-y: auto;
            padding: 0 16px 16px 16px;
            transition: transform 0.3s ease-out;
            transform: translateY(100%);
            -webkit-overflow-scrolling: touch;
        }}
        #mobile-info-panel.visible {{
            display: block;
            transform: translateY(0);
        }}
        #mobile-info-panel .mobile-panel-handle {{
            display: flex;
            justify-content: center;
            padding: 10px 0 6px 0;
            cursor: grab;
            position: sticky;
            top: 0;
            background: white;
            z-index: 1;
        }}
        #mobile-info-panel .mobile-panel-handle::after {{
            content: '';
            width: 40px;
            height: 4px;
            background: #ccc;
            border-radius: 2px;
        }}
        #mobile-info-panel .mobile-panel-close {{
            position: sticky;
            top: 0;
            float: right;
            font-size: 28px;
            cursor: pointer;
            color: #666;
            z-index: 2;
            background: white;
            border: none;
            padding: 0 5px;
            line-height: 1;
            margin-top: -30px;
        }}
        #mobile-info-panel .popup-content {{
            min-width: unset;
        }}
        @media (max-width: 768px) {{
            .leaflet-popup {{ display: none !important; }}
        }}
        @media (min-width: 769px) {{
            #mobile-info-panel {{ display: none !important; }}
        }}
    </style>
</head>
<body>
    <div id="header">
        <h1>🏠 Asuntojen hintakartta</h1>
        <p class="forecast-note">* Ennuste, laskettu viimeisen 5 vuoden trendin perusteella</p>
        <button id="mobile-menu-toggle" onclick="toggleMobileMenu()">☰</button>
    </div>
    
    <div id="controls">
        <div class="control-group">
            <label for="building-type-select">Huoneistotyyppi:</label>
            <select id="building-type-select" onchange="updateMap()">
                <option value="0" selected>Kaikki</option>
                <option value="1">Kerrostalo yksiöt</option>
                <option value="2">Kerrostalo kaksiot</option>
                <option value="3">Kerrostalo kolmiot+</option>
                <option value="5">Rivitalot</option>
            </select>
        </div>
        
        <div class="control-group">
            <label for="metric-select">Mittari:</label>
            <select id="metric-select" onchange="updateMap()">
                <option value="keskihinta_aritm_nw" selected>Neliöhinta (€/m²)</option>
                <option value="lkm_julk20">Kauppojen lukumäärä</option>
                <option value="vuokratuotto">Vuokratuotto (%)</option>
                <option value="hinta_tulot">Hinta/tulot -suhde</option>
            </select>
        </div>
        
        <div class="control-group" id="forecast-model-selector" style="display:none;">
            <label for="forecast-model-select">Ennustemalli (2026*):</label>
            <select id="forecast-model-select" onchange="updateMap()">
                <option value="linear" selected>Lineaarinen</option>
                <option value="arima">ARIMA</option>
                <option value="exponential">Exp. Smoothing</option>
                <option value="sarimax_euribor">SARIMAX-Euribor</option>
            </select>
        </div>
        
        <div class="control-group">
            <label for="view-mode-select">Näkymä:</label>
            <select id="view-mode-select" onchange="updateMap()">
                <option value="absolute" selected>Absoluuttinen</option>
                <option value="change">Muutos-%</option>
                <option value="analysis">Analyysi (5v trendi)</option>
                <option value="animation">Animaatio: Kartta</option>
                <option value="animation-chart">Animaatio: Diagrammi</option>
            </select>
        </div>
        
        <div class="control-group" id="year-selector-single">
            <label for="year-select">Vuosi:</label>
            <select id="year-select" onchange="updateMap()">
                {chr(10).join(f'                <option value="{year}" {"selected" if year == latest_year else ""}>{year}{"*" if year == "2026" else ""}</option>' for year in available_years)}
            </select>
        </div>
        
        <div class="control-group" id="year-selector-range" style="display:none;">
            <label for="year-from">Alku:</label>
            <select id="year-from" onchange="updateMap()">
                {chr(10).join(f'                <option value="{year}">{year}{"*" if year == "2026" else ""}</option>' for year in available_years)}
            </select>
            
            <label for="year-to">Loppu:</label>
            <select id="year-to" onchange="updateMap()">
                {chr(10).join(f'                <option value="{year}" {"selected" if year == latest_year else ""}>{year}{"*" if year == "2026" else ""}</option>' for year in available_years)}
            </select>
        </div>
        
        <div class="control-group" id="animation-controls" style="display:none;">
            <button id="play-button" onclick="toggleAnimation()">▶️ Toista</button>
            <label for="animation-speed">Nopeus:</label>
            <select id="animation-speed">
                <option value="2000">Hidas</option>
                <option value="1000" selected>Normaali</option>
                <option value="500">Nopea</option>
            </select>
            <span id="animation-year" style="font-weight: bold; margin-left: 10px;"></span>
        </div>
        
        <div class="control-group" id="animation-chart-controls" style="display:none;">
            <label for="chart-city-select">Alue:</label>
            <select id="chart-city-select" onchange="updateChartDisplay()">
                <option value="all" selected>Koko maa</option>
                <option value="helsinki">Helsinki</option>
                <option value="espoo">Espoo</option>
                <option value="vantaa">Vantaa</option>
                <option value="tampere">Tampere</option>
                <option value="turku">Turku</option>
                <option value="oulu">Oulu</option>
                <option value="kuopio">Kuopio</option>
            </select>
            
            <button id="chart-play-button" onclick="toggleChartAnimation()">▶️ Toista</button>
            <label for="chart-animation-speed">Nopeus:</label>
            <select id="chart-animation-speed">
                <option value="2000">Hidas</option>
                <option value="1000" selected>Normaali</option>
                <option value="500">Nopea</option>
            </select>
            <span id="chart-animation-year" style="font-weight: bold; margin-left: 10px;"></span>
        </div>
    </div>
    
    <div id="stats">
        <div class="stat-box">
            <div class="label">Postinumeroalueita</div>
            <div class="value">{len(geojson_data['features'])}</div>
        </div>
        <div class="stat-box">
            <div class="label" id="stat-label">Keskihinta {latest_year}</div>
            <div class="value" id="stat-value">{avg_price:,} €/m²</div>
        </div>
        <div class="stat-box">
            <div class="label" id="stat-max-label">Kallein</div>
            <div class="value" style="color: #e74c3c;" id="stat-max">{max_price:,} €/m²</div>
        </div>
        <div class="stat-box">
            <div class="label" id="stat-min-label">Halvin</div>
            <div class="value" style="color: #27ae60;" id="stat-min">{min_price:,} €/m²</div>
        </div>
    </div>
    
    <div class="city-buttons">
        <button onclick="map.setView([60.1699, 24.9384], 12)">Helsinki</button>
        <button onclick="map.setView([60.2052, 24.6566], 12)">Espoo</button>
        <button onclick="map.setView([60.2944, 24.9722], 12)">Vantaa</button>
        <button onclick="map.setView([61.4978, 23.7608], 12)">Tampere</button>
        <button onclick="map.setView([60.4518, 22.2706], 12)">Turku</button>
        <button onclick="map.setView([65.0121, 25.4651], 12)">Oulu</button>
        <button onclick="map.setView([62.8924, 27.6782], 12)">Kuopio</button>
    </div>
    
    <div id="search-box">
        <input type="text" id="search" placeholder="Hae postinumeroa..." onkeyup="filterMap()">
    </div>
    
    <button id="top10-toggle" onclick="toggleTop10Panel()">🏆 Top 10</button>
    <button id="finder-toggle" onclick="toggleFinderPanel()">🔍 Paras alue</button>
    <div id="map"></div>

    <!-- Mobiili-infopaneeli (popup-korvike) -->
    <div id="mobile-info-panel">
        <div class="mobile-panel-handle"></div>
        <button class="mobile-panel-close" onclick="closeMobilePanel()">&times;</button>
        <div id="mobile-info-content"></div>
    </div>
    
    <!-- Paras alue -hakupaneeli -->
    <div id="finder-panel">
        <div class="finder-header">
            <h2>🔍 Paras alue minulle</h2>
            <button class="finder-close" onclick="closeFinderPanel()">&times;</button>
        </div>
        <div class="finder-form">
            <div class="finder-group">
                <label>📍 Kunta</label>
                <select id="finder-kunta">
                    <option value="all">Kaikki kunnat</option>
                    {kunnat_options}
                </select>
            </div>
            <div class="finder-group">
                <label>🏠 Huoneistotyyppi</label>
                <select id="finder-building-type">
                    <option value="0" selected>Kaikki</option>
                    <option value="1">Kerrostalo yksiöt</option>
                    <option value="2">Kerrostalo kaksiot</option>
                    <option value="3">Kerrostalo kolmiot+</option>
                    <option value="5">Rivitalot</option>
                </select>
            </div>
            <div class="finder-group">
                <label>💰 Max neliöhinta</label>
                <input type="range" id="finder-max-price" min="500" max="10000" step="100" value="4000" oninput="document.getElementById('finder-price-val').textContent=this.value+' €/m²'">
                <div class="finder-range-value" id="finder-price-val">4000 €/m²</div>
            </div>
            <div class="finder-group">
                <label>👥 Min väkiluku alueella</label>
                <input type="range" id="finder-min-pop" min="0" max="10000" step="100" value="0" oninput="document.getElementById('finder-pop-val').textContent=this.value === '0' ? 'Ei rajoitusta' : this.value+' asukasta'">
                <div class="finder-range-value" id="finder-pop-val">Ei rajoitusta</div>
            </div>
            <div class="finder-group">
                <label>🏪 Vaaditut palvelut</label>
                <div class="finder-checks">
                    <label class="finder-check"><input type="checkbox" id="finder-kaupat"> 🛒 Ruokakaupat</label>
                    <label class="finder-check"><input type="checkbox" id="finder-koulut"> 🏫 Koulut</label>
                    <label class="finder-check"><input type="checkbox" id="finder-paivakodit"> 🧒 Päiväkodit</label>
                    <label class="finder-check"><input type="checkbox" id="finder-liikunta"> 💪 Liikunta</label>
                    <label class="finder-check"><input type="checkbox" id="finder-terveys"> 🏥 Terveys</label>
                    <label class="finder-check"><input type="checkbox" id="finder-liikenne"> 🚌 Julk.liikenne</label>
                    <label class="finder-check"><input type="checkbox" id="finder-kirjastot"> 📚 Kirjastot</label>
                    <label class="finder-check"><input type="checkbox" id="finder-apteekit"> 💊 Apteekit</label>
                </div>
            </div>
            <div class="finder-group">
                <label>⭐ Min palveluindeksi</label>
                <input type="range" id="finder-min-palvelu" min="0" max="20" step="0.5" value="0" oninput="document.getElementById('finder-palvelu-val').textContent=this.value === '0' ? 'Ei rajoitusta' : this.value">
                <div class="finder-range-value" id="finder-palvelu-val">Ei rajoitusta</div>
            </div>
            <div class="finder-group">
                <label>🚌 Max matka-aika keskustaan</label>
                <input type="range" id="finder-max-matka" min="0" max="120" step="5" value="0" oninput="document.getElementById('finder-matka-val').textContent=this.value === '0' ? 'Ei rajoitusta' : this.value+' min'">
                <div class="finder-range-value" id="finder-matka-val">Ei rajoitusta</div>
            </div>
            <button class="finder-btn" onclick="runFinderSearch()">🔍 Etsi sopivat alueet</button>
            <button class="finder-reset" onclick="resetFinderSearch()">↩ Nollaa suodattimet</button>
        </div>
        <div class="finder-results" id="finder-results"></div>
    </div>
    
    <!-- Top 10 -paneeli -->
    <div id="top10-panel">
        <div class="top10-header">
            <h2>🏆 Top 10 -listat</h2>
            <button class="top10-close" onclick="closeTop10Panel()">&times;</button>
        </div>
        <div class="top10-tabs">
            <div class="top10-tab active" data-list="kalleimmat" onclick="switchTop10Tab(this)">💎 Kalleimmat</div>
            <div class="top10-tab" data-list="halvimmat" onclick="switchTop10Tab(this)">💚 Halvimmat</div>
            <div class="top10-tab" data-list="nousseet" onclick="switchTop10Tab(this)">📈 Eniten nousseet</div>
            <div class="top10-tab" data-list="laskeneet" onclick="switchTop10Tab(this)">📉 Eniten laskeneet</div>
            <div class="top10-tab" data-list="tuotto" onclick="switchTop10Tab(this)">💰 Paras tuotto</div>
            <div class="top10-tab" data-list="palvelut" onclick="switchTop10Tab(this)">🏪 Parhaat palvelut</div>
        </div>
        <div class="top10-list" id="top10-list"></div>
    </div>
    <div id="chart-container" style="display:none; position: absolute; top: 270px; left: 0; right: 0; bottom: 0; background: white; padding: 20px; overflow-y: auto; z-index: 1000;">
        <canvas id="bar-chart"></canvas>
    </div>
    
    <!-- Aikasarjakaavio-modal -->
    <div id="timeseries-modal" onclick="if(event.target===this)closeTimeSeriesModal()">
        <div id="timeseries-panel">
            <button class="ts-close-btn" onclick="closeTimeSeriesModal()">&times;</button>
            <h2 id="ts-title"></h2>
            <div class="ts-area-name" id="ts-area-name"></div>
            <div class="ts-chart-section">
                <h3>🏠 Hintakehitys (€/m²)</h3>
                <canvas id="ts-price-chart"></canvas>
            </div>
            <div class="ts-chart-section">
                <h3>📊 Kauppojen lukumäärä</h3>
                <canvas id="ts-transactions-chart"></canvas>
            </div>
            <div class="ts-chart-section" id="ts-rent-section" style="display:none;">
                <h3>🔑 Vuokrakehitys (€/m²/kk)</h3>
                <canvas id="ts-rent-chart"></canvas>
            </div>
            <div class="ts-chart-section" id="ts-yield-section" style="display:none;">
                <h3>💰 Vuokratuottokehitys (%)</h3>
                <canvas id="ts-yield-chart"></canvas>
            </div>
            <div class="ts-chart-section" id="ts-population-section" style="display:none;">
                <h3>👥 Väestö &amp; keski-ikä</h3>
                <canvas id="ts-population-chart"></canvas>
            </div>
            <div class="ts-chart-section" id="ts-income-section" style="display:none;">
                <h3>💶 Tulotaso &amp; työttömyys</h3>
                <canvas id="ts-income-chart"></canvas>
            </div>
            <div class="ts-chart-section" id="ts-age-section" style="display:none;">
                <h3>👶 Ikärakenne (%)</h3>
                <canvas id="ts-age-chart"></canvas>
            </div>
            <div class="ts-chart-section" id="ts-housing-section" style="display:none;">
                <h3>🏗️ Asuntorakenne &amp; hallinta</h3>
                <canvas id="ts-housing-chart"></canvas>
            </div>
            <div class="ts-chart-section" id="ts-euribor-section" style="display:none;">
                <h3>📈 Hinta vs. Euribor</h3>
                <canvas id="ts-euribor-chart"></canvas>
            </div>
        </div>
    </div>
    
    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
    <script>
        var map = L.map('map').setView([60.1699, 24.9384], 8);
        
        L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png', {{
            attribution: '© OpenStreetMap contributors'
        }}).addTo(map);

        // Mobiilitunnistus
        var isMobileDevice = window.matchMedia('(max-width: 768px)').matches;
        window.matchMedia('(max-width: 768px)').addEventListener('change', function(e) {{
            isMobileDevice = e.matches;
            if (!isMobileDevice) closeMobilePanel();
        }});

        // Mobiili-infopaneelin hallinta
        function openMobilePanel(content) {{
            var panel = document.getElementById('mobile-info-panel');
            var contentEl = document.getElementById('mobile-info-content');
            contentEl.innerHTML = content;
            panel.style.display = 'block';
            panel.offsetHeight;
            panel.classList.add('visible');
        }}

        function closeMobilePanel() {{
            var panel = document.getElementById('mobile-info-panel');
            panel.classList.remove('visible');
            setTimeout(function() {{
                if (!panel.classList.contains('visible')) {{
                    panel.style.display = 'none';
                }}
            }}, 300);
        }}

        // Swipe-alas sulkee mobiilipaneelin
        (function() {{
            var panel = document.getElementById('mobile-info-panel');
            var startY = 0, currentY = 0, isDragging = false;

            panel.addEventListener('touchstart', function(e) {{
                if (panel.scrollTop <= 0) {{
                    startY = e.touches[0].clientY;
                    isDragging = true;
                }}
            }}, {{ passive: true }});

            panel.addEventListener('touchmove', function(e) {{
                if (!isDragging) return;
                currentY = e.touches[0].clientY;
                var diff = currentY - startY;
                if (diff > 0) {{
                    panel.style.transform = 'translateY(' + diff + 'px)';
                    panel.style.transition = 'none';
                }}
            }}, {{ passive: true }});

            panel.addEventListener('touchend', function() {{
                if (!isDragging) return;
                isDragging = false;
                panel.style.transition = 'transform 0.3s ease-out';
                var diff = currentY - startY;
                if (diff > 80) {{
                    closeMobilePanel();
                }} else {{
                    panel.style.transform = 'translateY(0)';
                }}
                startY = 0;
                currentY = 0;
            }});
        }})();

        // Sulje mobiilipaneeli kun karttaa klikataan tai liikutetaan
        map.on('click', function(e) {{
            if (isMobileDevice && !e.originalEvent._fromLayer) {{
                closeMobilePanel();
            }}
        }});
        map.on('movestart', function() {{
            if (isMobileDevice) closeMobilePanel();
        }});

        // Bind popup: mobiilissa käyttää alapaneelia, desktopilla normaali popup
        function bindMobilePopup(layer, popupContent, feature) {{
            if (!isMobileDevice) {{
                layer.bindPopup(popupContent, {{ maxWidth: 300 }});
            }}
            layer.on('click', function(e) {{
                selectedFeature = feature;
                if (isMobileDevice) {{
                    if (e.originalEvent) e.originalEvent._fromLayer = true;
                    openMobilePanel(popupContent);
                }}
            }});
        }}

        // Sulje mobiilivalikko kun karttaa klikataan
        map.on('click', function() {{
            var controls = document.getElementById('controls');
            var button = document.getElementById('mobile-menu-toggle');
            if (controls.classList.contains('mobile-menu-open')) {{
                controls.classList.remove('mobile-menu-open');
                button.innerHTML = '☰';
            }}
        }});
        
        // GeoJSON data
        var geojsonData = {geojson_json};
        var availableYears = {years_json};
        var buildingTypes = {building_types_json};
        var ennusteetMallit = {ennusteet_mallit_json};  // Ennustemallit (linear, arima, exponential, sarimax_euribor)
        var euriborData = {euribor_json};  // Euribor-aikasarja vuosittain
        var geoJsonLayer;
        var currentLegend;
        
        // Aikasarjakaaviot
        var selectedFeature = null;
        var tsCharts = {{}};
        
        function destroyTsCharts() {{
            Object.keys(tsCharts).forEach(function(k) {{ if (tsCharts[k]) tsCharts[k].destroy(); }});
            tsCharts = {{}};
        }}
        
        function openTimeSeriesModal() {{
            if (!selectedFeature) return;
            var feature = selectedFeature;
            var props = feature.properties;
            
            document.getElementById('ts-title').textContent = props.postinumer;
            document.getElementById('ts-area-name').textContent = props.name;
            
            destroyTsCharts();
            
            var btColors = {{'0': '#1e3c72', '1': '#e74c3c', '2': '#f39c12', '3': '#27ae60', '5': '#9b59b6'}};
            var btNames = buildingTypes;
            
            // 1. Hintakehitys
            var priceDatasets = [];
            ['0', '1', '2', '3', '5'].forEach(function(bt) {{
                var prices = [];
                availableYears.forEach(function(y) {{
                    prices.push(getValue(feature, y, bt, 'keskihinta_aritm_nw') || null);
                }});
                if (prices.some(function(v) {{ return v !== null; }})) {{
                    priceDatasets.push({{
                        label: btNames[bt],
                        data: prices,
                        borderColor: btColors[bt],
                        backgroundColor: btColors[bt] + '20',
                        tension: 0.3,
                        spanGaps: true,
                        pointRadius: 3
                    }});
                }}
            }});
            
            var priceLabels = availableYears.map(function(y) {{ return y == 2026 ? y + '*' : y; }});
            
            tsCharts.price = new Chart(document.getElementById('ts-price-chart'), {{
                type: 'line',
                data: {{ labels: priceLabels, datasets: priceDatasets }},
                options: {{
                    responsive: true,
                    interaction: {{ mode: 'index', intersect: false }},
                    plugins: {{ legend: {{ position: 'bottom', labels: {{ boxWidth: 12, font: {{ size: 11 }} }} }} }},
                    scales: {{ y: {{ beginAtZero: false, title: {{ display: true, text: '€/m²' }} }} }}
                }}
            }});
            
            // 2. Kauppojen lukumäärä
            var txDatasets = [];
            ['0', '1', '2', '3', '5'].forEach(function(bt) {{
                var counts = [];
                availableYears.forEach(function(y) {{
                    counts.push(getValue(feature, y, bt, 'lkm_julk20') || null);
                }});
                if (counts.some(function(v) {{ return v !== null; }})) {{
                    txDatasets.push({{
                        label: btNames[bt],
                        data: counts,
                        borderColor: btColors[bt],
                        backgroundColor: btColors[bt] + '40',
                        tension: 0.3,
                        spanGaps: true,
                        pointRadius: 3
                    }});
                }}
            }});
            
            tsCharts.transactions = new Chart(document.getElementById('ts-transactions-chart'), {{
                type: 'line',
                data: {{ labels: priceLabels, datasets: txDatasets }},
                options: {{
                    responsive: true,
                    interaction: {{ mode: 'index', intersect: false }},
                    plugins: {{ legend: {{ position: 'bottom', labels: {{ boxWidth: 12, font: {{ size: 11 }} }} }} }},
                    scales: {{ y: {{ beginAtZero: true, title: {{ display: true, text: 'kpl' }} }} }}
                }}
            }});
            
            // 3. Vuokrakehitys
            var rentSection = document.getElementById('ts-rent-section');
            var vuokra = props.vuokra;
            if (vuokra && Object.keys(vuokra).length > 0) {{
                rentSection.style.display = 'block';
                var rentDatasets = [];
                var rentYears = Object.keys(vuokra).sort();
                
                ['0', '1', '2', '3'].forEach(function(bt) {{
                    var rents = [];
                    rentYears.forEach(function(y) {{
                        var rd = vuokra[y] && vuokra[y][bt];
                        rents.push(rd ? rd.keskivuokra : null);
                    }});
                    if (rents.some(function(v) {{ return v !== null; }})) {{
                        rentDatasets.push({{
                            label: btNames[bt] || bt,
                            data: rents,
                            borderColor: btColors[bt],
                            backgroundColor: btColors[bt] + '20',
                            tension: 0.3,
                            spanGaps: true,
                            pointRadius: 3
                        }});
                    }}
                }});
                
                tsCharts.rent = new Chart(document.getElementById('ts-rent-chart'), {{
                    type: 'line',
                    data: {{ labels: rentYears, datasets: rentDatasets }},
                    options: {{
                        responsive: true,
                        interaction: {{ mode: 'index', intersect: false }},
                        plugins: {{ legend: {{ position: 'bottom', labels: {{ boxWidth: 12, font: {{ size: 11 }} }} }} }},
                        scales: {{ y: {{ beginAtZero: false, title: {{ display: true, text: '€/m²/kk' }} }} }}
                    }}
                }});
            }} else {{
                rentSection.style.display = 'none';
            }}
            
            // 4. Vuokratuotto
            var yieldSection = document.getElementById('ts-yield-section');
            if (vuokra && Object.keys(vuokra).length > 0) {{
                var yieldDatasets = [];
                var yieldYears = Object.keys(vuokra).sort();
                
                ['0', '1', '2', '3'].forEach(function(bt) {{
                    var yields = [];
                    yieldYears.forEach(function(y) {{
                        var yv = getVuokratuotto(feature, y, bt);
                        yields.push(yv || null);
                    }});
                    if (yields.some(function(v) {{ return v !== null; }})) {{
                        yieldDatasets.push({{
                            label: btNames[bt] || bt,
                            data: yields,
                            borderColor: btColors[bt],
                            backgroundColor: btColors[bt] + '20',
                            tension: 0.3,
                            spanGaps: true,
                            pointRadius: 3
                        }});
                    }}
                }});
                
                if (yieldDatasets.length > 0) {{
                    yieldSection.style.display = 'block';
                    tsCharts.yieldChart = new Chart(document.getElementById('ts-yield-chart'), {{
                        type: 'line',
                        data: {{ labels: yieldYears, datasets: yieldDatasets }},
                        options: {{
                            responsive: true,
                            interaction: {{ mode: 'index', intersect: false }},
                            plugins: {{ legend: {{ position: 'bottom', labels: {{ boxWidth: 12, font: {{ size: 11 }} }} }} }},
                            scales: {{ y: {{ beginAtZero: false, title: {{ display: true, text: '%' }} }} }}
                        }}
                    }});
                }} else {{
                    yieldSection.style.display = 'none';
                }}
            }} else {{
                yieldSection.style.display = 'none';
            }}
            
            // 5. Väestö & keski-ikä
            var popSection = document.getElementById('ts-population-section');
            var paavo = props.paavo_aikasarja;
            if (paavo && Object.keys(paavo).length > 0) {{
                popSection.style.display = 'block';
                var paavoYears = Object.keys(paavo).sort();
                var displayYears = paavoYears.map(function(y) {{ return parseInt(y) - 1; }});
                
                tsCharts.population = new Chart(document.getElementById('ts-population-chart'), {{
                    type: 'line',
                    data: {{
                        labels: displayYears,
                        datasets: [{{
                            label: 'Asukkaat',
                            data: paavoYears.map(function(y) {{ return paavo[y].vaesto || null; }}),
                            borderColor: '#3498db',
                            backgroundColor: '#3498db20',
                            tension: 0.3,
                            pointRadius: 3,
                            yAxisID: 'y'
                        }}, {{
                            label: 'Keski-ikä (v)',
                            data: paavoYears.map(function(y) {{ return paavo[y].keski_ika || null; }}),
                            borderColor: '#e67e22',
                            backgroundColor: '#e67e2220',
                            tension: 0.3,
                            pointRadius: 3,
                            yAxisID: 'y1'
                        }}]
                    }},
                    options: {{
                        responsive: true,
                        interaction: {{ mode: 'index', intersect: false }},
                        plugins: {{ legend: {{ position: 'bottom', labels: {{ boxWidth: 12, font: {{ size: 11 }} }} }} }},
                        scales: {{
                            y: {{ position: 'left', title: {{ display: true, text: 'Asukkaat' }} }},
                            y1: {{ position: 'right', title: {{ display: true, text: 'Keski-ikä (v)' }}, grid: {{ drawOnChartArea: false }} }}
                        }}
                    }}
                }});
            }} else {{
                popSection.style.display = 'none';
            }}
            
            // 6. Tulotaso & työttömyys
            var incSection = document.getElementById('ts-income-section');
            if (paavo && Object.keys(paavo).length > 0) {{
                incSection.style.display = 'block';
                var paavoYears2 = Object.keys(paavo).sort();
                var displayYears2 = paavoYears2.map(function(y) {{ return parseInt(y) - 1; }});
                
                tsCharts.income = new Chart(document.getElementById('ts-income-chart'), {{
                    type: 'line',
                    data: {{
                        labels: displayYears2,
                        datasets: [{{
                            label: 'Keskitulo (€/v)',
                            data: paavoYears2.map(function(y) {{ return paavo[y].keskitulo || null; }}),
                            borderColor: '#27ae60',
                            backgroundColor: '#27ae6020',
                            tension: 0.3,
                            pointRadius: 3,
                            yAxisID: 'y'
                        }}, {{
                            label: 'Työttömyys (%)',
                            data: paavoYears2.map(function(y) {{ return paavo[y].tyottomyysaste || null; }}),
                            borderColor: '#e74c3c',
                            backgroundColor: '#e74c3c20',
                            tension: 0.3,
                            pointRadius: 3,
                            yAxisID: 'y1'
                        }}]
                    }},
                    options: {{
                        responsive: true,
                        interaction: {{ mode: 'index', intersect: false }},
                        plugins: {{ legend: {{ position: 'bottom', labels: {{ boxWidth: 12, font: {{ size: 11 }} }} }} }},
                        scales: {{
                            y: {{ position: 'left', title: {{ display: true, text: '€/vuosi' }} }},
                            y1: {{ position: 'right', title: {{ display: true, text: '%' }}, grid: {{ drawOnChartArea: false }} }}
                        }}
                    }}
                }});
            }} else {{
                incSection.style.display = 'none';
            }}
            
            // 7. Ikärakenne (lapset, työikäiset, eläkeikäiset %)
            var ageSection = document.getElementById('ts-age-section');
            if (paavo && Object.keys(paavo).length > 0) {{
                var hasAge = Object.values(paavo).some(function(v) {{ return v.lapset_osuus !== undefined; }});
                if (hasAge) {{
                    ageSection.style.display = 'block';
                    var ageYears = Object.keys(paavo).sort();
                    var ageDisplayYears = ageYears.map(function(y) {{ return parseInt(y) - 1; }});
                    
                    tsCharts.age = new Chart(document.getElementById('ts-age-chart'), {{
                        type: 'line',
                        data: {{
                            labels: ageDisplayYears,
                            datasets: [{{
                                label: 'Lapset 0-17 (%)',
                                data: ageYears.map(function(y) {{ return paavo[y].lapset_osuus || null; }}),
                                borderColor: '#3498db',
                                backgroundColor: '#3498db20',
                                tension: 0.3,
                                pointRadius: 3
                            }}, {{
                                label: 'Työikäiset 18-64 (%)',
                                data: ageYears.map(function(y) {{ return paavo[y].tyoikaiset_osuus || null; }}),
                                borderColor: '#27ae60',
                                backgroundColor: '#27ae6020',
                                tension: 0.3,
                                pointRadius: 3
                            }}, {{
                                label: 'Eläkeikäiset 65+ (%)',
                                data: ageYears.map(function(y) {{ return paavo[y].elakeikaiset_osuus || null; }}),
                                borderColor: '#e67e22',
                                backgroundColor: '#e67e2220',
                                tension: 0.3,
                                pointRadius: 3
                            }}]
                        }},
                        options: {{
                            responsive: true,
                            interaction: {{ mode: 'index', intersect: false }},
                            plugins: {{ legend: {{ position: 'bottom', labels: {{ boxWidth: 12, font: {{ size: 11 }} }} }} }},
                            scales: {{ y: {{ title: {{ display: true, text: '%' }}, min: 0, max: 100 }} }}
                        }}
                    }});
                }} else {{
                    ageSection.style.display = 'none';
                }}
            }} else {{
                ageSection.style.display = 'none';
            }}
            
            // 8. Asuntorakenne & hallinta
            var housingSection = document.getElementById('ts-housing-section');
            if (paavo && Object.keys(paavo).length > 0) {{
                var hasHousing = Object.values(paavo).some(function(v) {{ return v.omistusaste !== undefined; }});
                if (hasHousing) {{
                    housingSection.style.display = 'block';
                    var hYears = Object.keys(paavo).sort();
                    var hDisplayYears = hYears.map(function(y) {{ return parseInt(y) - 1; }});
                    
                    tsCharts.housing = new Chart(document.getElementById('ts-housing-chart'), {{
                        type: 'line',
                        data: {{
                            labels: hDisplayYears,
                            datasets: [{{
                                label: 'Omistusaste (%)',
                                data: hYears.map(function(y) {{ return paavo[y].omistusaste || null; }}),
                                borderColor: '#27ae60',
                                backgroundColor: '#27ae6020',
                                tension: 0.3,
                                pointRadius: 3,
                                yAxisID: 'y'
                            }}, {{
                                label: 'Vuokra-aste (%)',
                                data: hYears.map(function(y) {{ return paavo[y].vuokra_aste || null; }}),
                                borderColor: '#e74c3c',
                                backgroundColor: '#e74c3c20',
                                tension: 0.3,
                                pointRadius: 3,
                                yAxisID: 'y'
                            }}, {{
                                label: 'Kerrostalo (%)',
                                data: hYears.map(function(y) {{ return paavo[y].kerrostalo_osuus || null; }}),
                                borderColor: '#9b59b6',
                                backgroundColor: '#9b59b620',
                                tension: 0.3,
                                pointRadius: 3,
                                borderDash: [5, 5],
                                yAxisID: 'y'
                            }}]
                        }},
                        options: {{
                            responsive: true,
                            interaction: {{ mode: 'index', intersect: false }},
                            plugins: {{ legend: {{ position: 'bottom', labels: {{ boxWidth: 12, font: {{ size: 11 }} }} }} }},
                            scales: {{ y: {{ title: {{ display: true, text: '%' }}, min: 0 }} }}
                        }}
                    }});
                }} else {{
                    housingSection.style.display = 'none';
                }}
            }} else {{
                housingSection.style.display = 'none';
            }}
            
            // 9. Hinta vs. Euribor
            var euriborSection = document.getElementById('ts-euribor-section');
            if (euriborData && Object.keys(euriborData).length > 0) {{
                euriborSection.style.display = 'block';
                var priceByYear = {{}};
                var bt0 = '0';  // Kaikki talotyypit
                availableYears.forEach(function(y) {{
                    var v = getValue(feature, y, bt0, 'keskihinta_aritm_nw');
                    if (v) priceByYear[y] = v;
                }});
                
                // Yhdistä vuodet joille on sekä hinta että Euribor
                var commonYears = Object.keys(priceByYear).filter(function(y) {{ return euriborData[y]; }}).sort();
                
                if (commonYears.length > 3) {{
                    tsCharts.euribor = new Chart(document.getElementById('ts-euribor-chart'), {{
                        type: 'line',
                        data: {{
                            labels: commonYears,
                            datasets: [{{
                                label: 'Neliöhinta (€/m²)',
                                data: commonYears.map(function(y) {{ return priceByYear[y] || null; }}),
                                borderColor: '#1e3c72',
                                backgroundColor: '#1e3c7220',
                                tension: 0.3,
                                pointRadius: 3,
                                yAxisID: 'y'
                            }}, {{
                                label: '12kk Euribor (%)',
                                data: commonYears.map(function(y) {{ return euriborData[y] ? euriborData[y].keskiarvo : null; }}),
                                borderColor: '#e74c3c',
                                backgroundColor: '#e74c3c20',
                                tension: 0.3,
                                pointRadius: 3,
                                yAxisID: 'y1'
                            }}]
                        }},
                        options: {{
                            responsive: true,
                            interaction: {{ mode: 'index', intersect: false }},
                            plugins: {{ legend: {{ position: 'bottom', labels: {{ boxWidth: 12, font: {{ size: 11 }} }} }} }},
                            scales: {{
                                y: {{ position: 'left', title: {{ display: true, text: '€/m²' }} }},
                                y1: {{ position: 'right', title: {{ display: true, text: 'Euribor %' }}, grid: {{ drawOnChartArea: false }} }}
                            }}
                        }}
                    }});
                }} else {{
                    euriborSection.style.display = 'none';
                }}
            }} else {{
                euriborSection.style.display = 'none';
            }}
            
            document.getElementById('timeseries-modal').style.display = 'block';
        }}
        
        function closeTimeSeriesModal() {{
            document.getElementById('timeseries-modal').style.display = 'none';
            destroyTsCharts();
        }}
        
        // Sulje modal Esc-näppäimellä
        document.addEventListener('keydown', function(e) {{
            if (e.key === 'Escape') closeTimeSeriesModal();
        }});
        
        // Animaatio-muuttujat
        var animationInterval = null;
        var animationCurrentYear = null;
        var isAnimationPlaying = false;
        
        // Diagrammi-animaatio-muuttujat
        var chartAnimationInterval = null;
        var chartAnimationCurrentYear = null;
        var isChartAnimationPlaying = false;
        
        // Kaupunkien postinumeroalueet
        var cityPostalCodes = {{
            'helsinki': ['00', '01'],  // 00xxx ja 01xxx (osa)
            'espoo': ['02'],  // 02xxx
            'vantaa': ['01'],  // 01xxx
            'tampere': ['33'],  // 33xxx
            'turku': ['20', '21'],  // 20xxx ja 21xxx
            'oulu': ['90'],  // 90xxx
            'kuopio': ['70']  // 70xxx
        }};
        
        // Värit hinnoille  
        function getColorPrice(price) {{
            if (price > 8000) return '#8B0000';
            else if (price > 6000) return '#e74c3c';
            else if (price > 5000) return '#f39c12';
            else if (price > 4000) return '#f1c40f';
            else if (price > 3000) return '#9acd32';
            else if (price > 2000) return '#27ae60';
            else return '#2ecc71';
        }}
        
        // Värit kauppojen lukumäärille
        function getColorTransactions(count) {{
            if (count > 100) return '#2ecc71';
            else if (count > 50) return '#27ae60';
            else if (count > 30) return '#9acd32';
            else if (count > 20) return '#f1c40f';
            else if (count > 10) return '#f39c12';
            else if (count > 5) return '#e74c3c';
            else return '#8B0000';
        }}
        
        // Värit muutosprosentille
        function getColorChange(change) {{
            if (change > 15) return '#2ecc71';
            else if (change > 10) return '#27ae60';
            else if (change > 5) return '#9acd32';
            else if (change > 0) return '#f1c40f';
            else if (change > -5) return '#f39c12';
            else if (change > -10) return '#e74c3c';
            else return '#8B0000';
        }}
        
        // Värit hinta/tulot -suhteelle - matala = vihreä (edullinen), korkea = punainen (kallis)
        function getColorRatio(ratio) {{
            if (ratio > 12) return '#8B0000';
            else if (ratio > 10) return '#e74c3c';
            else if (ratio > 8) return '#f39c12';
            else if (ratio > 6) return '#f1c40f';
            else if (ratio > 5) return '#9acd32';
            else if (ratio > 4) return '#27ae60';
            else return '#2ecc71';
        }}
        
        // Hae hinta/tulot -suhde (vuosien palkat per 60m² asunto)
        function getHintaTuloSuhde(feature, year, buildingType) {{
            var priceData = feature.properties.data;
            if (!priceData || !priceData[year] || !priceData[year][buildingType]) return null;
            var price = priceData[year][buildingType].keskihinta_aritm_nw;
            if (!price || price <= 0) return null;
            
            // Paavo-data on +1 vuosi (pno_tilasto_2025 = tiedot vuodelta 2024)
            var paavoYear = parseInt(year) + 1;
            var paavo = feature.properties.paavo_aikasarja;
            if (!paavo) return null;
            
            // Etsi paras Paavo-vuosi
            var tulot = null;
            if (paavo[paavoYear] && paavo[paavoYear].keskitulo) {{
                tulot = paavo[paavoYear].keskitulo;
            }} else {{
                // Fallback: lähin vanhempi vuosi
                var vuodet = Object.keys(paavo).map(Number).sort(function(a,b) {{ return b-a; }});
                for (var i = 0; i < vuodet.length; i++) {{
                    if (vuodet[i] <= paavoYear && paavo[vuodet[i]] && paavo[vuodet[i]].keskitulo) {{
                        tulot = paavo[vuodet[i]].keskitulo;
                        break;
                    }}
                }}
            }}
            if (!tulot || tulot <= 0) return null;
            
            return (price * 60) / tulot;
        }}
        
        // Värit vuokratuotolle (%) - korkea tuotto = vihreä
        function getColorYield(yieldPct) {{
            if (yieldPct > 8) return '#2ecc71';
            else if (yieldPct > 7) return '#27ae60';
            else if (yieldPct > 6) return '#9acd32';
            else if (yieldPct > 5) return '#f1c40f';
            else if (yieldPct > 4) return '#f39c12';
            else if (yieldPct > 3) return '#e74c3c';
            else return '#8B0000';
        }}
        
        // Hae vuokratuotto datasta
        function getVuokratuotto(feature, year, buildingType) {{
            var vuokra = feature.properties.vuokra;
            if (!vuokra || !vuokra[year]) return null;
            
            // Ei vuokradataa rivitaloille
            var bt = buildingType;
            if (bt === '5') return null;
            
            var rentData = vuokra[year][bt];
            if (!rentData || !rentData.keskivuokra) return null;
            
            var priceData = feature.properties.data;
            if (!priceData || !priceData[year] || !priceData[year][bt]) return null;
            
            var price = priceData[year][bt].keskihinta_aritm_nw;
            if (!price || price <= 0) return null;
            
            // Vuokratuotto: (kuukausivuokra × 12) / ostohinta × 100
            var monthlyRent = rentData.keskivuokra;
            var annualRent = monthlyRent * 12;
            return (annualRent / price) * 100;
        }}
        
        // Hae vuokra datasta
        function getVuokra(feature, year, buildingType) {{
            var vuokra = feature.properties.vuokra;
            if (!vuokra || !vuokra[year]) return null;
            var bt = buildingType;
            if (bt === '5') return null;
            var rentData = vuokra[year][bt];
            if (!rentData || !rentData.keskivuokra) return null;
            return rentData.keskivuokra;
        }}
        
        
        // Hae arvo datasta
        function getValue(feature, year, buildingType, metric) {{
            var data = feature.properties.data;
            
            // Jos vuosi on 2026, käytä valittua ennustemallia
            if (year === '2026' || year === 2026) {{
                var forecastModel = document.getElementById('forecast-model-select') ? 
                                   document.getElementById('forecast-model-select').value : 'linear';
                var postcode = feature.properties.postinumer;
                
                // Yritä hakea ennuste valitulla mallilla
                if (ennusteetMallit[postcode] && 
                    ennusteetMallit[postcode][buildingType] && 
                    ennusteetMallit[postcode][buildingType][forecastModel]) {{
                    return ennusteetMallit[postcode][buildingType][forecastModel][metric] || null;
                }}
                
                // Fallback: käytä perinteistä dataa jos ennustetta ei löydy
                if (!data || !data[year] || !data[year][buildingType]) return null;
                return data[year][buildingType][metric] || null;
            }}
            
            // Muille vuosille käytä tavallista dataa
            if (!data || !data[year] || !data[year][buildingType]) return null;
            return data[year][buildingType][metric] || null;
        }}
        
        // Rakennetaan laajennettu väestö+palvelu -popup-osio
        function buildExpandedPopup(props, selectedYear) {{
            var html = '';
            
            // Matka-aika
            if (props.matka_aika && props.matka_aika.matka_aika_min) {{
                var ma = props.matka_aika;
                var matkaColor = ma.matka_aika_min <= 20 ? '#27ae60' : ma.matka_aika_min <= 45 ? '#f39c12' : ma.matka_aika_min <= 90 ? '#e67e22' : '#e74c3c';
                var kulkutapa = ma.lahde === 'digitransit' ? 'julkinen liikenne' : 'laskennallinen arvio (auto)';
                html += '<div class="details" style="margin-top: 10px; border-top: 1px solid #ddd; padding-top: 5px;">' +
                    '<strong>🚌 Matka-aika keskustaan:</strong><br>' +
                    '🏙️ ' + ma.lahin_keskusta + ': <strong style="color:' + matkaColor + '">' + ma.matka_aika_min + ' min</strong> (' + ma.etaisyys_km + ' km)<br>' +
                    '<span style="font-size:11px;color:#888">' + kulkutapa + '</span></div>';
            }}
            
            // Paavo: laajennetut väestötiedot
            if (props.paavo_aikasarja) {{
                var targetPaavoVuosi = parseInt(selectedYear) + 1;
                var vuodet = Object.keys(props.paavo_aikasarja).map(Number).sort(function(a,b) {{ return b-a; }});
                var paavoVuosi = vuodet.find(function(v) {{ return v <= targetPaavoVuosi; }}) || vuodet[0];
                var paavo = paavoVuosi ? props.paavo_aikasarja[paavoVuosi] : null;
                
                if (paavo && paavo.vaesto) {{
                    var vuosiLabel = paavoVuosi - 1;
                    html += '<div class="details" style="margin-top: 10px; border-top: 1px solid #ddd; padding-top: 5px;">' +
                        '<strong>👥 Väestötiedot (' + vuosiLabel + '):</strong><br>' +
                        'Asukkaat: ' + paavo.vaesto.toLocaleString() + '<br>' +
                        'Keski-ikä: ' + paavo.keski_ika + ' v<br>' +
                        'Keskitulo: ' + paavo.keskitulo.toLocaleString() + ' €/v<br>' +
                        'Työttömyys: ' + paavo.tyottomyysaste.toFixed(1) + ' %<br>' +
                        'Väestötiheys: ' + paavo.vaestotiheys.toFixed(0) + ' as/km²</div>';
                    
                    // Ikärakenne
                    if (paavo.lapset_osuus !== undefined) {{
                        html += '<div class="details" style="margin-top: 5px; border-top: 1px solid #eee; padding-top: 3px;">' +
                            '<strong>👶 Ikärakenne:</strong><br>' +
                            '👶 Lapset (0-17): ' + paavo.lapset_osuus + ' %<br>' +
                            '💼 Työikäiset (18-64): ' + paavo.tyoikaiset_osuus + ' %<br>' +
                            '🧓 Eläkeikäiset (65+): ' + paavo.elakeikaiset_osuus + ' %</div>';
                    }}
                    
                    // Asuntorakenne & hallinta
                    if (paavo.omistusaste !== undefined) {{
                        html += '<div class="details" style="margin-top: 5px; border-top: 1px solid #eee; padding-top: 3px;">' +
                            '<strong>🏗️ Asuntorakenne:</strong><br>' +
                            '🏢 Kerrostalo: ' + (paavo.kerrostalo_osuus || 0) + ' %<br>' +
                            '📐 Keskipinta-ala: ' + (paavo.ra_as_kpa || 0) + ' m²<br>' +
                            '🔑 Omistusasuntoja: ' + paavo.omistusaste + ' % | Vuokra: ' + paavo.vuokra_aste + ' %</div>';
                    }}
                    
                    // Koulutus & työpaikat
                    if (paavo.korkeakoulutetut_osuus !== undefined) {{
                        // Fallback: jos tp_tyopy === 0 (dataa ei julkaistu tälle vuodelle),
                        // etsi viimeisin vuosi jolla on työpaikkatietoja
                        var ictOsuus = paavo.tp_ict_osuus || 0;
                        var palvelutOsuus = paavo.tp_palvelut_osuus || 0;
                        var tpVuosiLabel = '';
                        if (paavo.tp_tyopy === 0 && props.paavo_aikasarja) {{
                            var tpVuodet = Object.keys(props.paavo_aikasarja).map(Number).sort(function(a,b) {{ return b-a; }});
                            for (var ti = 0; ti < tpVuodet.length; ti++) {{
                                var tpV = props.paavo_aikasarja[tpVuodet[ti]];
                                if (tpV && tpV.tp_tyopy > 0) {{
                                    ictOsuus = tpV.tp_ict_osuus || 0;
                                    palvelutOsuus = tpV.tp_palvelut_osuus || 0;
                                    tpVuosiLabel = ' (' + (tpVuodet[ti] - 1) + ')';
                                    break;
                                }}
                            }}
                        }}
                        html += '<div class="details" style="margin-top: 5px; border-top: 1px solid #eee; padding-top: 3px;">' +
                            '<strong>🎓 Koulutus & työ:</strong><br>' +
                            '🎓 Korkeakoulutetut: ' + paavo.korkeakoulutetut_osuus + ' %<br>' +
                            '💻 ICT-työpaikat: ' + ictOsuus + ' %' + tpVuosiLabel + '<br>' +
                            '🏭 Palveluala: ' + palvelutOsuus + ' %' + tpVuosiLabel + '</div>';
                    }}
                }}
            }}
            
            // Palvelut (laajennettu)
            if (props.palvelut && Object.keys(props.palvelut).length > 0) {{
                var p = props.palvelut;
                if (p.kaupat !== undefined && p.palveluindeksi > 0) {{
                    html += '<div class="details" style="margin-top: 10px; border-top: 1px solid #ddd; padding-top: 5px;">' +
                        '<strong>🏪 Palvelut (postinumeroalueella):</strong><br>' +
                        '🛒 Ruokakaupat: ' + p.kaupat + '&nbsp;&nbsp;🏫 Koulut: ' + p.koulut + '&nbsp;&nbsp;🧒 Päiväkodit: ' + p.paivakodit + '<br>' +
                        '💪 Liikunta: ' + p.liikuntapaikat + '&nbsp;&nbsp;🏥 Terveys: ' + p.terveysasemat + '&nbsp;&nbsp;🚌 Liikenne: ' + p.julkinen_liikenne + '<br>' +
                        '📚 Kirjastot: ' + (p.kirjastot || 0) + '&nbsp;&nbsp;💊 Apteekit: ' + (p.apteekit || 0) + '<br>' +
                        '🍽️ Ravintolat: ' + (p.ravintolat || 0) + '&nbsp;&nbsp;☕ Kahvilat: ' + (p.kahvilat || 0) + '&nbsp;&nbsp;🌳 Puistot: ' + (p.puistot || 0) + '<br>' +
                        '⭐ Palveluindeksi: ' + p.palveluindeksi.toFixed(1) + '</div>';
                }}
            }}
            
            return html;
        }}
        
        // Yleinen mittarin arvon haku - reitittää oikeaan getter-funktioon
        function getMetricValue(feature, year, buildingType, metric) {{
            if (metric === 'vuokratuotto') return getVuokratuotto(feature, year, buildingType);
            if (metric === 'hinta_tulot') return getHintaTuloSuhde(feature, year, buildingType);
            return getValue(feature, year, buildingType, metric);
        }}
        
        // Mittarin yksikkö
        function getMetricUnit(metric) {{
            if (metric === 'keskihinta_aritm_nw') return 'EUR/m\u00b2';
            if (metric === 'vuokratuotto') return '%';
            if (metric === 'hinta_tulot') return 'v';
            return 'kpl';
        }}
        
        // Mittarin väritys
        function getMetricColor(metric, value) {{
            if (metric === 'keskihinta_aritm_nw') return getColorPrice(value);
            if (metric === 'vuokratuotto') return getColorYield(value);
            if (metric === 'hinta_tulot') return getColorRatio(value);
            return getColorTransactions(value);
        }}
        
        // Mittarin nimi
        function getMetricName(metric) {{
            if (metric === 'keskihinta_aritm_nw') return 'Neliöhinta';
            if (metric === 'vuokratuotto') return 'Vuokratuotto';
            if (metric === 'hinta_tulot') return 'Hinta/tulot';
            return 'Kaupat';
        }}
        
        // Muotoile mittarin arvo popup-näkymään
        function formatMetricValue(value, metric) {{
            if (metric === 'vuokratuotto') return value.toFixed(1) + ' %';
            if (metric === 'hinta_tulot') return value.toFixed(1) + ' v';
            return value.toLocaleString() + ' ' + getMetricUnit(metric);
        }}
        
        // Toggle mobiilivalikko
        function toggleMobileMenu() {{
            var controls = document.getElementById('controls');
            var button = document.getElementById('mobile-menu-toggle');
            
            if (controls.classList.contains('mobile-menu-open')) {{
                controls.classList.remove('mobile-menu-open');
                button.innerHTML = '☰';
            }} else {{
                controls.classList.add('mobile-menu-open');
                button.innerHTML = '✕';
            }}
        }}
        
        // Päivitä kartta
        function updateMap() {{
            var mode = document.getElementById('view-mode-select').value;
            var buildingType = document.getElementById('building-type-select').value;
            var metric = document.getElementById('metric-select').value;
            
            // Pysäytä animaatiot jos ne ovat käynnissä
            if (animationInterval) {{
                stopAnimation();
            }}
            if (chartAnimationInterval) {{
                stopChartAnimation();
            }}
            
            // Näytä/piilota kartta ja diagrammi
            var mapDiv = document.getElementById('map');
            var chartDiv = document.getElementById('chart-container');
            
            // Näytä/piilota vuosivalitsimet ja animaatiokontrollit
            if (mode === 'absolute') {{
                document.getElementById('year-selector-single').style.display = 'flex';
                document.getElementById('year-selector-range').style.display = 'none';
                document.getElementById('animation-controls').style.display = 'none';
                document.getElementById('animation-chart-controls').style.display = 'none';
                mapDiv.style.display = 'block';
                chartDiv.style.display = 'none';
                
                // Näytä mallivalitsin jos vuosi on 2026
                var selectedYear = document.getElementById('year-select').value;
                var modelSelector = document.getElementById('forecast-model-selector');
                if (modelSelector) {{
                    modelSelector.style.display = (selectedYear === '2026') ? 'flex' : 'none';
                }}
            }} else if (mode === 'change') {{
                document.getElementById('year-selector-single').style.display = 'none';
                document.getElementById('year-selector-range').style.display = 'flex';
                document.getElementById('animation-controls').style.display = 'none';
                document.getElementById('animation-chart-controls').style.display = 'none';
                mapDiv.style.display = 'block';
                chartDiv.style.display = 'none';
            }} else if (mode === 'analysis') {{
                document.getElementById('year-selector-single').style.display = 'none';
                document.getElementById('year-selector-range').style.display = 'none';
                document.getElementById('animation-controls').style.display = 'none';
                document.getElementById('animation-chart-controls').style.display = 'none';
                mapDiv.style.display = 'block';
                chartDiv.style.display = 'none';
            }} else if (mode === 'animation') {{
                document.getElementById('year-selector-single').style.display = 'none';
                document.getElementById('year-selector-range').style.display = 'none';
                document.getElementById('animation-controls').style.display = 'flex';
                document.getElementById('animation-chart-controls').style.display = 'none';
                mapDiv.style.display = 'block';
                chartDiv.style.display = 'none';
                animationCurrentYear = availableYears[0];
                document.getElementById('animation-year').textContent = animationCurrentYear + (animationCurrentYear == 2026 ? '*' : '');
            }} else if (mode === 'animation-chart') {{
                document.getElementById('year-selector-single').style.display = 'none';
                document.getElementById('year-selector-range').style.display = 'none';
                document.getElementById('animation-controls').style.display = 'none';
                document.getElementById('animation-chart-controls').style.display = 'flex';
                mapDiv.style.display = 'none';
                chartDiv.style.display = 'block';
                chartAnimationCurrentYear = availableYears[0];
                document.getElementById('chart-animation-year').textContent = chartAnimationCurrentYear + (chartAnimationCurrentYear == 2026 ? '*' : '');
            }}
            
            // Poista vanha layer
            if (geoJsonLayer) map.removeLayer(geoJsonLayer);
            if (currentLegend) map.removeControl(currentLegend);
            
            // Luo uusi layer
            if (mode === 'absolute') {{
                createAbsoluteMap(buildingType, metric);
            }} else if (mode === 'change') {{
                createChangeMap(buildingType, metric);
            }} else if (mode === 'analysis') {{
                createAnalysisMap(buildingType, metric);
            }} else if (mode === 'animation') {{
                createAnimationFrame(animationCurrentYear, buildingType, metric);
            }} else if (mode === 'animation-chart') {{
                var city = document.getElementById('chart-city-select').value;
                createChartFrame(chartAnimationCurrentYear, buildingType, metric, city);
            }}
            
            updateStats();
        }}
        
        // Päivitä diagrammin näyttö kun kaupunkia vaihdetaan
        function updateChartDisplay() {{
            if (chartAnimationInterval) {{
                stopChartAnimation();
            }}
            var buildingType = document.getElementById('building-type-select').value;
            var metric = document.getElementById('metric-select').value;
            var city = document.getElementById('chart-city-select').value;
            createChartFrame(chartAnimationCurrentYear, buildingType, metric, city);
        }}
        
        // Luo absoluuttinen kartta
        function createAbsoluteMap(buildingType, metric) {{
            var selectedYear = document.getElementById('year-select').value;
            var isPrice = (metric === 'keskihinta_aritm_nw');
            var isYield = (metric === 'vuokratuotto');
            var isRatio = (metric === 'hinta_tulot');
            
            geoJsonLayer = L.geoJSON(geojsonData, {{
                smoothFactor: 0,  // Ei geometrian yksinkertaistusta, tarkemmat rajat
                style: function(feature) {{
                    if (isYield) {{
                        var yieldVal = getVuokratuotto(feature, selectedYear, buildingType);
                        var color = yieldVal ? getColorYield(yieldVal) : '#ccc';
                    }} else if (isRatio) {{
                        var ratioVal = getHintaTuloSuhde(feature, selectedYear, buildingType);
                        var color = ratioVal ? getColorRatio(ratioVal) : '#ccc';
                    }} else {{
                        var value = getValue(feature, selectedYear, buildingType, metric);
                        var color = value ? (isPrice ? getColorPrice(value) : getColorTransactions(value)) : '#ccc';
                    }}
                    return {{
                        fillColor: color,
                        fillOpacity: 0.7,
                        color: '#fff',
                        weight: 1,
                        opacity: 1
                    }};
                }},
                onEachFeature: function(feature, layer) {{
                    var props = feature.properties;
                    
                    var popupContent;
                    
                    if (isRatio) {{
                        var ratioVal = getHintaTuloSuhde(feature, selectedYear, buildingType);
                        if (ratioVal) {{
                            var priceVal = getValue(feature, selectedYear, buildingType, 'keskihinta_aritm_nw');
                            var paavoY = parseInt(selectedYear) + 1;
                            var pa = props.paavo_aikasarja;
                            var tuloVal = 0;
                            if (pa && pa[paavoY]) tuloVal = pa[paavoY].keskitulo;
                            else if (pa) {{
                                var vv = Object.keys(pa).map(Number).sort(function(a,b){{return b-a;}});
                                for (var vi = 0; vi < vv.length; vi++) {{ if (vv[vi] <= paavoY && pa[vv[vi]].keskitulo) {{ tuloVal = pa[vv[vi]].keskitulo; break; }} }}
                            }}
                            popupContent = '<div class="popup-content">' +
                                '<h3>' + props.postinumer + '</h3>' +
                                '<div class="price" style="color: ' + getColorRatio(ratioVal) + ';">' + ratioVal.toFixed(1) + ' vuotta</div>' +
                                '<div class="details">' + props.name + '</div>' +
                                '<div class="details">' + selectedYear + ' | ' + buildingTypes[buildingType] + '</div>' +
                                '<div class="details" style="margin-top: 10px; border-top: 1px solid #ddd; padding-top: 5px;">' +
                                '<strong>🏠 Hinta/tulot -suhde:</strong><br>' +
                                '💰 Neliöhinta: ' + priceVal.toLocaleString() + ' €/m²<br>' +
                                '📐 60m² asunto: ' + (priceVal * 60).toLocaleString() + ' €<br>' +
                                '💶 Keskitulo: ' + tuloVal.toLocaleString() + ' €/v<br>' +
                                '📊 Suhde: <strong>' + ratioVal.toFixed(1) + ' vuoden palkat</strong></div>' +
                                buildExpandedPopup(props, selectedYear) +
                                '</div>';
                        }} else {{
                            popupContent = '<div class="popup-content">' +
                                '<h3>' + props.postinumer + '</h3>' +
                                '<div class="details">' + props.name + '</div>' +
                                '<div class="details" style="color: #999; font-style: italic;">Ei hinta- tai tulotietoja (' + selectedYear + ' | ' + buildingTypes[buildingType] + ')</div>' +
                                '</div>';
                        }}
                    }} else if (isYield) {{
                        var yieldVal = getVuokratuotto(feature, selectedYear, buildingType);
                        var rentVal = getVuokra(feature, selectedYear, buildingType);
                        var priceVal = getValue(feature, selectedYear, buildingType, 'keskihinta_aritm_nw');
                        
                        if (yieldVal) {{
                            popupContent = '<div class="popup-content">' +
                                '<h3>' + props.postinumer + '</h3>' +
                                '<div class="price" style="color: ' + getColorYield(yieldVal) + ';">' + yieldVal.toFixed(1) + ' %</div>' +
                                '<div class="details">' + props.name + '</div>' +
                                '<div class="details">' + selectedYear + ' | ' + buildingTypes[buildingType] + '</div>' +
                                '<div class="details" style="margin-top: 10px; border-top: 1px solid #ddd; padding-top: 5px;">' +
                                '<strong>📊 Vuokra vs. osto:</strong><br>' +
                                '🏠 Ostohinta: ' + priceVal.toLocaleString() + ' €/m²<br>' +
                                '🔑 Vuokra: ' + rentVal.toFixed(2) + ' €/m²/kk<br>' +
                                '💰 Vuosivuokra: ' + (rentVal * 12).toFixed(0) + ' €/m²/v<br>' +
                                '📈 Bruttovuokratuotto: <strong>' + yieldVal.toFixed(2) + ' %</strong></div>' +
                                buildExpandedPopup(props, selectedYear) +
                                '</div>';
                        }} else {{
                            popupContent = '<div class="popup-content">' +
                                '<h3>' + props.postinumer + '</h3>' +
                                '<div class="details">' + props.name + '</div>' +
                                '<div class="details" style="color: #999; font-style: italic;">Ei vuokra- tai hintatietoja (' + selectedYear + ' | ' + buildingTypes[buildingType] + ')</div>' +
                                '</div>';
                        }}
                    }} else {{
                        var value = getValue(feature, selectedYear, buildingType, metric);
                    
                    if (value) {{
                        var metricLabel = isPrice ? 'EUR/m²' : 'kpl';
                        popupContent = '<div class="popup-content">' +
                            '<h3>' + props.postinumer + '</h3>' +
                            '<div class="price">' + value.toLocaleString() + ' ' + metricLabel + '</div>' +
                            '<div class="details">' + props.name + '</div>' +
                            '<div class="details">' + selectedYear + ' | ' + buildingTypes[buildingType] + '</div>';
                        
                        // Lisää vuokratiedot jos saatavilla
                        var rentVal = getVuokra(feature, selectedYear, buildingType);
                        if (rentVal && isPrice) {{
                            var yieldVal = getVuokratuotto(feature, selectedYear, buildingType);
                            popupContent += '<div class="details" style="margin-top: 10px; border-top: 1px solid #ddd; padding-top: 5px;">' +
                                '<strong>🔑 Vuokra vs. osto:</strong><br>' +
                                'Vuokra: ' + rentVal.toFixed(2) + ' €/m²/kk<br>';
                            if (yieldVal) {{
                                popupContent += 'Bruttovuokratuotto: <strong style="color:' + getColorYield(yieldVal) + '">' + yieldVal.toFixed(1) + ' %</strong>';
                            }}
                            popupContent += '</div>';
                        }}
                        
                        // Laajennetut väestö-, palvelu- ja matka-aikatiedot
                        popupContent += buildExpandedPopup(props, selectedYear);
                        
                        popupContent += '</div>';
                    }} else {{
                        popupContent = '<div class="popup-content">' +
                            '<h3>' + props.postinumer + '</h3>' +
                            '<div class="details">' + props.name + '</div>' +
                            '<div class="details" style="color: #999; font-style: italic;">Ei kauppoja (' + selectedYear + ' | ' + buildingTypes[buildingType] + ')</div>';
                        
                        // Laajennetut tiedot myös kun ei kauppoja
                        popupContent += buildExpandedPopup(props, selectedYear);
                        
                        popupContent += '</div>';
                    }}
                    }} // close isRatio/isYield/else
                    // Lisää aikasarjanappi popupiin
                    popupContent = popupContent.replace(/<\\/div>$/, '<button class="ts-btn" onclick="openTimeSeriesModal()">📊 Näytä aikasarja</button></div>');
                    bindMobilePopup(layer, popupContent, feature);
                    layer.on('mouseover', function(e) {{
                        this.setStyle({{ fillOpacity: 0.9, weight: 2 }});
                    }});
                    layer.on('mouseout', function(e) {{
                        geoJsonLayer.resetStyle(this);
                    }});
                }}
            }}).addTo(map);
            
            // Legenda
            createLegend(metric);
        }}
        
        // Luo muutoskartta
        function createChangeMap(buildingType, metric) {{
            var yearFrom = document.getElementById('year-from').value;
            var yearTo = document.getElementById('year-to').value;
            
            geoJsonLayer = L.geoJSON(geojsonData, {{
                smoothFactor: 0,  // Ei geometrian yksinkertaistusta, tarkemmat rajat
                style: function(feature) {{
                    var valueFrom = getMetricValue(feature, yearFrom, buildingType, metric);
                    var valueTo = getMetricValue(feature, yearTo, buildingType, metric);
                    
                    if (valueFrom && valueTo && valueFrom > 0) {{
                        var change = ((valueTo - valueFrom) / valueFrom) * 100;
                        return {{
                            fillColor: getColorChange(change),
                            fillOpacity: 0.7,
                            color: '#fff',
                            weight: 1,
                            opacity: 1
                        }};
                    }} else {{
                        return {{
                            fillColor: '#ccc',
                            fillOpacity: 0.3,
                            color: '#fff',
                            weight: 1,
                            opacity: 1
                        }};
                    }}
                }},
                onEachFeature: function(feature, layer) {{
                    var props = feature.properties;
                    var valueFrom = getMetricValue(feature, yearFrom, buildingType, metric);
                    var valueTo = getMetricValue(feature, yearTo, buildingType, metric);
                    
                    var popupContent;
                    if (valueFrom && valueTo && valueFrom > 0) {{
                        var change = ((valueTo - valueFrom) / valueFrom) * 100;
                        var absChange = valueTo - valueFrom;
                        var changeSign = change >= 0 ? '+' : '';
                        var unit = getMetricUnit(metric);
                        var isDecimal = (metric === 'vuokratuotto' || metric === 'hinta_tulot');
                        
                        popupContent = '<div class="popup-content">' +
                            '<h3>' + props.postinumer + '</h3>' +
                            '<div class="price">' + changeSign + change.toFixed(1) + ' %</div>' +
                            '<div class="details">' + props.name + '</div>' +
                            '<div class="details">' + yearFrom + ': ' + (isDecimal ? valueFrom.toFixed(1) : valueFrom.toLocaleString()) + ' ' + unit + '<br>' +
                            yearTo + ': ' + (isDecimal ? valueTo.toFixed(1) : valueTo.toLocaleString()) + ' ' + unit + '<br>' +
                            'Muutos: ' + changeSign + (isDecimal ? absChange.toFixed(1) : absChange.toLocaleString()) + ' ' + unit + '</div>' +
                            '<div class="details">' + buildingTypes[buildingType] + '</div>' +
                            '</div>';
                    }} else {{
                        popupContent = '<div class="popup-content">' +
                            '<h3>' + props.postinumer + '</h3>' +
                            '<div class="details">' + props.name + '</div>' +
                            '<div class="details" style="color: #999; font-style: italic;">Ei riittävästi dataa muutoksen laskemiseen<br>' +
                            '(' + yearFrom + ' - ' + yearTo + ' | ' + buildingTypes[buildingType] + ')</div>' +
                            '</div>';
                    }}
                    popupContent = popupContent.replace(/<\\/div>$/, '<button class="ts-btn" onclick="openTimeSeriesModal()">📊 Näytä aikasarja</button></div>');
                    bindMobilePopup(layer, popupContent, feature);
                    layer.on('mouseover', function(e) {{
                        this.setStyle({{ fillOpacity: 0.9, weight: 2 }});
                    }});
                    layer.on('mouseout', function(e) {{
                        geoJsonLayer.resetStyle(this);
                    }});
                }}
            }}).addTo(map);
            
            // Legenda muutoksille
            createChangeLegend();
        }}
        
        // Väritys trendianalyysille
        function getColorTrend(change) {{
            // Käytetään samaa väriskaalaaa kuin muutoksissa
            if (change > 15) return '#2ecc71';
            else if (change > 10) return '#27ae60';
            else if (change > 5) return '#9acd32';
            else if (change > 0) return '#f1c40f';
            else if (change > -5) return '#f39c12';
            else if (change > -10) return '#e74c3c';
            else return '#8B0000';
        }}
        
        // Luo trendianalyysikartta
        function createAnalysisMap(buildingType, metric) {{
            var isPrice = (metric === 'keskihinta_aritm_nw');
            
            geoJsonLayer = L.geoJSON(geojsonData, {{
                smoothFactor: 0,
                style: function(feature) {{
                    var change5v;
                    if (isPrice) {{
                        var analyysi = feature.properties.analyysi;
                        change5v = (analyysi && analyysi.hinta_muutos_5v !== null && analyysi.hinta_muutos_5v !== undefined) ? analyysi.hinta_muutos_5v : null;
                    }} else {{
                        // Laske 5v muutos lennossa muille mittareille
                        var valFrom = getMetricValue(feature, '2021', buildingType, metric);
                        var valTo = getMetricValue(feature, '2025', buildingType, metric);
                        change5v = (valFrom && valTo && valFrom > 0) ? ((valTo - valFrom) / valFrom * 100) : null;
                    }}
                    
                    if (change5v !== null) {{
                        return {{
                            fillColor: getColorTrend(change5v),
                            fillOpacity: 0.7,
                            color: '#fff',
                            weight: 1,
                            opacity: 1
                        }};
                    }} else {{
                        return {{
                            fillColor: '#ccc',
                            fillOpacity: 0.3,
                            color: '#fff',
                            weight: 1,
                            opacity: 1
                        }};
                    }}
                }},
                onEachFeature: function(feature, layer) {{
                    var props = feature.properties;
                    var popupContent;
                    
                    if (isPrice) {{
                        // Alkuperäinen hinta-analyysi pre-computed datasta
                        var analyysi = props.analyysi;
                        if (analyysi && analyysi.hinta_muutos_5v !== null && analyysi.hinta_muutos_5v !== undefined) {{
                            var changeSign = analyysi.hinta_muutos_5v >= 0 ? '+' : '';
                            var trendiEmoji = analyysi.trendi === 'nouseva' ? String.fromCodePoint(0x1F4C8) : 
                                             analyysi.trendi === 'laskeva' ? String.fromCodePoint(0x1F4C9) : String.fromCodePoint(0x1F4CA);
                            var aktiivisuusEmoji = analyysi.aktiivisuus === 'korkea' ? String.fromCodePoint(0x1F525) : 
                                                  analyysi.aktiivisuus === 'keskitaso' ? String.fromCodePoint(0x25AA, 0xFE0F) : String.fromCodePoint(0x2744, 0xFE0F);
                            
                            popupContent = '<div class="popup-content">' +
                                '<h3>' + props.postinumer + '</h3>' +
                                '<div class="price">' + changeSign + analyysi.hinta_muutos_5v.toFixed(1) + ' %</div>' +
                                '<div class="details">' + props.name + '</div>' +
                                '<div class="details" style="margin-top: 10px;">' +
                                '<strong>' + String.fromCodePoint(0x1F3E0) + ' Asuntohinnat (2021-2025)</strong><br>' +
                                trendiEmoji + ' ' + analyysi.trendi.charAt(0).toUpperCase() + analyysi.trendi.slice(1) + '<br>' +
                                String.fromCodePoint(0x1F4CA) + ' Kauppoja: ' + analyysi.keskim_kaupat_vuosi.toFixed(1) + ' / vuosi<br>' +
                                aktiivisuusEmoji + ' Aktiivisuus: ' + analyysi.aktiivisuus + '<br>' +
                                String.fromCodePoint(0x1F4C8) + ' Volatiliteetti: ' + analyysi.volatiliteetti.toFixed(1) + ' %</div>';
                        }} else {{
                            popupContent = '<div class="popup-content">' +
                                '<h3>' + props.postinumer + '</h3>' +
                                '<div class="details">' + props.name + '</div>' +
                                '<div class="details" style="color: #999; font-style: italic;">Ei riitt' + String.fromCharCode(228) + 'v' + String.fromCharCode(228) + 'sti dataa trendianalyysiin</div>' +
                                '</div>';
                        }}
                    }} else {{
                        // Muut mittarit: laske 5v muutos lennossa
                        var valFrom = getMetricValue(feature, '2021', buildingType, metric);
                        var valTo = getMetricValue(feature, '2025', buildingType, metric);
                        
                        if (valFrom && valTo && valFrom > 0) {{
                            var change5v = ((valTo - valFrom) / valFrom * 100);
                            var changeSign = change5v >= 0 ? '+' : '';
                            var mName = getMetricName(metric);
                            var unit = getMetricUnit(metric);
                            var isDecimal = (metric === 'vuokratuotto' || metric === 'hinta_tulot');
                            var trendiLabel = change5v > 5 ? 'Nouseva' : (change5v < -5 ? 'Laskeva' : 'Vakaa');
                            var trendiEmoji = change5v > 5 ? String.fromCodePoint(0x1F4C8) : 
                                             (change5v < -5 ? String.fromCodePoint(0x1F4C9) : String.fromCodePoint(0x1F4CA));
                            
                            popupContent = '<div class="popup-content">' +
                                '<h3>' + props.postinumer + '</h3>' +
                                '<div class="price">' + changeSign + change5v.toFixed(1) + ' %</div>' +
                                '<div class="details">' + props.name + '</div>' +
                                '<div class="details" style="margin-top: 10px;">' +
                                '<strong>' + mName + ' (2021-2025)</strong><br>' +
                                trendiEmoji + ' ' + trendiLabel + '<br>' +
                                '2021: ' + (isDecimal ? valFrom.toFixed(1) : valFrom.toLocaleString()) + ' ' + unit + '<br>' +
                                '2025: ' + (isDecimal ? valTo.toFixed(1) : valTo.toLocaleString()) + ' ' + unit + '</div>';
                        }} else {{
                            popupContent = '<div class="popup-content">' +
                                '<h3>' + props.postinumer + '</h3>' +
                                '<div class="details">' + props.name + '</div>' +
                                '<div class="details" style="color: #999; font-style: italic;">Ei riitt' + String.fromCharCode(228) + 'v' + String.fromCharCode(228) + 'sti dataa trendianalyysiin</div>' +
                                '</div>';
                        }}
                    }}
                    
                    // Lisää väestö- ja palvelutiedot (kaikille mittareille)
                    if (popupContent.indexOf('font-style: italic') === -1) {{
                        if (props.paavo_aikasarja) {{
                            var paavoAlku = 2022;
                            var paavoLoppu = 2026;
                            var vuodet = Object.keys(props.paavo_aikasarja).map(Number).sort();
                            var alkuVuosi = vuodet.find(v => v >= paavoAlku) || vuodet[vuodet.length - 1];
                            var loppuVuosi = vuodet[vuodet.length - 1];
                            
                            if (props.paavo_aikasarja[alkuVuosi] && props.paavo_aikasarja[loppuVuosi] && alkuVuosi !== loppuVuosi) {{
                                var paavoAlkuData = props.paavo_aikasarja[alkuVuosi];
                                var paavoLoppuData = props.paavo_aikasarja[loppuVuosi];
                                
                                var vaestoMuutos = ((paavoLoppuData.vaesto - paavoAlkuData.vaesto) / paavoAlkuData.vaesto * 100);
                                var ikaMuutos = paavoLoppuData.keski_ika - paavoAlkuData.keski_ika;
                                var tuloMuutos = ((paavoLoppuData.keskitulo - paavoAlkuData.keskitulo) / paavoAlkuData.keskitulo * 100);
                                var tyottomyysMuutos = paavoLoppuData.tyottomyysaste - paavoAlkuData.tyottomyysaste;
                                
                                var vaestoSign = vaestoMuutos >= 0 ? '+' : '';
                                var ikaSign = ikaMuutos >= 0 ? '+' : '';
                                var tuloSign = tuloMuutos >= 0 ? '+' : '';
                                var tyottomyysSign = tyottomyysMuutos >= 0 ? '+' : '';
                                
                                var naytettavaAlku = alkuVuosi - 1;
                                var naytettavaLoppu = loppuVuosi - 1;
                                
                                // Suljetaan ensin details ja lisätään väestöosuus
                                popupContent = popupContent.replace(/<\\/div>\\s*$/, '') +
                                    '<div class="details" style="margin-top: 10px; border-top: 1px solid #ddd; padding-top: 5px;">' +
                                    '<strong>' + String.fromCodePoint(0x1F465) + ' V' + String.fromCharCode(228) + 'est' + String.fromCharCode(246) + 'muutokset (' + naytettavaAlku + '-' + naytettavaLoppu + ')</strong><br>' +
                                    'Asukkaat: ' + vaestoSign + vaestoMuutos.toFixed(1) + ' %<br>' +
                                    'Keski-ik' + String.fromCharCode(228) + ': ' + ikaSign + ikaMuutos.toFixed(1) + ' v<br>' +
                                    'Keskitulo: ' + tuloSign + tuloMuutos.toFixed(1) + ' %<br>' +
                                    'Ty' + String.fromCharCode(246) + 'tt' + String.fromCharCode(246) + 'myys: ' + tyottomyysSign + tyottomyysMuutos.toFixed(1) + ' %-yks</div>';
                            }}
                        }}
                        
                        if (props.palvelut && Object.keys(props.palvelut).length > 0) {{
                            var palvelut = props.palvelut;
                            if (palvelut.kaupat !== undefined && palvelut.palveluindeksi > 0) {{
                                popupContent = popupContent.replace(/<\\/div>\\s*$/, '') +
                                    '<div class="details" style="margin-top: 10px; border-top: 1px solid #ddd; padding-top: 5px;">' +
                                    '<strong>' + String.fromCodePoint(0x1F3EA) + ' Palvelut (postinumeroalueella):</strong><br>' +
                                    String.fromCodePoint(0x1F6D2) + ' Ruokakaupat: ' + palvelut.kaupat + '<br>' +
                                    String.fromCodePoint(0x1F3EB) + ' Koulut: ' + palvelut.koulut + '<br>' +
                                    String.fromCodePoint(0x1F9D2) + ' P' + String.fromCharCode(228) + 'iv' + String.fromCharCode(228) + 'kodit: ' + palvelut.paivakodit + '<br>' +
                                    String.fromCodePoint(0x1F4AA) + ' Liikuntapaikat: ' + palvelut.liikuntapaikat + '<br>' +
                                    String.fromCodePoint(0x1F3E5) + ' Terveysasemat: ' + palvelut.terveysasemat + '<br>' +
                                    String.fromCodePoint(0x1F68C) + ' Julk. liikenne: ' + palvelut.julkinen_liikenne + '<br>' +
                                    String.fromCodePoint(0x1F4DA) + ' Kirjastot: ' + (palvelut.kirjastot || 0) + '<br>' +
                                    String.fromCodePoint(0x1F48A) + ' Apteekit: ' + (palvelut.apteekit || 0) + '<br>' +
                                    String.fromCodePoint(0x2B50) + ' Palveluindeksi: ' + palvelut.palveluindeksi.toFixed(1) + '</div>';
                            }}
                        }}
                        
                        popupContent += '</div>';
                    }}
                    
                    popupContent = popupContent.replace(/<\\/div>$/, '<button class="ts-btn" onclick="openTimeSeriesModal()">' + String.fromCodePoint(0x1F4CA) + ' N' + String.fromCharCode(228) + 'yt' + String.fromCharCode(228) + ' aikasarja</button></div>');
                    bindMobilePopup(layer, popupContent, feature);
                    layer.on('mouseover', function(e) {{
                        this.setStyle({{ fillOpacity: 0.9, weight: 2 }});
                    }});
                    layer.on('mouseout', function(e) {{
                        geoJsonLayer.resetStyle(this);
                    }});
                }}
            }}).addTo(map);
            
            // Legenda trendianalyysille
            createAnalysisLegend();
        }}
        
        // Luo animaatiokehys tietylle vuodelle
        function createAnimationFrame(year, buildingType, metric) {{
            
            geoJsonLayer = L.geoJSON(geojsonData, {{
                smoothFactor: 0,
                style: function(feature) {{
                    var value = getMetricValue(feature, year, buildingType, metric);
                    var color = value ? getMetricColor(metric, value) : '#ccc';
                    return {{
                        fillColor: color,
                        fillOpacity: 0.7,
                        color: '#fff',
                        weight: 1,
                        opacity: 1
                    }};
                }},
                onEachFeature: function(feature, layer) {{
                    var props = feature.properties;
                    var value = getMetricValue(feature, year, buildingType, metric);
                    
                    if (value) {{
                        var popupContent = '<div class="popup-content">' +
                            '<h3>' + props.postinumer + '</h3>' +
                            '<div class="price">' + formatMetricValue(value, metric) + '</div>' +
                            '<div class="details">' + props.name + '</div>' +
                            '<div class="details">' + year + (year == 2026 ? '*' : '') + ' | ' + buildingTypes[buildingType] + '</div>' +
                            '<button class="ts-btn" onclick="openTimeSeriesModal()">📊 Näytä aikasarja</button>' +
                            '</div>';
                        bindMobilePopup(layer, popupContent, feature);
                    }}
                    layer.on('mouseover', function(e) {{
                        this.setStyle({{ fillOpacity: 0.9, weight: 2 }});
                    }});
                    layer.on('mouseout', function(e) {{
                        geoJsonLayer.resetStyle(this);
                    }});
                }}
            }}).addTo(map);
            
            createLegend(metric);
        }}
        
        // Animaation käynnistys/pysäytys
        function toggleAnimation() {{
            if (isAnimationPlaying) {{
                stopAnimation();
            }} else {{
                startAnimation();
            }}
        }}
        
        function startAnimation() {{
            isAnimationPlaying = true;
            document.getElementById('play-button').textContent = '⏸️ Tauko';
            
            var buildingType = document.getElementById('building-type-select').value;
            var metric = document.getElementById('metric-select').value;
            var speed = parseInt(document.getElementById('animation-speed').value);
            
            var currentIndex = availableYears.indexOf(animationCurrentYear.toString());
            
            animationInterval = setInterval(function() {{
                currentIndex++;
                if (currentIndex >= availableYears.length) {{
                    currentIndex = 0; // Aloita alusta
                }}
                
                animationCurrentYear = availableYears[currentIndex];
                document.getElementById('animation-year').textContent = animationCurrentYear + (animationCurrentYear == 2026 ? '*' : '');
                
                // Päivitä kartta
                if (geoJsonLayer) map.removeLayer(geoJsonLayer);
                if (currentLegend) map.removeControl(currentLegend);
                createAnimationFrame(animationCurrentYear, buildingType, metric);
            }}, speed);
        }}
        
        function stopAnimation() {{
            isAnimationPlaying = false;
            document.getElementById('play-button').textContent = '▶️ Toista';
            if (animationInterval) {{
                clearInterval(animationInterval);
                animationInterval = null;
            }}
        }}
        
        // Diagrammi-animaatio funktiot
        function getTop10Areas(year, buildingType, metric, city) {{
            var areas = [];
            
            geojsonData.features.forEach(function(feature) {{
                var props = feature.properties;
                var value = getMetricValue(feature, year, buildingType, metric);
                
                if (value) {{
                    var postinumero = props.postinumer;
                    
                    // Suodata kaupungin mukaan
                    var includeArea = false;
                    if (city === 'all') {{
                        includeArea = true;
                    }} else if (cityPostalCodes[city]) {{
                        var postalPrefix = postinumero.substring(0, 2);
                        includeArea = cityPostalCodes[city].indexOf(postalPrefix) !== -1;
                    }}
                    
                    if (includeArea) {{
                        areas.push({{
                            postinumero: postinumero,
                            nimi: props.name,
                            hinta: value
                        }});
                    }}
                }}
            }});
            
            // Järjestä arvon mukaan laskevasti ja ota top 10
            areas.sort(function(a, b) {{ return b.hinta - a.hinta; }});
            return areas.slice(0, 10);
        }}
        
        function createChartFrame(year, buildingType, metric, city) {{
            var top10 = getTop10Areas(year, buildingType, metric, city);
            
            if (top10.length === 0) {{
                document.getElementById('chart-container').innerHTML = '<div style="text-align: center; padding: 50px;"><h2>Ei dataa tälle valinnalle</h2></div>';
                return;
            }}
            
            // Kaupungin nimi otsikkoon
            var cityNames = {{
                'all': 'Koko maa',
                'helsinki': 'Helsinki',
                'espoo': 'Espoo',
                'vantaa': 'Vantaa',
                'tampere': 'Tampere',
                'turku': 'Turku',
                'oulu': 'Oulu',
                'kuopio': 'Kuopio'
            }};
            var cityName = cityNames[city] || 'Koko maa';
            
            // Luo HTML vaakapylväsdiagrammi
            var maxPrice = top10[0].hinta;
            var metricTitles = {{
                'keskihinta_aritm_nw': 'Top 10 Kalleimmat Postinumeroalueet',
                'lkm_julk20': 'Top 10 Aktiivisimmat Postinumeroalueet',
                'vuokratuotto': 'Top 10 Tuottoisimmat Postinumeroalueet',
                'hinta_tulot': 'Top 10 Kalleimmat (hinta/tulot) Postinumeroalueet'
            }};
            var chartTitle = (metricTitles[metric] || 'Top 10') + ' - ' + year + (year == 2026 ? '*' : '');
            var unit = getMetricUnit(metric);
            var html = '<div style="max-width: 1200px; margin: 0 auto;">';
            html += '<h2 style="text-align: center; margin-bottom: 10px;">' + chartTitle + '</h2>';
            html += '<div style="font-size: 16px; color: #1e3c72; text-align: center; margin-bottom: 10px; font-weight: bold;">' + cityName + '</div>';
            html += '<div style="font-size: 14px; color: #666; text-align: center; margin-bottom: 20px;">Huoneistotyyppi: ' + buildingTypes[buildingType] + '</div>';
            
            top10.forEach(function(area, index) {{
                var percentage = (area.hinta / maxPrice) * 100;
                var barColor = getMetricColor(metric, area.hinta);
                var isDecimal = (metric === 'vuokratuotto' || metric === 'hinta_tulot');
                var displayValue = isDecimal ? area.hinta.toFixed(1) + ' ' + unit : area.hinta.toLocaleString() + ' ' + unit;
                
                html += '<div style="margin-bottom: 20px;">';
                html += '<div style="display: flex; align-items: center; margin-bottom: 5px;">';
                html += '<div style="width: 60px; font-weight: bold; color: #333;">' + (index + 1) + '.</div>';
                html += '<div style="width: 120px; font-weight: bold; color: #1e3c72;">' + area.postinumero + '</div>';
                html += '<div style="flex: 1; color: #666; font-size: 14px;">' + area.nimi + '</div>';
                html += '<div style="width: 140px; text-align: right; font-weight: bold; color: ' + barColor + ';">' + displayValue + '</div>';
                html += '</div>';
                html += '<div style="margin-left: 60px; background: #f0f0f0; height: 30px; border-radius: 5px; overflow: hidden;">';
                html += '<div style="background: ' + barColor + '; height: 100%; width: ' + percentage + '%; transition: width 0.3s ease;"></div>';
                html += '</div>';
                html += '</div>';
            }});
            
            html += '</div>';
            document.getElementById('chart-container').innerHTML = html;
        }}
        
        function toggleChartAnimation() {{
            if (isChartAnimationPlaying) {{
                stopChartAnimation();
            }} else {{
                startChartAnimation();
            }}
        }}
        
        function startChartAnimation() {{
            isChartAnimationPlaying = true;
            document.getElementById('chart-play-button').textContent = '⏸️ Tauko';
            
            var buildingType = document.getElementById('building-type-select').value;
            var metric = document.getElementById('metric-select').value;
            var city = document.getElementById('chart-city-select').value;
            var speed = parseInt(document.getElementById('chart-animation-speed').value);
            
            var currentIndex = availableYears.indexOf(chartAnimationCurrentYear.toString());
            
            chartAnimationInterval = setInterval(function() {{
                currentIndex++;
                if (currentIndex >= availableYears.length) {{
                    currentIndex = 0; // Aloita alusta
                }}
                
                chartAnimationCurrentYear = availableYears[currentIndex];
                document.getElementById('chart-animation-year').textContent = chartAnimationCurrentYear + (chartAnimationCurrentYear == 2026 ? '*' : '');
                
                // Päivitä diagrammi
                createChartFrame(chartAnimationCurrentYear, buildingType, metric, city);
            }}, speed);
        }}
        
        function stopChartAnimation() {{
            isChartAnimationPlaying = false;
            document.getElementById('chart-play-button').textContent = '▶️ Toista';
            if (chartAnimationInterval) {{
                clearInterval(chartAnimationInterval);
                chartAnimationInterval = null;
            }}
        }}
        
        // Luo legenda
        function createLegend(metric) {{
            currentLegend = L.control({{position: 'bottomright'}});
            currentLegend.onAdd = function(map) {{
                var div = L.DomUtil.create('div', 'legend');
                
                if (metric === 'keskihinta_aritm_nw') {{
                    div.innerHTML = '<h4>Hinta €/m²</h4>';
                    var grades = [0, 2000, 3000, 4000, 5000, 6000, 8000];
                    var labels = ['< 2000', '2000-3000', '3000-4000', '4000-5000', '5000-6000', '6000-8000', '> 8000'];
                    for (var i = 0; i < grades.length; i++) {{
                        div.innerHTML += '<div class="legend-item"><div class="legend-color" style="background:' + 
                            getColorPrice(grades[i] + 1) + '"></div>' + labels[i] + '</div>';
                    }}
                }} else if (metric === 'hinta_tulot') {{
                    div.innerHTML = '<h4>Hinta/tulot (vuosia)</h4>';
                    var grades = [0, 4, 5, 6, 8, 10, 12];
                    var labels = ['< 4', '4-5', '5-6', '6-8', '8-10', '10-12', '> 12'];
                    for (var i = 0; i < grades.length; i++) {{
                        div.innerHTML += '<div class="legend-item"><div class="legend-color" style="background:' + 
                            getColorRatio(grades[i] + 0.5) + '"></div>' + labels[i] + '</div>';
                    }}
                }} else if (metric === 'vuokratuotto') {{
                    div.innerHTML = '<h4>Vuokratuotto %</h4>';
                    var grades = [8, 7, 6, 5, 4, 3, 0];
                    var labels = ['> 8 %', '7-8 %', '6-7 %', '5-6 %', '4-5 %', '3-4 %', '< 3 %'];
                    for (var i = 0; i < grades.length; i++) {{
                        div.innerHTML += '<div class="legend-item"><div class="legend-color" style="background:' + 
                            getColorYield(grades[i] + 0.5) + '"></div>' + labels[i] + '</div>';
                    }}
                }} else {{
                    div.innerHTML = '<h4>Kauppoja (kpl)</h4>';
                    var grades = [0, 5, 10, 20, 30, 50, 100];
                    var labels = ['< 5', '5-10', '10-20', '20-30', '30-50', '50-100', '> 100'];
                    for (var i = grades.length - 1; i >= 0; i--) {{
                        div.innerHTML += '<div class="legend-item"><div class="legend-color" style="background:' + 
                            getColorTransactions(grades[i] + 1) + '"></div>' + labels[i] + '</div>';
                    }}
                }}
                return div;
            }};
            currentLegend.addTo(map);
        }}
        
        // Luo legenda muutoksille
        function createChangeLegend() {{
            currentLegend = L.control({{position: 'bottomright'}});
            currentLegend.onAdd = function(map) {{
                var div = L.DomUtil.create('div', 'legend');
                div.innerHTML = '<h4>Muutos-%</h4>';
                var grades = [15, 10, 5, 0, -5, -10];
                var labels = ['> 15%', '10% - 15%', '5% - 10%', '0% - 5%', '-5% - 0%', '-10% - -5%', '< -10%'];
                for (var i = 0; i < grades.length; i++) {{
                    div.innerHTML += '<div class="legend-item"><div class="legend-color" style="background:' + 
                        getColorChange(grades[i] + 1) + '"></div>' + labels[i] + '</div>';
                }}
                div.innerHTML += '<div class="legend-item"><div class="legend-color" style="background:' + 
                    getColorChange(-15) + '"></div>' + labels[6] + '</div>';
                return div;
            }};
            currentLegend.addTo(map);
        }}
        
        // Luo legenda trendianalyysille
        function createAnalysisLegend() {{
            currentLegend = L.control({{position: 'bottomright'}});
            currentLegend.onAdd = function(map) {{
                var div = L.DomUtil.create('div', 'legend');
                div.innerHTML = '<h4>5v trendi %</h4>';
                var grades = [15, 10, 5, 0, -5, -10];
                var labels = ['> 15%', '10% - 15%', '5% - 10%', '0% - 5%', '-5% - 0%', '-10% - -5%', '< -10%'];
                for (var i = 0; i < grades.length; i++) {{
                    div.innerHTML += '<div class="legend-item"><div class="legend-color" style="background:' + 
                        getColorTrend(grades[i] + 1) + '"></div>' + labels[i] + '</div>';
                }}
                div.innerHTML += '<div class="legend-item"><div class="legend-color" style="background:' + 
                    getColorTrend(-15) + '"></div>' + labels[6] + '</div>';
                return div;
            }};
            currentLegend.addTo(map);
        }}
        
        // Päivitä tilastot
        function updateStats() {{
            var mode = document.getElementById('view-mode-select').value;
            var buildingType = document.getElementById('building-type-select').value;
            var metric = document.getElementById('metric-select').value;
            var isPrice = (metric === 'keskihinta_aritm_nw');
            var isYield = (metric === 'vuokratuotto');
            var isRatio = (metric === 'hinta_tulot');
            var metricLabel = isPrice ? 'EUR/m²' : (isYield ? '%' : (isRatio ? 'v' : 'kpl'));
            
            if (mode === 'absolute') {{
                var selectedYear = document.getElementById('year-select').value;
                var values = [];
                
                geojsonData.features.forEach(function(feature) {{
                    if (isYield) {{
                        var yv = getVuokratuotto(feature, selectedYear, buildingType);
                        if (yv) values.push(yv);
                    }} else if (isRatio) {{
                        var rv = getHintaTuloSuhde(feature, selectedYear, buildingType);
                        if (rv) values.push(rv);
                    }} else {{
                        var value = getValue(feature, selectedYear, buildingType, metric);
                        if (value) values.push(value);
                    }}
                }});
                
                if (values.length > 0) {{
                    if (isRatio) {{
                        var avg = (values.reduce((a,b) => a + b, 0) / values.length).toFixed(1);
                        var max = Math.max(...values).toFixed(1);
                        var min = Math.min(...values).toFixed(1);
                        
                        document.getElementById('stat-label').textContent = 'Keskiarvo ' + selectedYear;
                        document.getElementById('stat-value').textContent = avg + ' v';
                        document.getElementById('stat-max-label').textContent = 'Kallein';
                        document.getElementById('stat-max').textContent = max + ' v';
                        document.getElementById('stat-min-label').textContent = 'Edullisin';
                        document.getElementById('stat-min').textContent = min + ' v';
                    }} else if (isYield) {{
                        var avg = (values.reduce((a,b) => a + b, 0) / values.length).toFixed(1);
                        var max = Math.max(...values).toFixed(1);
                        var min = Math.min(...values).toFixed(1);
                        
                        document.getElementById('stat-label').textContent = 'Keskituotto ' + selectedYear;
                        document.getElementById('stat-value').textContent = avg + ' %';
                        document.getElementById('stat-max-label').textContent = 'Korkein';
                        document.getElementById('stat-max').textContent = max + ' %';
                        document.getElementById('stat-min-label').textContent = 'Matalin';
                        document.getElementById('stat-min').textContent = min + ' %';
                    }} else {{
                    var avg = Math.round(values.reduce((a,b) => a + b, 0) / values.length);
                    var max = Math.max(...values);
                    var min = Math.min(...values);
                    
                    document.getElementById('stat-label').textContent = (isPrice ? 'Keskihinta ' : 'Keskiarvo ') + selectedYear;
                    document.getElementById('stat-value').textContent = avg.toLocaleString() + ' ' + metricLabel;
                    document.getElementById('stat-max-label').textContent = isPrice ? 'Kallein' : 'Suurin';
                    document.getElementById('stat-max').textContent = max.toLocaleString() + ' ' + metricLabel;
                    document.getElementById('stat-min-label').textContent = isPrice ? 'Halvin' : 'Pienin';
                    document.getElementById('stat-min').textContent = min.toLocaleString() + ' ' + metricLabel;
                    }}
                }}
            }} else {{
                var yearFrom = document.getElementById('year-from').value;
                var yearTo = document.getElementById('year-to').value;
                var changes = [];
                
                geojsonData.features.forEach(function(feature) {{
                    var valueFrom = getMetricValue(feature, yearFrom, buildingType, metric);
                    var valueTo = getMetricValue(feature, yearTo, buildingType, metric);
                    if (valueFrom && valueTo && valueFrom > 0) {{
                        var change = ((valueTo - valueFrom) / valueFrom) * 100;
                        changes.push(change);
                    }}
                }});
                
                if (changes.length > 0) {{
                    var avg = changes.reduce((a,b) => a + b, 0) / changes.length;
                    var max = Math.max(...changes);
                    var min = Math.min(...changes);
                    
                    document.getElementById('stat-label').textContent = 'Keskimuutos ' + yearFrom + '-' + yearTo;
                    document.getElementById('stat-value').textContent = (avg >= 0 ? '+' : '') + avg.toFixed(1) + ' %';
                    document.getElementById('stat-max-label').textContent = 'Suurin nousu';
                    document.getElementById('stat-max').textContent = '+' + max.toFixed(1) + ' %';
                    document.getElementById('stat-min-label').textContent = 'Suurin lasku';
                    document.getElementById('stat-min').textContent = min.toFixed(1) + ' %';
                }}
            }}
        }}
        
        // Hakutoiminto
        function filterMap() {{
            var query = document.getElementById('search').value.toLowerCase();
            
            geoJsonLayer.eachLayer(function(layer) {{
                var props = layer.feature.properties;
                var postcode = props.postinumer.toLowerCase();
                var name = props.name.toLowerCase();
                
                if (query === '' || postcode.includes(query) || name.includes(query)) {{
                    layer.setStyle({{opacity: 1, fillOpacity: 0.7}});
                }} else {{
                    layer.setStyle({{opacity: 0.1, fillOpacity: 0.1}});
                }}
            }});
        }}
        
        // Top 10 -paneeli
        var currentTop10Tab = 'kalleimmat';
        
        function toggleTop10Panel() {{
            var panel = document.getElementById('top10-panel');
            if (panel.style.display === 'block') {{
                closeTop10Panel();
            }} else {{
                panel.style.display = 'block';
                renderTop10List(currentTop10Tab);
            }}
        }}
        
        function closeTop10Panel() {{
            document.getElementById('top10-panel').style.display = 'none';
        }}
        
        function switchTop10Tab(el) {{
            document.querySelectorAll('.top10-tab').forEach(function(t) {{ t.classList.remove('active'); }});
            el.classList.add('active');
            currentTop10Tab = el.getAttribute('data-list');
            renderTop10List(currentTop10Tab);
        }}
        
        function getTop10Data(listType) {{
            var year = document.getElementById('year-select').value;
            var bt = document.getElementById('building-type-select').value;
            var items = [];
            
            geojsonData.features.forEach(function(feature) {{
                var props = feature.properties;
                var postcode = props.postinumer;
                var name = props.name;
                
                if (listType === 'kalleimmat' || listType === 'halvimmat') {{
                    var price = getValue(feature, year, bt, 'keskihinta_aritm_nw');
                    if (price) items.push({{ zip: postcode, name: name, value: price, label: price.toLocaleString() + ' \u20ac/m\u00b2', feature: feature }});
                }} else if (listType === 'nousseet' || listType === 'laskeneet') {{
                    var prevYear = (parseInt(year) - 5).toString();
                    var pFrom = getValue(feature, prevYear, bt, 'keskihinta_aritm_nw');
                    var pTo = getValue(feature, year, bt, 'keskihinta_aritm_nw');
                    if (pFrom && pTo && pFrom > 0) {{
                        var change = ((pTo - pFrom) / pFrom) * 100;
                        items.push({{ zip: postcode, name: name, value: change, label: (change >= 0 ? '+' : '') + change.toFixed(1) + ' %', feature: feature }});
                    }}
                }} else if (listType === 'tuotto') {{
                    var yv = getVuokratuotto(feature, year, bt);
                    if (yv) items.push({{ zip: postcode, name: name, value: yv, label: yv.toFixed(1) + ' %', feature: feature }});
                }} else if (listType === 'palvelut') {{
                    if (props.palvelut && props.palvelut.palveluindeksi > 0) {{
                        items.push({{ zip: postcode, name: name, value: props.palvelut.palveluindeksi, label: props.palvelut.palveluindeksi.toFixed(1), feature: feature }});
                    }}
                }}
            }});
            
            // Lajittelu
            if (listType === 'halvimmat' || listType === 'laskeneet') {{
                items.sort(function(a, b) {{ return a.value - b.value; }});
            }} else {{
                items.sort(function(a, b) {{ return b.value - a.value; }});
            }}
            
            return items.slice(0, 10);
        }}
        
        function renderTop10List(listType) {{
            var items = getTop10Data(listType);
            var titles = {{
                'kalleimmat': String.fromCodePoint(0x1F48E) + ' Kalleimmat alueet',
                'halvimmat': String.fromCodePoint(0x1F49A) + ' Halvimmat alueet',
                'nousseet': String.fromCodePoint(0x1F4C8) + ' Eniten nousseet (5v)',
                'laskeneet': String.fromCodePoint(0x1F4C9) + ' Eniten laskeneet (5v)',
                'tuotto': String.fromCodePoint(0x1F4B0) + ' Paras vuokratuotto',
                'palvelut': String.fromCodePoint(0x1F3EA) + ' Parhaat palvelut'
            }};
            var colorFns = {{
                'kalleimmat': function(v) {{ return getColorPrice(v); }},
                'halvimmat': function(v) {{ return getColorPrice(v); }},
                'nousseet': function(v) {{ return getColorChange(v); }},
                'laskeneet': function(v) {{ return getColorChange(v); }},
                'tuotto': function(v) {{ return getColorYield(v); }},
                'palvelut': function() {{ return '#f39c12'; }}
            }};
            
            var year = document.getElementById('year-select').value;
            var yearLabel = (listType === 'palvelut') ? 'OSM 2025' : year;
            var html = '<div style="padding: 5px 0 10px; font-size: 12px; color: #888;">' + titles[listType] + ' (' + yearLabel + ')</div>';
            
            if (items.length === 0) {{
                html += '<div style="text-align:center; padding: 30px; color: #999;">Ei dataa t\u00e4lle valinnalle</div>';
            }} else {{
                items.forEach(function(item, i) {{
                    var color = colorFns[listType](item.value);
                    var q = String.fromCharCode(39);
                    html += '<div class="top10-item" onclick="zoomToArea(' + q + item.zip + q + ')">' +
                        '<div class="top10-rank">' + (i + 1) + '.</div>' +
                        '<div class="top10-info"><span class="top10-zip">' + item.zip + '</span> <span class="top10-name">' + item.name + '</span></div>' +
                        '<div class="top10-value" style="color:' + color + '">' + item.label + '</div></div>';
                }});
            }}
            
            document.getElementById('top10-list').innerHTML = html;
        }}
        
        function zoomToArea(postcode) {{
            geoJsonLayer.eachLayer(function(layer) {{
                if (layer.feature.properties.postinumer === postcode) {{
                    map.fitBounds(layer.getBounds(), {{ maxZoom: 14 }});
                    if (isMobileDevice) {{
                        layer.fire('click');
                    }} else {{
                        layer.openPopup();
                    }}
                    selectedFeature = layer.feature;
                }}
            }});
            closeTop10Panel();
        }}
        
        // Paras alue -hakutyökalu
        var finderHighlightLayers = [];
        
        function toggleFinderPanel() {{
            var panel = document.getElementById('finder-panel');
            if (panel.style.display === 'block') {{
                closeFinderPanel();
            }} else {{
                panel.style.display = 'block';
            }}
        }}
        
        function closeFinderPanel() {{
            document.getElementById('finder-panel').style.display = 'none';
        }}
        
        function resetFinderSearch() {{
            document.getElementById('finder-kunta').value = 'all';
            document.getElementById('finder-building-type').value = '0';
            document.getElementById('finder-max-price').value = 4000;
            document.getElementById('finder-price-val').textContent = '4000 \u20ac/m\u00b2';
            document.getElementById('finder-min-pop').value = 0;
            document.getElementById('finder-pop-val').textContent = 'Ei rajoitusta';
            document.getElementById('finder-min-palvelu').value = 0;
            document.getElementById('finder-palvelu-val').textContent = 'Ei rajoitusta';
            document.getElementById('finder-kaupat').checked = false;
            document.getElementById('finder-koulut').checked = false;
            document.getElementById('finder-paivakodit').checked = false;
            document.getElementById('finder-liikunta').checked = false;
            document.getElementById('finder-terveys').checked = false;
            document.getElementById('finder-liikenne').checked = false;
            document.getElementById('finder-kirjastot').checked = false;
            document.getElementById('finder-apteekit').checked = false;
            document.getElementById('finder-max-matka').value = 0;
            document.getElementById('finder-matka-val').textContent = 'Ei rajoitusta';
            document.getElementById('finder-results').innerHTML = '';
            // Palauta kartan tyylit
            clearFinderHighlight();
        }}
        
        function clearFinderHighlight() {{
            if (geoJsonLayer) {{
                geoJsonLayer.eachLayer(function(layer) {{
                    geoJsonLayer.resetStyle(layer);
                }});
            }}
        }}
        
        function runFinderSearch() {{
            var kunta = document.getElementById('finder-kunta').value;
            var bt = document.getElementById('finder-building-type').value;
            var maxPrice = parseFloat(document.getElementById('finder-max-price').value);
            var minPop = parseInt(document.getElementById('finder-min-pop').value);
            var minPalvelu = parseFloat(document.getElementById('finder-min-palvelu').value);
            var maxMatka = parseInt(document.getElementById('finder-max-matka').value);
            
            var reqKaupat = document.getElementById('finder-kaupat').checked;
            var reqKoulut = document.getElementById('finder-koulut').checked;
            var reqPaivakodit = document.getElementById('finder-paivakodit').checked;
            var reqLiikunta = document.getElementById('finder-liikunta').checked;
            var reqTerveys = document.getElementById('finder-terveys').checked;
            var reqLiikenne = document.getElementById('finder-liikenne').checked;
            var reqKirjastot = document.getElementById('finder-kirjastot').checked;
            var reqApteekit = document.getElementById('finder-apteekit').checked;
            
            var year = document.getElementById('year-select').value;
            var results = [];
            
            geojsonData.features.forEach(function(feature) {{
                var props = feature.properties;
                
                // Kuntasuodatin
                if (kunta !== 'all' && props.city !== kunta) return;
                
                // Hintasuodatin
                var price = getValue(feature, year, bt, 'keskihinta_aritm_nw');
                if (!price || price > maxPrice) return;
                
                // Väkiluku
                var paavo = props.paavo;
                var pop = paavo ? (paavo.vaesto || 0) : 0;
                if (minPop > 0 && pop < minPop) return;
                
                // Palvelut
                var palvelut = props.palvelut || {{}};
                if (reqKaupat && (!palvelut.kaupat || palvelut.kaupat < 1)) return;
                if (reqKoulut && (!palvelut.koulut || palvelut.koulut < 1)) return;
                if (reqPaivakodit && (!palvelut.paivakodit || palvelut.paivakodit < 1)) return;
                if (reqLiikunta && (!palvelut.liikuntapaikat || palvelut.liikuntapaikat < 1)) return;
                if (reqTerveys && (!palvelut.terveysasemat || palvelut.terveysasemat < 1)) return;
                if (reqLiikenne && (!palvelut.julkinen_liikenne || palvelut.julkinen_liikenne < 1)) return;
                if (reqKirjastot && (!palvelut.kirjastot || palvelut.kirjastot < 1)) return;
                if (reqApteekit && (!palvelut.apteekit || palvelut.apteekit < 1)) return;
                
                // Palveluindeksi
                var pIdx = palvelut.palveluindeksi || 0;
                if (minPalvelu > 0 && pIdx < minPalvelu) return;
                
                // Matka-aika
                var matkaAika = props.matka_aika ? (props.matka_aika.matka_aika_min || 0) : 0;
                if (maxMatka > 0 && matkaAika > maxMatka) return;
                
                results.push({{
                    zip: props.postinumer,
                    name: props.name,
                    city: props.city || '',
                    price: price,
                    pop: pop,
                    palveluindeksi: pIdx,
                    matkaAika: matkaAika,
                    feature: feature
                }});
            }});
            
            // Järjestä ensin palveluindeksin, sitten halvimman hinnan mukaan
            results.sort(function(a, b) {{
                // Ensin palveluindeksin mukaan (paras ensin)
                if (b.palveluindeksi !== a.palveluindeksi) return b.palveluindeksi - a.palveluindeksi;
                // Sitten halvempi ensin
                return a.price - b.price;
            }});
            
            // Korosta sopivat alueet kartalla
            highlightFinderResults(results);
            
            // Näytä tulokset
            var html = '<div class="finder-results-header">' + results.length + ' sopivaa aluetta</div>';
            
            if (results.length === 0) {{
                html += '<div style="text-align:center; padding: 30px; color: #999;">Ei alueita n\u00e4ill\u00e4 suodattimilla.<br>Kokeile nostaa max-hintaa tai v\u00e4hent\u00e4\u00e4 palveluvaatimuksia.</div>';
            }} else {{
                var showCount = Math.min(results.length, 50);
                for (var i = 0; i < showCount; i++) {{
                    var r = results[i];
                    var q = String.fromCharCode(39);
                    html += '<div class="finder-result-item" onclick="zoomToFinderArea(' + q + r.zip + q + ')">' +
                        '<div class="finder-result-rank">' + (i + 1) + '.</div>' +
                        '<div class="finder-result-info">' +
                        '<span class="fr-zip">' + r.zip + '</span> <span class="fr-name">' + r.name + '</span>' +
                        '<div class="fr-city">' + r.city + (r.pop > 0 ? ' | ' + r.pop.toLocaleString() + ' as.' : '') + '</div>' +
                        '</div>' +
                        '<div class="finder-result-value">' +
                        '<div class="fr-price">' + r.price.toLocaleString() + ' \u20ac/m\u00b2</div>' +
                        '<div class="fr-services">' + (r.palveluindeksi > 0 ? '\u2b50 ' + r.palveluindeksi.toFixed(1) : '') + (r.matkaAika > 0 ? ' 🚌 ' + r.matkaAika + ' min' : '') + '</div>' +
                        '</div></div>';
                }}
                if (results.length > 50) {{
                    html += '<div style="text-align:center; padding: 10px; color: #888; font-size: 12px;">N\u00e4ytet\u00e4\u00e4n 50 / ' + results.length + ' tulosta</div>';
                }}
            }}
            
            document.getElementById('finder-results').innerHTML = html;
        }}
        
        function highlightFinderResults(results) {{
            var matchZips = {{}};
            results.forEach(function(r) {{ matchZips[r.zip] = true; }});
            
            geoJsonLayer.eachLayer(function(layer) {{
                var zip = layer.feature.properties.postinumer;
                if (matchZips[zip]) {{
                    layer.setStyle({{
                        fillColor: '#27ae60',
                        fillOpacity: 0.7,
                        color: '#1a7a42',
                        weight: 2,
                        opacity: 1
                    }});
                }} else {{
                    layer.setStyle({{
                        fillOpacity: 0.08,
                        opacity: 0.2,
                        weight: 0.5
                    }});
                }}
            }});
        }}
        
        function zoomToFinderArea(postcode) {{
            geoJsonLayer.eachLayer(function(layer) {{
                if (layer.feature.properties.postinumer === postcode) {{
                    map.fitBounds(layer.getBounds(), {{ maxZoom: 14 }});
                    if (isMobileDevice) {{
                        layer.fire('click');
                    }} else {{
                        layer.openPopup();
                    }}
                    selectedFeature = layer.feature;
                }}
            }});
        }}
        
        // Alusta kartta
        updateMap();
    </script>
</body>
</html>
'''

# Tallenna HTML
with open('kartta.html', 'w', encoding='utf-8') as f:
    f.write(html)

print(f"\n✅ Kartta luotu: kartta.html")
print(f"   Postinumeroalueita: {len(geojson_data['features'])}")
print(f"   Saatavilla vuodet: {', '.join(available_years)}")
print(f"   Ominaisuudet:")
print(f"   - Polygon-pohjaiset alueet")
print(f"   - Talotyypit: {', '.join(building_types.values())}")
print(f"   - Mittarit: Neliöhinnat ja kauppojen lukumäärät")
print(f"   - Absoluuttiset arvot ja vuosimuutokset")
