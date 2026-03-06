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
  - **Laajennetut palvelut:** 9 kategoriaa (+ ravintolat, kahvilat, puistot)
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
- **Laskentamenetelmä:** Point-in-polygon tarkistus postinumeroalueen tarkoilla rajoilla (osmium-parseri)
- **Palvelukategoriat:** (6 kpl)
  - 🛒 Kaupat (`shop=supermarket`, `shop=convenience`)
  - 🏫 Koulut (`amenity=school`)
  - 🧒 Päiväkodit (`amenity=kindergarten`)
  - 💪 Liikuntapaikat (`leisure=fitness_centre`, `leisure=sports_centre`)
  - 🏥 Terveysasemat (`amenity=doctors`, `amenity=clinic`, `amenity=hospital`)
  - 🚌 Julkinen liikenne (`highway=bus_stop`, `railway=station`, `railway=tram_stop`, `railway=halt`)
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
  | Kaupat | 1.0 |
  | Liikuntapaikat | 0.8 |
  | Julkinen liikenne | 0.5 |

  Logaritminen skaalaus ja pinta-alanormalisointi estävät suurten maaseutualueiden raakamäärien (esim. sadat bussipysäkit pitkien teiden varrella) dominointia. Tyypilliset arvot: 0–15 (Helsinki kantakaupunki ~10–15, kaupunkikeskustat ~5–8, maaseutu <1).
- **Kattavuus:** 1134/1723 postinumeroalueella palvelutietoja (66%)
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

# 4. Laske 5 vuoden trendianalyysi
python laske_trendianalyysi.py

# 5. Laske edistyneet ennustemallit (ARIMA, Exponential Smoothing, SARIMAX-Euribor)
python laske_ennusteet.py

# 6. Lataa matka-ajat keskustaan (Digitransit API tai laskennallinen arvio)
python lataa_matka_ajat.py

# 7. Lataa 12 kk Euribor-aikasarja (ECB Statistical Data Warehouse)
python lataa_euribor.py

# 8. Luo interaktiivinen kartta
python kartta_polygon.py
```

Avaa `kartta.html` selaimessa.

**Huom:** 
- Vaiheet 1-5 hakevat dataa verkosta tai laskevat ennusteita
- `asuntohinnat.py` kestää ~1-2 min (StatFin API)
- `rikasta_data.py` kestää ~5-10 min (Paavo WFS API + OSM-datan lataus ~676 MB + parsing 1.7M nodea)
- `laske_ennusteet.py` kestää ~5-20 min (ARIMA, Exponential Smoothing ja SARIMAX-Euribor mallit)
- `lataa_matka_ajat.py` kestää ~1-2 min (laskennallinen arvio) tai ~30-60 min (Digitransit API)
- `lataa_euribor.py` kestää ~5 s (ECB API)
- `kartta_polygon.py` generoi kartan nopeasti (~10-30 s)

## Tiedostot

### Dataskriptit
- `asuntohinnat.py` - Hakee asuntohintadatan Tilastokeskuksesta (2009-2025) ja laskee lineaarisen ennusteen (2026)
- `lataa_postinumeroalueet.py` - Hakee postinumeroalueiden tarkat geometriat Tilastokeskuksen WFS-rajapinnasta
- `rikasta_data.py` - Hakee Paavo-väestötiedot aikasarjana (2015-2026, 113 kenttää + 8 johdettua muuttujaa) ja palvelutiedot OSM-datasta (9 kategoriaa)
- `laske_trendianalyysi.py` - Laskee 5 vuoden trendit, volatiliteetin ja markkinaaktiivisuuden
- `laske_ennusteet.py` - Laskee edistyneet ennustemallit (ARIMA, Exponential Smoothing, SARIMAX-Euribor) vuodelle 2026
- `lataa_matka_ajat.py` - Laskee matka-ajat lähimpään kaupunkikeskustaan (Digitransit API / Haversine-fallback)
- `lataa_euribor.py` - Hakee 12 kk Euribor-aikasarjan ECB:n Statistical Data Warehouse -rajapinnasta
- `kartta_polygon.py` - Luo interaktiivisen kartan

### Datatiedostot (generoituvat)
- `data/asuntohinnat.json` - Asuntohintadata vuosittain (2009-2026), huoneistotyypeittäin (~7.9 MB)
- `data/postinumerot_hinnat.geojson` - Postinumeroalueiden tarkat geometriat + hinnat (~16.6 MB)
- `data/postinumerokoordinaatit.json` - Alueiden keskipisteet
- `data/rikastettu_data.json` - Väestötiedot aikasarjana (2015-2026, 3044 aluetta) + palvelutiedot (~1.2 MB)
- `data/trendianalyysi.json` - 5 vuoden trendianalyysi (867 aluetta) (~217 KB)
- `data/ennusteet_mallit.json` - Ennusteet neljällä mallilla (Linear, ARIMA, Exponential, SARIMAX-Euribor) (~800 KB)
- `data/matka_ajat.json` - Matka-ajat lähimpään keskustaan (1723 aluetta, 7 kaupunkia) (~200 KB)
- `data/euribor.json` - 12 kk Euribor-korko kuukausittain ja vuosikeskiarvoin (2005–2026) (~10 KB)
- `data/korrelaatiot.json` - Placeholder korrelaatioanalyysia varten
- `finland-latest.osm.pbf` - OpenStreetMap data Suomesta (~676 MB, ladataan rikasta_data.py:llä)

### Kartat (generoituvat)
- `kartta.html` - Interaktiivinen polygon-kartta (~20+ MB)

## Tekninen toteutus

- **Karttakirjasto:** Leaflet 1.9.4
- **Datalähde:** 
  - Asuntohinnat: Tilastokeskus StatFin API (ashi_13mu)
  - Geometriat: Tilastokeskus WFS API (postialue:pno_tilasto)
  - Väestötiedot: Tilastokeskus WFS API (postialue:pno_tilasto_XXXX, vuodet 2015-2026, 113 kenttää)
  - Palvelutiedot: OpenStreetMap via Geofabrik (finland-latest.osm.pbf, 9 kategoriaa)
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
  - 9 palvelukategoriaa, painotettu palveluindeksi
  - 1134/1723 alueella palvelutietoja (66%)
  - Snapshot nykyhetkestä (ei aikasarjaa)
- **Datamäärä:** 
  - 18 vuotta (17 todellista + 1 ennuste)
  - 5 huoneistotyyppiä (1 painotettu keskiarvo + 4 yksittäistä tyyppiä)
  - 2 mittaria (hinta, kauppamäärä)
  - 1723 postinumeroaluetta
  - ≈ 155,000 datapistettä asuntohinnoissa
  - ≈ 36,500 datapistettä väestötiedoissa (113 kenttää + 8 johdettua per alue per vuosi)
  - ≈ 15,000 datapistettä palvelutiedoissa (9 kategoriaa × 1134 aluetta + palveluindeksit)
  - ≈ 1,723 matka-aikatietoa (minuutit, lähin keskusta, etäisyys km)
  - ≈ 254 kuukausittaista + 22 vuosittaista Euribor-datapistettä
  - ≈ 414,000 koordinaattipistettä geometrioissa

### GitHub Actions deployment

Kartta päivittyy automaattisesti ilman manuaalista työtä:

1. **Workflow ajastus:** Joka kuukauden 1. päivä klo 03:00 UTC
2. **Datan haku:** 
   - Tilastokeskuksen StatFin API → Asuntohinnat (2009-2025)
   - Tilastokeskuksen WFS API → Tarkat postinumeroalueiden geometriat
   - Tilastokeskuksen WFS API → Väestötiedot (Paavo 2015-2026)
   - Geofabrik → OSM-data (~676 MB) → Palvelutiedot (osmium-parsing)
3. **Ennusteet:** Lineaarinen trendianalyysi → 2026 ennusteet
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
  - *Kategoriat:* kaupat, koulut, päiväkodit, liikuntapaikat, terveysasemat, julkinen liikenne

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
  - *Toteutus:* Suodatinpaneeli oikeassa reunassa: kuntavalinta (293 kuntaa), huoneistotyyppivalinta, max neliöhinta (liukusäädin), min väkiluku, palveluvaatimukset (kaupat, koulut, päiväkodit, liikunta, terveys, julk.liikenne), min palveluindeksi, max matka-aika keskustaan (0–120 min). Tulokset korostetaan kartalla vihreällä ja listataan paneelissa palveluindeksin mukaan. Klikkaus zoomaa alueelle.
  - *Nappi:* "🔍 Paras alue" -painike kartan vasemmassa alareunassa.

- **Hinta/tulot -suhdekartta** (asumisen kohtuuhintaisuus) ✅ Toteutettu
  - *Miksi:* Absoluuttinen hinta ei kerro kaikkea. Affordable-indeksi (vuosipalkat per asunto) on informatiivisempi.
  - *Toteutus:* Uusi mittari dropdown-valikossa: `keskihinta × 60m² / keskitulot`. Värikartta suhdeluvun mukaan (vihreä < 5 v, punainen > 12 v). Popup näyttää 60m² hinnan, keskitulon ja suhteen vuosissa.
  - *Esimerkki:* "00100: 11.2 vuoden palkat. 90100 (Oulu): 4.8 vuoden palkat."

- **Vuokra vs. osto -vertailu**
  - *Miksi:* Vuokratuotto-% on sijoittajan tärkein mittari. Missä vuokraus on kannattavampaa kuin ostaminen?
  - *Toteutus:* Jos vuokradata saatavissa (Tilastokeskus tai Vuokraovi), laske gross yield = vuosivuokra / ostohinta.
  - *Haaste:* Vuokradatan saatavuus postinumeroalueittain.

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

#### D. Datan laajentaminen

- **LIPAS-liikuntapaikkatiedot**
  - *Miksi:* Virallinen ja kattavampi kuin OSM erityisesti uimahalleille, ulkoilureiteille ja frisbeegolf-radoille.
  - *Toteutus:* `lipas.fi/api` → JSON, suora `location.postalCode`-yhdistys. ~40 000 kohdetta.

- **Kiinteistöverotiedot kunnittain**
  - *Miksi:* Kiinteistövero vaihtelee 0.93–2.0 % ja vaikuttaa asumiskustannuksiin.
  - *Toteutus:* Kuntaliiton data → pno→kunta mapping → vero-% jokaiselle postinumeroalueelle.

- **Rakennuskustannusindeksi**
  - *Miksi:* Glaeser & Gyourko (2005): rakennuskustannukset asettavat alarajan hinnoille.
  - *Toteutus:* Tilastokeskus (rki). Yhteinen kaikille → näytä aikasarjakaaviossa hinnan rinnalla.

- **Sotkanet terveys- ja hyvinvointidata (kuntataso)**
  - *Miksi:* Sairastavuusindeksi ja toimeentulotuki kertovat alueen hyvinvoinnista.
  - *Toteutus:* `sotkanet.fi/api` → 3000 indikaattoria kuntataso → pno-yhdistys.

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
- ✅ **Palvelut** — 9 kategoriaa OSM-datasta, palveluindeksi (tiheys/km², log-skaalaus)
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
| Kaupat | `shop=supermarket`, `shop=convenience` |
| Koulut | `amenity=school` |
| Päiväkodit | `amenity=kindergarten` |
| Liikuntapaikat | `leisure=fitness_centre`, `leisure=sports_centre` |
| Terveysasemat | `amenity=doctors`, `amenity=clinic`, `amenity=hospital` |
| Julkinen liikenne | `highway=bus_stop`, `railway=station/tram_stop/halt` |
| Ravintolat | `amenity=restaurant` |
| Kahvilat | `amenity=cafe`, `amenity=bar` |
| Puistot | `leisure=park` |

**Lisäksi saatavilla OSM:stä (ei vielä käytössä):**
| Kategoria | OSM-tagi | Relevanssi hintakarttaan |
|-----------|----------|------------------------|
| Ravintolat/kahvilat | `amenity=restaurant`, `amenity=cafe`, `amenity=bar` | ✅ Toteutettu 6.3.2026 |
| Puistot/viheralueet | `leisure=park`, `natural=wood`, `landuse=forest` | ✅ Puistot toteutettu, metsät ei vielä |
| Kirjastot | `amenity=library` | Keskitaso — julkiset palvelut |
| Apteekit | `amenity=pharmacy` | Keskitaso — terveyspalvelut |
| Pankit/pankkiautomaatit | `amenity=bank`, `amenity=atm` | Matala |
| Elokuvateatterit | `amenity=cinema` | Matala — vapaa-ajan palvelut |
| Kirkot/uskonnolliset | `amenity=place_of_worship` | Matala |
| Parkkipaikat | `amenity=parking` | Matala — autoistumisaste |
| Latauspisteet | `amenity=charging_station` | Nouseva — sähköautot |
| Uimapaikat | `leisure=swimming_pool`, `natural=beach` | Matala |

### 4. LIPAS — Liikuntapaikkatietojärjestelmä
**URL:** `https://lipas.fi/api/sports-places`
**Ylläpitäjä:** Jyväskylän yliopisto / OKM
**Sisältö:** Kaikki Suomen liikuntapaikat (n. 40 000 kpl)
**Kenttä:** `location.postalCode` — suora postinumeroyhdistys
**Tyypit:** uimahallit, jäähallit, liikuntasalit, kentät, ladut, ulkoilureitit, uimarannat, frisbeegolf-radat jne.
**Lisenssi:** CC BY 4.0
**Etu OSM:ään verrattuna:** Virallinen, kattavampi erityisesti ulkoilureiteille ja erikoisliikuntapaikoille

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

### Yhteenvetotaulukko: Datalähteet prioriteettijärjestyksessä

| # | Datalähde | Taso | Avoin API | Nyt käytössä | Kenttiä | Prioriteetti lisäykselle |
|---|-----------|------|-----------|-------------|--------|------------------------|
| 1 | **Paavo WFS** | Postinumero | ✅ | ✅ (113/113) | 113 | ✅ Valmis |
| 2 | **StatFin ashi** | Postinumero | ✅ | ✅ | ~10 | ✅ Valmis |
| 3 | **StatFin asvu** | Postinumero | ✅ | ✅ | ~5 | ✅ Valmis |
| 4 | **OSM Geofabrik** | Point-in-polygon | ✅ | ✅ (9 kat.) | ∞ | ✅ Valmis |
| 5 | **Digitransit** | Reititys | ✅ (rek.) | ✅ | matka-aika | ✅ Valmis |
| 6 | **LIPAS** | Postinumero | ✅ | ⬜ | ~40k paikkaa | Keskitaso |
| 7 | **Suomen Pankki/ECB** | Koko maa | ✅ | ✅ | Euribor | ✅ Valmis |
| 8 | **Kuntaliitto** | Kunta | ✅ | ⬜ | Verot | Keskitaso |
| 9 | **THL Sotkanet** | Kunta | ✅ | ⬜ | ~3000 | Matala (ei pno) |
| 10 | **FMI** | Asema | ✅ | ⬜ | Sää/ilma | Matala |
| 11 | **HSY** | PK-seutu | ✅ | ⬜ | Ympäristö | Matala (rajattu) |
| 12 | **Poliisi** | Kunta | osittain | ⬜ | Rikokset | Matala (ei pno) |
| 13 | **MML** | Spatial | ✅ | ⬜ | Maasto | Matala |
| 14 | **Traficom** | Kunta | ✅ | ⬜ | Ajoneuvot | Matala |

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

## Lähdeviitteet

- Asuntohinnat: [Tilastokeskus StatFin](https://stat.fi/) - ashi_13mu
- Postinumeroalueet: [Tilastokeskus geo.stat.fi](https://geo.stat.fi/) - postialue:pno_tilasto
- Väestötiedot: [Tilastokeskus Paavo](https://www.stat.fi/tup/paavo/) - postialue:pno_tilasto_XXXX (113 kenttää)
- Palvelutiedot: [OpenStreetMap](https://www.openstreetmap.org/) via [Geofabrik](https://download.geofabrik.de/europe/finland.html) - finland-latest.osm.pbf (9 kategoriaa)
- Matka-ajat: [Digitransit](https://digitransit.fi/) Routing API v2 + Haversine-laskennallinen arvio
- Euribor: [ECB Statistical Data Warehouse](https://data.ecb.europa.eu/) - 12 kk Euribor (2005–2026)
- Karttakirjasto: [Leaflet](https://leafletjs.com/)
- OSM-parsing: [pyosmium](https://osmcode.org/pyosmium/)
