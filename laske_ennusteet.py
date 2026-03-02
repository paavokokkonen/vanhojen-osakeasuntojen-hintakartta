#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Laskee asuntohintojen ennusteet useilla eri malleilla vuodelle 2026.

Mallit:
1. Linear - Yksinkertainen lineaarinen trendi (5 vuoden keskiarvo)
2. ARIMA - AutoRegressive Integrated Moving Average
3. ExponentialSmoothing - Holt's exponential smoothing with trend

Tallennetaan tulokset data/ennusteet_mallit.json
"""

import json
import numpy as np
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

# Yritä tuoda statsmodels, mutta jatka ilman sitä jos ei ole asennettuna
try:
    from statsmodels.tsa.holtwinters import SimpleExpSmoothing
    from statsmodels.tsa.arima.model import ARIMA
    HAS_STATSMODELS = True
except ImportError:
    print("⚠️  statsmodels ei ole asennettu. Käytetään vain lineaarista mallia.")
    print("   Asenna: pip install statsmodels")
    HAS_STATSMODELS = False


def calculate_linear_forecast(years, values):
    """Lineaarinen trendi - yksinkertainen keskiarvon muutos"""
    if len(values) < 2:
        return None
    
    # Laske keskimääräinen vuosimuutos
    changes = [values[i] - values[i-1] for i in range(1, len(values))]
    avg_change = sum(changes) / len(changes)
    forecast = values[-1] + avg_change
    
    return max(0, forecast)


def calculate_arima_forecast(years, values):
    """ARIMA(1,1,1) - autoregressive integrated moving average"""
    if not HAS_STATSMODELS or len(values) < 5:
        return None
    
    try:
        # ARIMA(1,1,1) - yksinkertainen malli joka toimii useimmilla aikasarjoilla
        model = ARIMA(values, order=(1, 1, 1))
        fitted_model = model.fit()
        forecast = fitted_model.forecast(steps=1)[0]
        return max(0, float(forecast))
    except:
        # Jos ARIMA epäonnistuu, palauta None
        return None


def calculate_exponential_smoothing_forecast(years, values):
    """Exponential Smoothing - Holt's method with trend"""
    if not HAS_STATSMODELS or len(values) < 3:
        return None
    
    try:
        # Yksinkertainen exponential smoothing
        model = SimpleExpSmoothing(values)
        fitted_model = model.fit()
        forecast = fitted_model.forecast(steps=1)[0]
        return max(0, float(forecast))
    except:
        return None


def calculate_all_forecasts(data, available_years, forecast_year='2026'):
    """
    Laske ennusteet kaikilla malleilla.
    
    Returns:
        dict: Postinumero -> talotyyppi -> malli -> ennuste
    """
    print(f"\n📊 Lasketaan ennusteet vuodelle {forecast_year}...")
    print(f"   Käytettävissä mallit: Linear, ", end="")
    if HAS_STATSMODELS:
        print("ARIMA, ExponentialSmoothing")
    else:
        print("(ARIMA ja ExponentialSmoothing vaativat statsmodels-kirjaston)")
    
    # Käytä viimeisiä 5-10 vuotta ennusteeseen
    recent_years = sorted([y for y in available_years if int(y) >= 2017])[-10:]
    
    results = {}
    total_areas = len(data)
    processed = 0
    
    for postcode, info in data.items():
        years_data = info.get('data', {})
        results[postcode] = {}
        
        # Käy läpi kaikki talotyypit
        for building_type in ['0', '1', '2', '3', '5']:  # Lisätään '0' = Kaikki
            # Kerää historiallinen data
            historical_prices = []
            historical_transactions = []
            
            for year in recent_years:
                if year in years_data and building_type in years_data[year]:
                    year_data = years_data[year][building_type]
                    if 'keskihinta_aritm_nw' in year_data and year_data['keskihinta_aritm_nw'] is not None:
                        historical_prices.append((int(year), year_data['keskihinta_aritm_nw']))
                    if 'lkm_julk20' in year_data and year_data['lkm_julk20'] is not None:
                        historical_transactions.append((int(year), year_data['lkm_julk20']))
            
            # Laske ennusteet jos tarpeeksi dataa
            if len(historical_prices) >= 3:
                years = [y[0] for y in historical_prices]
                prices = [y[1] for y in historical_prices]
                
                forecasts = {}
                
                # Linear forecast
                linear_price = calculate_linear_forecast(years, prices)
                if linear_price is not None:
                    forecasts['linear'] = {
                        'keskihinta_aritm_nw': round(linear_price, 2)
                    }
                
                # ARIMA forecast
                if HAS_STATSMODELS:
                    arima_price = calculate_arima_forecast(years, prices)
                    if arima_price is not None:
                        forecasts['arima'] = {
                            'keskihinta_aritm_nw': round(arima_price, 2)
                        }
                    
                    # Exponential Smoothing forecast
                    exp_price = calculate_exponential_smoothing_forecast(years, prices)
                    if exp_price is not None:
                        forecasts['exponential'] = {
                            'keskihinta_aritm_nw': round(exp_price, 2)
                        }
                
                # Tallenna jos jotain ennusteita saatiin
                if forecasts:
                    results[postcode][building_type] = forecasts
        
        processed += 1
        if processed % 100 == 0:
            print(f"   Käsitelty {processed}/{total_areas} aluetta...")
    
    # Laske tilastot
    linear_count = sum(1 for pc in results.values() for bt in pc.values() if 'linear' in bt)
    arima_count = sum(1 for pc in results.values() for bt in pc.values() if 'arima' in bt)
    exp_count = sum(1 for pc in results.values() for bt in pc.values() if 'exponential' in bt)
    
    print(f"\n✅ Ennusteet laskettu:")
    print(f"   Linear: {linear_count} ennustetta")
    if HAS_STATSMODELS:
        print(f"   ARIMA: {arima_count} ennustetta")
        print(f"   ExponentialSmoothing: {exp_count} ennustetta")
    
    return results


def main():
    print("=" * 70)
    print("ASUNTOHINTOJEN ENNUSTEMALLIT")
    print("=" * 70)
    
    # Lataa asuntohintadata
    print("\n📂 Ladataan asuntohintadataa...")
    try:
        with open('asuntohinnat.json', 'r', encoding='utf-8') as f:
            json_data = json.load(f)
            asunto_data = json_data.get('data', {})
            metadata = json_data.get('metadata', {})
    except FileNotFoundError:
        print("❌ Virhe: asuntohinnat.json ei löydy!")
        print("   Aja ensin: python asuntohinnat.py")
        return
    
    # Hae käytettävissä olevat vuodet metadatasta
    available_years = [y for y in metadata.get('years', []) if y != '2026']  # Poista ennustevuosi
    
    if not available_years:
        print("❌ Virhe: Ei historiallista dataa!")
        return
    
    print(f"   Käytettävissä vuodet: {min(available_years)}-{max(available_years)}")
    print(f"   Yhteensä {len(asunto_data)} postinumeroaluetta")
    
    # Laske ennusteet
    forecasts = calculate_all_forecasts(asunto_data, available_years, forecast_year='2026')
    
    # Tallenna tulokset
    output_file = 'data/ennusteet_mallit.json'
    print(f"\n💾 Tallennetaan tulokset: {output_file}")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(forecasts, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ Valmis! Ennusteet tallennettu tiedostoon {output_file}")
    print("\nSeuraava vaihe: Päivitä kartta komennolla: python kartta_polygon.py")


if __name__ == '__main__':
    main()
