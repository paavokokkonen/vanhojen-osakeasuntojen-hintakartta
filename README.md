# Asuntojen hintakartta

Interaktiivinen kartta Suomen asuntojen keskihinnoista ja kauppamääristä postinumeroalueittain vuosilta 2009-2026*.

**Datalähteet:** 
- Asuntohinnat ja kauppamäärät: Tilastokeskus (StatFin) - Vanhojen osakeasuntojen neliöhinnat ja kauppojen lukumäärät postinumeroalueittain (taulukko ashi_13mu)
- Postinumeroalueiden geometria: Tilastokeskus geo.stat.fi (postialue:pno_tilasto) - Tarkat postinumeroalueet, ~240 koordinaattipistettä per alue

**Huom:** * = Vuosi 2026 on ennuste, laskettu viimeisen 5 vuoden lineaarisen trendin perusteella. Kartta aukeaa oletuksena vuoteen 2025 (viimeisin datavuosi).

## Ominaisuudet

### 📊 Datasisältö
- **18 vuotta historiallista dataa** (2009-2025) + ennuste vuodelle 2026*
- **Huoneistotyypit:**
  - Kaikki (painotettu keskiarvo, painotettuna kauppojen lukumäärällä)
  - Kerrostalo yksiöt
  - Kerrostalo kaksiot
  - Kerrostalo kolmiot+
  - Rivitalot
- **Kaksi mittaria:**
  - Neliöhinnat (EUR/m²)
  - Kauppojen lukumäärä (kpl)
- **1723 postinumeroaluetta** joilla asuntohintadataa

### 🗺️ Karttaominaisuudet
- **Polygon-pohjaiset postinumeroalueet** (tarkat rajat, ei geometrian yksinkertaistusta)
- **Korkea geometriatarkkuus** - Keskimäärin 240 koordinaattipistettä per alue
- **Neljä tarkastelunäkymää:**
  - **Absoluuttiset arvot** - valitse vuosi, huoneistotyyppi ja mittari
  - **Vuosimuutokset** - vertaa kahta vuotta, näe %-muutokset
  - **Analyysi (5v trendi)** - trendisuunta, volatiliteetti, markkinaaktiivisuus ja väestömuutokset
  - **Animaatio: Kartta** - katso hintojen kehitys animaationa 2009-2026
  - **Animaatio: Diagrammi** - top 10 kalleimmat alueet vaakapylväsdiagrammina, animoituna ajassa
- **Intuitiiviset väriskalat:**
  - Hinnoissa: vihreä = halpa, punainen = kallis
  - Kauppojen määrissä: vihreä = paljon kauppoja, punainen = vähän
  - Muutos-%:ssä: vihreä = positiivinen kasvu, punainen = negatiivinen lasku
- **Informatiiviset popup-ikkunat:**
  - Kaikilla alueilla näkyy postinumero ja nimi
  - Alueilla joilla on kauppoja: hinnat ja määrät
  - Alueilla ilman kauppoja: "Ei kauppoja" -ilmoitus
  - Absoluuttisessa näkymässä: väestötiedot (väkiluku, keski-ikä, keskitulo, työttömyysaste) + palvelutiedot
  - Analyysissa: 5 vuoden muutokset hinnoissa ja väestötiedoissa + palvelutiedot
  - **Laajennetut Paavo-tiedot:** ikärakenne (lapset/työikäiset/eläkeikäiset %), asuntorakenne (kerrostalo%, keskipinta-ala, omistus/vuokra%), koulutus & työ (korkeakoulutetut%, ICT%, palveluala%)
  - **Matka-aika keskustaan:** lähimmän keskustan nimi, minuutit, kilometrit, kulkutapa
  - **Laajennetut palvelut:** 11 kategoriaa (+ ravintolat, kahvilat, puistot, kirjastot, apteekit)
- **Hakutoiminto** postinumeroalueille
- **Kaupunkinavigointi** (Helsinki, Espoo, Vantaa, Tampere, Turku, Oulu, Kuopio)
- **Dynaamiset tilastot** valituista parametreista

### 🎬 Animaatio-ominaisuudet
- **Kartta-animaatio:**
  - Automaattinen siirtyminen vuosien 2009-2026 läpi
  - Play/pause-painike ja kolme nopeutta (Hidas 2s, Normaali 1s, Nopea 0.5s per kehys)
  - Toimii sekä neliöhinnoille että kauppamäärille
  - Kaikille huoneistotyypeille
- **Diagrammi-animaatio:**
  - Top 10 kalleimmat postinumeroalueet vaakapylväsdiagrammina
  - Suodata kaupungin mukaan (Koko maa, Helsinki, Espoo, Vantaa, Tampere, Turku, Oulu, Kuopio)
  - Valittavissa huoneistotyyppi
  - Animoituu automaattisesti vuosien läpi
  - Värikoodaus kuten kartalla (vihreä→punainen hinnan mukaan)
  - Play/pause-painike ja nopeusvalinta

### 📊 Väestötiedot ja trendianalyysi
- **Paavo-tiedot** (Tilastokeskus) vuosille 2015-2026:
  - Väkiluku, keski-ikä, keskitulo, työttömyysaste
  - Väestötiheys, koulutustaso, työlliset/työttömät
  - Näkyvissä absoluuttisessa näkymässä
- **5 vuoden trendianalyysi** (867 aluetta):
  - Hinnan kehitys (%, euroa)
  - Markkinaaktiivisuus (keskimääräinen kauppamäärä)
  - Volatiliteetti (hintojen vaihtelu)
  - Väestömuutokset (väkiluku, ikä, tulot, työttömyys)

### 🏪 Palvelutiedot (OpenStreetMap)
- **Datalähde:** Geofabrik finland-latest.osm.pbf (~676 MB, päivittyy päivittäin)
- **Laskentamenetelmä:** Point-in-polygon tarkistus postinumeroalueen tarkoilla rajoilla (osmium-parseri, nodet + wayt)
- **Palvelukategoriat:** (11 kpl)
  - 🛒 Ruokakaupat (`shop=supermarket`, `shop=convenience`) — *nimetty uudelleen 9.3.2026: tagit kattavat vain supermarketit ja lähikaupat*
  - 🏫 Koulut (`amenity=school`)
  - 🧒 Päiväkodit (`amenity=kindergarten`)
  - 💪 Liikuntapaikat (`leisure=fitness_centre`, `leisure=sports_centre`)
  - 🏥 Terveysasemat (`amenity=doctors`, `amenity=clinic`, `amenity=hospital`)
  - 🚌 Julkinen liikenne (`highway=bus_stop`, `railway=station`, `railway=tram_stop`, `railway=halt`)
  - 🍽️ Ravintolat (`amenity=restaurant`) — *uusi 6.3.2026*
  - ☕ Kahvilat (`amenity=cafe`, `amenity=bar`) — *uusi 6.3.2026*
  - 🌳 Puistot (`leisure=park`) — *uusi 6.3.2026*
  - 📚 Kirjastot (`amenity=library`) — *uusi 9.3.2026*
  - 💊 Apteekit (`amenity=pharmacy`) — *uusi 9.3.2026*
- **Palveluindeksi** — tiheyyspohjainen, logaritmisesti skaalattu:
  ```
  palveluindeksi = Σ wₖ · ln(1 + nₖ / A)
  ```
  missä `nₖ` = palvelukategorian k lukumäärä, `A` = postinumeroalueen pinta-ala (km²), `wₖ` = paino:
  | Kategoria | Paino (wₖ) |
  |-----------|-----------|
  | Koulut | 1.5 |
  | Terveysasemat | 1.3 |
  | Päiväkodit | 1.2 |
  | Apteekit | 1.1 |
  | Ruokakaupat | 1.0 |
  | Kirjastot | 1.0 |
  | Liikuntapaikat | 0.8 |
  | Ravintolat | 0.7 |
  | Puistot | 0.6 |
  | Julkinen liikenne | 0.5 |
  | Kahvilat | 0.5 |

  Logaritminen skaalaus ja pinta-alanormalisointi estävät suurten maaseutualueiden raakamäärien (esim. sadat bussipysäkit pitkien teiden varrella) dominointia. Tyypilliset arvot: 0–15 (Helsinki kantakaupunki ~10–15, kaupunkikeskustat ~5–8, maaseutu <1).
- **Kattavuus:** 1715/1723 postinumeroalueella palvelutietoja (99.5%)
- **OSM-elementtityypit:** Parseri käsittelee sekä node- että way-elementit (6.3.2026 korjaus — pelkkä node-parsinta jätti 36–98% palveluista huomioimatta kategoriasta riippuen)
- **Huom:** Palvelut ovat snapshot nykyhetkestä, ei aikasarjaa

### 🔮 Ennusteet ja mallit
- **Oletuksena viimeisin datavuosi (2025)** - Kartta aukeaa vuoteen 2025, joka on viimeisin Tilastokeskuksen julkaisema datavuosi
- **Ennustevuosi (2026*) valittavissa erikseen** - Käyttäjän on valittava aktiivisesti vuosi 2026 nähdäkseen ennusteet
- **Neljä ennustemallia** vuodelle 2026:
  - **Lineaarinen trendi** - Yksinkertainen keskimääräinen vuosimuutos (5 vuoden historia)
  - **ARIMA** - AutoRegressive Integrated Moving Average, aikasarja-analyysi
  - **Exponential Smoothing** - Holt's exponential smoothing -menetelmä
  - **SARIMAX-Euribor** - SARIMAX(1,1,1) 12 kk Euribor-korko eksogenisenä muuttujana (ECB data 2005–2026) — *uusi 6.3.2026*
- **Interaktiivinen mallivalinta** - Valitse ennustemalli pudotusvalikosta kun tarkastelet vuotta 2026*
- **Kattavat ennusteet**:
  - Linear: ~3000 ennustetta
  - ARIMA: ~2700 ennustetta (vaatii riittävästi dataa)
  - Exponential Smoothing: ~3000 ennustetta
  - SARIMAX-Euribor: ~2700 ennustetta
- **Visuaalinen erottelu** tähdellä (*) ennustevuodesta
- **Mallivertailu** - Näe miten eri mallit ennustavat samalle alueelle

### 🚌 Matka-aika keskustaan
- **Datalähde:** Digitransit Routing API v2 (julkinen liikenne) tai laskennallinen Haversine-arvio (auto)
- **Keskustat:** Helsinki, Tampere, Turku, Oulu, Kuopio, Jyväskylä, Lahti
- **Logiikka:** Jokaiselle postinumeroalueelle lasketaan matka-aika lähimpään kaupunkikeskustaan
- **Kulkutapa näkyvissä:** Popup näyttää onko kyseessä julkisen liikenteen aika (Digitransit) vai laskennallinen arvio (auto, kaava: 10 + km × 2.5 min)
- **Värikoodaus popupissa:** 🟢 ≤20 min, 🟡 ≤45 min, 🟠 ≤90 min, 🔴 >90 min
- **Kattavuus:** 1723 postinumeroaluetta
- **Finder-integraatio:** "Paras alue" -hakutyökalussa matka-aika-suodatin (0–120 min liukusäädin)

### 📈 Euribor-aikasarja
- **Datalähde:** ECB Statistical Data Warehouse (12 kk Euribor)
- **Aikasarja:** 2005–2026 (254 kuukausidatapistettä, 22 vuosikeskiarvoa)
- **Käyttö:**
  - SARIMAX-ennustemallissa eksogenisenä muuttujana
  - Aikasarjakaaviossa: Hinta vs. Euribor -kaksoisakselikuvio
- **URL:** `https://data-api.ecb.europa.eu/service/data/FM/M.U2.EUR.RT.MM.EURIBOR1YD_.HSTA`

## Asennus

```bash
# Asenna riippuvuudet
pip install -r requirements.txt
```

## Käyttö

### GitHub Pages (julkinen kartta)

Kartta päivittyy automaattisesti kerran kuukaudessa GitHub Actionsin kautta:
- 🌐 Käytä suoraan julkista versiota (linkki repositoryn kuvauksessa)
- ⚙️ Automaattinen päivitys joka kuukauden 1. päivä
- 🔄 Manuaalinen päivitys: Actions-välilehdellä → "Päivitä ja julkaise asuntohintakartta" → Run workflow

### Paikallinen käyttö (kehitys/testaus)

```bash
# 1. Päivitä asuntohintadata Tilastokeskuksesta (2009-2025) ja laske lineaarinen ennuste (2026)
python asuntohinnat.py

# 2. Lataa postinumeroalueet Tilastokeskuksen WFS-rajapinnasta
python lataa_postinumeroalueet.py

# 3. Hae väestötiedot Paavo-tietokannasta (2015-2026) ja palvelutiedot OSM-datasta
python rikasta_data.py

# 4. Lataa vuokradata Tilastokeskuksesta (2015-2025, kvartaali → vuosikeskiarvot)
python lataa_vuokrat.py

# 5. Laske 5 vuoden trendianalyysi
python laske_trendianalyysi.py

# 6. Laske edistyneet ennustemallit (ARIMA, Exponential Smoothing, SARIMAX-Euribor)
python laske_ennusteet.py

# 7. Lataa matka-ajat keskustaan (Digitransit API tai laskennallinen arvio)
python lataa_matka_ajat.py

# 8. Lataa 12 kk Euribor-aikasarja (ECB Statistical Data Warehouse)
python lataa_euribor.py

# 9. Laske korrelaatiot asuntohintojen ja muuttujien välillä
python analysoi_korrelaatiot.py

# 10. Luo interaktiivinen kartta
python kartta_polygon.py
```

Avaa `kartta.html` selaimessa.

**Huom:** 
- Vaiheet 1-8 hakevat dataa verkosta tai laskevat ennusteita
- `asuntohinnat.py` kestää ~1-2 min (StatFin API)
- `rikasta_data.py` kestää ~5-10 min (Paavo WFS API + OSM-datan lataus ~676 MB + parsing 1.7M nodea)
- `laske_ennusteet.py` kestää ~5-20 min (ARIMA, Exponential Smoothing ja SARIMAX-Euribor mallit)
- `lataa_matka_ajat.py` kestää ~1-2 min (laskennallinen arvio) tai ~30-60 min (Digitransit API)
- `lataa_euribor.py` kestää ~5 s (ECB API)
- `kartta_polygon.py` generoi kartan nopeasti (~10-30 s)

## Tiedostot

### Dataskriptit (pipeline-järjestyksessä)
1. `asuntohinnat.py` — Hakee asuntohintadatan Tilastokeskuksesta (2009-2025) ja laskee lineaarisen ennusteen (2026)
2. `lataa_postinumeroalueet.py` — Hakee postinumeroalueiden tarkat geometriat Tilastokeskuksen WFS-rajapinnasta
3. `rikasta_data.py` — Hakee Paavo-väestötiedot aikasarjana (2015-2026, 113 kenttää + 8 johdettua muuttujaa) ja palvelutiedot OSM-datasta (11 kategoriaa)
4. `lataa_vuokrat.py` — Hakee vuokradatan Tilastokeskuksesta (StatFin asvu_13eb, kvartaali → vuosikeskiarvot 2015-2025)
5. `laske_trendianalyysi.py` — Laskee 5 vuoden trendit, volatiliteetin ja markkinaaktiivisuuden
6. `laske_ennusteet.py` — Laskee edistyneet ennustemallit (ARIMA, Exponential Smoothing, SARIMAX-Euribor) vuodelle 2026
7. `lataa_matka_ajat.py` — Laskee matka-ajat lähimpään kaupunkikeskustaan (Digitransit API / Haversine-fallback)
8. `lataa_euribor.py` — Hakee 12 kk Euribor-aikasarjan ECB:n Statistical Data Warehouse -rajapinnasta
9. `analysoi_korrelaatiot.py` — Laskee korrelaatiot asuntohintojen ja muuttujien (tulotaso, palveluindeksi, etäisyys ym.) välillä
10. `kartta_polygon.py` — Luo interaktiivisen kartan kaikista datatiedostoista

### Apuskriptit
- `laske_palveluindeksi.py` — Laskee palveluindeksin uudelleen normalisoituna (ei vaadi OSM-parsintaa). Hyödyllinen painojen säätöön kehityksessä.
- `tarkista_paavo_vuosi.py` — Debug-työkalu: tarkistaa Paavo-datan vuosien saatavuuden WFS-rajapinnasta

### Datatiedostot (generoituvat)
- `data/asuntohinnat.json` - Asuntohintadata vuosittain (2009-2026), huoneistotyypeittäin (~7.9 MB)
- `data/postinumerot_hinnat.geojson` - Postinumeroalueiden tarkat geometriat + hinnat (~16.6 MB)
- `data/postinumerokoordinaatit.json` - Alueiden keskipisteet
- `data/rikastettu_data.json` — Väestötiedot aikasarjana (2015-2026, 3044 aluetta) + palvelutiedot (~96 MB)
- `data/vuokradata.json` — Vuokradatan neliövuokrat ja lukumäärät postinumeroittain (2015-2025) (~1.9 MB)
- `data/trendianalyysi.json` — 5 vuoden trendianalyysi (867 aluetta) (~217 KB)
- `data/ennusteet_mallit.json` — Ennusteet neljällä mallilla (Linear, ARIMA, Exponential, SARIMAX-Euribor) (~900 KB)
- `data/matka_ajat.json` — Matka-ajat lähimpään keskustaan (1723 aluetta, 7 kaupunkia) (~240 KB)
- `data/euribor.json` — 12 kk Euribor-korko kuukausittain ja vuosikeskiarvoin (2005–2026) (~10 KB)
- `data/korrelaatiot.json` — Korrelaatioanalyysi: Pearsonin r, p-arvot ja scatterplot-data 11 muuttujalle
- `finland-latest.osm.pbf` - OpenStreetMap data Suomesta (~676 MB, ladataan rikasta_data.py:llä)

### Kartat (generoituvat)
- `kartta.html` - Interaktiivinen polygon-kartta (~20+ MB)

## Tekninen toteutus

- **Karttakirjasto:** Leaflet 1.9.4
- **Datalähde:** 
  - Asuntohinnat: Tilastokeskus StatFin API (ashi_13mu)
  - Geometriat: Tilastokeskus WFS API (postialue:pno_tilasto)
  - Väestötiedot: Tilastokeskus WFS API (postialue:pno_tilasto_XXXX, vuodet 2015-2026, 113 kenttää)
  - Palvelutiedot: OpenStreetMap via Geofabrik (finland-latest.osm.pbf, 11 kategoriaa)
  - Vuokradata: Tilastokeskus StatFin API (asvu_13eb)
  - Matka-ajat: Digitransit Routing API v2 / Haversine-laskennallinen arvio
  - Euribor: ECB Statistical Data Warehouse (12 kk Euribor, 2005–2026)
- **Geometriatarkkuus:**
  - 8 desimaalin koordinaattitarkkuus (WFS: `coordinate_precision:8`)
  - Ei geometrian yksinkertaistusta (WFS: `decimation:NONE`, Leaflet: `smoothFactor:0`)
  - Keskimäärin 240 koordinaattipistettä per postinumeroalue
- **Koordinaattijärjestelmä:** WGS84 (EPSG:4326) kartalla, ETRS-TM35FIN (EPSG:3067) lähteessä
- **Datan yhdistäminen:** Suodatetaan 3018 postinumeroalueesta vain ne 1723, joilla on asuntohintadataa
- **Ennustemenetelmät (2026*):**
  - **Linear** - Yksinkertainen lineaarinen trendi viimeisen 5 vuoden (2021-2025) datasta
  - **ARIMA** - ARIMA(1,1,1) autoregressive integrated moving average (statsmodels)
  - **Exponential Smoothing** - Holt's simple exponential smoothing (statsmodels)
  - **SARIMAX-Euribor** - SARIMAX(1,1,1) 12 kk Euribor eksogenisenä muuttujana (Himmelberg ym. 2005: korko on tärkein makroselittäjä)
  - Käyttäjä voi valita mallin kartalla pudotusvalikosta
- **Trendianalyysi:** 5 vuoden (2019-2024) lineaarinen regressio, volatiliteetti (keskihajonta), aktiivisuus (keskimääräiset kaupat)
- **Väestödata:** 
  - Aikasarja 2015-2026 (12 vuotta × 3044 postinumeroaluetta ≈ 36,500 tietuetta)
  - Huom: Paavo-data julkaistaan +1 vuoden viiveellä (pno_tilasto_2025 sisältää 31.12.2024 tilanteen)
  - 113 kenttää per postinumero (ikäjakauma, tuloluokat, rakennuskanta, 26 toimialaa, talouksien tyyppi, omistus/vuokra)
  - 8 johdettua muuttujaa (lapset_osuus, työikäiset_osuus, eläkeikäiset_osuus, omistusaste, vuokra_aste, korkeakoulutetut_osuus, kerrostalo_osuus, tp_palvelut_osuus, tp_ict_osuus)
- **Palveludata:**
  - OSM-data parsed osmium-kirjastolla (1.7M+ nodea)
  - Point-in-polygon tarkistus shapely-kirjastolla
  - 11 palvelukategoriaa, painotettu palveluindeksi
  - 1715/1723 alueella palvelutietoja (99.5%)
  - Snapshot nykyhetkestä (ei aikasarjaa)
- **Datamäärä:** 
  - 18 vuotta (17 todellista + 1 ennuste)
  - 5 huoneistotyyppiä (1 painotettu keskiarvo + 4 yksittäistä tyyppiä)
  - 2 mittaria (hinta, kauppamäärä)
  - 1723 postinumeroaluetta
  - ≈ 155,000 datapistettä asuntohinnoissa
  - ≈ 36,500 datapistettä väestötiedoissa (113 kenttää + 8 johdettua per alue per vuosi)
  - ≈ 19,000 datapistettä palvelutiedoissa (11 kategoriaa × 1715 aluetta + palveluindeksit)
  - ≈ 1,723 matka-aikatietoa (minuutit, lähin keskusta, etäisyys km)
  - ≈ 254 kuukausittaista + 22 vuosittaista Euribor-datapistettä
  - ≈ 414,000 koordinaattipistettä geometrioissa

### GitHub Actions deployment

Kartta päivittyy automaattisesti ilman manuaalista työtä:

1. **Workflow ajastus:** Joka kuukauden 1. päivä klo 03:00 UTC
2. **Datan haku:** 
   - Tilastokeskuksen StatFin API → Asuntohinnat (2009-2025) + Vuokradata (2015-2025)
   - Tilastokeskuksen WFS API → Tarkat postinumeroalueiden geometriat
   - Tilastokeskuksen WFS API → Väestötiedot (Paavo 2015-2026)
   - Geofabrik → OSM-data (~676 MB) → Palvelutiedot (osmium-parsing, 11 kategoriaa)
   - Digitransit / Haversine → Matka-ajat 7 kaupunkikeskustaan
   - ECB → 12 kk Euribor-aikasarja
3. **Analyysi:** Trendianalyysi, ennusteet (4 mallia), korrelaatiot
4. **Kartan generointi:** Python-skriptit luovat kartta.html:n
5. **Julkaisu:** GitHub Pages palvelee automaattisesti päivitetyn kartan

**Edut:**
- ✅ Ei generoituja tiedostoja repositoriossa (repo pysyy kevyenä ~50 KB)
- ✅ Data aina ajantasalla ilman manuaalista päivitystä
- ✅ Täysin toistettava prosessi (lähdekoodista valmiiseen karttaan)
- ✅ Julkinen verkkopalvelu ilman palvelinkuluja

## 💡 Kehitysideat (Tulevat ominaisuudet)

### 📚 Kirjallisuuskatsaukseen perustuvat ideat

Alla olevat ideat nousevat suoraan tutkimuskirjallisuudesta (ks. Kirjallisuuskatsaus-osio). Ne on ryhmitelty toteutettavuuden ja odotetun lisäarvon mukaan.

#### A. Ennustemallit — tutkimuspohjaiset parannukset

| Idea | Tutkimusperusta | Toteutus | Prioriteetti |
|------|----------------|----------|-------------|
| **Korkotaso eksogenisenä muuttujana** | Himmelberg ym. (2005): korko on tärkein makroselittäjä. 1 %-yksikön muutos → 5–10 % hintavaikutus | ✅ Toteutettu 6.3.2026: 12 kk Euribor ECB:stä, SARIMAX(1,1,1) `exog=[euribor]`, 2726 ennustetta. | ✅ Valmis |
| **Tulotaso ja työttömyys ennusteissa** | Holly & Jones (1997): tulot ja hinnat yhteisintegroituneita | Paavo-data on jo käytettävissä. Lisää aluetason tulot ja työttömyys SARIMAX-mallin eksogenisinä muuttujina. | ⭐ Korkea |
| **Väestönmuutos ennusteissa** | Mankiw & Weil (1989): työikäinen väestö ennustaa kysyntää | Paavo-väestödata aikasarjana 2015–2026. Lisää väestönmuutos-% eksogenisena muuttujana. | ⭐ Korkea |
| **Hedoninen hintamalli** | Rosen (1974): hinta = ominaisuuksien summa | Regressiomalli: hinta ~ palveluindeksi + tulotaso + väkiluku + keski-ikä + työttömyys. Poikkileikkausennuste. | Keskitaso |
| **Spatiaalinen autoregressio (SAR)** | LeSage & Pace (2009): naapurialueet vaikuttavat toisiinsa | Lisää naapurialueiden hinnat selittäjäksi (spatial lag). `spreg`- tai `pysal`-kirjasto. | Matala (monimutkainen) |

**Konkreettinen toteutusesimerkki — Euribor-malli:**
```python
# laske_ennusteet.py — lisää korkotaso eksogenisenä muuttujana
from statsmodels.tsa.statespace.sarimax import SARIMAX
import pandas as pd

# Hae 12kk Euribor (Suomen Pankki / ECB)
euribor = pd.Series({2015: 0.06, 2016: -0.01, 2017: -0.19, 2018: -0.17,
                      2019: -0.26, 2020: -0.30, 2021: -0.50, 2022: 0.57,
                      2023: 3.86, 2024: 3.55, 2025: 2.50})

# Ennustevuoden korko (ECB forward rate tai oletus)
euribor_ennuste = pd.Series({2026: 2.20})

model = SARIMAX(hinnat, exog=euribor, order=(1,1,1))
results = model.fit()
ennuste = results.forecast(steps=1, exog=euribor_ennuste)
```

#### B. Karttanäkymät — uudet kerrokset kirjallisuudesta

| Idea | Tutkimusperusta | Datalähde | Prioriteetti |
|------|----------------|-----------|-------------|
| **Kohtuuhintaisuusindeksi (affordability)** | Himmelberg ym. (2005): user cost of housing | ✅ Jo toteutettu (hinta/tulot-suhde) | ✅ Valmis |
| **P/R-ratio (hinta/vuokra-suhde)** | Brännback & Oikarinen (2019): P/R-ratio kertoo yli/aliarvostuksesta | Omistushinnat + vuokradata jo käytettävissä. Laske `ostohinta / (vuosivuokra)`. Näytä kartalla. | ⭐ Korkea |
| **Matka-aikakartta (isokroni)** | Alonso (1964), Laakso (1997): saavutettavuus #1 hintaselittäjä | ✅ Toteutettu 6.3.2026: Digitransit API + Haversine-fallback, 7 kaupunkia, värikoodattu popup, finder-integraatio. | ✅ Valmis |
| **Koulujen laatu** | Black (1999), Harjunen ym. (2018): koulun laatu → 2–5 % hintavaikutus | Opetushallituksen Vipunen-tietopalvelu: oppimistulokset alueittain | Keskitaso |
| **Rikollisuuskartta** | Gibbons (2004): -10 % rikoksia → +1–3 % hintoja | Poliisi / tilastokeskus: rikokset kunnittain | Keskitaso |
| **Viheralueindeksi** | Votsis & Perrels (2016): viheralueet +3–5 % Suomessa | OSM: `leisure=park`, `natural=wood` → pinta-ala per postinumero | Keskitaso |
| **Kaavoitus ja rakennusoikeus** | Saiz (2010), Glaeser ym. (2005): tarjontarajoitteet nostavat hintoja | Kuntien avoin kaavoitusdata (vaihtelee kunnittain) | Matala (saatavuus) |
| **Käveltävyysindeksi (walkability)** | Pope & Pope (2015): palvelujen läheisyys nostaa hintoja | OSM-data + etäisyyslaskelma: montako palvelua 500m / 1km säteellä | Keskitaso |

#### C. Analyysityökalut — tutkimuspohjaiset

| Idea | Tutkimusperusta | Toteutus |
|------|----------------|----------|
| **Regression-pohjainen hintadekomponointi** | Rosen (1974): hedoninen hinta = osien summa | Sovita OLS: `hinta ~ tulotaso + palveluindeksi + väkiluku + keski_ika + työttömyys`. Näytä kunkin tekijän euro-osuus. "Tämän alueen hinnasta 35 % selittyy tulotasolla, 20 % palveluilla…" |
| **Bubble detector (yliarvostus)** | Case & Shiller (1989): spekulaatio ajaa hintoja fundamentaalien yli | Laske `toteutunut_hinta / selitetty_hinta` (residuaali). Jos > 1.2 → mahdollinen kupla. Väritä kartalla punaiseksi. |
| **Palveluindeksi vs. hinta (scatter)** | Black (1999), Pope & Pope (2015) | ✅ Jo kehitysideana. Scatter plot + regressiosuora. R²-arvo näkyviin. |
| **Muuttoliikkeen vaikutusanalyysi** | Tervo (2000), Aro (2007) | Paavo-väestömuutos → korrelaatio hintatrendin kanssa. Näytä nuolikartta: mistä mihin ihmiset muuttavat. |

#### D. Prioriteettijärjestys (kirjallisuuden perusteella)

Tutkimuskirjallisuuden selitysvoiman ja teknisen toteutettavuuden perusteella suositeltu toteutusjärjestys:

1. **🥇 P/R-ratio kartalle** — helppo toteuttaa (data on), korkea informaatioarvo sijoittajille
2. ~~**🥇 Euribor eksogenisenä**~~ — ✅ Toteutettu 6.3.2026
3. **🥈 Tulotaso + väestö ennusteissa** — Paavo-data jo käytössä, vain mallipäivitys
4. ~~**🥈 Matka-aikakartta**~~ — ✅ Toteutettu 6.3.2026
5. **🥉 Hedoninen regressio** — kokonaisvaltainen selittävä malli, vaatii tilastotieteen osaamista
6. ~~**🥉 Viheralueindeksi OSM:stä**~~ — ✅ Toteutettu 6.3.2026

### 1. Ennustemallien parantaminen

**Tavoite:** Parantaa ennusteiden tarkkuutta ja antaa käyttäjille parempi käsitys ennusteiden epävarmuudesta.

**Ideat:**

- **Prophet-malli** (Facebookin aikasarja-ennuste)
  - *Miksi:* Prophet käsittelee automaattisesti trendien muutoksia ja poikkeavia arvoja. Soveltuu hyvin asuntomarkkinadataan.
  - *Toteutus:* `fbprophet`-kirjasto, lisää ~60MB riippuvuuksia. Vaatii vähintään 2 vuoden dataa per alue.

- **Luottamusvälit ennusteille** (ennusteen epävarmuus)
  - *Miksi:* Ennuste on aina epävarma. Luottamusvälit (esim. 80%, 95%) kertovat, kuinka varmoja voimme olla ennusteesta.
  - *Toteutus:* Lasketaan jäännösten keskihajonta ja oletetaan normaalijakauma. Visualisoidaan läpinäkyvänä alueena kartalla.
  - *Esimerkki:* "00100: Ennuste 7400 €/m² (95% luottamusväli: 6800-8000 €/m²)"

- **Useamman vuoden ennusteet** (2027-2030)
  - *Miksi:* Pitkäaikaiset sijoittajat hyötyvät pidemmän aikavälin ennusteista.
  - *Haaste:* Epävarmuus kasvaa jyrkästi jokaista vuotta kohden.
  - *Toteutus:* Käytä malleja, jotka palauttavat useita askelia eteenpäin. Näytä kasvavat luottamusvälit.

- **Mallivertailu ja tarkkuusmetriikat**
  - *Miksi:* Eri mallit sopivat eri alueille. Käyttäjän pitäisi tietää, miten luotettava ennuste on.
  - *Toteutus:* Laske RMSE, MAE, R² vertaamalla 2020-2024 ennusteita todelliseen dataan. Näytä parhaiten toiminut malli per alue.
  - *Esimerkki:* "00100: ARIMA paras (RMSE=142 €/m²), Linear keskinkertainen (RMSE=218 €/m²)"

- **Eksogeniset muuttujat** (ulkoiset tekijät) ✅ Osittain toteutettu
  - *Miksi:* Asuntohintoihin vaikuttavat Euribor-korot, työttömyys, väestönkasvu.
  - *Toteutus:* ✅ Euribor-korot haettu ECB:stä ja käytetty SARIMAX-mallissa. Työttömyys ja väestödata Paavosta saatavilla seuraavaksi.

### 2. Korrelaatioanalyysi ja data-visualisointi

**Tavoite:** Auttaa käyttäjiä ymmärtämään, mitkä tekijät vaikuttavat asuntohintoihin ja nähdä trendejä helpommin.

**Ideat:**

- **Aikasarjakaaviot** (line charts) ✅ Toteutettu
  - *Miksi:* Yksittäisen alueen trendin näkeminen vuosittain on helpompaa viivakaaviosta kuin kartalta.
  - *Toteutus:* Klikkaa postinumeroaluetta kartalla → popupissa "📊 Näytä aikasarja" -nappi → avaa sivupaneelin Chart.js-viivakaavioilla: hintakehitys, kaupat, vuokrat, vuokratuotto, väestö & keski-ikä, tulotaso & työttömyys, ikärakenne, asuntorakenne & hallinta, hinta vs. Euribor. Kaikki huoneistotyypit samassa kaaviossa.
  - *Esimerkki:* "00100: Hinta noussut tasaisesti 2009-2019 (+4.1%/v), romahdus 2020 (-3.2%), elpynyt 2021-2025 (+3.8%/v)."

- **Interaktiivinen korrelaatiomatriisi**
  - *Miksi:* Käyttäjät voivat nähdä nopeasti, mitkä tekijät korreloivat hintojen kanssa.
  - *Toteutus:* Laske Pearsonin korrelaatiot hintadatan, väestödatan ja trendien välillä. Visualisoi lämpökarttana.

- **Palveluindeksin vaikutus hintoihin**
  - *Miksi:* Tutkia korrelaatiota palveluiden määrän ja asuntohintojen välillä.
  - *Toteutus:* Scatter plot palveluindeksi vs. hinta. Näytä regressiosuora.
  - *Hypoteesi:* Alueet, joilla paljon kauppoja ja julkista liikennettä, ovat yleensä kalliimpia.

- **Scatter plot -näkymä** (hajontakuvio)
  - *Miksi:* Visualisoi alueita kahdessa ulottuvuudessa, esim. hinta vs. tulot. Käyttäjä voi tunnistaa outlier-alueita.
  - *Toteutus:* Uusi välilehti "Analyysi". Käyttäjä valitsee X- ja Y-akselin. Jokainen piste = postinumeroalue.

- **Histogrammit** (jakaumat)
  - *Miksi:* Näyttää, miten hinnat jakautuvat koko maassa tai valitussa kaupungissa.
  - *Toteutus:* Laske hintojen frekvenssit bineihin. Visualisoi palkkikaaviossa. Korosta valittu alue.

### 3. Aluevertailu ja benchmarking

**Tavoite:** Mahdollistaa usean alueen vertailu rinnakkain ja samankaltaisten alueiden löytäminen.

**Ideat:**

- **Multi-select aluevertailu** (monen alueen vertailu)
  - *Miksi:* Asunnon ostaja vertaa usein 2-5 aluetta keskenään. "Onko Kallio vai Vallila parempi sijoitus?"
  - *Toteutus:* Shift+klikkaa postinumeroalueita kartalla → valitaan useita. Aukea vertailutaulukko tai rinnakkaiset viivakuviot.

- **Naapurustohaku** (lähialueet)
  - *Miksi:* Auttaa löytämään "piilohelmet" lähellä kalliita alueita.
  - *Toteutus:* Klikkaa aluetta → korosta kaikki alueet 5 km säteellä. Näytä niiden keskihinnat ja trendit.

- **Klusterianalyysi** (samankaltaiset alueet)
  - *Miksi:* "Missä muualla on samankaltainen kehitys kuin Kalliossa?"
  - *Toteutus:* K-means clustering scikit-learn:llä. Klusteroi alueet ryhmiin. Väritä kartta klustereittain.

- **Benchmark-indeksi** (vertailu keskiarvoon)
  - *Miksi:* Näyttää, onko alue yli/ali keskiarvon. Helppo tapa arvioida alueen houkuttelevuutta.
  - *Toteutus:* Laske PK-seudun / koko Suomen keskihinta. Näytä +/- % poikkeama per alue.

### 4. Käyttöliittymäparannukset

**Tavoite:** Parantaa käyttökokemusta ja tehdä kartasta helpommin jaettava.

**Ideat:**

- **✅ Mobiilioptimeinti** (toteutettu 5.3.2026)
  - *Status:* ✅ Toteutettu
  - *Toteutettu:*
    - Hamburger-valikko (☰) piilottaa kontrollit mobiilissa
    - Stats-palkki kelluvana overlay:na kartan päällä
    - Kompakti header (alaotsikot piilotettu mobiilissa)
    - Kartta lähes koko näytön korkuinen (calc(100vh - 50px))
    - Valikko sulkeutuu automaattisesti karttaa klikatessa
    - Haku-kenttä piilotettu mobiilissa hamburger-painikkeen tieltä

- **✅ Animaatioiden alasvetovalikko** (toteutettu 4.3.2026)
  - *Status:* ✅ Toteutettu

- **Jakolinkit** (URL-parametrit) ⭐ Korkea prioriteetti
  - *Miksi:* Käyttäjät haluavat jakaa tarkan näkymän. "Katso tätä aluetta!"
  - *Toteutus:* URL query parameters: `?year=2025&zip=00100&type=0&metric=keskihinta_aritm_nw&zoom=13&lat=60.17&lng=24.94`. JavaScript lukee parametrit sivun latautuessa.

- **Tumma tila** (dark mode)
  - *Miksi:* Vähentää silmien rasitusta hämärässä ja säästää energiaa OLED-näytöillä.
  - *Toteutus:* CSS-muuttujat väreille. CartoDB Dark Matter tiles. Local storage muistaa valinnan.

- **PDF/PNG-vienti** (kartan tallennus)
  - *Miksi:* Karttanäkymien jakaminen raporteissa ja sosiaalisessa mediassa.
  - *Toteutus:* html2canvas-kirjasto tai Leaflet.EasyPrint plugin.

- **Suosikkialueet** (tallennus local storageen)
  - *Miksi:* Asunnon ostaja seuraa 3-5 kiinnostavaa aluetta. Nopea pääsy tallennettuihin alueisiin.
  - *Toteutus:* Tähti-ikoni popup:ssa. LocalStorage tallentaa. Sidebar listaa suosikit.

- **Palveluindeksin mukauttaminen**
  - *Miksi:* Eri käyttäjät arvostavat eri palveluita. Lapsiperheelle päiväkodit tärkeitä, eläkeläiselle kaupat.
  - *Toteutus:* Liukusäätimet jokaiselle palvelukategorialle. Palveluindeksi lasketaan uudelleen dynaamisesti.

### 5. Lisädatan integrointi

**Tavoite:** Rikastaa karttaa ulkopuolisilla tietolähteillä, jotka vaikuttavat asuntohintoihin.

**Ideat:**

- **✅ Palvelutiedot** (toteutettu 4.3.2026)
  - *Status:* ✅ Toteutettu
  - *Ratkaisu:* Geofabrik OSM data + paikallinen parsing (osmium-kirjasto)
  - *Kattavuus:* 1711/3044 postinumeroalueella (56%)
  - *Kategoriat:* ruokakaupat, koulut, päiväkodit, liikuntapaikat, terveysasemat, julkinen liikenne, kirjastot, apteekit

- **Liikennedata** (matka-aika keskustaan) ✅ Toteutettu
  - *Status:* ✅ Toteutettu 6.3.2026
  - *Ratkaisu:* Digitransit API v2 (julkinen liikenne) + Haversine-fallback (laskennallinen auto-arvio). 7 kaupunkikeskustaa. Matka-aika, etäisyys km, lähin keskusta, kulkutapa näkyvissä popupissa.
  - *Kattavuus:* 1723 postinumeroaluetta

- **Uudiskohteet** (rakenteilla olevat asunnot)
  - *Miksi:* Isot rakennusprojektit voivat vaikuttaa alueen hintoihin.
  - *Toteutus:* Rakennetun ympäristön tietojärjestelmä (RYTJ). Merkitse kartalle rakennusprojektit.

- **Kiinteistöverotiedot**
  - *Miksi:* Kiinteistöverokannat vaihtelevat kunnittain (0.93-2.0%).
  - *Toteutus:* Hae kunnat, joihin postinumeroalueet kuuluvat. Kuntaliiton data verokannoista.

- **Ilmanlaatu ja melu** (ympäristötekijät)
  - *Miksi:* Hyvä ilmanlaatu ja alhainen melutaso nostavat asuntojen arvoa.
  - *Toteutus:* HSY ilmanlaatu-API (PK-seutu). PM2.5-pitoisuudet ja dB-tasot postinumeroalueittain.

### 6. Uudet analyysityökalut

**Tavoite:** Tarjota käyttäjille syvempää analyysiä ja henkilökohtaisia suosituksia.

**Ideat:**

- **Postinumeroalueen profiilisivu** ⭐ Korkea prioriteetti
  - *Miksi:* Kaikki tieto yhdestä alueesta yhdessä paikassa: aikasarjakaavio, väestötiedot, palvelut, naapurialueet, ennuste.
  - *Toteutus:* Klikkaa aluetta → avautuu koko näytön modal. Chart.js viivakaaviolle, taulukot tiedoille.
  - *Esimerkki:* "00100 Helsinki: Hinnat, väestö, palvelut, 5v trendi, ennuste — kaikki yhdellä sivulla."

- **"Paras alue minulle" -hakutyökalu** ✅ Toteutettu
  - *Miksi:* Asunnon ostaja tietää budjettinsa ja tarpeensa, mutta ei tunne kaikkia alueita.
  - *Toteutus:* Suodatinpaneeli oikeassa reunassa: kuntavalinta (293 kuntaa), huoneistotyyppivalinta, max neliöhinta (liukusäädin), min väkiluku, palveluvaatimukset (ruokakaupat, koulut, päiväkodit, liikunta, terveys, julk.liikenne, kirjastot, apteekit), min palveluindeksi, max matka-aika keskustaan (0–120 min). Tulokset korostetaan kartalla vihreällä ja listataan paneelissa palveluindeksin mukaan. Klikkaus zoomaa alueelle.
  - *Nappi:* "🔍 Paras alue" -painike kartan vasemmassa alareunassa.

- **Hinta/tulot -suhdekartta** (asumisen kohtuuhintaisuus) ✅ Toteutettu
  - *Miksi:* Absoluuttinen hinta ei kerro kaikkea. Affordable-indeksi (vuosipalkat per asunto) on informatiivisempi.
  - *Toteutus:* Uusi mittari dropdown-valikossa: `keskihinta × 60m² / keskitulot`. Värikartta suhdeluvun mukaan (vihreä < 5 v, punainen > 12 v). Popup näyttää 60m² hinnan, keskitulon ja suhteen vuosissa.
  - *Esimerkki:* "00100: 11.2 vuoden palkat. 90100 (Oulu): 4.8 vuoden palkat."

- **Vuokra vs. osto -vertailu (P/R-ratio)**
  - *Miksi:* Vuokratuotto-% on sijoittajan tärkein mittari. Missä vuokraus on kannattavampaa kuin ostaminen?
  - *Toteutus:* Vuokradata nyt käytössä (`lataa_vuokrat.py`, StatFin asvu_13eb). Laske gross yield = vuosivuokra / ostohinta. Näytä P/R-ratio kartalla uutena mittarina.
  - *Tilanne:* Data valmiina, toteutus seuraavaksi.

- **Inflaatiokorjatut hinnat**
  - *Miksi:* 2009 ja 2025 hinnat eivät ole vertailukelpoisia nimellisarvoina. Reaalihinnat kertovat todellisen kehityksen.
  - *Toteutus:* Hae kuluttajahintaindeksi Tilastokeskuksesta. Deflatoi kaikki hinnat vuoden 2025 euroiksi. Uusi toggle "Nimellinen / Reaalinen".

- **Top 10 -listat** ✅ Toteutettu
  - *Miksi:* Nopea yleiskatsaus kiinnostaviin alueisiin ilman koko kartan selaamista.
  - *Toteutus:* Sivupaneeli vasemmalla: 6 listatyöppä (Kalleimmat, Halvimmat, Eniten nousseet 5v, Eniten laskeneet 5v, Paras vuokratuotto, Parhaat palvelut). Klikkaus zoomaa alueelle ja avaa popupin.
  - *Nappi:* "🏆 Top 10" -painike kartan vasemmassa alareunassa.

- **Service Worker + offline-tuki** (PWA)
  - *Miksi:* Kartta toimisi ilman nettiä latauksen jälkeen. Hyödyllinen esim. asuntonäytöillä.
  - *Toteutus:* Progressive Web App manifest + Service Worker cachettaa karttadatan ja tiilet.

- **Rakennusvuositieto**
  - *Miksi:* Alueen keskimääräinen rakennusvuosi kertoo paljon rakennuskannan laadusta ja remonttitarpeesta.
  - *Toteutus:* Tilastokeskuksen rakennuskanta-data. Laske keskimääräinen rakennusvuosi postinumeroalueittain.

### 7. Uudet kehitysehdotukset (6.3.2026 jälkeen)

Alla olevat ehdotukset perustuvat toteutettuihin ominaisuuksiin ja niiden jatkokehitykseen.

#### A. Ennustemallien jatkokehitys

- **Tulotaso ja väestö SARIMAX-eksogenisinä** ⭐ Korkea prioriteetti
  - *Miksi:* Holly & Jones (1997): tulot ja hinnat ovat yhteisintegroituneita. Mankiw & Weil (1989): työikäinen väestö ennustaa kysyntää.
  - *Toteutus:* Paavo-aikasarjadata (tulot, väestönmuutos-%) jo käytettävissä. Lisää aluetason tulotaso ja väestönmuutos SARIMAX-mallin eksogenisinä muuttujina Euriborin rinnalle.
  - *Odotettu hyöty:* Aluekohtainen ennusteen tarkennus — Euribor vaikuttaa kaikille alueille samalla tavalla, mutta tulotaso ja väestö eriyttävät ennusteet.

- **Ennusteiden backtesting ja tarkkuusmetriikat** ⭐ Korkea prioriteetti
  - *Miksi:* Nyt on 4 ennustemallia mutta ei tietoa kumpi on paras millekin alueelle.
  - *Toteutus:* Jaa data: history (2009-2023) vs. test (2024-2025). Laske RMSE, MAE, MAPE per malli per alue. Näytä kartalla "paras malli" per alue. Popup: "SARIMAX-Euribor paras tällä alueella (RMSE=89 €/m²)".
  - *Bonus:* Ensemble-ennuste (painotettu keskiarvo parhaiden mallien mukaan).

- **Luottamusvälit ennusteille**
  - *Miksi:* Ennusteen epävarmuus on tärkeä tieto. Nyt näytetään vain pisteluku.
  - *Toteutus:* Laske jäännösten keskihajonta historiallisesta datasta. Näytä 80% ja 95% luottamusvälit popupissa ja aikasarjakaaviossa.

- **Prophet/NeuralProphet -malli**
  - *Miksi:* Käsittelee automaattisesti trendien muutoksia ja poikkeavia arvoja.
  - *Toteutus:* `neuralprophet`-kirjasto (kevyempi kuin alkuperäinen Prophet). Tukee regressoreita (Euribor, tulotaso).

#### B. Matka-aikojen jatkokehitys

- **Isokronikartta (matka-aikakerrokset)** ⭐ Korkea prioriteetti
  - *Miksi:* "Missä pääsen töihin alle 30 minuutissa?" on tyypillinen asunnonetsijän kysymys.
  - *Toteutus:* Uusi värikarttataso matka-ajan mukaan. Vihreä ≤20 min, keltainen ≤40 min, oranssi ≤60 min, punainen >60 min. Valittava kohdekaupunki dropdownista.

- **Digitransit API-avaimella tarkka joukkoliikennedata**
  - *Miksi:* Haversine-fallback antaa vain suuntaa-antavan auto-arvion. Oikea joukkoliikenneaika voi olla moninkertainen (erityisesti maaseudulla).
  - *Toteutus:* Rekisteröidy `digitransit.fi/developers`, aseta `DIGITRANSIT_API_KEY`. Skripti tukee jo API:a — vain avain puuttuu.

- **Matka-aika useampiin kohteisiin**
  - *Miksi:* Ei kaikki käy töissä lähimmässä keskustassa.
  - *Toteutus:* Lisää kohteita: yliopistot, lentokentät, suuret työnantajat. Käyttäjä valitsee oman kohteensa kartalla → matka-aika lasketaan lennossa.

#### C. Visualisoinnit ja analyysityökalut

- **Hedoninen hintamalli (regressio)** ⭐ Korkea prioriteetti
  - *Miksi:* Rosen (1974): hinta on ominaisuuksien summa. Nyt on riittävästi piirteitä (~20 muuttujaa per alue).
  - *Toteutus:* OLS-regressio: `hinta ~ tulotaso + palveluindeksi + matka_aika + omistusaste + korkeakoulutetut + kerrostalo_osuus + ...`. Näytä kunkin tekijän euro-osuus popupissa: "Tämän alueen hinnasta 35 % selittyy tulotasolla, 20 % matka-ajalla, 15 % palveluilla…"

- **Bubble detector (yliarvostustunnistin)**
  - *Miksi:* Case & Shiller (1989): hinta vs. fundamentaaliarvo paljastaa mahdolliset kuplat.
  - *Toteutus:* Laske hedonisen mallin `toteutunut_hinta / selitetty_hinta`. Jos suhde > 1.2 → mahdollinen yliarvostus. Väritä kartalla punaiseksi. "00100: Hinta 18% yli fundamentaaliarvon."

- **Multi-select aluevertailu**
  - *Miksi:* Asunnonostaja vertaa tyypillisesti 2–5 aluetta.
  - *Toteutus:* Shift+klikkaa useita alueita → vertailutaulukko: hinta, matka-aika, palveluindeksi, väestörakenne, tulotaso, ennuste rinnakkain.

- **Inflaatiokorjatut hinnat**
  - *Miksi:* 2009 ja 2025 eurot eivät ole vertailukelpoisia.
  - *Toteutus:* Hae kuluttajahintaindeksi Tilastokeskuksesta (StatFin khi). Deflatoi hinnat vuoden 2025 euroiksi. Toggle "Nimellinen / Reaalinen" kartalla.

- **Scatter plot -analyysityökalu**
  - *Miksi:* Visualisoi korrelaatioita: matka-aika vs. hinta, palveluindeksi vs. hinta, tulotaso vs. hinta.
  - *Toteutus:* Uusi välilehti "Analyysi". Käyttäjä valitsee X- ja Y-akselin. Jokainen piste = postinumeroalue. R²-arvo ja regressiosuora näkyviin.

#### D. Datan laajentaminen — uudet datalähteet (kartoitettu 9.3.2026)

Alla olevat lähteet on kartoitettu avoindata.suomi.fi:stä, LIPAS:n API-dokumentaatiosta, SYKE:n paikkatietopalveluista ja StatFin PxWeb-rajapinnasta.

- **LIPAS-liikuntapaikkatiedot** ⭐ Korkea prioriteetti
  - *Miksi:* Virallinen rekisteri, 48 000+ liikuntapaikkaa. Kattavampi kuin OSM erityisesti ulkoilureiteille, frisbeegolf-radoille, uimahalleille.
  - *Toteutus:* `api.lipas.fi/v2/sports-sites` → REST JSON, suora `location.postalCode`-yhdistys. Ei vaadi rekisteröitymistä. Myös WFS/WMS: `lipas.cc.jyu.fi/geoserver`.
  - *Esimerkki:* `curl "https://api.lipas.fi/v2/sports-sites?type-codes=3110&city-codes=91"`
  - *Hyöty:* Liikuntapaikkojen määrä per postinumeroalue → palveluindeksin rikastus, alueen vetovoima

- **YKR-taajama ja yhdyskuntarakenteen aluejako (SYKE)** ⭐ Korkea prioriteetti
  - *Miksi:* Virallinen taajamaluokitus — kaupunkikeskus vs. lähiö vs. maaseutu on vahva hintaselittäjä.
  - *Toteutus:* SYKE WFS-rajapinta → spatial join postinumeroalueille. Dominoiva taajamatyyppi per postinumero.
  - *Hyöty:* Luokittelumuuttuja hintamalleihin ja ennusteisiin. Koko Suomen kattavuus.

- **SeutuRAMAVA — tonttivaranto postinumeroittain (HSY)**
  - *Miksi:* Saiz (2010): tarjontarajoitteet nostavat hintoja. Tonttivaranto kertoo uudistuotantopotentiaalista.
  - *Toteutus:* XLSX-lataus avoindata.suomi.fi:stä. Suoraan postinumeroavaimella. Kentät: rakennusoikeus, käyttöönotettu kerrosala, laskennallinen varanto.
  - *Kattavuus:* Vain PKS (Helsinki, Espoo, Vantaa, Kauniainen). Puolivuosittainen päivitys.

- **Tulvavaaravyöhykkeet (SYKE)**
  - *Miksi:* Tulvariski-osuus alueesta on negatiivinen hintavaikuttaja.
  - *Toteutus:* WMS/ESRI REST `paikkatieto.ymparisto.fi/arcgis/rest/services/Tulva/` → spatial join postinumeroalueille.
  - *Kattavuus:* Koko Suomi. CC BY 4.0.

- **HSY maanpeiteaineisto — viheralueosuus**
  - *Miksi:* Votsis & Perrels (2016): viheralueet +3–5 % Suomessa. Erinomainen ympäristömuuttuja.
  - *Toteutus:* WFS `kartta.hsy.fi/geoserver` → spatial join → viheralueiden osuus postinumeroalueen pinta-alasta.
  - *Kattavuus:* Helsingin seutu.

- **HSY rakennukset — rakennusvuosi ja käyttötarkoitus**
  - *Miksi:* Oikarinen (2015): uudiskohde vs. 1970-luvun talo → 20–35 % hintaero.
  - *Toteutus:* WFS → spatial join → keskimääräinen rakennusvuosi, käyttötarkoitusjakauma per postinumero.
  - *Kattavuus:* Vain PKS.

- **Kiinteistöverotiedot kunnittain**
  - *Miksi:* Kiinteistövero vaihtelee 0.93–2.0 % ja vaikuttaa asumiskustannuksiin.
  - *Toteutus:* Kuntaliiton data → pno→kunta mapping → vero-% jokaiselle postinumeroalueelle.

- **Rakennuskustannusindeksi**
  - *Miksi:* Glaeser & Gyourko (2005): rakennuskustannukset asettavat alarajan hinnoille.
  - *Toteutus:* Tilastokeskus (rki). Yhteinen kaikille → näytä aikasarjakaaviossa hinnan rinnalla.

- **Sotkanet terveys- ja hyvinvointidata (kuntataso)**
  - *Miksi:* Sairastavuusindeksi ja toimeentulotuki kertovat alueen hyvinvoinnista.
  - *Toteutus:* `sotkanet.fi` REST API → ~3000 indikaattoria kuntataso → pno→kunta-yhdistys.

#### E. Käyttöliittymäparannukset

- **Jakolinkit (URL-parametrit)** ⭐ Korkea prioriteetti
  - *Miksi:* "Katso tätä aluetta!" — käyttäjät haluavat jakaa tarkan näkymän.
  - *Toteutus:* URL query: `?year=2025&zip=00100&type=0&metric=keskihinta`. JS lukee parametrit latautuessa.

- **Tumma tila (dark mode)**
  - *Miksi:* Silmien säästö ja OLED-energiansäästö.
  - *Toteutus:* CSS-muuttujat + CartoDB Dark Matter tiilet. LocalStorage muistaa valinnan.

- **PDF/PNG-vienti**
  - *Miksi:* Karttanäkymien jakaminen raporteissa ja somessa.
  - *Toteutus:* html2canvas tai Leaflet.EasyPrint plugin.

- **Palveluindeksin mukauttaminen (käyttäjäkohtaiset painot)**
  - *Miksi:* Lapsiperheelle päiväkodit tärkeitä, eläkeläiselle kaupat.
  - *Toteutus:* Liukusäätimet jokaiselle 9 kategorialle. Indeksi lasketaan uudelleen dynaamisesti selaimessa.

#### F. Tärkeimmät seuraavat kehityskohteet (priorisoitu 9.3.2026)

Alla olevat kohteet on priorisoitu tutkimuskirjallisuuden selitysvoiman, teknisen toteutettavuuden ja datan saatavuuden perusteella.

| # | Kehityskohde | Hyöty | Työmäärä | Riippuvuudet |
|---|-------------|-------|---------|-------------|
| 🥇 | **P/R-ratio kartalle** (hinta/vuokra-suhde) | Sijoittajan tärkein mittari. Brännback & Oikarinen (2019): P/R-ratio kertoo yli/aliarvostuksesta. | Pieni — vuokradata (asvu) ja hinnat jo käytettävissä | Ei uusia datanoutoja |
| 🥇 | **LIPAS-liikuntapaikat** | 48k+ kohdetta, koko Suomi, helppo REST API. Täydentää OSM-palveluindeksiä merkittävästi. | Pieni — suora JSON-nouto postinumeroavaimella | Ei ulkoisia riippuvuuksia |
| 🥇 | **Tulotaso + väestö SARIMAX-eksogenisinä** | Holly & Jones (1997): tulot ja hinnat yhteisintegroituneita. Paavo-data jo käytettävissä. | Keskisuuri — mallipäivitys laske_ennusteet.py | Paavo-aikasarja |
| 🥈 | **Ennusteiden backtesting** | Nyt 4 mallia ilman tarkkuustietoa. RMSE/MAE/MAPE per malli per alue → käyttäjä tietää mikä malli on paras. | Keskisuuri — retroennusteet 2009-2023 → vertailu 2024-2025 | Ei uusia datanoutoja |
| 🥈 | **YKR-taajamaluokitus (SYKE)** | Koko Suomi, vahva hintaselittäjä: kaupunkikeskus/lähiö/maaseutu. Uusi kategorinen muuttuja. | Keskisuuri — WFS-nouto + spatial join | SYKE WFS, shapely |
| 🥈 | **Hedoninen regressio popupiin** | Rosen (1974): hinta = osien summa. Nyt ~20 muuttujaa per alue → OLS-malli → "35% tulotasosta, 20% matka-ajasta". | Keskisuuri | Kaikki nykyiset muuttujat |
| 🥈 | **Jakolinkit (URL-parametrit)** | Käyttäjät haluavat jakaa näkymiä: `?year=2025&zip=00100`. Parantaa käyttökokemusta merkittävästi. | Pieni — JS-muutos kartta_polygon.py | Ei datanoutoja |
| 🥉 | **Tulvavaaravyöhykkeet (SYKE)** | Koko Suomi, riskimuuttuja. Negatiivinen hintavaikutus. | Keskisuuri — WMS/ESRI REST + spatial join | SYKE palvelut, shapely |
| 🥉 | **Inflaatiokorjatut hinnat** | 2009 ja 2025 eurot eivät ole vertailukelpoisia. KHI Tilastokeskuksesta. | Pieni — StatFin API + deflatointi | StatFin khi |
| 🥉 | **Luottamusvälit ennusteille** | Pisteluku ilman epävarmuutta on puutteellinen. 80/95% luottamusvälit. | Pieni-keskisuuri | Ei uusia datanoutoja |

**Osallistu kehitykseen!** Ehdotuksia ja pull requestejä otetaan vastaan mielellään.

---

## Kirjallisuuskatsaus: Asuntojen ja vuokrien hintoja selittävät tekijät

Asuntomarkkinoiden hinnanmuodostus on laajasti tutkittu aihe taloustieteessä. Alla on kooste keskeisistä tutkimuksista ja teorioista, jotka selittävät asuntojen osto- ja vuokrahintojen vaihtelua.

### 1. Sijainti ja saavutettavuus

Asuntomarkkinoiden perusteorian mukaan sijainti on tärkein yksittäinen hintaselittäjä.

- **Alonso-Muth-Mills -malli** (Alonso, 1964; Muth, 1969; Mills, 1972): Monosentrinen kaupunkimalli, jossa asuntojen hinnat laskevat etäisyyden kasvaessa keskustasta. Asukkaiden on valittava halvemman asumisen ja pidempien matka-aikojen välillä (*bid-rent curve*).
- **Debrezion, Pels & Rietveld (2007)**: Meta-analyysi 57 tutkimuksesta osoitti, että joukkoliikenneasemien läheisyys nostaa asuntojen hintoja keskimäärin 2–4 % (rautatieasema) ja 1–2 % (bussipysäkki) alueesta riippuen.
- **Laakso (1997)**: Suomessa saavutettavuus Helsingin keskusta-alueelle on merkittävin yksittäinen hintaselittäjä pääkaupunkiseudulla. 10 min lyhyempi matka-aika nostaa neliöhintaa n. 5–8 %.

### 2. Hedoninen hinnoittelu — asunnon ja alueen ominaisuudet

- **Rosen (1974)**: *Hedonic pricing* -teoria, jonka mukaan asunnon hinta muodostuu osiensa summana: sijainti, koko, kunto, kerros, rakennusvuosi, piha, parveke jne. Jokainen ominaisuus antaa marginaalisen lisäarvon.
- **Sirmans, Macpherson & Zietz (2005)**: Kattava meta-analyysi hedonisista hintatutkimuksista. Merkittävimmät selittäjät: pinta-ala (+), huoneiden lukumäärä (+), ikä (−), kunto (+), autotalli (+), uima-allas (+), ilmastointi (+). Huoneiston koko selittää tyypillisesti 30–50 % hinnan vaihtelusta.
- **Oikarinen (2015)**: Suomessa asunnon ikä, kunto ja kerros vaikuttavat merkittävästi. Uudiskohde vs. 1970-luvun talo: hintaero jopa 20–35 % samalla sijainnilla.

### 3. Makrotaloudelliset tekijät

#### 3.1 Korot ja rahapolitiikka
- **Himmelberg, Mayer & Sinai (2005)**: Korot ovat asuntohintojen tärkein makrotason selittäjä. 1 %-yksikön koronnousu laskee hintoja n. 5–10 % pitkällä aikavälillä.
- **Oikarinen (2009)**: Suomessa 12 kk euriborin muutokset selittävät merkittävän osan lyhyen aikavälin hintavaihteluista. Matala korkotaso 2010-luvulla selittää hintojen nousua erityisesti kasvukeskuksissa.

#### 3.2 Tulot ja työllisyys
- **Holly & Jones (1997)**: Reaalipalkat ja asuntohinnat ovat pitkän aikavälin yhteisintegroituneita — tulokehitys on hintojen fundamentaali perusta.
- **Mankiw & Weil (1989)**: Työikäisen väestön (25–44 v) määrä ennustaa asuntokysyntää. Suuren ikäluokan perheenperustamisvaihe nosti hintoja 1970–90-luvuilla.
- **Laakso & Loikkanen (2004)**: Suomessa tulotaso selittää kaupunkien välisiä hintaeroja parhaiten. Helsinki–Oulu -hintaero selittyy pitkälti tulotasoerolla.

#### 3.3 Inflaatio ja rakennuskustannukset
- **Glaeser & Gyourko (2005)**: Rakennuskustannukset asettavat alarajan asuntohinnoille. Kalliilla alueilla hintaero rakennuskustannuksiin nähden selittyy maan hinnalla ja sääntelyllä. Esim. Manhattanilla rakennuskustannus on vain 50 % myyntihinnasta.

### 4. Tarjonta ja sääntely

- **Saiz (2010)**: Maankäytön sääntely ja maantieteelliset rajoitteet (meri, järvet, jyrkät rinteet) rajoittavat tarjontaa ja nostavat hintoja. Tarjontajousto on tärkein yksittäinen tekijä joka erottaa korkean ja matalan hintakasvun kaupungit.
- **Glaeser, Gyourko & Saks (2005)**: Tiukka kaavoitus nostaa asuntojen hintoja 20–50 % verrattuna vapaan kaavoituksen alueisiin. Pelkkä maapolitiikka selittää merkittävän osan Kalifornian ja Teksasin hintaerosta.
- **Oikarinen, Peltola & Valtonen (2015)**: Suomessa kaavoitusprosessin hitaus rajoittaa asuntotuotantoa erityisesti pääkaupunkiseudulla. Tonttimaan niukkuus Helsingissä nostaa hintoja.

### 5. Väestörakenne ja muuttoliike

- **Tervo (2000)**: Suomen sisäinen muuttoliike suuntautuu kasvukeskuksiin, mikä nostaa hintoja kohdealueilla ja laskee lähtöalueilla. 1990-luvun muuttoliike selittää hintojen eriytymistä maakuntien välillä.
- **Aro (2007)**: Kaupungistuminen ja erityisesti nuorten ikäluokkien muutto yliopisto- ja kasvukaupunkeihin ajaa hintakehitystä. Muuttotappiokunnissa hinnat laskevat tai stagnoivat.
- **Eurostat (2020)**: EU-tasolla väestönkasvu on merkittävin pitkän aikavälin asuntohintojen selittäjä. 1 % väestönlisäys → 1,5–2 % hinnannousu.

### 6. Palvelut ja alueen vetovoimatekijät

- **Black (1999)**: Koulun laatu nostaa asuntojen hintoja. Yhdysvalloissa koulupiirin rajan ylittäminen parempaan koulupiiriin nostaa hintoja 2–5 %. Vaikutus todettu myös mm. Isossa-Britanniassa (Gibbons & Machin, 2003) ja Suomessa (Harjunen ym., 2018).
- **Gibbons (2004)**: Rikollisuus laskee hintoja. 10 % vähemmän rikoksia → 1–3 % korkeammat hinnat.
- **Pope & Pope (2015)**: Ravintoloiden, kahviloiden ja kauppojen läheisyys nostaa hintoja. "Walkability" (käveltävyys) on viime vuosina korostunut hintaselittäjänä.
- **Votsis & Perrels (2016)**: Suomessa viheralueiden läheisyys nostaa hintoja erityisesti kaupunkialueilla 3–5 %.

### 7. Vuokrien erityistekijät

Vuokramarkkinat noudattavat pääosin samoja hintatekijöitä kuin omistusasuntomarkkinat, mutta joitakin eroja on:

- **DiPasquale & Wheaton (1996)**: *Four-quadrant model* — vuokrat määräytyvät ensisijaisesti kysynnän (tulot, väestö, työllisyys) ja tarjonnan (rakennuskanta) tasapainosta. Omistushinnat reagoivat lisäksi korkoihin ja tuotto-odotuksiin.
- **Arnott (1987)**: Vuokrien sopeutuminen on hitaampaa kuin omistushintojen, koska vuokrasopimukset ovat kiinteitä (tyypillisesti 1 vuosi). Uudet vuokrasopimukset reagoivat nopeammin markkinamuutoksiin kuin uusittavat.
- **Eerola & Saarimaa (2018)**: Suomessa ARA-vuokra-asunnot ja vapaarahoitteiset vuokra-asunnot muodostavat erilliset segmentit. Vuokrasääntely vaikuttaa tarjontaan.
- **Brännback & Oikarinen (2019)**: Suomessa vuokrien ja omistushintojen suhde (P/R-ratio) vaihtelee merkittävästi: Helsinki ~25–30, muut kasvukeskukset ~15–20, maaseutu ~10–12. Korkea suhdeluku indikoi spekulatiivista kysyntää tai matalia korkoja.

### 8. Yhteenveto: Hintaselittäjien hierarkia

Tutkimuskirjallisuuden perusteella asuntojen ja vuokrien hintoja selittävät tekijät voidaan ryhmitellä vaikuttavuusjärjestykseen:

| Sija | Tekijä | Selitysvoima | Keskeinen lähde |
|------|--------|-------------|-----------------|
| 1 | **Sijainti ja saavutettavuus** | Erittäin suuri | Alonso (1964), Laakso (1997) |
| 2 | **Alueen tulotaso ja työllisyys** | Suuri | Holly & Jones (1997) |
| 3 | **Korkoympäristö** | Suuri (syklinen) | Himmelberg ym. (2005) |
| 4 | **Asunnon ominaisuudet** (koko, ikä, kunto) | Suuri | Rosen (1974), Sirmans ym. (2005) |
| 5 | **Tarjontarajoitteet ja kaavoitus** | Merkittävä | Saiz (2010), Glaeser ym. (2005) |
| 6 | **Väestönkasvu ja muuttoliike** | Merkittävä | Tervo (2000), Mankiw & Weil (1989) |
| 7 | **Palvelut** (koulut, liikenne, kaupat) | Kohtalainen | Black (1999), Pope & Pope (2015) |
| 8 | **Ympäristötekijät** (viheralueet, melu, rikollisuus) | Kohtalainen | Gibbons (2004), Votsis (2016) |
| 9 | **Spekulaatio ja odotukset** | Syklinen | Case & Shiller (1989) |

### Relevanssi tälle projektille

Tässä hintakarttaprojektissa mitataan useita näistä tekijöistä:
- ✅ **Sijainti** — postinumeroalueet, kaupunkinavigointi, matka-aika keskustaan (7 kaupunkia)
- ✅ **Tulotaso** — Paavo-tietokannan keskitulot, hinta/tulot-suhde, tuloluokat
- ✅ **Väestö** — väkiluku, keski-ikä, ikärakenne (20 ikäryhmää), muuttoliike (väestönmuutos-%)
- ✅ **Palvelut** — 11 kategoriaa OSM-datasta, palveluindeksi (tiheys/km², log-skaalaus)
- ✅ **Työllisyys** — työttömyysaste Paavosta, 26 toimialaa
- ✅ **Korkoympäristö** — 12 kk Euribor (ECB, 2005–2026), SARIMAX-ennustemalli
- ✅ **Asuntorakenne** — kerrostalo/pientalo-osuus, keskipinta-ala, omistus/vuokra
- ✅ **Koulutustaso** — korkeakoulutetut-%, koulutusastejakauma
- ⬜ **Asunnon ominaisuudet** — ei saatavilla aggregaattitasolla
- ⬜ **Kaavoitus ja tarjonta** — ei dataa saatavilla

---

## 📊 Tutkimus: Saatavilla oleva postinumerotason data Suomesta

Kattava kartoitus kaikista avoimista ja puoliavoimista datalähteistä, jotka tarjoavat tietoa postinumeroalueittain tai jotka voidaan yhdistää postinumeroalueisiin. Tutkimus tehty 5.3.2026.

### 1. Tilastokeskus: Paavo-tietokanta (WFS API) ⭐ Ensisijainen lähde

**URL:** `https://geo.stat.fi/geoserver/postialue/wfs` (layer `pno_tilasto_XXXX`)
**Aikasarja:** 2010–2024 (päivittyy tammikuussa)
**Postinumeroalueita:** ~3 019
**Kenttiä:** 113 per vuosi
**Lisenssi:** CC BY 4.0 (avoin)

| Tietoryhmä | Etuliite | Kenttiä | Esimerkkimuuttujat |
|-----------|---------|--------|-------------------|
| **Asukasrakenne** | `he_` | 24 | `he_vakiy` (väkiluku), `he_kika` (keski-ikä), `he_miehet`, `he_naiset`, 20 ikäryhmää (0–2, 3–6, 7–12, …, 80–84, 85+) |
| **Koulutusaste** | `ko_` | 7 | `ko_ika18y` (18+ asukkaat), `ko_perus` (perusaste), `ko_ammat` (ammattikoulutus), `ko_yl_kork` (ylempi korkeakoulututkinto), `ko_al_kork` (alempi kk), `ko_yliop` (tutkijakoulutus), `ko_koul` (koulutustiedot yhteensä) |
| **Asukkaiden tulot** | `hr_` | 7 | `hr_mtu` (asuntokuntien mediaanitulot), `hr_ktu` (keskitulot), `hr_ovy` (tulot yhteensä), `hr_pi_tul` (pienituloiset), `hr_ke_tul` (keskituloiset), `hr_hy_tul` (hyvätuloiset) |
| **Talouksien tulot** | `tr_` | 7 | `tr_mtu` (talouksien mediaanitulot), `tr_ktu` (keskitulot), `tr_kuty` (taloustyyppi), `tr_pi_tul`, `tr_ke_tul`, `tr_hy_tul`, `tr_ovy` |
| **Talouksien koko ja elämänvaihe** | `te_` | 17 | `te_taly` (talouksia yht.), `te_yks` (yksinasuvat), `te_nuor` (nuoret), `te_laps` (lapsiperheet), `te_klap` (kouluikäiset lapset), `te_aklap` (aikuisten lapsiperheet), `te_elak` (eläkeläistaloudet), `te_omis_as` (omistusasunnot), `te_vuok_as` (vuokra-asunnot), `te_takk` (talouden keskikoko), `te_as_valj` (asumisväljyys m²/hlö) |
| **Rakennukset ja asunnot** | `ra_` | 9 | `ra_raky` (rakennuksia yht.), `ra_asrak` (asuinrakennuksia), `ra_asunn` (asuntoja yht.), `ra_kt_as` (kerrostaloasuntoja), `ra_pt_as` (pientaloasuntoja), `ra_muu_as` (muita asuntoja), `ra_ke` (kesämökkejä), `ra_muut` (muut rakennukset), `ra_as_kpa` (asuntojen keskipinta-ala m²) |
| **Työpaikat toimialoittain** | `tp_` | 26 | `tp_tyopy` (työpaikkoja yht.), `tp_alku_a` (alkutuotanto), `tp_c_teol` (teollisuus), `tp_f_rake` (rakentaminen), `tp_g_kaup` (kauppa), `tp_h_kulj` (kuljetus), `tp_i_majo` (majoitus/ravintola), `tp_j_info` (ICT), `tp_k_raho` (rahoitus), `tp_m_erik` (erikoispalvelut), `tp_p_koul` (koulutus), `tp_q_terv` (terveys) + 14 muuta toimialaa |
| **Pääasiallinen toiminta** | `pt_` | 7 | `pt_vakiy` (väestö yht.), `pt_tyoll` (työlliset), `pt_tyott` (työttömät), `pt_opisk` (opiskelijat), `pt_elakel` (eläkeläiset), `pt_muut` (muut), `pt_0_14` (0–14-vuotiaat) |
| **Sijainti ja geometria** | — | 4 | `euref_x/y` (koordinaatit), `pinta_ala` (m²), `kunta` (kuntakoodi) |

**Käytössä projektissa:** Kaikki 113 kenttää + 8 johdettua muuttujaa (lapset_osuus, työikäiset_osuus, eläkeikäiset_osuus, omistusaste, vuokra_aste, korkeakoulutetut_osuus, kerrostalo_osuus, tp_palvelut_osuus, tp_ict_osuus)

### 2. Tilastokeskus: StatFin-tietokannat (PxWeb API)

#### 2a. Osakeasuntojen hinnat ✅ Käytössä
**Taulukko:** `ashi_13mu` (vuosittain) + `ashi_13mt` (neljännesvuosittain)
**Aikasarja:** 2009–2025
**Muuttujat:** neliöhinta (€/m²), kauppojen lukumäärä
**Luokittelu:** postinumeroalue × talotyyppi (kerrostalo yksiöt/kaksiot/kolmiot+, rivitalot)

#### 2b. Vuokrat postinumeroalueittain ✅ Käytössä
**Taulukko:** `asvu_13eb`
**Aikasarja:** 2015Q1–2025Q4
**Muuttujat:** vapaarahoitteisten vuokra-asuntojen keskineliövuokra (€/m²/kk)
**Luokittelu:** postinumeroalue × huoneluku × neljännes

#### 2c. Vuokraindeksi (alueittain, EI postinumerotasolla)
**Taulukko:** `asvu_11x4` / `asvu_11x5`
**Taso:** suuret kaupungit ja seutukunnat

### 3. OpenStreetMap (Geofabrik) ✅ Käytössä
**Tiedosto:** `finland-latest.osm.pbf` (~676 MB)
**Parseri:** osmium (Python pyosmium)
**Postinumerotasolle yhdistäminen:** point-in-polygon tarkistus

**Käytössä olevat tagit:**
| Kategoria | OSM-tagi |
|-----------|----------|
| Ruokakaupat | `shop=supermarket`, `shop=convenience` |
| Koulut | `amenity=school` |
| Päiväkodit | `amenity=kindergarten` |
| Liikuntapaikat | `leisure=fitness_centre`, `leisure=sports_centre` |
| Terveysasemat | `amenity=doctors`, `amenity=clinic`, `amenity=hospital` |
| Julkinen liikenne | `highway=bus_stop`, `railway=station/tram_stop/halt` |
| Ravintolat | `amenity=restaurant` |
| Kahvilat | `amenity=cafe`, `amenity=bar` |
| Puistot | `leisure=park` |
| Kirjastot | `amenity=library` |
| Apteekit | `amenity=pharmacy` |

**Lisäksi saatavilla OSM:stä (ei vielä käytössä):**
| Kategoria | OSM-tagi | Relevanssi hintakarttaan |
|-----------|----------|------------------------|
| Ravintolat/kahvilat | `amenity=restaurant`, `amenity=cafe`, `amenity=bar` | ✅ Toteutettu 6.3.2026 |
| Puistot/viheralueet | `leisure=park`, `natural=wood`, `landuse=forest` | ✅ Puistot toteutettu, metsät ei vielä |
| Kirjastot | `amenity=library` | ✅ Toteutettu 9.3.2026 |
| Apteekit | `amenity=pharmacy` | ✅ Toteutettu 9.3.2026 |
| Pankit/pankkiautomaatit | `amenity=bank`, `amenity=atm` | Matala |
| Elokuvateatterit | `amenity=cinema` | Matala — vapaa-ajan palvelut |
| Kirkot/uskonnolliset | `amenity=place_of_worship` | Matala |
| Parkkipaikat | `amenity=parking` | Matala — autoistumisaste |
| Latauspisteet | `amenity=charging_station` | Nouseva — sähköautot |
| Uimapaikat | `leisure=swimming_pool`, `natural=beach` | Matala |

### 4. LIPAS — Liikuntapaikkatietojärjestelmä ⭐ Seuraava integroitava
**REST API:** `https://api.lipas.fi/v2/sports-sites` (ei vaadi rekisteröitymistä)
**GeoServer:** `http://lipas.cc.jyu.fi/geoserver` (WFS/WMS)
**GitHub:** `https://github.com/lipas-liikuntapaikat/lipas`
**Ylläpitäjä:** Jyväskylän yliopisto, liikuntatieteiden tiedekunta / OKM
**Sisältö:** 48 000+ liikuntapaikkaa koko Suomessa
**Kenttä:** `location.postalCode` — suora postinumeroyhdistys
**Tyypit:** uimahallit, jäähallit, kuntosalit, liikuntasalit, urheilukentät, ulkoilureitit, ladut, uimarannat, frisbeegolf-radat, hiihtoputket ym.
**Esimerkki:** `curl "https://api.lipas.fi/v2/sports-sites?type-codes=3110&city-codes=91"` (uimahallit Helsingissä)
**Lisenssi:** CC BY 4.0
**Etu OSM:ään verrattuna:** Virallinen rekisteri, kattavampi erityisesti ulkoilureiteille, frisbeegolf-radoille ja erikoisliikuntapaikoille. Päivittyy jatkuvasti kuntien ilmoitusten perusteella.

### 5. Digitransit — Joukkoliikennedata
**URL:** `https://api.digitransit.fi/` (rekisteröinti vaaditaan)
**Kattavuus:** HSL (PK-seutu), Waltti (Tampere, Turku, Oulu, Kuopio, Lahti, Joensuu ym.), VR
**Data:**
- **Reittisuunnittelu:** matka-aika pisteestä A pisteeseen (julkinen liikenne, kävely, pyöräily)
- **Pysäkit:** kaikki joukkoliikennepysäkit sijainteineen
- **GTFS-syötteet:** aikatauludata, reittien geometriat
**Postinumerotasolle:** Laske matka-aika postinumeron centroidista keskustaan → matka-aikaindeksi
**Relevanssi:** Erittäin korkea — Alonso (1964), Laakso (1997): saavutettavuus on #1 hintaselittäjä

### 6. THL Sotkanet — Terveys- ja hyvinvointidata
**URL:** `https://sotkanet.fi/sotkanet/fi/api/`
**Taso:** Kunta ja hyvinvointialue (EI postinumero)
**Indikaattoreita:** ~3 000 (terveys, sosiaalipalvelut, hyvinvointi)
**Esimerkkejä:** sairastavuusindeksi, toimeentulotuki, lastensuojeluilmoitukset, mielenterveysindeksi
**Postinumerotasolle:** Yhdistettävissä kuntakoodin kautta (pno → kunta → Sotkanet), mutta tuo vain kuntatason tarkkuutta

### 7. Verohallinto / Kuntaliitto — Verotiedot
**Taso:** Kunta
**Data:**
- Kiinteistöveroprosentit (yleinen, vakituinen asunto, muu asunto, rakentamaton tontti)
- Kunnallisvero-% 
**Postinumerotasolle:** pno → kunta mapping — kaikilla saman kunnan postinumeroilla sama arvo
**URL:** `https://www.kuntaliitto.fi/talous/kiinteistoveroprosentit`

### 8. Suomen Pankki / EKP — Makrodata
**Taso:** Koko Suomi (ei alueellista)
**Data:**
| Muuttuja | Lähde | Relevanssi |
|----------|-------|-----------|
| 12 kk Euribor | Suomen Pankki | Erittäin korkea — ennustemallien input |
| Asuntolainakannan kasvu | SP rahoitustilastot | Korkea |
| Kuluttajahintaindeksi | Tilastokeskus (khi) | Korkea — inflaatiokorjaus |
| Rakennuskustannusindeksi | Tilastokeskus (rki) | Keskitaso |
**Postinumerotasolle:** Yhteinen kaikille alueille → käytettävissä aikasarjamallien eksogenisenä muuttujana

### 9. Poliisi — Rikostilastot
**Taso:** Kunta / alue / poliisilaitos
**Data:** Rikosilmoitukset tyypeittäin (varkaudet, pahoinpitelyt, huumausainerikokset jne.)
**URL:** PolStat-palvelu
**Postinumerotasolle:** Vain kuntatason yhdistys. Gibbons (2004): rikostaso vaikuttaa asuntohintoihin −1–3 %.

### 10. Ilmatieteen laitos (FMI) — Ympäristödata
**URL:** `https://opendata.fmi.fi/wfs`
**Data:** Lämpötila, tuuli, sademäärä, auringonpaiste, ilmanlaatu (PM2.5, NO2)
**Taso:** Mittausasemakohtainen (n. 400 asemaa)
**Postinumerotasolle:** Interpolointi lähimmästä asemasta tai IDW-kerroin → likimääräinen
**Lisenssi:** CC BY 4.0

### 11. HSY — Pääkaupunkiseutu (Helsinki, Espoo, Vantaa, Kauniainen)
**URL:** `https://kartta.hsy.fi/geoserver/wfs`
**Data:** Ilmanlaatu, melualueet, viheralueet, energiankulutus, jätehuolto
**Taso:** Karttapohjainen (yhdistettävissä postinumeroon spatial join)
**Rajoitus:** Vain PK-seutu

### 12. Maanmittauslaitos (MML) — Maastotiedot
**URL:** `https://www.maanmittauslaitos.fi/kartat-ja-paikkatieto/asiantuntevalle-kayttajalle/tuotekuvaukset/maastotietokanta`
**Data:** Maasto, vesistöt, korkeusmalli, rakennukset (geometria), tiestö
**Lisenssi:** CC BY 4.0 (avoin)
**Postinumerotasolle:** Spatial join — esim. vesirajapituus, metsäpinta-ala, korkeuserot
**Relevanssi:** Matala–keskitaso

### 13. Traficom — Liikennedata
**Data:** Ajoneuvokanta, liikenneonnettomuudet, liikenneverkot
**Taso:** Kunta (ajoneuvotilasto), tie-elementti (onnettomuudet)
**Postinumerotasolle:** Ajoneuvotilasto vain kuntatasolla

### 14. Posti — Postinumerorekisteri
**URL:** `https://www.posti.fi` (CSV-lataus)
**Data:** Postinumero, nimi (fi/sv), kunta, maakunta, tyyppi (normaali/PL)
**Käyttö:** Metatietojen rikastus (kuntatieto, maakunta)

### 15. SeutuRAMAVA — Tonttivaranto postinumeroalueittain (HSY) ⭐ Uusi
**URL:** `https://avoindata.suomi.fi/data/fi/dataset/paakaupunkiseudun-tonttivaranto-postinumeroalueittain-seuturamava`
**Lataus:** XLSX-tiedostot (puolivuosittain, 2020–2025)
**Ylläpitäjä:** Helsingin seudun ympäristöpalvelut (HSY)
**Sisältö:** Asemakaavavaranto postinumeroittain:
- `kala` — rakennusoikeus (kerrosneliömetrit)
- `karaas` — käyttöönotettu asuinkerrosala
- `karamu` — käyttöönotettu muu kuin asuinkerrosala
- `laskvar_ak` — laskennallinen kerrostalovaranto
- `laskvar_ap` — laskennallinen pientalovaranto
- `laskvar_k` — laskennallinen liike- ja toimistotilavaranto
- `rakerayht` — rakenteilla oleva kerrosala yhteensä

**Kattavuus:** Vain pääkaupunkiseutu (Helsinki, Espoo, Vantaa, Kauniainen)
**Lisenssi:** CC BY 4.0
**Hyöty:** Suoraan postinumerotasolla. Tonttivaranto kertoo uudistuotantopotentiaalista → Saiz (2010): tarjontarajoitteet nostavat hintoja.
**Prioriteetti:** ⭐⭐ Keskikorkea — vain PKS, mutta erittäin relevantti hintaselittäjä.

### 16. SYKE — Tulvavaaravyöhykkeet ⭐ Uusi
**URL:** `https://paikkatieto.ymparisto.fi/arcgis/rest/services/Tulva/` (WMS/WCS/ESRI REST + ZIP-lataus)
**Ylläpitäjä:** Suomen ympäristökeskus (SYKE)
**Sisältö:** Vesistö- ja meritulvien vaarakartat eri todennäköisyyksillä (1/20a, 1/50a, 1/100a, 1/250a, 1/1000a), merkittävät tulvariskialueet
**Kattavuus:** Koko Suomi
**Lisenssi:** CC BY 4.0
**Postinumerotasolle:** Spatial join — laske tulvavaaravyöhykkeen osuus postinumeroalueen pinta-alasta
**Hyöty:** Tulvariski on negatiivinen hintavaikuttaja. Turvalliset rakentamiskorkeudet + riskialueet.
**Prioriteetti:** ⭐⭐ Keskikorkea — koko Suomi, vaatii spatiaalianalyysiä.

### 17. SYKE — YKR-taajama ja yhdyskuntarakenteen aluejako ⭐ Uusi
**URL:** SYKE:n kansallinen WFS-rajapinta (`paikkatieto.ymparisto.fi`)
**Avoindata:** `https://avoindata.suomi.fi/data/fi/dataset/ykr-taajama`
**Ylläpitäjä:** Suomen ympäristökeskus (SYKE)
**Sisältö:**
- **YKR-taajama** — Suomen virallinen taajamarajaus (Tilastokeskuksen käyttämä), 250m × 250m ruutupohjaisesti
- **Harva/tiheä taajama-alue** — tiheä taajama ≈ rakennettu asemakaavoitettu alue, harva = väljempi
- **Yhdyskuntarakenteen aluejako** — kaupunkikeskus, kaupungin kehysalue, maaseudun paikalliskeskus, kaupungin läheinen maaseutu jne.

**Kattavuus:** Koko Suomi
**Lisenssi:** CC BY 4.0
**Postinumerotasolle:** Spatial join — dominoiva taajamatyyppi per postinumeroalue
**Hyöty:** Taajamatyyppi (kaupunkikeskus vs. lähiö vs. maaseutu) on vahva hintaselittäjä. Luokittelumuuttuja hintamalleihin.
**Prioriteetti:** ⭐⭐⭐ Korkea — koko Suomi, vahva selittävä muuttuja.

### 18. FMI-ENFUSER / HSY — Ilmanlaatu ⭐ Uusi
**URL (FMI):** `https://opendata.fmi.fi/wfs` — ENFUSER-malli kaupunkialueille
**URL (HSY):** `https://kartta.hsy.fi/geoserver/wfs` — NO₂ vuosiraja-arvon ylitysalueet, mittausasemat
**Ylläpitäjä:** Ilmatieteen laitos (FMI) / Helsingin seudun ympäristöpalvelut (HSY)
**Sisältö:**
- FMI-ENFUSER: NO₂, PM2.5, PM10 pitoisuudet kaupunkialueilla suurella erotuskyvyllä
- HSY: typpidioksidin vuosiraja-arvon ylitysalueet PKS:llä, mittauspisteet ja pitoisuudet (2004–2024)

**Kattavuus:** Pääkaupunkiseutu (HSY, tarkka), koko Suomi (FMI, karkeampi)
**Lisenssi:** CC BY 4.0
**Postinumerotasolle:** Spatial join — keskimääräinen pitoisuus tai ylitysalueen osuus postinumeroalueesta
**Hyöty:** Ilmanlaatu vaikuttaa hintoihin: tutkitusti −1..5 % NO₂-ylitysalueella. Votsis & Perrels (2016).
**Prioriteetti:** ⭐ Matala-keskikorkea — vain kaupungit, vaatii spatiaalianalyysiä.

### 19. Helsingin seudun aluesarjat (PxWeb / WFS) ⭐ Uusi
**URL (PxWeb):** `https://stat.hel.fi/pxweb/fi/Aluesarjat/` (JSON-rajapinta)
**URL (WFS):** Avoinluvut-aineisto WFS-rajapintana
**Avoindata:** `https://avoindata.suomi.fi/data/fi/dataset/helsingin-seudun-aluesarjat-tilastotietokannan-tiedot-paikkatietona`
**Ylläpitäjä:** Helsingin kaupunginkanslia / Kaupunkitieto
**Sisältö:** Helsinki/Espoo/Vantaan osa-alueittaiset tilastot:
- Asuminen: asuntokanta, asuntotuotanto, hinnat, vuokrat
- Väestö: ikärakenne, äidinkieli, muuttoliike
- Koulutus: koulutusaste, oppilaitokset
- Tulot: tulotaso, tuloluokat
- Työmarkkinat: toimiala, työssäkäynti, työttömyys
- Rakentaminen: uudistuotanto, rakennusluvat

**Kattavuus:** Helsingin seutu (14 kuntaa), osa-alue-/piiri-/postinumerotaso
**Lisenssi:** CC BY 4.0
**Hyöty:** Yksityiskohtaisempaa dataa kuin Paavo (muuttoliike, asuntotuotanto). Erityisesti muuttoliike-data on arvokas — Tervo (2000): muuttoliike selittää hintaeroja.
**Prioriteetti:** ⭐⭐ Keskikorkea — vain Helsinki-seutu, mutta se kattaa suurimman markkinan.

### 20. HSY — Pääkaupunkiseudun rakennukset ⭐ Uusi
**URL:** `https://kartta.hsy.fi/geoserver/wfs` (WFS/WMS)
**Avoindata:** `https://avoindata.suomi.fi/data/fi/dataset/paakaupunkiseudun-rakennukset`
**Sisältö:** Rakennustason tietoja: rakennusvuosi, käyttötarkoitus, kerrosala, geometria
**Kattavuus:** Helsinki, Espoo, Vantaa, Kauniainen
**Lisenssi:** CC BY 4.0
**Postinumerotasolle:** Spatial join → tarkka rakennuskannan ikäjakauma ja käyttötarkoitusjakauma per postinumero
**Hyöty:** Oikarinen (2015): uudiskohde vs. 1970-luvun talo → 20–35 % hintaero. Keskimääräinen rakennusvuosi postinumeroalueella on vahva hintaselittäjä.
**Prioriteetti:** ⭐⭐ Keskikorkea — vain PKS, mutta erittäin tarkka tieto.

### 21. HSY — Maanpeiteaineisto ⭐ Uusi
**URL:** `https://kartta.hsy.fi/geoserver/wfs` (WFS/WMS)
**Avoindata:** `https://avoindata.suomi.fi/data/fi/dataset/paakaupunkiseudun-maanpeiteaineisto`
**Sisältö:** Maanpinta luokiteltu: tiet ja rakennukset, muu vettä läpäisemätön pinta, vettä läpäisevä pinta, kasvillisuusluokat (matala/keskikorkea/korkea), avokalliot
**Kattavuus:** Helsingin seutu
**Lisenssi:** CC BY 4.0
**Postinumerotasolle:** Spatial join — viheralueiden osuus postinumeroalueen pinta-alasta
**Hyöty:** Viheralueosuus on merkittävä hintaselittäjä: Votsis & Perrels (2016): +3–5 % Suomessa.
**Prioriteetti:** ⭐⭐ Keskikorkea — erinomainen ympäristömuuttuja, vain HKI-seutu.

### 22. HSY — Kävely- ja pyöräilyaikavyöhykkeet asemille ⭐ Uusi
**URL:** WFS/WMS/SHP
**Avoindata:** `https://avoindata.suomi.fi/data/fi/dataset/kavely-ja-pyorailyaikavyohykkeet-paakaupunkiseudun-asemille`
**Sisältö:** PKS juna- ja metroasemien saavutettavuusvyöhykkeet kävellen ja pyöräillen (5/10/15 min)
**Kattavuus:** Pääkaupunkiseutu
**Lisenssi:** CC BY 4.0
**Postinumerotasolle:** Spatial join — osuus postinumeroalueesta joka on 5/10/15 min asemasta
**Hyöty:** Debrezion ym. (2007): rautatieaseman läheisyys +2–4 % hintavaikutus. Täydentää Digitransit-matka-aikoja.
**Prioriteetti:** ⭐⭐ Keskikorkea.

### 23. StatFin — Rakennuskanta (PxWeb API) ⭐ Uusi
**URL:** `https://pxdata.stat.fi/PxWeb/api/v1/fi/StatFin/rakke/`
**Taulukot:**
- `116g` — Rakennukset käyttötarkoituksen ja valmistumisvuoden mukaan (2024)
- `116h` — Rakennukset käyttötarkoituksen ja lämmitysaineen mukaan (2024)
- `116i` — Rakennukset maakunnittain (2005–2024)
- `116j` — Kesämökit alueittain (1970–2024)

**Kattavuus:** Koko Suomi (kunta-/maakunta-taso, EI suoraan postinumero)
**Lisenssi:** CC BY 4.0
**Postinumerotasolle:** Kuntatasolla → postinumero→kunta-yhdistys (sama arvo kunnan sisällä)
**Hyöty:** Rakennuskannan ikäjakauma ja lämmitysmuoto kuntatasolla. Paavo sisältää jo osan, mutta rakke tarjoaa valmistumisvuosijakauman.
**Prioriteetti:** ⭐ Matala — kuntatasolla, Paavo kattaa jo osan.

### 24. Oppilaaksiottoalueet (Helsinki/Espoo/Vantaa) ⭐ Uusi
**URL:** WFS-rajapinnat kaupungeittain:
- Helsinki: `https://avoindata.suomi.fi/data/fi/dataset/helsingin-kaupungin-peruskoulujen-oppilaaksiottoaluerajat`
- Espoo: `https://avoindata.suomi.fi/data/fi/dataset/espoon-oppilaaksiottoalueet`
- Vantaa: `https://avoindata.suomi.fi/data/fi/dataset/vantaan-kaupungin-peruskoulujen-oppilaaksiottoaluerajat`

**Sisältö:** Peruskoulujen oppilaaksiottoalueiden rajat, nimet ja tunnukset
**Kattavuus:** PKS-kaupungit (kukin erikseen)
**Lisenssi:** CC BY 4.0
**Hyöty:** Black (1999), Harjunen ym. (2018): koulualueen vaikutus asuntohintoihin 2–5 %. Koulualueen yhdistäminen postinumeroalueisiin vaatii spatiaalista analyysiä.
**Prioriteetti:** ⭐ Matala — monimutkainen integraatio, vain PKS, vaatii koulun laatu-datan (Vipunen) rinnalle.

### 25. Energiatodistusrekisteri (Varke) ⭐ Uusi
**URL:** `https://energiatodistusrekisteri.fi/tietojenluovutus-ja-rajapinnat`
**Ylläpitäjä:** Valtion tukeman asuntorakentamisen keskus (Varke)
**Sisältö:** Rakennusten energiatodistukset: energialuokka (A–G), energiankulutus (kWh/m²/v)
**Kattavuus:** Koko Suomi (todistuksen omaavat rakennukset)
**Lisenssi:** Julkinen API (mahdollisesti tietojenluovutuspyynnöllä)
**Postinumerotasolle:** Aggregointi postinumeron mukaan → keskimääräinen energialuokka per alue
**Hyöty:** Energiatehokkuus vaikuttaa asumiskustannuksiin ja asuntojen arvoon.
**Prioriteetti:** ⭐ Matala — API:n saatavuus epävarma, vaatii tietojenluovutuspyyntöä.

### 26. Vipunen — Opetushallinnon tilastopalvelu (OPH / Tilastokeskus) ⭐ Uusi
**URL:** `https://vipunen.fi` (Power BI -raportit, ei REST API:a)
**Ylläpitäjä:** Opetushallitus (OPH) ja Tilastokeskus
**Sisältö:** Suomen kattavin koulutustilastojen palvelu. Raportit jaoteltuna koulutusasteittain:

**Perusopetus:**
- Oppilaitokset ja oppilaitos-verkon muutokset (lukumäärä, sijainti, koko)
- Oppilaasmäärät kouluittain ja alueittain
- Erityisen tuen saajat (osuus oppilaista)
- Aamu- ja iltapäivätoimintaan osallistuminen

**Lukiokoulutus:**
- Sisäänpääsyrajat lukioittain (alin keskiarvo / pisteraja) — **koulun haluttavuuden mittari**
- Ylioppilastutkinnon arvosanat lukioittain
- Hakijamäärät ja aloituspaikat
- Jatko-opintoihin siirtyminen

**Ammatillinen koulutus / AMK / Yliopistot:**
- Opiskelijamäärät, valmistuneet, työllistyminen
- Tutkimus- ja kehittämistoiminta (yliopistot)

**Alueelliset näkymät:**
- Väestön koulutusaste maakunnittain / kunnittain
- Oppilaitosten sijainti- ja kokotiedot kunnittain

**Kattavuus:** Koko Suomi, kunta- ja oppilaitostaso. Ei suoraa postinumerotasoa.
**Lisenssi:** CC BY 4.0 (osa raporteista, avoindata.suomi.fi:n kautta saatavat XLSX-aineistot)
**Rajapinta:** Ei virallista REST API:a. Data saatavilla:
1. **Power BI -raportit** — selainkäyttö, ei ohjelmallista poimintaa
2. **Avoindata.suomi.fi** — 9 datasettiä XLSX-muodossa (lukioiden sisäänpääsyrajat Helsinki/Espoo/Vantaa/Kauniainen, oppilaasmäärät kouluittain)
3. **Tilastokeskus StatFin** — koulutusastejakauma kunnittain PxWeb API:n kautta

**Postinumerotasolle:**
- Oppilaitoksen osoite → geokoodaus → point-in-polygon postinumeroalueisiin
- Lukioiden sisäänpääsyrajat → koulualueen vetovoiman mittari → oppilaaksiottoaluerajat (#24) yhdistettäväksi
- Koulutusastejakauma → pno→kunta-mapping (sama arvo kunnan sisällä)

**Hyöty asuntohintoihin:**
Black (1999): koulun laatu selittää 2–5 % asuntojen hintaerosta. Harjunen ym. (2018): Helsingissä arvostettu peruskoulualue nostaa hintoja merkittävästi. Lukion sisäänpääsyraja on helpoin saatavissa oleva "koulun laadun" proxy.

**Käyttö projektissa:**
- Yhdistä oppilaaksiottoalueisiin (#24) → "paras lähilukio: sisäänpääsyraja X" per postinumeroalue
- XLSX-aineistot avoindata.suomi.fi:stä ovat suoraviivaisimmat integroida

**Prioriteetti:** ⭐ Matala-keskikorkea — ei REST API:a, mutta XLSX + geokoodaus mahdollinen. Arvokas yhdistettynä oppilaaksiottoalueisiin.

### Yhteenvetotaulukko: Datalähteet prioriteettijärjestyksessä

| # | Datalähde | Taso | Avoin API | Nyt käytössä | Kenttiä | Prioriteetti lisäykselle |
|---|-----------|------|-----------|-------------|--------|------------------------|
| 1 | **Paavo WFS** | Postinumero | ✅ | ✅ (113/113) | 113 | ✅ Valmis |
| 2 | **StatFin ashi** | Postinumero | ✅ | ✅ | ~10 | ✅ Valmis |
| 3 | **StatFin asvu** | Postinumero | ✅ | ✅ | ~5 | ✅ Valmis |
| 4 | **OSM Geofabrik** | Point-in-polygon | ✅ | ✅ (11 kat.) | ∞ | ✅ Valmis |
| 5 | **Digitransit** | Reititys | ✅ (rek.) | ✅ | matka-aika | ✅ Valmis |
| 6 | **Suomen Pankki/ECB** | Koko maa | ✅ | ✅ | Euribor | ✅ Valmis |
| 7 | **LIPAS** | Postinumero | ✅ | ⬜ | ~48k paikkaa | ⭐⭐⭐ Korkea |
| 8 | **YKR-taajama (SYKE)** | Spatial (koko maa) | ✅ | ⬜ | Taajamatyyppi | ⭐⭐⭐ Korkea |
| 9 | **SeutuRAMAVA (HSY)** | Postinumero (PKS) | ✅ | ⬜ | ~15 | ⭐⭐ Keskikorkea |
| 10 | **Tulvavaaravyöhykkeet (SYKE)** | Spatial (koko maa) | ✅ | ⬜ | Riski-% | ⭐⭐ Keskikorkea |
| 11 | **HSY maanpeite** | Spatial (HKI-seutu) | ✅ | ⬜ | Viheralue-% | ⭐⭐ Keskikorkea |
| 12 | **HSY rakennukset** | Spatial (PKS) | ✅ | ⬜ | Rak.vuosi ym. | ⭐⭐ Keskikorkea |
| 13 | **HKI aluesarjat** | Osa-alue (HKI-seutu) | ✅ | ⬜ | Muuttoliike ym. | ⭐⭐ Keskikorkea |
| 14 | **HSY asemavyöhykkeet** | Spatial (PKS) | ✅ | ⬜ | 5/10/15 min | ⭐⭐ Keskikorkea |
| 15 | **Ilmanlaatu (FMI/HSY)** | Spatial | ✅ | ⬜ | NO₂, PM2.5 | ⭐ Matala-keski |
| 16 | **Kuntaliitto** | Kunta | ✅ | ⬜ | Verot | Keskitaso |
| 17 | **StatFin rakke** | Kunta | ✅ | ⬜ | Rak.vuosi | ⭐ Matala |
| 18 | **THL Sotkanet** | Kunta | ✅ | ⬜ | ~3000 | ⭐ Matala (ei pno) |
| 19 | **Energiatodistus** | Rakennus | osittain | ⬜ | E-luokka | ⭐ Matala |
| 20 | **Oppilaaksiottoalueet** | Spatial (PKS) | ✅ | ⬜ | Koulualueet | ⭐ Matala |
| 21 | **FMI** | Asema | ✅ | ⬜ | Sää/ilma | Matala |
| 22 | **Poliisi** | Kunta | osittain | ⬜ | Rikokset | Matala (ei pno) |
| 23 | **MML** | Spatial | ✅ | ⬜ | Maasto | Matala |
| 24 | **Traficom** | Kunta | ✅ | ⬜ | Ajoneuvot | Matala |
| 25 | **Posti** | Postinumero | ✅ | ⬜ | Metatiedot | Matala |
| 26 | **Vipunen (OPH)** | Oppilaitos/kunta | ⬜ (Power BI) | ⬜ | Sisäänpääsyrajat ym. | ⭐ Matala-keski |

### Konkreettiset suositukset: Mitä lisätä seuraavaksi?

**1. Paavon käyttämättömät kentät** ✅ Toteutettu 6.3.2026
- Kaikki 113 kenttää haetaan ja 8 johdettua muuttujaa lasketaan
- Ikäjakauma (20 ikäryhmää) → lapset/työikäiset/eläkeikäiset osuudet
- Tuloluokat (hr_pi_tul, hr_ke_tul, hr_hy_tul)
- Rakennuskanta (ra_as_kpa, ra_kt_as, ra_pt_as) → kerrostalo-osuus
- Työpaikka-aineisto (26 toimialaa) → ICT-osuus, palveluala-osuus
- Talouksien tyyppi (te_yks, te_laps, te_elak)
- Omistus vs. vuokra (te_omis_as, te_vuok_as) → omistusaste

**2. OSM-parserin laajentaminen** ✅ Toteutettu 6.3.2026
- Ravintolat (amenity=restaurant, paino 0.7)
- Kahvilat (amenity=cafe/bar, paino 0.5)
- Puistot (leisure=park, paino 0.6)

**3. Digitransit matka-aika** ✅ Toteutettu 6.3.2026
- Matka-aika 7 kaupunkikeskustaan (Helsinki, Tampere, Turku, Oulu, Kuopio, Jyväskylä, Lahti)
- Digitransit API (julkinen liikenne) + Haversine-fallback (auto)
- Värikoodattu popup + finder-suodatin

**4. Euribor-aikasarja** ✅ Toteutettu 6.3.2026
- ECB Statistical Data Warehouse, 2005–2026
- SARIMAX(1,1,1) ennustemalli eksogenisena muuttujana
- Hinta vs. Euribor -aikasarjakaavio

**5. Seuraavat korjaukset / kehitysideat**
- ✅ ~~**ICT-työpaikat ja palveluala-osuudet**~~ — Korjattu 9.3.2026. Juurisyy: Paavo 2026 -datasta puuttuu työpaikkatilasto (`tp_tyopy=0`), koska Tilastokeskus ei ole vielä julkaissut sitä. Popup käytti `max(vuodet)=2026`, jolla arvot olivat nollia. Korjaus: fallback viimeisimpaan vuoteen jolla `tp_tyopy > 0` (2025, data vuodelta 2024: esim. 00100 Helsinki ICT 21.3%, palveluala 83.9%).
- ✅ ~~**Nimeä "Kaupat" → "Ruokakaupat"**~~ — Korjattu 9.3.2026. Kaikki käyttöliittymän näkymät (popup, finder) päivitetty. Sisäinen avain `kaupat` säilytetty yhteensopivuuden vuoksi.
- ✅ ~~**Lisää kirjastot ja apteekit**~~ — Toteutettu 9.3.2026. OSM-tagit `amenity=library` ja `amenity=pharmacy` lisätty. Palvelukategoriat nyt 11 kpl. Painot: kirjastot 1.0, apteekit 1.1.
- 📋 **Priorisoitu kehityssuunnitelma** → katso kohta **7F. Tärkeimmät seuraavat kehityskohteet** (9.3.2026 kartoitus)

## Lähdeviitteet

- Asuntohinnat: [Tilastokeskus StatFin](https://stat.fi/) - ashi_13mu
- Postinumeroalueet: [Tilastokeskus geo.stat.fi](https://geo.stat.fi/) - postialue:pno_tilasto
- Väestötiedot: [Tilastokeskus Paavo](https://www.stat.fi/tup/paavo/) - postialue:pno_tilasto_XXXX (113 kenttää)
- Palvelutiedot: [OpenStreetMap](https://www.openstreetmap.org/) via [Geofabrik](https://download.geofabrik.de/europe/finland.html) - finland-latest.osm.pbf (11 kategoriaa)
- Matka-ajat: [Digitransit](https://digitransit.fi/) Routing API v2 + Haversine-laskennallinen arvio
- Euribor: [ECB Statistical Data Warehouse](https://data.ecb.europa.eu/) - 12 kk Euribor (2005–2026)
- Karttakirjasto: [Leaflet](https://leafletjs.com/)
- OSM-parsing: [pyosmium](https://osmcode.org/pyosmium/)
