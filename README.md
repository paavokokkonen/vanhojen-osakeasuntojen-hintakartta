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
- **Laskentamenetelmä:** Point-in-polygon tarkistus postinumeroalueen tarkoilla rajoilla
- **Palvelukategoriat:** (6 kpl)
  - 🛒 Kaupat (shop=supermarket, shop=convenience, shop=mall)
  - 🏫 Koulut (amenity=school)
  - 🧒 Päiväkodit (amenity=kindergarten)
  - 💪 Liikuntapaikat (leisure=sports_centre, leisure=fitness_centre, leisure=stadium, leisure=pitch)
  - 🏥 Terveysasemat (amenity=clinic, amenity=doctors, amenity=hospital)
  - 🚌 Julkinen liikenne (railway=*, public_transport=stop_position)
- **Palveluindeksi:** Painotettu keskiarvo (kaupat 30%, julkinen liikenne 25%, koulut 15%, päiväkodit 15%, liikuntapaikat 10%, terveysasemat 5%)
- **Kattavuus:** 1134/1723 postinumeroalueella palvelutietoja (66%)
- **Huom:** Palvelut ovat snapshot nykyhetkestä, ei aikasarjaa

### 🔮 Ennusteet ja mallit
- **Oletuksena viimeisin datavuosi (2025)** - Kartta aukeaa vuoteen 2025, joka on viimeisin Tilastokeskuksen julkaisema datavuosi
- **Ennustevuosi (2026*) valittavissa erikseen** - Käyttäjän on valittava aktiivisesti vuosi 2026 nähdäkseen ennusteet
- **Kolme ennustemallia** vuodelle 2026:
  - **Lineaarinen trendi** - Yksinkertainen keskimääräinen vuosimuutos (5 vuoden historia)
  - **ARIMA** - AutoRegressive Integrated Moving Average, aikasarja-analyysi
  - **Exponential Smoothing** - Holt's exponential smoothing -menetelmä
- **Interaktiivinen mallivalinta** - Valitse ennustemalli pudotusvalikosta kun tarkastelet vuotta 2026*
- **Kattavat ennusteet**:
  - Linear: ~3000 ennustetta
  - ARIMA: ~2700 ennustetta (vaatii riittävästi dataa)
  - Exponential Smoothing: ~3000 ennustetta
- **Visuaalinen erottelu** tähdellä (*) ennustevuodesta
- **Mallivertailu** - Näe miten eri mallit ennustavat samalle alueelle

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

# 5. Laske edistyneet ennustemallit (ARIMA, Exponential Smoothing)
python laske_ennusteet.py

# 6. Luo interaktiivinen kartta
python kartta_polygon.py
```

Avaa `kartta.html` selaimessa.

**Huom:** 
- Vaiheet 1-5 hakevat dataa verkosta tai laskevat ennusteita
- `asuntohinnat.py` kestää ~1-2 min (StatFin API)
- `rikasta_data.py` kestää ~5-10 min (Paavo WFS API + OSM-datan lataus ~676 MB + parsing 1.7M nodea)
- `laske_ennusteet.py` kestää ~2-3 min (ARIMA ja Exponential Smoothing mallit)
- `kartta_polygon.py` generoi kartan nopeasti (~10-30 s)

## Tiedostot

### Dataskriptit
- `asuntohinnat.py` - Hakee asuntohintadatan Tilastokeskuksesta (2009-2025) ja laskee lineaarisen ennusteen (2026)
- `lataa_postinumeroalueet.py` - Hakee postinumeroalueiden tarkat geometriat Tilastokeskuksen WFS-rajapinnasta
- `rikasta_data.py` - Hakee Paavo-väestötiedot aikasarjana (2015-2026) ja palvelutiedot OSM-datasta (Geofabrik)
- `laske_trendianalyysi.py` - Laskee 5 vuoden trendit, volatiliteetin ja markkinaaktiivisuuden
- `laske_ennusteet.py` - Laskee edistyneet ennustemallit (ARIMA, Exponential Smoothing) vuodelle 2026
- `kartta_polygon.py` - Luo interaktiivisen kartan

### Datatiedostot (generoituvat)
- `data/asuntohinnat.json` - Asuntohintadata vuosittain (2009-2026), huoneistotyypeittäin (~7.9 MB)
- `data/postinumerot_hinnat.geojson` - Postinumeroalueiden tarkat geometriat + hinnat (~16.6 MB)
- `data/postinumerokoordinaatit.json` - Alueiden keskipisteet
- `data/rikastettu_data.json` - Väestötiedot aikasarjana (2015-2026, 3044 aluetta) + palvelutiedot (~1.2 MB)
- `data/trendianalyysi.json` - 5 vuoden trendianalyysi (867 aluetta) (~217 KB)
- `data/ennusteet_mallit.json` - Ennusteet kolmella mallilla (Linear, ARIMA, Exponential) (~600 KB)
- `data/korrelaatiot.json` - Placeholder korrelaatioanalyysia varten
- `finland-latest.osm.pbf` - OpenStreetMap data Suomesta (~676 MB, ladataan rikasta_data.py:llä)

### Kartat (generoituvat)
- `kartta.html` - Interaktiivinen polygon-kartta (~20+ MB)

## Tekninen toteutus

- **Karttakirjasto:** Leaflet 1.9.4
- **Datalähde:** 
  - Asuntohinnat: Tilastokeskus StatFin API (ashi_13mu)
  - Geometriat: Tilastokeskus WFS API (postialue:pno_tilasto)
  - Väestötiedot: Tilastokeskus WFS API (postialue:pno_tilasto_XXXX, vuodet 2015-2026)
  - Palvelutiedot: OpenStreetMap via Geofabrik (finland-latest.osm.pbf)
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
  - Käyttäjä voi valita mallin kartalla pudotusvalikosta
- **Trendianalyysi:** 5 vuoden (2019-2024) lineaarinen regressio, volatiliteetti (keskihajonta), aktiivisuus (keskimääräiset kaupat)
- **Väestödata:** 
  - Aikasarja 2015-2026 (12 vuotta × 3044 postinumeroaluetta ≈ 36,500 tietuetta)
  - Huom: Paavo-data julkaistaan +1 vuoden viiveellä (pno_tilasto_2025 sisältää 31.12.2024 tilanteen)
- **Palveludata:**
  - OSM-data parsed osmium-kirjastolla (1.7M+ nodea)
  - Point-in-polygon tarkistus shapely-kirjastolla
  - 6 palvelukategoriaa, painotettu palveluindeksi
  - 1134/1723 alueella palvelutietoja (66%)
  - Snapshot nykyhetkestä (ei aikasarjaa)
- **Datamäärä:** 
  - 18 vuotta (17 todellista + 1 ennuste)
  - 5 huoneistotyyppiä (1 painotettu keskiarvo + 4 yksittäistä tyyppiä)
  - 2 mittaria (hinta, kauppamäärä)
  - 1723 postinumeroaluetta
  - ≈ 155,000 datapistettä asuntohinnoissa
  - ≈ 36,500 datapistettä väestötiedoissa
  - ≈ 10,000 datapistettä palvelutiedoissa (6 kategoriaa × 1134 aluetta + palveluindeksit)
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

### 1. Ennustemallien parantaminen

**Tavoite:** Parantaa ennusteiden tarkkuutta ja antaa käyttäjille parempi käsitys ennusteiden epävarmuudesta.

**Ideat:**

- **Prophet-malli** (Facebookin aikasarja-ennuste)
  - *Miksi:* Prophet käsittelee automaattisesti kausivaihttelua, trendien muutoksia ja poikkeavia arvoja. Soveltuu hyvin asuntomarkkinadataan, jossa on kausiluontoista vaihtelua (kesä vs. talvi).
  - *Toteutus:* `fbprophet`-kirjasto, lisää ~60MB riippuvuuksia. Vaatii vähintään 2 vuoden dataa per alue.
  - *Esimerkki:* "Helsinki 00100: Prophet ennustaa hinnan nousua 3.2% vuonna 2026, ottaen huomioon kevään ja syksyn kauppasesongin."

- **LSTM-neuroverkko** (syväoppimismalli pitkille aikasarjoille)
  - *Miksi:* LSTM oppii pitkän aikavälin riippuvuuksia datasta ja voi havaita monimutkaisia trendejä. Toimii hyvin alueilla, joissa on riittävästi historiadataa.
  - *Toteutus:* TensorFlow/Keras, lisää ~500MB riippuvuuksia. Vaatii harjoittelua, joka kestää useita minuutteja.
  - *Haaste:* Vaatii paljon dataa (>10 vuotta) ja laskentaa. Ei välttämättä toimi alueilla, joilla vain vähän kauppoja.
  - *Esimerkki:* "LSTM malli tunnistaa, että Kallio-alueella hinnat nousevat nopeammin kuin lineaarinen trendi ennustaa."

- **Luottamusvälit ennusteille** (ennusteen epävarmuus)
  - *Miksi:* Ennuste on aina epävarma. Luottamusvälit (esim. 80%, 95%) kertovat, kuinka varmoja voimme olla ennusteesta.
  - *Toteutus:* Lasketaan jäännösten keskihajonta ja oletetaan normaalijakauma. Visualisoidaan läpinäkyvänä alueena kartalla.
  - *Esimerkki:* "00100: Ennuste 7400 €/m² (95% luottamusväli: 6800-8000 €/m²)"

- **Useamman vuoden ennusteet** (2027-2030)
  - *Miksi:* Pitkäaikaiset sijoittajat ja kaupunkisuunnittelijat hyötyvät pidemmän aikavälin ennusteista.
  - *Haaste:* Epävarmuus kasvaa jyrkästi jokaista vuotta kohden. 5 vuoden ennuste on hyvin epävarma.
  - *Toteutus:* Käytä malleja, jotka palauttavat useita askelia eteenpäin. Näytä growing luottamusvälit.

- **Mallivertailu ja tarkkuusmetriikat**
  - *Miksi:* Eri mallit sopivat eri alueille. Käyttäjän pitäisi tietää, miten luotettava ennuste on.
  - *Toteutus:* Laske RMSE (Root Mean Square Error), MAE (Mean Absolute Error), R² (selitysaste) vertaamalla 2020-2024 ennusteita todelliseen dataan. Näytä parhaiten toiminut malli per alue.
  - *Esimerkki:* "00100: ARIMA paras (RMSE=142 €/m²), Linear keskinkertainen (RMSE=218 €/m²)"

- **Eksogeniset muuttujat** (ulkoiset tekijät)
  - *Miksi:* Asuntohintoihin vaikuttavat Euribor-korot, työttömyys, väestönkasvu. Malli, joka ottaa nämä huomioon, on tarkempi.
  - *Toteutus:* Hae Euribor-korot, työttömyysprosentit Tilastokeskuksesta. Käytä SARIMAX- tai Prophet-mallissa eksogenisina muuttujina.
  - *Esimerkki:* "Kun Euribor nousee 1%, hinnat laskevat keskimäärin 2.3% seuraavan vuoden aikana."

### 2. Korrelaatioanalyysi ja data-visualisointi

**Tavoite:** Auttaa käyttäjiä ymmärtämään, mitkä tekijät vaikuttavat asuntohintoihin ja nähdä trendejä kartalla helpommin.

**Ideat:**

- **Interaktiivinen korrelaatiomatriisi**
  - *Miksi:* Käyttäjät voivat nähdä nopeasti, että esim. keskitulo korreloi 0.68 neliöhintojen kanssa, mutta työttömyys -0.42.
  - *Toteutus:* Laske Pearsonin korrelaatiot hintdatan, väestödatan ja trendien välillä. Visualisoi lämpökarttana (heatmap) Chart.js:llä tai D3.js:llä.
  - *Esimerkki:* "Suurin positiivinen korrelaatio: Keskitulo (0.68). Suurin negatiivinen: Työttömyys (-0.42)."

- **Palveluindeksin vaikutus hintoihin**
  - *Miksi:* Tutkia korrelaatiota palveluiden määrän ja asuntohintojen välillä. Ovatko hyvin palvellut alueet kalliimpia?
  - *Toteutus:* Laske Pearsonin korrelaatio palveluindeksin ja neliöhinnan välillä. Scatter plot palveluindeksi vs. hinta. Näytä regressiosuora.
  - *Hypoteesi:* Alueet, joilla paljon kauppoja ja julkista liikennettä, ovat yleensä kalliimpia.
  - *Esimerkki:* "Palveluindeksi korreloi +0.52 neliöhintojen kanssa. Jokainen +10 palveluindeksin piste nostaa hintoja keskimäärin ~200 €/m²."

- **Scatter plot -näkymä** (hajontakuvio)
  - *Miksi:* Visualisoi alueita kahdessa ulottuvuudessa, esim. hinta vs. tulot. Käyttäjä voi tunnistaa outlier-alueita (kalliit mutta matala tulotaso).
  - *Toteutus:* Uusi välilehti "Analyysi". Käyttäjä valitsee X- ja Y-akselin (esim. keskihinta, keskitulo, etäisyys keskustaan). Jokainen piste = postinumeroalue. Hover näyttää postinumeron.
  - *Esimerkki:* "Käyttäjä näkee, että 00100 (Helsingin keskusta) on erillään muista: korkea hinta, korkea tulotaso."

- **Aikasarjakaaviot** (line charts)
  - *Miksi:* Yksittäisen alueen trendin näkeminen vuosittain on helpompaa viivakaaviosta kuin kartalta.
  - *Toteutus:* Klikkaa postinumeroaluetta kartalla → aukea modal/sidebar, jossa viivakaaviossa näkyy 2009-2026 kehitys (hinnat, kaupat, väestö). Chart.js tai Plotly.
  - *Esimerkki:* "00100: Hinta noussut tasaisesti 2009-2019 (+4.1%/v), romahdus 2020 (-3.2%), elpynyt 2021-2025 (+3.8%/v)."

- **Histogrammit** (jakaumat)
  - *Miksi:* Näyttää, miten hinnat jakautuvat koko maassa tai valitussa kaupungissa. Käyttäjä näkee, onko alue kalleimmassa 10%:ssa.
  - *Toteutus:* Laske hintojen frekvenssit bineihin (esim. 2000-2500 €/m², 2500-3000 €/m²). Visualisoi palkkikaaviossa. Korosta valittu alue.
  - *Esimerkki:* "Hintojen mediaani 3400 €/m². 00100 (7400 €/m²) on kalleimmassa 1%:ssa."

- **Heatmap-kalenteri** (kuukausittainen vaihtelu)
  - *Miksi:* Kauppamäärät vaihtelevat kuukausittain (kesä/syksy aktiivinen, talvi hiljainen). Auttaa tunnistamaan parhaan kauppa-ajan.
  - *Haaste:* Tilastokeskuksen data on vuositasolla, ei kuukausitasolla. Tarvitaan toinen datalähde (esim. Etuovi API, jos saatavilla).
  - *Esimerkki:* "Kesäkuu 2024: 142 kauppaa. Tammikuu 2024: 87 kauppaa. Paras myyntikuukausi: Syyskuu."

### 3. Aluevertailu ja benchmarking

**Tavoite:** Mahdollistaa usean alueen vertailu rinnakkain ja samankaltaisten alueiden löytäminen.

**Ideat:**

- **Multi-select aluevertailu** (monen alueen vertailu)
  - *Miksi:* Asunnon ostaja vertaa usein 2-5 aluetta keskenään. "Onko Kallio vai Vallila parempi sijoitus?"
  - *Toteutus:* Shift+klikkaa postinumeroalueita kartalla → valitaan useita. Aukea vertailutaulukko tai rinnakkaiset viivakuviot. Näytä hinnat, trendit, väestö vierekkäin.
  - *Esimerkki:* "Vertailu: 00530 (Munkkiniemi) vs. 00570 (Pajamäki). Munkkiniemi +4.2%/v, Pajamäki +2.1%/v. Munkkiniemi kalliimpi mutta nopeampi kasvu."

- **Naapurustohaku** (lähialueet)
  - *Miksi:* Asunnon ostaja haluaa tietää, miten naapurialueet hinnoitellaan. Auttaa löytämään "piilohelmet" lähellä kalliita alueita.
  - *Toteutus:* Klikkaa aluetta → korosta kaikki alueet 5 km säteellä. Näytä niiden keskihinnat ja trendit. Käytä Turf.js:ää lasketaan etäisyydet.
  - *Esimerkki:* "00100 naapurustossa: 00160 (+3.8%/v), 00170 (+2.9%/v), 00180 (+4.1%/v)."

- **Klusterianalyysi** (samankaltaiset alueet)
  - *Miksi:* Löydä alueita, jotka ovat samanlaisia hinnaltaan, trendiltään ja väestörakenteeltaan. "Missä muualla on samankaltainen kehitys kuin Kalliossa?"
  - *Toteutus:* K-means clustering tai hierarkkinen klusterointi scikit-learn:llä. Klusteroi alueet 3-5 ryhmään (esim. "Nopeasti kasvavat kaupunkialueet", "Vakaat esikaupungit", "Laskevat syrjäalueet"). Väritä kartta klustereittain.
  - *Esimerkki:* "Klusteri 1 (Nopeasti kasvavat): 00100, 00530, 02100 (Espoon keskus). Keskimääräinen kasvu +4.5%/v."

- **Benchmark-indeksi** (vertailu keskiarvoon)
  - *Miksi:* Näyttää, onko alue yli/ali keskiarvon. Helppo tapa arvioida alueen houkuttelevuutta.
  - *Toteutus:* Laske pääkaupunkiseudun / koko Suomen keskihinta ja trendi. Näytä jokaiselle alueelle +/- % poikkeama. Esim. "00100: +78% yli PK-seudun keskiarvon (4150 €/m²)."
  - *Esimerkki:* "00710 (Helsinki-Myllypuro): -12% alle PK-seudun keskiarvon. Edullinen alue pääkaupunkiseudulla."

- **Peer group -analyysi** (vastaavat alueet)
  - *Miksi:* Vertaa aluetta vastaavankokoisiin alueisiin väkiluvun, tulotason ja sijainnin perusteella. "Onko 00530 kallis verrattuna vastaaviin lähiöihin?"
  - *Toteutus:* Suodata alueet, joilla ±20% väkiluku ja ±15% keskitulo. Vertaa hintatrendejä. Näytä tulosdiagrammina.
  - *Esimerkki:* "00530 peer group (10 aluetta): Keskihinta 5200 €/m². 00530 on 8% kalliimpi kuin peer-ryhmän mediaani."

### 4. Käyttöliittymäparannukset

**Tavoite:** Parantaa käyttökokemusta, erityisesti mobiilissa, ja tehdä kartasta helpommin jaettava.

**Ideat:**

- **✅ Mobiilioptimeinti** (osittain toteutettu 4.3.2026)
  - *Status:* ✅ Toteutettu
  - *Toteutettu:*
    - CSS media queries (@media max-width: 768px) lisätty
    - Pienempi otsikko ja tiiviimmät kontrollit mobiilissa
    - Muutoskartan inputs piilossa oletuksena, näytetään vain kun muutoskartta valittu
    - Fonttikoot ja välimatkat optimoitu kosketusnäytöille
    - Animaation play/pause ja speed-kontrollit näkyvissä mobiilissakin
  - *Vielä toteutettavana:*
    - Hamburger-valikko
    - Swipe-gesturet animaatioille
    - Touch-optimoidut zoom-kontrollit

- **✅ Animaatioiden alasvetovalikko** (toteutettu 4.3.2026)
  - *Status:* ✅ Toteutettu
  - *Muutos:* Radio-painikkeet → dropdown-valikko
  - *Edut:* Säästää tilaa, helpompi käyttää kosketusnäytöllä

- **Tumma tila** (dark mode)
  - *Miksi:* Vähentää silmien rasitusta hämärässä ja säästää energiaa OLED-näytöillä.
  - *Toteutus:* CSS-muuttujat väreille. Toggle-nappi otsikossa. Kartta käyttää dark-themed tiles (esim. CartoDB Dark Matter). Local storage muistaa valinnan.
  - *Esimerkki:* "Dark modessa tausta #1a1a1a, teksti #e0e0e0, polygonit tummemmat värit."

- **PDF/PNG-vienti** (kartan tallennus)
  - *Miksi:* Käyttäjät haluavat jakaa karttanäkymiä raporteissa, esityksissä tai sosiaalisessa mediassa.
  - *Toteutus:* Leaflet.EasyPrint plugin tai html2canvas-kirjasto. Nappi "Tallenna PNG". Ottaa screenshot kartasta + legendasta + otsikosta.
  - *Esimerkki:* "Käyttäjä tallentaa 2025 yksiöiden hintakartan PNG:nä ja jakaa Twitterissä."

- **Suosikkialueet** (tallennus local storageen)
  - *Miksi:* Asunnon ostaja seuraa 3-5 kiinnostavaa aluetta. Nopea pääsy tallennettuihin alueisiin.
  - *Toteutus:* Tähti-ikoni jokaisessa popup:ssa. Klikkaus tallentaa postinumeron `localStorage`:en. Sidebar listaa suosikit. Klikkaus zoomaa alueeseen.
  - *Esimerkki:* "Käyttäjä tallentaa 00530, 00570, 00710. Palaa kartalle myöhemmin → valitsee '00530' suosikeista → kartta zoomaa sinne."

- **Jakolinkit** (URL-parametrit)
  - *Miksi:* Käyttäjät haluavat jakaa tarkan näkymän (vuosi, postinumero, mittari, zoom). "Katso tätä aluetta!"
  - *Toteutus:* URL query parameters: `?year=2025&zip=00100&type=0&metric=keskihinta_aritm_nw&zoom=13&lat=60.17&lng=24.94`. JavaScript lukee parametrit sivun latautuessa ja asettaa oikean näkymän.
  - *Esimerkki:* "Käyttäjä jakaa linkin `kartta.html?year=2025&zip=00100` → vastaanottaja näkee suoraan Helsingin keskustan hinnat 2025."

- **Kieli-vaihtoehdot** (monikielisyys)
  - *Miksi:* Englanninkielinen versio houkuttelee kansainvälisiä sijoittajia ja tutkijoita.
  - *Toteutus:* Kaikki tekstit JSON-tiedostossa (`fi.json`, `en.json`). Toggle-nappi "FI | EN". JavaScript lataa oikean kielen. Muuttaa otsikot, labelit, legendat.
  - *Esimerkki:* "EN-versio: 'Housing Price Map', 'Old Condominiums', 'Average price per m²'."

- **Palveluindeksin mukauttaminen**
  - *Miksi:* Eri käyttäjät arvostavat eri palveluita. Lapsiperheelle päiväkodit tärkeitä, eläkeläiselle kaupat ja terveysasemat.
  - *Toteutus:* Liukusäätimet (sliders) jokaiselle palvelukategorialle (kaupat, koulut, päiväkodit...). Käyttäjä asettaa painotukset (yhteensä 100%). Palveluindeksi lasketaan uudelleen dynaamisesti. Kartta päivittyy.
  - *Esimerkki:* "Lapsiperhe: Koulut 40%, Päiväkodit 40%, Kaupat 20%. Eläkeläinen: Kaupat 50%, Terveysasemat 30%, Julkinen liikenne 20%. Kartta näyttää eri alueet korostuneina."

### 5. Lisädatan integrointi

**Tavoite:** Rikastaa karttaa ulkopuolisilla tietolähteillä, jotka vaikuttavat asuntohintoihin.

**Ideat:**

- **Liikennedata** (matka-aika keskustaan)
  - *Miksi:* Matka-aika työpaikalle on tärkein tekijä asunnon valinnassa. Alueet, joista pääsee nopeasti keskustaan, ovat kalliimpia.
  - *Toteutus:* HSL Reittiopas API (pääkaupunkiseutu) tai Google Maps Distance Matrix API (maksullinen). Laske matka-aika alueelta Helsingin rautatieasemalle aamu-ruuhkassa (klo 8). Tallenna `liikennedata.json`.
  - *Esimerkki:* "00100: 0 min. 00710: 18 min julkisilla (metro). 01450: 52 min julkisilla."
  - *Haaste:* Google API on maksullinen (0.005€/haku, 1723 aluetta = 8.6€). HSL API toimii vain PK-seudulla.

- **✅ Palvelutiedot** (kaupat, koulut, päiväkodit, liikuntapaikat, terveysasemat, julkinen liikenne)
  - *Status:* ✅ Toteutettu (4.3.2026)
  - *Ratkaisu:* Geofabrik OSM data + paikallinen parsing (osmium-kirjasto)
  - *Toteutettu:*
    - Ladataan finland-latest.osm.pbf (~676 MB) Geofabrikista
    - Parsitaan osmium-kirjastolla (1.7M+ nodea)
    - Point-in-polygon tarkistus shapely:llä (ei enää 1 km säde, vaan tarkat postinumeroaluerajat)
    - 6 palvelukategoriaa: kaupat, koulut, päiväkodit, liikuntapaikat, terveysasemat, julkinen liikenne
    - Painotettu palveluindeksi (kaupat 30%, julkinen liikenne 25%, koulut 15%, päiväkodit 15%, liikuntapaikat 10%, terveysasemat 5%)
    - Näkyy popup-ikkunoissa emojeilla 🛒🏫🧒💪🏥🚌
  - *Kattavuus:* 1134/1723 postinumeroalueella (66%)
  - *Haasteet:* 
    - Ei aikasarjaa (vain nykyhetken snapshot)
    - Vanhemmat alueet ja syrjäseudut usein ilman OSM-dataa
    - OSM-datan laatu vaihtelee alueittain
  - *Vaihtoehdot historialliseen dataan:*
    - Geofabrik arkisto (historialliset snapshotit eri vuosilta)
    - OSM Full History dump (erittäin suuri tiedosto)
  - **⚠️ Aikaisemmat haasteet Overpass API:n kanssa (ratkaistu):**
    - Overpass API rate limiting: 0/10 onnistunutta hakua
    - Ratkaistu vaihtamalla Geofabrik-ratkaisuun (lokaalir parsing)

- **Uudiskohteet** (rakenteilla olevat asunnot)
  - *Miksi:* Isot rakennusprojektit voivat vaikuttaa alueen hintoihin (lisää tarjontaa → hinnat laskevat, tai parantaa alueen imagoa → hinnat nousevat).
  - *Toteutus:* Rakennetun ympäristön tietojärjestelmä (RYTJ) tai YIT/Bonava/SRV -rakennusyhtiöiden avoimet kohteet. Merkitse kartalle rakennusprojektit pisteinä.
  - *Esimerkki:* "00100: 3 uudiskohdetta rakenteilla (yhteensä 420 asuntoa). Valmistuu 2025-2027."

- **Kiinteistöverotiedot**
  - *Miksi:* Kiinteistöverokannat vaihtelevat kunnittain (0.93-2.0%). Korkea kiinteistövero voi alentaa asuntojen kysyntää.
  - *Toteutus:* Hae kunnat, joihin postinumeroalueet kuuluvat. Scrape kuntien veroprosentit verohallinnon sivuilta tai käytä Kuntaliiton dataa. Tallenna `verotiedot.json`.
  - *Esimerkki:* "00100 (Helsinki): Kiinteistövero 1.0%. 02100 (Espoo): 0.93%. Edullisuusetu Espoossa."

- **Energiatehokkuus** (rakennuskannan energialuokat)
  - *Miksi:* Vanhemmat rakennukset (E-G luokat) ovat kalliimpia ylläpitää. Uudet energiatehokkaat (A-B) ovat kysyttyjä.
  - *Haaste:* Energiatodistukset ovat kiinteistökohtaisia, ei postinumeroaluekohtaisia. Tarvitaan aggregointi. Motivan energiatodistusrekisteri?
  - *Toteutus:* Jos data saatavilla, laske postinumeroalueen keskimääräinen energialuokka painotettuna asuntojen määrällä.
  - *Esimerkki:* "00100: Keskimääräinen energialuokka C (vanha rakennuskanta). Energiakustannus ~1800€/v."

- **Ilmanlaatu ja melu** (ympäristötekijät)
  - *Miksi:* Hyvä ilmanlaatu ja alhainen melutaso nostavat asuntojen arvoa. Vilkkaat tiet ja teollisuusalueet laskevat.
  - *Toteutus:* HSY (Helsingin seudun ympäristöpalvelut) ilmanlaatu-API. Tulliluodon melumalli (Helsingin kaupunki). Tallenna keskimääräiset PM2.5-pitoisuudet ja dB-tasot postinumeroalueittain.
  - *Esimerkki:* "00100: PM2.5 keskiarvo 6.2 µg/m³ (hyvä). Melutaso 65 dB (kohtalainen, vilkas liikenne). 00570: PM2.5 5.1 µg/m³, 54 dB (hiljainen)."

- **Historiallinen palveludata** (palveluiden kehityksen seuranta)
  - *Miksi:* Nähdä miten palvelut ovat kehittyneet alueilla ajan myötä. Onko alueelle tullut lisää kauppoja? Onko koulu suljettu?
  - *Toteutus:* Lataa Geofabrik arkistosta historiallisia OSM-snapshoteja (esim. 2015, 2017, 2019, 2021, 2023, 2025). Parse jokaiselle vuodelle palvelutiedot samalla tavalla. Tallenna aikasarjana.
  - *Haaste:* ~3-5 GB per snapshot-vuosi. Yhteensä ~20-30 GB dataa 6 vuodelle. Parsing kestää ~30-60 min kaikille vuosille.
  - *Hyöty:* Palvelutiedot voisi integroida 5v trendianalyysiin. Tutkia korrelaatiota palveluiden lisääntymisen ja hintojen nousun välillä.
  - *Esimerkki:* "00100: Kauppoja lisääntynyt 18→24 (2015-2025). Metro-asemia +2. Palveluindeksi kasvanut 65→78. Samaan aikana hinnat nousseet +42%."

**Osallistu kehitykseen!** Ehdotuksia ja pull requestejä otetaan vastaan mielellään.

## Lähdeviitteet

- Asuntohinnat: [Tilastokeskus StatFin](https://stat.fi/) - ashi_13mu
- Postinumeroalueet: [Tilastokeskus geo.stat.fi](https://geo.stat.fi/) - postialue:pno_tilasto
- Väestötiedot: [Tilastokeskus Paavo](https://www.stat.fi/tup/paavo/) - postialue:pno_tilasto_XXXX
- Palvelutiedot: [OpenStreetMap](https://www.openstreetmap.org/) via [Geofabrik](https://download.geofabrik.de/europe/finland.html) - finland-latest.osm.pbf
- Karttakirjasto: [Leaflet](https://leafletjs.com/)
- OSM-parsing: [pyosmium](https://osmcode.org/pyosmium/)
