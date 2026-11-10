# Muutosloki

Sivuston versio näkyy puhelimen valikossa ja Evästeet-sivulla. Versio on määritelty tiedostossa `js/menu.js` (`SITE_VERSION`) ja tiedoston `tools/rakenna.py` vakiossa `VERSIO`.

Numerointi: **pää.osa.korjaus**. Kokonaan uusi ulkoasu tai rakenne nostaa pääversiota, uusi sivu tai osio osaversiota ja pieni korjaus korjausversiota.

## 2.6.1

- Julkaisu Domainhotellin kotisivutilaan: `.htaccess` (https- ja www-ohjaus, 404-sivu, tiedostotyypit, pakkaus, välimuisti, tietoturvaotsakkeet, ylläpitotiedostojen esto) ja julkaisuskripti `tools/julkaise.ps1` (WinSCP).

## 2.6.0

- Etusivulle oma Varautuminen-paneeli (04, salvianvihreä) Paikkatietopalvelujen jälkeen: otsikko, kaksi kappaletta, kolme korttia ja painike Varautuminen-sivulle. Paneelivalitsimeen uusi laatta, numerot 04–08.
- Paikkatietopalvelut-paneelin neljäs kortti poistettu (korvattu omalla paneelilla).
- Vaakavierityksen kaistat kavennettu 58 px → 50 px, jotta kahdeksan paneelia mahtuu.

## 2.5.0

- Uusi palvelusivu "Paikkatiedon jatkuvuus" (`/paikkatiedon-jatkuvuus/`, englanniksi `/en/gis-continuity/`), valikossa nimellä Varautuminen / Preparedness Kiinteistöveroselvitysten ja Paikkatietopalvelujen rinnalla: ongelma, toiminta neljänä vaiheena, mitä kunta saa (käyttöönotto, ylläpito, tuki varautumiseen), taustaa ja tarjouspyyntö. Tuotenimeä tai opinnäytetyötä ei mainita.
- Etusivun Paikkatietopalvelut-paneeliin neljäs kortti, joka vie uudelle sivulle.
- Yläpalkki levennetty (enintään 1440 px sisältöä) ja valikon tiivis tila 1180–1600 px näytöille, jotta valikko mahtuu yhdelle riville.
- Hakukonetiedot (Service), sitemap.xml ja llms.txt päivitetty.

## 2.4.7

- Vaakavierityksen paneelit tiivistetty, jotta ne mahtuvat näkymään ilman sisäistä pystyvieritystä (tietokoneen näytöt noin 1440 × 900 ja suuremmat):
  - Referenssit kahdessa sarakkeessa: lainaus vasemmalla, teksti, logot ja painike oikealla.
  - Yhteystietojen lomake tiiviimmäksi (nimi ja organisaatio rinnakkain, matalampi viestikenttä).
  - Yleisesti pienemmät välit, ingressit ja korttien täytteet vaakatilassa.

## 2.4.6

- Evästeet-sivulta poistettu Etusivulle-painike.
- Yhteystiedoissa (etusivu ja Yhteystiedot-sivu) verkkosivu linkkinä muodossa vlindata.fi ja Y-tunnus linkkinä YTJ:n yritystietoihin.

## 2.4.5

- Evästeet-sivun toteutusriville pieni pyöreä kuva ja nimi: "Tekninen toteutus: Oskari Summanen, summanen.org".

## 2.4.4

- Evästeet-sivun alalaita samaan tyyliin kuin puhelimen valikko: Evästeasetukset, © ja versio, tekninen toteutus omilla riveillään. Erillinen "Muuta evästevalintaa" -painike korvattu Evästeasetukset-linkillä.

## 2.4.3

- Puhelimen valikossa "Tekninen toteutus: summanen.org" omalle rivilleen.

## 2.4.2

- "Toteutus: summanen.org" → "Tekninen toteutus: summanen.org" (englanniksi "Technical implementation") Evästeet-sivulla ja puhelimen valikossa.

## 2.4.1

- Yhteistyössä-kortti poistettu Yritys-sivulta (ja kuva `img/oskari-summanen.webp`). Toteutusmaininta Evästeet-sivulla, puhelimen valikossa ja hakukonetiedoissa säilyy.

## 2.4.0

- Yritys-sivulle "Yhteistyössä"-kortti: Oskari Summanen, summanen.org – kumppani, joka tekee rekisterivertailut ja analyysit sekä toteuttaa ja ylläpitää sivuston. Kuva `img/oskari-summanen.webp`.
- Toteuttajamaininta "Toteutus: summanen.org" Evästeet-sivun alalaitaan ja puhelimen valikon alariville.
- Hakukonetietoihin sivuston tekijä (`creator`): Oskari Summanen, summanen.org.

## 2.3.0

- Kiinteistöveroselvitykset-sivulle uusi osio "Raportit kunnan johdolle" (`#raportit`): kiinteistöveroanalyysi ja kiinteistöveroprojektin vaikuttavuusseuranta (kolme kertaa vuodessa), tekstit Virpiltä. Kummassakin "Kysy raportista" -painike Yhteystiedot-sivulle.
- Sama englanniksi ("Reports for municipal management") ja llms.txt-tiedostoon.

## 2.2.0

Virpin muutospyynnöt (marraskuu 2026).

- Alatunniste poistettu kaikilta sivuilta. Evästeet-linkki on yläpalkin valikossa; puhelimen valikossa myös Evästeasetukset, © ja versio. Tietokoneella versio näkyy Evästeet-sivulla. Valikko tiivistyy 1180–1440 px näytöillä, jotta se mahtuu yhdelle riville.
- Y-tunnus etusivun Yhteystiedot-paneeliin ja Yhteystiedot-sivulle.
- Etusivun yrittäjäpaneeli: "VLiNdATA Oy:n yrittäjä", tausta "kuntien paikkatiedosta, rekistereistä ja maankäytöstä".
- Kiinteistöveroselvitykset: listaan "Vuosittainen kiinteistöverokertymän raportointi"; "Miten yhteistyö etenee?" neljänä korttina otsikoineen ja selityksineen; lause koko rakennuskannan selvityksestä poistettu.
- Paikkatietopalvelut: viisi osiota yhdistetty kolmeksi korostetuksi laatikoksi (tuottaminen ja päivittäminen, analyysit ja käsittely, asiantuntija-apu ja toimintatapojen kehittäminen).
- Yritys: tekstimuutokset ja kaksi uutta kappaletta (viranhaltijoiden lempeä potkiminen, yhteistyöverkostot).
- Referenssit: uusi Auran kunnan tapauskuvaus, vaiheet aikajanana (2024, 2024–2026, 2025–2026) ja tavoiteosio; otsikko leipätekstin yläpuolelle; logojen johdanto uudistettu.
- Versionumero rakennusskriptissä yhdessä vakiossa (`VERSIO`), sivupohjissa merkintä `{{versio}}`.

## 2.1.1

- Virpin kuvat vaihdettu keskenään: metsäkuva aloitukseen ja yhteystietoihin, kalliokuva yrittäjäosioon ja Yritys-sivulle.
- Vaakavierityksessä ohitetut paneelit jäävät vasempaan reunaan samanlaisina kaistoina (numero ja nimi) kuin tulevat paneelit oikealla. Kaistaa napsauttamalla pääsee takaisin paneeliin.

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
