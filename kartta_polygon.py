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
        if paavo_aikasarja:
            viimeisin_vuosi = max(paavo_aikasarja.keys())
            feature['properties']['paavo'] = paavo_aikasarja[viimeisin_vuosi]
            feature['properties']['paavo_aikasarja'] = paavo_aikasarja
        else:
            feature['properties']['paavo'] = None
            feature['properties']['paavo_aikasarja'] = {}

# Luo JavaScript-muuttujat
years_json = json.dumps(available_years)
building_types_json = json.dumps(building_types)
geojson_json = json.dumps(geojson_data)
ennusteet_mallit_json = json.dumps(ennusteet_mallit)

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

html = f'''<!DOCTYPE html>
<html lang="fi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Asuntojen hintakartta 2009-{latest_year}</title>
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; }}
        
        #header {{
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            color: white;
            padding: 20px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.2);
        }}
        #header h1 {{ font-size: 24px; margin-bottom: 5px; }}
        #header p {{ opacity: 0.8; font-size: 14px; }}
        #header .forecast-note {{ opacity: 0.7; font-size: 12px; font-style: italic; margin-top: 5px; }}
        
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
        #controls input[type="radio"] {{
            margin-left: 10px;
            margin-right: 4px;
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
            .city-buttons {{
                display: none; /* Piilota pienillä näytöillä */
            }}
            #search-box {{
                top: 10px;
                right: 10px;
                left: auto;
            }}
        }}
    </style>
</head>
<body>
    <div id="header">
        <h1>🏠 Asuntojen hintakartta</h1>
        <p>Vanhat osakeasunnot 2009-2026 | Tilastokeskus</p>
        <p class="forecast-note">* Ennuste, laskettu viimeisen 5 vuoden trendin perusteella</p>
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
            </select>
        </div>
        
        <div class="control-group" id="forecast-model-selector" style="display:none;">
            <label for="forecast-model-select">Ennustemalli (2026*):</label>
            <select id="forecast-model-select" onchange="updateMap()">
                <option value="linear" selected>Lineaarinen</option>
                <option value="arima">ARIMA</option>
                <option value="exponential">Exp. Smoothing</option>
            </select>
        </div>
        
        <div class="control-group">
            <input type="radio" id="mode-absolute" name="mode" value="absolute" checked onchange="updateMap()">
            <label for="mode-absolute">Absoluuttinen</label>
            
            <input type="radio" id="mode-change" name="mode" value="change" onchange="updateMap()">
            <label for="mode-change">Muutos-%</label>
            
            <input type="radio" id="mode-analysis" name="mode" value="analysis" onchange="updateMap()">
            <label for="mode-analysis">Analyysi (5v trendi)</label>
            
            <input type="radio" id="mode-animation" name="mode" value="animation" onchange="updateMap()">
            <label for="mode-animation">Animaatio: Kartta</label>
            
            <input type="radio" id="mode-animation-chart" name="mode" value="animation-chart" onchange="updateMap()">
            <label for="mode-animation-chart">Animaatio: Diagrammi</label>
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
    
    <div id="map"></div>
    <div id="chart-container" style="display:none; position: absolute; top: 270px; left: 0; right: 0; bottom: 0; background: white; padding: 20px; overflow-y: auto; z-index: 1000;">
        <canvas id="bar-chart"></canvas>
    </div>
    
    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
    <script>
        var map = L.map('map').setView([60.1699, 24.9384], 8);
        
        L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png', {{
            attribution: '© OpenStreetMap contributors'
        }}).addTo(map);
        
        // GeoJSON data
        var geojsonData = {geojson_json};
        var availableYears = {years_json};
        var buildingTypes = {building_types_json};
        var ennusteetMallit = {ennusteet_mallit_json};  // Ennustemallit (linear, arima, exponential)
        var geoJsonLayer;
        var currentLegend;
        
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
        
        // Päivitä kartta
        function updateMap() {{
            var mode = document.querySelector('input[name="mode"]:checked').value;
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
                createAnalysisMap();
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
            var metric = 'keskihinta_aritm_nw';
            var city = document.getElementById('chart-city-select').value;
            createChartFrame(chartAnimationCurrentYear, buildingType, metric, city);
        }}
        
        // Luo absoluuttinen kartta
        function createAbsoluteMap(buildingType, metric) {{
            var selectedYear = document.getElementById('year-select').value;
            var isPrice = (metric === 'keskihinta_aritm_nw');
            
            geoJsonLayer = L.geoJSON(geojsonData, {{
                smoothFactor: 0,  // Ei geometrian yksinkertaistusta, tarkemmat rajat
                style: function(feature) {{
                    var value = getValue(feature, selectedYear, buildingType, metric);
                    var color = value ? (isPrice ? getColorPrice(value) : getColorTransactions(value)) : '#ccc';
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
                    var value = getValue(feature, selectedYear, buildingType, metric);
                    
                    var popupContent;
                    if (value) {{
                        var metricLabel = isPrice ? 'EUR/m²' : 'kpl';
                        popupContent = '<div class="popup-content">' +
                            '<h3>' + props.postinumer + '</h3>' +
                            '<div class="price">' + value.toLocaleString() + ' ' + metricLabel + '</div>' +
                            '<div class="details">' + props.name + '</div>' +
                            '<div class="details">' + selectedYear + ' | ' + buildingTypes[buildingType] + '</div>';
                        
                        // Lisää väestötiedot jos saatavilla
                        if (props.paavo_aikasarja) {{
                            // Paavo-data on -2v (pno_tilasto_2026 = 31.12.2024)
                            // Joten asuntohintavuoteen lisätään +2 kun haetaan väestötietoja
                            var targetPaavoVuosi = parseInt(selectedYear) + 2;
                            var vuodet = Object.keys(props.paavo_aikasarja).map(Number).sort((a, b) => b - a);
                            var maxPaavoVuosi = vuodet[0]; // Suurin saatavilla oleva vuosi
                            
                            if (props.paavo_aikasarja[targetPaavoVuosi]) {{
                                // Löytyi tarkka vuosi
                                var paavo = props.paavo_aikasarja[targetPaavoVuosi];
                                popupContent += '<div class="details" style="margin-top: 10px; border-top: 1px solid #ddd; padding-top: 5px;">' +
                                    '<strong>👥 Väestötiedot (' + selectedYear + '):</strong><br>' +
                                    'Asukkaat: ' + paavo.vaesto.toLocaleString() + '<br>' +
                                    'Keski-ikä: ' + paavo.keski_ika + ' v<br>' +
                                    'Keskitulo: ' + paavo.keskitulo.toLocaleString() + ' €/v<br>' +
                                    'Työttömyys: ' + paavo.tyottomyysaste.toFixed(1) + ' %<br>' +
                                    'Väestötiheys: ' + paavo.vaestotiheys.toFixed(0) + ' as/km²</div>';
                            }} else if (targetPaavoVuosi > maxPaavoVuosi) {{
                                // Tarvittava vuosi on tulevaisuudessa, ei vielä julkaistu
                                var julkaisuVuosi = targetPaavoVuosi; // pno_tilasto_XXXX julkaistaan vuonna XXXX
                                popupContent += '<div class="details" style="margin-top: 10px; border-top: 1px solid #ddd; padding-top: 5px;">' +
                                    '<strong>👥 Väestötiedot (' + selectedYear + '):</strong><br>' +
                                    '<em style="color: #999;">Tietoja ei ole vielä julkaistu<br>(julkaistaan arviolta ' + julkaisuVuosi + ')</em></div>';
                            }} else {{
                                // Käytetään lähintä vanhempaa dataa
                                var paavoVuosi = vuodet.find(v => v <= targetPaavoVuosi);
                                if (paavoVuosi && props.paavo_aikasarja[paavoVuosi]) {{
                                    var paavo = props.paavo_aikasarja[paavoVuosi];
                                    var naytettavaVuosi = paavoVuosi - 2; // Muunna takaisin asuntohintavuodeksi
                                    popupContent += '<div class="details" style="margin-top: 10px; border-top: 1px solid #ddd; padding-top: 5px;">' +
                                        '<strong>👥 Väestötiedot (' + naytettavaVuosi + '):</strong><br>' +
                                        'Asukkaat: ' + paavo.vaesto.toLocaleString() + '<br>' +
                                        'Keski-ikä: ' + paavo.keski_ika + ' v<br>' +
                                        'Keskitulo: ' + paavo.keskitulo.toLocaleString() + ' €/v<br>' +
                                        'Työttömyys: ' + paavo.tyottomyysaste.toFixed(1) + ' %<br>' +
                                        'Väestötiheys: ' + paavo.vaestotiheys.toFixed(0) + ' as/km²</div>';
                                }}
                            }}
                        }}
                        popupContent += '</div>';
                    }} else {{
                        popupContent = '<div class="popup-content">' +
                            '<h3>' + props.postinumer + '</h3>' +
                            '<div class="details">' + props.name + '</div>' +
                            '<div class="details" style="color: #999; font-style: italic;">Ei kauppoja (' + selectedYear + ' | ' + buildingTypes[buildingType] + ')</div>';
                        
                        // Lisää väestötiedot myös kun ei kauppoja
                        if (props.paavo_aikasarja) {{
                            // Paavo-data on -2v (pno_tilasto_2026 = 31.12.2024)
                            var targetPaavoVuosi = parseInt(selectedYear) + 2;
                            var vuodet = Object.keys(props.paavo_aikasarja).map(Number).sort((a, b) => b - a);
                            var maxPaavoVuosi = vuodet[0];
                            
                            if (props.paavo_aikasarja[targetPaavoVuosi]) {{
                                var paavo = props.paavo_aikasarja[targetPaavoVuosi];
                                popupContent += '<div class="details" style="margin-top: 10px; border-top: 1px solid #ddd; padding-top: 5px;">' +
                                    '<strong>👥 Väestötiedot (' + selectedYear + '):</strong><br>' +
                                    'Asukkaat: ' + paavo.vaesto.toLocaleString() + '<br>' +
                                    'Keski-ikä: ' + paavo.keski_ika + ' v<br>' +
                                    'Keskitulo: ' + paavo.keskitulo.toLocaleString() + ' €/v<br>' +
                                    'Työttömyys: ' + paavo.tyottomyysaste.toFixed(1) + ' %<br>' +
                                    'Väestötiheys: ' + paavo.vaestotiheys.toFixed(0) + ' as/km²</div>';
                            }} else if (targetPaavoVuosi > maxPaavoVuosi) {{
                                var julkaisuVuosi = targetPaavoVuosi;
                                popupContent += '<div class="details" style="margin-top: 10px; border-top: 1px solid #ddd; padding-top: 5px;">' +
                                    '<strong>👥 Väestötiedot (' + selectedYear + '):</strong><br>' +
                                    '<em style="color: #999;">Tietoja ei ole vielä julkaistu<br>(julkaistaan arviolta ' + julkaisuVuosi + ')</em></div>';
                            }} else {{
                                var paavoVuosi = vuodet.find(v => v <= targetPaavoVuosi);
                                if (paavoVuosi && props.paavo_aikasarja[paavoVuosi]) {{
                                    var paavo = props.paavo_aikasarja[paavoVuosi];
                                    var naytettavaVuosi = paavoVuosi - 2;
                                    popupContent += '<div class="details" style="margin-top: 10px; border-top: 1px solid #ddd; padding-top: 5px;">' +
                                        '<strong>👥 Väestötiedot (' + naytettavaVuosi + '):</strong><br>' +
                                        'Asukkaat: ' + paavo.vaesto.toLocaleString() + '<br>' +
                                        'Keski-ikä: ' + paavo.keski_ika + ' v<br>' +
                                        'Keskitulo: ' + paavo.keskitulo.toLocaleString() + ' €/v<br>' +
                                        'Työttömyys: ' + paavo.tyottomyysaste.toFixed(1) + ' %<br>' +
                                        'Väestötiheys: ' + paavo.vaestotiheys.toFixed(0) + ' as/km²</div>';
                                }}
                            }}
                        }}
                        popupContent += '</div>';
                    }}
                    layer.bindPopup(popupContent);
                    
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
                    var valueFrom = getValue(feature, yearFrom, buildingType, metric);
                    var valueTo = getValue(feature, yearTo, buildingType, metric);
                    
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
                    var valueFrom = getValue(feature, yearFrom, buildingType, metric);
                    var valueTo = getValue(feature, yearTo, buildingType, metric);
                    
                    var popupContent;
                    if (valueFrom && valueTo && valueFrom > 0) {{
                        var change = ((valueTo - valueFrom) / valueFrom) * 100;
                        var absChange = valueTo - valueFrom;
                        var changeSign = change >= 0 ? '+' : '';
                        var isPrice = (metric === 'keskihinta_aritm_nw');
                        var metricLabel = isPrice ? 'EUR/m²' : 'kpl';
                        
                        popupContent = '<div class="popup-content">' +
                            '<h3>' + props.postinumer + '</h3>' +
                            '<div class="price">' + changeSign + change.toFixed(1) + ' %</div>' +
                            '<div class="details">' + props.name + '</div>' +
                            '<div class="details">' + yearFrom + ': ' + valueFrom.toLocaleString() + ' ' + metricLabel + '<br>' +
                            yearTo + ': ' + valueTo.toLocaleString() + ' ' + metricLabel + '<br>' +
                            'Muutos: ' + changeSign + absChange.toLocaleString() + ' ' + metricLabel + '</div>' +
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
                    layer.bindPopup(popupContent);
                    
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
        function createAnalysisMap() {{
            geoJsonLayer = L.geoJSON(geojsonData, {{
                smoothFactor: 0,
                style: function(feature) {{
                    var analyysi = feature.properties.analyysi;
                    
                    if (analyysi && analyysi.hinta_muutos_5v !== null && analyysi.hinta_muutos_5v !== undefined) {{
                        return {{
                            fillColor: getColorTrend(analyysi.hinta_muutos_5v),
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
                    var analyysi = props.analyysi;
                    
                    var popupContent;
                    if (analyysi && analyysi.hinta_muutos_5v !== null && analyysi.hinta_muutos_5v !== undefined) {{
                        var changeSign = analyysi.hinta_muutos_5v >= 0 ? '+' : '';
                        var trendiEmoji = analyysi.trendi === 'nouseva' ? '📈' : 
                                         analyysi.trendi === 'laskeva' ? '📉' : '📊';
                        var aktiivisuusEmoji = analyysi.aktiivisuus === 'korkea' ? '🔥' : 
                                              analyysi.aktiivisuus === 'keskitaso' ? '▪️' : '❄️';
                        
                        popupContent = '<div class="popup-content">' +
                            '<h3>' + props.postinumer + '</h3>' +
                            '<div class="price">' + changeSign + analyysi.hinta_muutos_5v.toFixed(1) + ' %</div>' +
                            '<div class="details">' + props.name + '</div>' +
                            '<div class="details" style="margin-top: 10px;">' +
                            '<strong>🏠 Asuntohinnat (2021-2025)</strong><br>' +
                            trendiEmoji + ' ' + analyysi.trendi.charAt(0).toUpperCase() + analyysi.trendi.slice(1) + '<br>' +
                            '📊 Kauppoja: ' + analyysi.keskim_kaupat_vuosi.toFixed(1) + ' / vuosi<br>' +
                            aktiivisuusEmoji + ' Aktiivisuus: ' + analyysi.aktiivisuus + '<br>' +
                            '📈 Volatiliteetti: ' + analyysi.volatiliteetti.toFixed(1) + ' %</div>';
                        
                        // Lisää väestötietojen muutokset 5v ajalta
                        if (props.paavo_aikasarja) {{
                            // Laske muutokset: 2021 -> 2025 (Paavo 2023 -> 2027, mutta käytä saatavilla olevaa)
                            var paavoAlku = 2023; // 2021 + 2
                            var paavoLoppu = 2027; // 2025 + 2
                            var vuodet = Object.keys(props.paavo_aikasarja).map(Number).sort();
                            
                            // Etsi lähimmät saatavilla olevat vuodet
                            var alkuVuosi = vuodet.find(v => v >= paavoAlku) || vuodet[vuodet.length - 1];
                            var loppuVuosi = vuodet[vuodet.length - 1]; // Viimeisin saatavilla
                            
                            if (props.paavo_aikasarja[alkuVuosi] && props.paavo_aikasarja[loppuVuosi] && alkuVuosi !== loppuVuosi) {{
                                var paavoAlkuData = props.paavo_aikasarja[alkuVuosi];
                                var paavoLoppuData = props.paavo_aikasarja[loppuVuosi];
                                
                                // Laske muutokset
                                var vaestoMuutos = ((paavoLoppuData.vaesto - paavoAlkuData.vaesto) / paavoAlkuData.vaesto * 100);
                                var ikaMuutos = paavoLoppuData.keski_ika - paavoAlkuData.keski_ika;
                                var tuloMuutos = ((paavoLoppuData.keskitulo - paavoAlkuData.keskitulo) / paavoAlkuData.keskitulo * 100);
                                var tyottomyysMuutos = paavoLoppuData.tyottomyysaste - paavoAlkuData.tyottomyysaste;
                                
                                var vaestoSign = vaestoMuutos >= 0 ? '+' : '';
                                var ikaSign = ikaMuutos >= 0 ? '+' : '';
                                var tuloSign = tuloMuutos >= 0 ? '+' : '';
                                var tyottomyysSign = tyottomyysMuutos >= 0 ? '+' : '';
                                
                                var naytettavaAlku = alkuVuosi - 2;
                                var naytettavaLoppu = loppuVuosi - 2;
                                
                                popupContent += '<div class="details" style="margin-top: 10px; border-top: 1px solid #ddd; padding-top: 5px;">' +
                                    '<strong>👥 Väestömuutokset (' + naytettavaAlku + '-' + naytettavaLoppu + ')</strong><br>' +
                                    'Asukkaat: ' + vaestoSign + vaestoMuutos.toFixed(1) + ' %<br>' +
                                    'Keski-ikä: ' + ikaSign + ikaMuutos.toFixed(1) + ' v<br>' +
                                    'Keskitulo: ' + tuloSign + tuloMuutos.toFixed(1) + ' %<br>' +
                                    'Työttömyys: ' + tyottomyysSign + tyottomyysMuutos.toFixed(1) + ' %-yks</div>';
                            }}
                        }}
                        
                        popupContent += '</div>';
                    }} else {{
                        popupContent = '<div class="popup-content">' +
                            '<h3>' + props.postinumer + '</h3>' +
                            '<div class="details">' + props.name + '</div>' +
                            '<div class="details" style="color: #999; font-style: italic;">Ei riittävästi dataa trendianalyysiin</div>' +
                            '</div>';
                    }}
                    layer.bindPopup(popupContent);
                    
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
            var isPrice = (metric === 'keskihinta_aritm_nw');
            
            geoJsonLayer = L.geoJSON(geojsonData, {{
                smoothFactor: 0,
                style: function(feature) {{
                    var value = getValue(feature, year, buildingType, metric);
                    var color = value ? (isPrice ? getColorPrice(value) : getColorTransactions(value)) : '#ccc';
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
                    var value = getValue(feature, year, buildingType, metric);
                    
                    if (value) {{
                        var metricLabel = isPrice ? 'EUR/m²' : 'kpl';
                        var popupContent = '<div class="popup-content">' +
                            '<h3>' + props.postinumer + '</h3>' +
                            '<div class="price">' + value.toLocaleString() + ' ' + metricLabel + '</div>' +
                            '<div class="details">' + props.name + '</div>' +
                            '<div class="details">' + year + (year == 2026 ? '*' : '') + ' | ' + buildingTypes[buildingType] + '</div>' +
                            '</div>';
                        layer.bindPopup(popupContent);
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
                var value = getValue(feature, year, buildingType, metric);
                
                if (value && metric === 'keskihinta_aritm_nw') {{ // Vain neliöhinnalle
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
            
            // Järjestä hinnan mukaan laskevasti ja ota top 10
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
            var html = '<div style="max-width: 1200px; margin: 0 auto;">';
            html += '<h2 style="text-align: center; margin-bottom: 10px;">Top 10 Kalleimmat Postinumeroalueet - ' + year + (year == 2026 ? '*' : '') + '</h2>';
            html += '<div style="font-size: 16px; color: #1e3c72; text-align: center; margin-bottom: 10px; font-weight: bold;">' + cityName + '</div>';
            html += '<div style="font-size: 14px; color: #666; text-align: center; margin-bottom: 20px;">Huoneistotyyppi: ' + buildingTypes[buildingType] + '</div>';
            
            top10.forEach(function(area, index) {{
                var percentage = (area.hinta / maxPrice) * 100;
                var barColor;
                
                // Värikoodaus kuten kartassa
                if (area.hinta > 8000) barColor = '#8B0000';
                else if (area.hinta > 6000) barColor = '#e74c3c';
                else if (area.hinta > 5000) barColor = '#f39c12';
                else if (area.hinta > 4000) barColor = '#f1c40f';
                else if (area.hinta > 3000) barColor = '#9acd32';
                else if (area.hinta > 2000) barColor = '#27ae60';
                else barColor = '#2ecc71';
                
                html += '<div style="margin-bottom: 20px;">';
                html += '<div style="display: flex; align-items: center; margin-bottom: 5px;">';
                html += '<div style="width: 60px; font-weight: bold; color: #333;">' + (index + 1) + '.</div>';
                html += '<div style="width: 120px; font-weight: bold; color: #1e3c72;">' + area.postinumero + '</div>';
                html += '<div style="flex: 1; color: #666; font-size: 14px;">' + area.nimi + '</div>';
                html += '<div style="width: 120px; text-align: right; font-weight: bold; color: ' + barColor + ';">' + area.hinta.toLocaleString() + ' €/m²</div>';
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
            var metric = 'keskihinta_aritm_nw'; // Aina neliöhinta diagrammille
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
            var mode = document.querySelector('input[name="mode"]:checked').value;
            var buildingType = document.getElementById('building-type-select').value;
            var metric = document.getElementById('metric-select').value;
            var isPrice = (metric === 'keskihinta_aritm_nw');
            var metricLabel = isPrice ? 'EUR/m²' : 'kpl';
            
            if (mode === 'absolute') {{
                var selectedYear = document.getElementById('year-select').value;
                var values = [];
                
                geojsonData.features.forEach(function(feature) {{
                    var value = getValue(feature, selectedYear, buildingType, metric);
                    if (value) values.push(value);
                }});
                
                if (values.length > 0) {{
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
            }} else {{
                var yearFrom = document.getElementById('year-from').value;
                var yearTo = document.getElementById('year-to').value;
                var changes = [];
                
                geojsonData.features.forEach(function(feature) {{
                    var valueFrom = getValue(feature, yearFrom, buildingType, metric);
                    var valueTo = getValue(feature, yearTo, buildingType, metric);
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
