#!/usr/bin/env python3
"""
Rikasta asuntohintadata väestötiedoilla ja palveluilla
=======================================================
Hakee:
- Paavo-väestötiedot (Tilastokeskus)
- Etäisyydet keskustoihin
- Palvelut (OSM Geofabrik data, parsitaan paikallisesti)
"""

import requests
import json
import time
import os
import math
from xml.etree import ElementTree as ET
from shapely.geometry import shape, Point
from shapely.ops import nearest_points
import math

try:
    import osmium
    OSMIUM_AVAILABLE = True
except ImportError:
    OSMIUM_AVAILABLE = False
    print("[WARNING] osmium ei asennettu. Palvelutietojen haku ohitetaan.")
    print("   Asenna: pip install osmium")

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
                        
                        # Tallenna vuoden tiedot — kaikki Paavo-kentät
                        vuosi_data = {
                            # --- Perustiedot (HE) ---
                            'vaesto': props.get('he_vakiy') or 0,
                            'keski_ika': props.get('he_kika') or 0,
                            'miehet': props.get('he_miehet') or 0,
                            'naiset': props.get('he_naiset') or 0,
                            # Ikäjakauma (20 ikäryhmää)
                            'ika_0_2': props.get('he_0_2') or 0,
                            'ika_3_6': props.get('he_3_6') or 0,
                            'ika_7_12': props.get('he_7_12') or 0,
                            'ika_13_15': props.get('he_13_15') or 0,
                            'ika_16_17': props.get('he_16_17') or 0,
                            'ika_18_19': props.get('he_18_19') or 0,
                            'ika_20_24': props.get('he_20_24') or 0,
                            'ika_25_29': props.get('he_25_29') or 0,
                            'ika_30_34': props.get('he_30_34') or 0,
                            'ika_35_39': props.get('he_35_39') or 0,
                            'ika_40_44': props.get('he_40_44') or 0,
                            'ika_45_49': props.get('he_45_49') or 0,
                            'ika_50_54': props.get('he_50_54') or 0,
                            'ika_55_59': props.get('he_55_59') or 0,
                            'ika_60_64': props.get('he_60_64') or 0,
                            'ika_65_69': props.get('he_65_69') or 0,
                            'ika_70_74': props.get('he_70_74') or 0,
                            'ika_75_79': props.get('he_75_79') or 0,
                            'ika_80_84': props.get('he_80_84') or 0,
                            'ika_85_': props.get('he_85_') or 0,
                            
                            # --- Pääasiallinen toiminta (PT) ---
                            'tyolliset': props.get('pt_tyoll') or 0,
                            'tyottomat': props.get('pt_tyott') or 0,
                            'elakelaiset': props.get('pt_elakel') or 0,
                            'opiskelijat': props.get('pt_opisk') or 0,
                            'pt_muut': props.get('pt_muut') or 0,
                            'pt_0_14': props.get('pt_0_14') or 0,
                            
                            # --- Asukkaiden tulot (HR) ---
                            'keskitulo': props.get('hr_mtu') or 0,  # Mediaanitulot
                            'hr_ktu': props.get('hr_ktu') or 0,  # Keskitulot
                            'hr_pi_tul': props.get('hr_pi_tul') or 0,  # Pienituloiset
                            'hr_ke_tul': props.get('hr_ke_tul') or 0,  # Keskituloiset
                            'hr_hy_tul': props.get('hr_hy_tul') or 0,  # Hyvätuloiset
                            'hr_ovy': props.get('hr_ovy') or 0,  # Tulot yhteensä
                            
                            # --- Talouksien tulot (TR) ---
                            'tr_mtu': props.get('tr_mtu') or 0,  # Talouksien mediaanitulot
                            'tr_ktu': props.get('tr_ktu') or 0,  # Talouksien keskitulot
                            'tr_pi_tul': props.get('tr_pi_tul') or 0,
                            'tr_ke_tul': props.get('tr_ke_tul') or 0,
                            'tr_hy_tul': props.get('tr_hy_tul') or 0,
                            
                            # --- Koulutusaste (KO) ---
                            'koulutustaso': props.get('ko_ika18y') or 0,  # 18+ asukkaat
                            'ko_perus': props.get('ko_perus') or 0,  # Perusaste
                            'ko_ammat': props.get('ko_ammat') or 0,  # Ammattikoulutus
                            'ko_al_kork': props.get('ko_al_kork') or 0,  # Alempi korkeakoulu
                            'ko_yl_kork': props.get('ko_yl_kork') or 0,  # Ylempi korkeakoulu
                            'ko_yliop': props.get('ko_yliop') or 0,  # Tutkijakoulutus
                            
                            # --- Taloudet (TE) ---
                            'asuntokuntia': props.get('te_as_valj') or 0,  # Asumisväljyys m²/hlö
                            'te_taly': props.get('te_taly') or 0,  # Talouksia yhteensä
                            'te_yks': props.get('te_yks') or 0,  # Yksinasuvat
                            'te_nuor': props.get('te_nuor') or 0,  # Nuoret
                            'te_laps': props.get('te_laps') or 0,  # Lapsiperheet
                            'te_klap': props.get('te_klap') or 0,  # Kouluikäisten lapsiperheet
                            'te_aklap': props.get('te_aklap') or 0,  # Aikuisten lapsiperheet
                            'te_elak': props.get('te_elak') or 0,  # Eläkeläistaloudet
                            'te_omis_as': props.get('te_omis_as') or 0,  # Omistusasunnot
                            'te_vuok_as': props.get('te_vuok_as') or 0,  # Vuokra-asunnot
                            'te_muu_as': props.get('te_muu_as') or 0,  # Muu hallintamuoto
                            'te_takk': props.get('te_takk') or 0,  # Talouden keskikoko
                            
                            # --- Rakennukset ja asunnot (RA) ---
                            'ra_raky': props.get('ra_raky') or 0,  # Rakennuksia yhteensä
                            'ra_asrak': props.get('ra_asrak') or 0,  # Asuinrakennuksia
                            'ra_asunn': props.get('ra_asunn') or 0,  # Asuntoja yhteensä
                            'ra_kt_as': props.get('ra_kt_as') or 0,  # Kerrostaloasuntoja
                            'ra_pt_as': props.get('ra_pt_as') or 0,  # Pientaloasuntoja
                            'ra_muu_as': props.get('ra_muu_as') or 0,  # Muita asuntoja
                            'ra_ke': props.get('ra_ke') or 0,  # Kesämökkejä
                            'ra_as_kpa': props.get('ra_as_kpa') or 0,  # Asuntojen keskipinta-ala m²
                            
                            # --- Työpaikat toimialoittain (TP) ---
                            'tp_tyopy': props.get('tp_tyopy') or 0,  # Työpaikkoja yhteensä
                            'tp_alku_a': props.get('tp_alku_a') or 0,  # A Alkutuotanto
                            'tp_b_kaiv': props.get('tp_b_kaiv') or 0,  # B Kaivostoiminta
                            'tp_c_teol': props.get('tp_c_teol') or 0,  # C Teollisuus
                            'tp_d_ener': props.get('tp_d_ener') or 0,  # D Energia
                            'tp_e_vesi': props.get('tp_e_vesi') or 0,  # E Vesihuolto
                            'tp_f_rake': props.get('tp_f_rake') or 0,  # F Rakentaminen
                            'tp_g_kaup': props.get('tp_g_kaup') or 0,  # G Kauppa
                            'tp_h_kulj': props.get('tp_h_kulj') or 0,  # H Kuljetus
                            'tp_i_majo': props.get('tp_i_majo') or 0,  # I Majoitus/ravintola
                            'tp_j_info': props.get('tp_j_info') or 0,  # J ICT
                            'tp_k_raho': props.get('tp_k_raho') or 0,  # K Rahoitus
                            'tp_l_kiin': props.get('tp_l_kiin') or 0,  # L Kiinteistö
                            'tp_m_erik': props.get('tp_m_erik') or 0,  # M Erikoispalvelut
                            'tp_n_hall': props.get('tp_n_hall') or 0,  # N Hallinto/tukipalvelut
                            'tp_o_julk': props.get('tp_o_julk') or 0,  # O Julkinen hallinto
                            'tp_p_koul': props.get('tp_p_koul') or 0,  # P Koulutus
                            'tp_q_terv': props.get('tp_q_terv') or 0,  # Q Terveys/sosiaali
                            'tp_r_taid': props.get('tp_r_taid') or 0,  # R Taide/viihde
                            'tp_s_muup': props.get('tp_s_muup') or 0,  # S Muu palvelu
                            'tp_t_koti': props.get('tp_t_koti') or 0,  # T Kotitaloustyö
                            'tp_u_kvli': props.get('tp_u_kvli') or 0,  # U Kansainväliset
                            'tp_x_tunt': props.get('tp_x_tunt') or 0,  # X Tuntematon
                        }
                        
                        paavo_dict[postinumero][str(vuosi)] = vuosi_data
                        
                        # Laske johdannaismuuttujat
                        
                        # Työttömyysaste
                        tyossa = vuosi_data['tyolliset'] + vuosi_data['tyottomat']
                        if tyossa > 0:
                            vuosi_data['tyottomyysaste'] = (vuosi_data['tyottomat'] / tyossa * 100)
                        else:
                            vuosi_data['tyottomyysaste'] = 0
                        
                        # Väestötiheys (per km²)
                        pinta_ala_km2 = (props.get('pinta_ala') or 0) / 1_000_000
                        if pinta_ala_km2 > 0:
                            vuosi_data['vaestotiheys'] = (vuosi_data['vaesto'] / pinta_ala_km2)
                        else:
                            vuosi_data['vaestotiheys'] = 0
                        
                        # Lapsiperheystävällisyys (0-17v osuus väestöstä %)
                        if vuosi_data['vaesto'] > 0:
                            lapset = (vuosi_data['ika_0_2'] + vuosi_data['ika_3_6'] + 
                                     vuosi_data['ika_7_12'] + vuosi_data['ika_13_15'] + 
                                     vuosi_data['ika_16_17'])
                            vuosi_data['lapset_osuus'] = round(lapset / vuosi_data['vaesto'] * 100, 1)
                            tyoikaiset = sum(vuosi_data.get(f'ika_{a}_{b}', 0) 
                                           for a, b in [(18,19),(20,24),(25,29),(30,34),(35,39),
                                                        (40,44),(45,49),(50,54),(55,59),(60,64)])
                            vuosi_data['tyoikaiset_osuus'] = round(tyoikaiset / vuosi_data['vaesto'] * 100, 1)
                            elakelaiset_ika = (vuosi_data['ika_65_69'] + vuosi_data['ika_70_74'] + 
                                              vuosi_data['ika_75_79'] + vuosi_data['ika_80_84'] + 
                                              vuosi_data['ika_85_'])
                            vuosi_data['elakeikaiset_osuus'] = round(elakelaiset_ika / vuosi_data['vaesto'] * 100, 1)
                        else:
                            vuosi_data['lapset_osuus'] = 0
                            vuosi_data['tyoikaiset_osuus'] = 0
                            vuosi_data['elakeikaiset_osuus'] = 0
                        
                        # Omistusaste (% talouksista)
                        te_total = vuosi_data['te_omis_as'] + vuosi_data['te_vuok_as'] + vuosi_data['te_muu_as']
                        if te_total > 0:
                            vuosi_data['omistusaste'] = round(vuosi_data['te_omis_as'] / te_total * 100, 1)
                            vuosi_data['vuokra_aste'] = round(vuosi_data['te_vuok_as'] / te_total * 100, 1)
                        else:
                            vuosi_data['omistusaste'] = 0
                            vuosi_data['vuokra_aste'] = 0
                        
                        # Koulutusrakenne (% 18+ väestöstä)
                        ko_total = vuosi_data['koulutustaso']  # ko_ika18y
                        if ko_total > 0:
                            vuosi_data['korkeakoulutetut_osuus'] = round(
                                (vuosi_data['ko_al_kork'] + vuosi_data['ko_yl_kork'] + vuosi_data['ko_yliop']) 
                                / ko_total * 100, 1)
                        else:
                            vuosi_data['korkeakoulutetut_osuus'] = 0
                        
                        # Kerrostalo-osuus (% asunnoista)
                        if vuosi_data['ra_asunn'] > 0:
                            vuosi_data['kerrostalo_osuus'] = round(vuosi_data['ra_kt_as'] / vuosi_data['ra_asunn'] * 100, 1)
                        else:
                            vuosi_data['kerrostalo_osuus'] = 0
                        
                        # Toimialarakenne (% kaikista työpaikoista)
                        tp_total = vuosi_data['tp_tyopy']
                        if tp_total > 0:
                            vuosi_data['tp_palvelut_osuus'] = round(
                                (vuosi_data['tp_g_kaup'] + vuosi_data['tp_i_majo'] + vuosi_data['tp_j_info'] + 
                                 vuosi_data['tp_k_raho'] + vuosi_data['tp_m_erik'] + vuosi_data['tp_p_koul'] + 
                                 vuosi_data['tp_q_terv'] + vuosi_data['tp_r_taid'] + vuosi_data['tp_s_muup']) 
                                / tp_total * 100, 1)
                            vuosi_data['tp_ict_osuus'] = round(vuosi_data['tp_j_info'] / tp_total * 100, 1)
                        else:
                            vuosi_data['tp_palvelut_osuus'] = 0
                            vuosi_data['tp_ict_osuus'] = 0
                        
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


def lataa_osm_tiedosto(tiedostonimi='finland-latest.osm.pbf'):
    """
    Lataa Suomen OSM-data Geofabrikista jos ei ole jo ladattu
    """
    if os.path.exists(tiedostonimi):
        koko_mb = os.path.getsize(tiedostonimi) / (1024 * 1024)
        print(f"   OSM-tiedosto löytyy: {tiedostonimi} ({koko_mb:.1f} MB)")
        return tiedostonimi
    
    print(f"   Ladataan OSM-tiedosto Geofabrikista...")
    print(f"   URL: https://download.geofabrik.de/europe/finland-latest.osm.pbf")
    print(f"   Tämä kestää useita minuutteja (~676 MB)...")
    
    url = 'https://download.geofabrik.de/europe/finland-latest.osm.pbf'
    
    try:
        # Käytä requests-kirjastoa streamingia varten
        response = requests.get(url, stream=True, timeout=600, headers={'User-Agent': 'Mozilla/5.0'})
        response.raise_for_status()
        
        total_size = int(response.headers.get('Content-Length', 0))
        downloaded = 0
        
        print(f"   Tiedoston koko: {total_size/(1024*1024):.1f} MB")
        
        with open(tiedostonimi, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)
                    if total_size > 0 and downloaded % (10 * 1024 * 1024) == 0:  # Printtaa joka 10 MB
                        progress = (downloaded / total_size) * 100
                        print(f"   Ladattu: {progress:.1f}% ({downloaded/(1024*1024):.1f} MB)")
        
        final_size = os.path.getsize(tiedostonimi) / (1024 * 1024)
        print(f"   [OK] Lataus valmis: {tiedostonimi} ({final_size:.1f} MB)")
        return tiedostonimi
        
    except Exception as e:
        print(f"   [ERROR] Lataus epäonnistui: {e}")
        print(f"   Voit ladata tiedoston manuaalisesti:")
        print(f"   https://download.geofabrik.de/europe/finland-latest.osm.pbf")
        if os.path.exists(tiedostonimi):
            os.remove(tiedostonimi)  # Poista osittain ladattu tiedosto
        return None


# Määritellään PalveluHandler vain jos osmium on saatavilla
if OSMIUM_AVAILABLE:
    class PalveluHandler(osmium.SimpleHandler):
        """
        Osmium handler joka kerää palvelutiedot kaikilta postinumeroalueilta
        Käyttää postinumeroalueiden tarkkoja geometrioita (point-in-polygon)
        """
        def __init__(self, postinumero_geometriat):
            super().__init__()
            self.postinumero_geometriat = postinumero_geometriat
            
            # Alusta palvelulaskurit jokaiselle alueelle
            self.palvelut = {}
            for pno in postinumero_geometriat.keys():
                self.palvelut[pno] = {
                    'kaupat': 0,
                    'koulut': 0,
                    'paivakodit': 0,
                    'liikuntapaikat': 0,
                    'terveysasemat': 0,
                    'julkinen_liikenne': 0,
                    'ravintolat': 0,
                    'kahvilat': 0,
                    'puistot': 0
                }
            
            self.kasitelty = 0
        
        def node(self, n):
            """Käsitellään jokainen OSM-node"""
            # Ohita nodet ilman tageja
            if not n.tags:
                return
            
            self.kasitelty += 1
            if self.kasitelty % 100000 == 0:
                print(f"\r   Käsitelty {self.kasitelty:,} nodea...", end='')
            
            node_lat = n.location.lat
            node_lon = n.location.lon
            point = Point(node_lon, node_lat)  # Shapely käyttää (lon, lat) järjestystä
            
            # Tarkista mihin palveluluokkaan kuuluu
            tags = {tag.k: tag.v for tag in n.tags}
            palvelutyyppi = None
            
            if tags.get('shop') in ['supermarket', 'convenience']:
                palvelutyyppi = 'kaupat'
            elif tags.get('amenity') == 'school':
                palvelutyyppi = 'koulut'
            elif tags.get('amenity') == 'kindergarten':
                palvelutyyppi = 'paivakodit'
            elif tags.get('leisure') in ['fitness_centre', 'sports_centre']:
                palvelutyyppi = 'liikuntapaikat'
            elif tags.get('amenity') in ['doctors', 'clinic', 'hospital']:
                palvelutyyppi = 'terveysasemat'
            elif tags.get('highway') == 'bus_stop' or tags.get('railway') in ['station', 'tram_stop', 'halt']:
                palvelutyyppi = 'julkinen_liikenne'
            elif tags.get('amenity') == 'restaurant':
                palvelutyyppi = 'ravintolat'
            elif tags.get('amenity') in ['cafe', 'bar']:
                palvelutyyppi = 'kahvilat'
            elif tags.get('leisure') == 'park':
                palvelutyyppi = 'puistot'
            
            if not palvelutyyppi:
                return
            
            # Tarkista mihin postinumeroalueeseen piste kuuluu (point-in-polygon)
            for pno, geom in self.postinumero_geometriat.items():
                if point.within(geom):
                    self.palvelut[pno][palvelutyyppi] += 1
                    break  # Piste voi kuulua vain yhteen alueeseen


def lataa_postinumeroalueiden_geometriat(geojson_file='postinumerot_hinnat.geojson'):
    """
    Lataa postinumeroalueiden geometriat GeoJSON-tiedostosta
    
    Args:
        geojson_file: GeoJSON-tiedoston polku
    
    Returns:
        dict: postinumero -> shapely geometry -mappaus
    """
    print(f"\nLadataan postinumeroalueiden geometrioita...")
    
    if not os.path.exists(geojson_file):
        print(f"   [ERROR] Tiedostoa ei loydy: {geojson_file}")
        return {}
    
    try:
        with open(geojson_file, 'r', encoding='utf-8') as f:
            geojson_data = json.load(f)
        
        geometriat = {}
        for feature in geojson_data.get('features', []):
            props = feature.get('properties', {})
            postinumero = props.get('postinumer')  # Korjattu: WFS API käyttää 'postinumer'-kenttää
            
            if postinumero and 'geometry' in feature:
                # Muunna GeoJSON geometria shapely geometriaksi
                geom = shape(feature['geometry'])
                geometriat[postinumero] = geom
        
        print(f"   Ladattu {len(geometriat)} postinumeroalueen geometria")
        return geometriat
        
    except Exception as e:
        print(f"   [ERROR] Virhe geometrioiden latauksessa: {e}")
        return {}


def hae_palvelut_osm_geofabrik(postinumero_geometriat, osm_tiedosto='finland-latest.osm.pbf'):
    """
    Hae palvelutiedot OSM-tiedostosta (Geofabrik) kaikille postinumeroalueille
    
    Args:
        postinumero_geometriat: dict postinumeroista ja niiden geometrioista (shapely)
        osm_tiedosto: OSM .pbf tiedoston nimi
    
    Returns:
        dict: palvelutiedot per postinumero
    """
    if not OSMIUM_AVAILABLE:
        print("   [WARNING] osmium ei kaytettavissa, ohitetaan palvelutiedot")
        return {}
    
    print(f"\nHaetaan palvelutietoja OSM-datasta...")
    print(f"   Tiedosto: {osm_tiedosto}")
    print(f"   Käytetään tarkkoja postinumeroaluerajoja")
    print(f"   Postinumeroalueita: {len(postinumero_geometriat)}")
    print(f"   HUOM: Tämä kestää useita minuutteja...")
    
    # Tarkista että tiedosto on olemassa
    if not os.path.exists(osm_tiedosto):
        print(f"   [ERROR] Tiedostoa ei loydy: {osm_tiedosto}")
        return {}
    
    # Luo handler ja parsita tiedosto
    handler = PalveluHandler(postinumero_geometriat)
    
    try:
        print(f"   Parsitaan OSM-tiedosto...")
        handler.apply_file(osm_tiedosto)
        print(f"\n   [OK] Kasitelty {handler.kasitelty:,} nodea")
        
        # Laske palveluindeksi jokaiselle alueelle
        # Käytetään tiheyttä (palvelut/km²) ja logaritmista skaalausta
        # jotta suurten maaseutualueiden raakamäärät eivät dominoi
        painot = {
            'kaupat': 1.0,
            'koulut': 1.5,
            'paivakodit': 1.2,
            'liikuntapaikat': 0.8,
            'terveysasemat': 1.3,
            'julkinen_liikenne': 0.5,
            'ravintolat': 0.7,
            'kahvilat': 0.5,
            'puistot': 0.6
        }
        
        # Laske alueiden pinta-alat km²
        alueen_alat = {}
        for pno, geom in postinumero_geometriat.items():
            centroid = geom.centroid
            lat_rad = math.radians(centroid.y)
            lat_factor = 111320  # m per degree lat
            lon_factor = 111320 * math.cos(lat_rad)  # m per degree lon
            area_km2 = geom.area * lat_factor * lon_factor / 1_000_000
            alueen_alat[pno] = max(area_km2, 0.01)  # Min 0.01 km² nollalla jaon esto
        
        alueet_palveluilla = 0
        for pno, palvelut in handler.palvelut.items():
            area = alueen_alat.get(pno, 1.0)
            palveluindeksi = sum(
                math.log(1 + palvelut[k] / area) * painot[k] for k in palvelut.keys()
            )
            palvelut['palveluindeksi'] = round(palveluindeksi, 2)
            
            if palveluindeksi > 0:
                alueet_palveluilla += 1
        
        print(f"   Alueita joilla palveluita: {alueet_palveluilla}/{len(postinumero_geometriat)}")
        
        return handler.palvelut
        
    except Exception as e:
        print(f"   [ERROR] Virhe parsinnassa: {e}")
        return {}


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
    
    # 4. Lataa postinumeroalueiden geometriat
    postinumero_geometriat = lataa_postinumeroalueiden_geometriat()
    
    # 5. Hae palvelutiedot OSM-datasta (Geofabrik)
    palvelut = {}
    if OSMIUM_AVAILABLE and postinumero_geometriat:
        print("\nPalvelutietojen haku OSM-datasta...")
        print(f"   OSMIUM_AVAILABLE: {OSMIUM_AVAILABLE}")
        print(f"   Geometrioita ladattu: {len(postinumero_geometriat)}")
        
        osm_tiedosto = lataa_osm_tiedosto('finland-latest.osm.pbf')
        
        if osm_tiedosto:
            print(f"   [OK] OSM-tiedosto valmis: {osm_tiedosto}")
            palvelut = hae_palvelut_osm_geofabrik(
                postinumero_geometriat, 
                osm_tiedosto=osm_tiedosto
            )
        else:
            print(f"   [ERROR] OSM-tiedoston lataus epaonnistui!")
            print(f"   [WARNING] Jatketaan ilman palvelutietoja")
    else:
        if not OSMIUM_AVAILABLE:
            print("\n[WARNING] Palvelutietojen haku ohitettu (osmium ei asennettu)")
            print(f"   Yrita: pip install osmium")
        elif not postinumero_geometriat:
            print("\n[WARNING] Palvelutietojen haku ohitettu (geometriat puuttuvat)")
            print(f"   Geometrioita: {len(postinumero_geometriat) if postinumero_geometriat else 0}")
    
    # 6. Yhdistä kaikki data
    rikastettu_data = {}
    
    for postinumero in paavo_data.keys():
        rikastettu_data[postinumero] = {
            'paavo': paavo_data.get(postinumero, {}),
            'etaisyydet': etaisyydet.get(postinumero, {}),
            'palvelut': palvelut.get(postinumero, {})
        }
    
    # 7. Tallenna
    output_file = 'data/rikastettu_data.json'
    
    os.makedirs('data', exist_ok=True)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(rikastettu_data, f, ensure_ascii=False, indent=2)
    
    print(f"\n[OK] Rikastettu data tallennettu: {output_file}")
    print(f"   Postinumeroalueita: {len(rikastettu_data)}")
    print(f"   - Paavo-tiedot: {len(paavo_data)}")
    print(f"   - Etaisyydet: {len(etaisyydet)}")
    if palvelut:
        alueet_palveluilla = sum(1 for p in palvelut.values() if p.get('palveluindeksi', 0) > 0)
        print(f"   - Palvelut: {len(palvelut)} ({alueet_palveluilla} alueella dataa)")
        print(f"   [OK] PALVELUTIEDOT MUKANA")
    else:
        print(f"   - Palvelut: 0 (ei dataa)")
        print(f"   [WARNING] PALVELUTIEDOT PUUTTUVAT - kartta ilman palveluita!")
    print("="*60)


if __name__ == "__main__":
    main()
