# Muutosloki

Sivuston versio näkyy alatunnisteessa. Versio on määritelty tiedostossa `js/menu.js` (`SITE_VERSION`) ja alatunnisteen oletusteksti tiedostossa `tools/rakenna.py`.

Numerointi: **pää.osa.korjaus**. Kokonaan uusi ulkoasu tai rakenne nostaa pääversiota, uusi sivu tai osio osaversiota ja pieni korjaus korjausversiota.

## 2.1.0

Etusivun vaakavieritys Virpin toteutusohjeen mukaan.

- Tietokoneella (vähintään 1180 × 620 px) etusivun seitsemän väripaneelia ovat vierekkäin. Tavallinen vieritys hiiren rullalla, kosketuslevyllä tai näppäimillä avaa seuraavan paneelin koko näkymän kokoiseksi, ja edellinen kapenee sivuun. Taaksepäin vierittäminen toimii samoin.
- Tulevat paneelit näkyvät oikeassa reunassa kaistoina, joissa on numero ja nimi; kaistaa napsauttamalla pääsee suoraan paneeliin. Alareunassa näkyy, monesko paneeli on auki.
- Jos paneelin sisältö on näkymää korkeampi, vieritys näyttää ensin sisällön loppuun ennen seuraavaa paneelia, joten mitään ei ohiteta.
- Sivuttainen pyyhkäisy kosketuslevyllä vierittää samaan suuntaan.
- Näppäimistöllä fokus avaa paneelin, jossa fokusoitu kohta on. Ankkurilinkit (esim. Ota yhteyttä) vievät oikeaan paneeliin.
- Puhelimella, tabletilla, matalalla näytöllä ja kun kävijä on pyytänyt vähemmän liikettä, etusivu pysyy tavallisena pystyvierityksenä.
- HTML ei muutu, joten hakukoneet ja ruudunlukijat lukevat sisällön kuten ennenkin.

## 2.0.0

Uusi ulkoasu ja sisältö Virpin toteutusohjeen mukaan.

### Rakenne ja sisältö
- Omat sivut: Kiinteistöveroselvitykset, Paikkatietopalvelut, Yritys, Referenssit ja Yhteystiedot. Selkeät osoitteet (esim. `/kiinteistoveroselvitykset/`).
- Etusivu seitsemänä värillisenä paneelina: aloitus, kiinteistöveroselvitykset, paikkatietopalvelut, miksi VLiNdATA, referenssit, yrittäjä ja yhteystiedot. Aloituksessa paneelivalitsin, josta pääsee suoraan osioon.
- Tekstit sanatarkasti toteutusohjeesta, englanninkieliset käännökset kaikille sivuille.
- Kari Tuohin (Auran kunta) lainaus etusivulla ja referenssisivulla.
- Yhteydenottolomake (nimi, kunta tai organisaatio, sähköposti, viesti) avaa viestin kävijän sähköpostiohjelmassa. Tietoja ei tallenneta sivustolle.
- Hinnat poistettu, koska niitä ei ole uusissa teksteissä.
- Vanhat osoitteet `evasteet.html` ja `en/cookies.html` ohjautuvat uusiin.

### Ulkoasu
- Virpin valokuvasta poimittu väripaletti: salvianvihreä, vaalea vihreä, metsänvihreä, hiekka, luonnonvalkoinen ja terrakotta.
- Otsikot Manrope, leipäteksti Inter (omalta palvelimelta).
- Kaksi valokuvaa: kallio (aloitus, yhteystiedot) ja metsä (yrittäjä, yritys). Karttakuvio tehosteena.
- Uudet jakokuvat.

### Ylläpito
- Sivut kootaan skriptillä `tools/rakenna.py` tekstitiedostoista `tools/sivut/fi` ja `tools/sivut/en`. Yhteinen yläpalkki, alatunniste ja hakukonetiedot ovat yhdessä paikassa.
- sitemap.xml tehdään samalla skriptillä.

### Saavutettavuus ja hakukoneet
- Tarkistettu axe-työkalulla (WCAG 2.2 AA) kaikilla sivuilla tietokoneen ja puhelimen leveydellä: ei virheitä.
- Murupolku ja BreadcrumbList alasivuilla, Service-tieto palvelusivuilla.

## 1.0.0

Ensimmäinen versio ilman Mobirisea. Ulkoasu ja tekstit ovat samat kuin aiemmalla vlindata.fi-sivulla.

- Sivu rakennettu uudelleen puhtaaksi HTML-, CSS- ja JavaScript-koodiksi ilman Mobirisea ja Bootstrapia.
- Evästeilmoitus (Google Consent Mode v2): GA4 latautuu vasta hyväksynnän jälkeen.
- Hakukonetiedot, jakokuvat, favicon, manifesti, robots.txt, sitemap.xml, llms.txt ja 404-sivu.
- Englanninkielinen etusivu ja evästesivu.
- Saavutettavuuskorjaukset (otsikkotasot, kontrastit, näppäimistökäyttö).
