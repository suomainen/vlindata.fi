# vlindata.fi

VLiNdATA Oy:n kotisivu, https://vlindata.fi/. Tekninen toteutus ja ylläpito: Oskari Summanen, [summanen.org](https://summanen.org/). Staattinen sivusto: tavallisia HTML-, CSS- ja JavaScript-tiedostoja ilman julkaisutyökalua. Sivut kootaan pienellä Python-skriptillä ja julkaistaan Domainhotellin kotisivutilaan WinSCP:llä.

## Rakenne

```
index.html                       etusivu (koottu, älä muokkaa käsin)
kiinteistoveroselvitykset/       palvelusivu
paikkatietopalvelut/             palvelusivu
paikkatiedon-jatkuvuus/          palvelusivu: paikallinen varajärjestelmä (valikossa "Varautuminen")
yritys/  referenssit/  yhteystiedot/  evasteet/
en/                              englanninkieliset sivut samassa järjestyksessä
404.html                         "sivua ei löytynyt" molemmilla kielillä
evasteet.html, en/cookies.html   vanhojen osoitteiden ohjaukset
css/style.css                    kaikki tyylit, värit muuttujina alussa
css/fonts.css, fonts/            Manrope ja Inter sekä lisenssit
js/consent.js                    evästeilmoitus ja Google Analytics 4
js/menu.js                       mobiilivalikko ja versionumero
js/teema.js                      vaalea/tumma ulkoasu ja yläpalkin teemanappi (ladataan heti, ilman deferiä)
js/contact-form.js               yhteydenottolomake (avaa sähköpostin)
js/vaakavieritys.js              etusivun vaakavieritys tietokoneella
img/                             valokuvat, karttakuviot, logot, jakokuvat
favicon.*, apple-touch-icon.png, img/icons/, site.webmanifest   kuvakkeet
robots.txt, sitemap.xml, llms.txt                               hakukoneille
tools/rakenna.py                 kokoaa sivut ja sitemap.xml:n
tools/julkaise.ps1               julkaisu Domainhotelliin WinSCP:llä
tools/commitviesti.ps1           automaattinen commit-viesti julkaise.bat:lle
.htaccess                        palvelimen asetukset (https, 404, välimuisti)
tools/sivut/fi/, tools/sivut/en/ sivujen tekstit (yksi tiedosto per sivu)
tools/ikonit/                    Lucide-ikonit, jotka skripti upottaa sivuille
```

## Esikatselu

```
python tools/rakenna.py
python -m http.server 8000
```

Avaa selaimessa http://localhost:8000/.

## Muokkaaminen

- **Tekstit:** muokkaa tiedostoa `tools/sivut/fi/<sivu>.html` ja vastaavaa `tools/sivut/en/<sivu>.html`, aja sitten `python tools/rakenna.py`. Älä muokkaa koottuja `index.html`-tiedostoja käsin, koska skripti kirjoittaa ne yli.
- **Sivujen otsikot, kuvaukset ja valikko:** `tools/rakenna.py`, kohta `SIVUT`.
- **Yläpalkki ja valikko (myös Evästeet, Evästeasetukset ja versio), evästeilmoitus:** `tools/rakenna.py`, funktiot `header` ja `evasteilmoitus` sekä `TEKSTIT`. Sivustolla ei ole erillistä alatunnistetta.
- **Referenssikuntien logot:** `tools/rakenna.py`, kohta `LOGOT`, ja kuvat kansioon `img/logot/`.
- **Värit ja fontit:** `css/style.css`, kohta 1. Kontrastit on laskettu kommentteihin; tarkista ne, jos vaihdat värejä.
- **Tumma ulkoasu:** `css/style.css`, kohta 1. Oletus on aina vaalea; tumma ulkoasu tulee käyttöön vain yläpalkin napista (`:root[data-teema="tumma"]`). Valinta tallentuu selaimeen avaimella `vlindata-teema` (js/teema.js).
- Sivupohjien merkinnät (`{{root}}`, `{{ikoni:nimi}}`, `{{sivu:avain}}`, `{{lomake}}`, `{{logot}}`, `{{murupolku}}`, `{{versio}}`) on selitetty skriptin alussa.

## Julkaisu

Sivusto julkaistaan Domainhotellin kotisivutilaan (`/public_html`) WinSCP:llä skriptillä `tools/julkaise.ps1`. GitHub on versionhallinta ja varmuuskopio; sivu ei ole GitHub Pagesissa.

### Kertaluonteinen valmistelu

1. Asenna [WinSCP](https://winscp.net/).
2. Luo WinSCP:ssä uusi yhteys (New Site) Domainhotellin FTP-tunnuksilla:
   - protokolla **SFTP** (portti 22), jos SSH on käytössä, muuten **FTP** + salaus **TLS/SSL Explicit** (portti 21). Ei salaamatonta FTP:tä.
   - palvelin, käyttäjätunnus ja salasana Domainhotellin tunnusviestistä
   - tallenna nimellä **vlindata** ja valitse tallenna salasana.
3. Avaa yhteys kerran WinSCP:n ikkunassa ja hyväksy palvelimen avain tai varmenne. Tarkista samalla, että sivuston juurikansio on `/public_html`.

Tunnuksia ei tallenneta repoon.

### Julkaisu

```
git add -A
git commit -m "Kuvaus muutoksesta"
git tag -a v2.6.1 -m "Kuvaus"
git push --follow-tags
.\tools\julkaise.ps1 -Esikatselu   # näyttää, mitä siirtyisi
.\tools\julkaise.ps1               # julkaisee muuttuneet tiedostot
```

Ensimmäisellä kerralla:

```
.\tools\julkaise.ps1 -Varmuuskopio   # vanha sivu talteen kansioon ..\vlindata-varmuuskopio\
.\tools\julkaise.ps1                 # uusi sivu palvelimelle
.\tools\julkaise.ps1 -Poista -Esikatselu   # näyttää vanhan sivun jäänteet
.\tools\julkaise.ps1 -Poista               # poistaa ne
```

Skripti ei siirrä ylläpitotiedostoja (`tools/`, `.git/`, `README.md`, `CHANGELOG.md`, `*.bat`), eikä `-Poista` koske palvelimen omiin kansioihin (`.well-known/`, `cgi-bin/`). Se varoittaa, jos repossa on tallentamattomia muutoksia. Loki: `%TEMP%\vlindata-julkaisu.log`.

### Pikakomento `julkaise.bat`

Oskarin koneella repon juuressa on `julkaise.bat`, joka ei ole versionhallinnassa (`.git/info/exclude`). Se kokoaa sivut, tekee commitin ja version tagin (`js/menu.js`:n `SITE_VERSION`), vie muutokset GitHubiin ja julkaisee esikatselun jälkeen palvelimelle. Commit-viestin muodostaa `tools/commitviesti.ps1`: uuden version kohdalla muutoslokin ensimmäinen kohta, muuten "ylläpito", ja runkoon muuttuneet tiedostot.

`tools/rakenna.py` kirjoittaa sivut aina LF-rivinvaihdoin, jotta Windowsissa ajettuna git ei näe kaikkia sivuja muuttuneina.

### Palvelimen asetukset (`.htaccess`)

`.htaccess` julkaistaan muiden tiedostojen mukana. Se ohjaa osoitteet muotoon `https://vlindata.fi/` (myös www- ja http-osoitteet), ottaa käyttöön 404-sivun, estää kansiolistauksen ja ylläpitotiedostojen näkymisen, asettaa tiedostotyypit, pakkauksen, välimuistin ja tietoturvaotsakkeet.

Jos push GitHubiin hylätään ("fetch first"): `git pull --rebase` ja uudelleen `git push --follow-tags`.

## Versiointi

- Versio näkyy puhelimen valikossa ja Evästeet-sivulla. Numero on tiedostossa `js/menu.js` (`SITE_VERSION`) ja `tools/rakenna.py`:n vakiossa `VERSIO`; nosta molemmat.
- Kirjaa muutos `CHANGELOG.md`:hen (uusin ensin, ei päivämääriä).
- Merkitse versio: `git tag -a v2.0.1 -m "Kuvaus"` ja julkaise `git push --follow-tags`.
- Pelkkä README- tai muutoslokimuutos ei nosta versiota.

## Etusivun vaakavieritys

`js/vaakavieritys.js` asettaa etusivun paneelit (`<section class="panel" data-hz="Nimi">`) vierekkäin, kun näyttö on vähintään 1180 × 620 px eikä kävijä ole pyytänyt vähemmän liikettä. Muuten sivu on tavallinen pystysivu. Asetukset (kaistojen leveys 50 px, avautumisen pituus) ovat tiedoston alussa; kaistan leveys on myös `css/style.css`:ssä (`.hz__kaista`) ja tyylit `css/style.css`:n kohdassa 17. Uusi paneeli lisätään etusivun tekstitiedostoon `data-hz`-nimen kanssa, ja se tulee vaakavieritykseen automaattisesti.

## Analytiikka ja evästeet

Google Analytics 4 (G-73CPF19H48) ladataan vasta, kun kävijä hyväksyy evästeet (Google Consent Mode v2). Valinta tallennetaan selaimeen (`vlindata-consent`), ja sen voi muuttaa Evästeet-sivun napista tai puhelimen valikon Evästeasetukset-napista. Peruminen poistaa GA-evästeet.

Yhteydenottolomake ei lähetä tietoja millekään palvelimelle: se avaa viestin kävijän omassa sähköpostiohjelmassa. Siksi lomakkeen kautta ei voi tulla roskapostia eikä tietoja tallennu sivustolle.

## Hakukoneet ja jakaminen

Jokaisella sivulla on otsikko, kuvaus, canonical, kieliversiolinkit (hreflang), Open Graph- ja X-kortti sekä rakenteinen tieto (JSON-LD: WebSite, Organization, Person, WebPage, alasivuilla BreadcrumbList ja palvelusivuilla Service). Jakokuvat: `img/og-kuva.jpg` ja `img/og-kuva-en.jpg`.

## Kolmannen osapuolen tiedostot ja oikeudet

| Tiedosto | Versio | Lisenssi tai oikeus |
|---|---|---|
| Manrope (`fonts/manrope-latin-wght.woff2`) | @fontsource-variable/manrope 5.3.0 | SIL Open Font License 1.1, `fonts/OFL-Manrope.txt` |
| Inter (`fonts/inter-latin-wght.woff2`) | @fontsource-variable/inter 5.3.0 | SIL Open Font License 1.1, `fonts/OFL-Inter.txt` |
| Ikonit (`tools/ikonit/`) | lucide-static 1.66.0 | ISC, `LICENSE-lucide.txt` |
| Kuntien logot (`img/logot/`) | – | kuntien tavaramerkkejä, käytössä referensseinä |
| Valokuvat (`img/virpi-*.jpg`) | – | kuvaajan tekijänoikeus, käyttölupa VLiNdATA Oy:llä |
| Kuva `img/oskari-summanen.webp` | – | Oskari Summasen kuva, käyttölupa |

© VLiNdATA Oy. Kaikki oikeudet pidätetään.
