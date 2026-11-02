# vlindata.fi

VLiNdATA Oy:n kotisivu, https://vlindata.fi/. Staattinen sivusto: tavallisia HTML-, CSS- ja JavaScript-tiedostoja ilman julkaisutyökalua. Sivut kootaan pienellä Python-skriptillä, ja ne voi julkaista sellaisenaan GitHub Pagesissa tai millä tahansa palvelimella.

## Rakenne

```
index.html                       etusivu (koottu, älä muokkaa käsin)
kiinteistoveroselvitykset/       palvelusivu
paikkatietopalvelut/             palvelusivu
yritys/  referenssit/  yhteystiedot/  evasteet/
en/                              englanninkieliset sivut samassa järjestyksessä
404.html                         "sivua ei löytynyt" molemmilla kielillä
evasteet.html, en/cookies.html   vanhojen osoitteiden ohjaukset
css/style.css                    kaikki tyylit, värit muuttujina alussa
css/fonts.css, fonts/            Manrope ja Inter sekä lisenssit
js/consent.js                    evästeilmoitus ja Google Analytics 4
js/menu.js                       mobiilivalikko ja versionumero
js/contact-form.js               yhteydenottolomake (avaa sähköpostin)
img/                             valokuvat, karttakuviot, logot, jakokuvat
favicon.*, apple-touch-icon.png, img/icons/, site.webmanifest   kuvakkeet
robots.txt, sitemap.xml, llms.txt                               hakukoneille
tools/rakenna.py                 kokoaa sivut ja sitemap.xml:n
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
- **Alatunniste, evästeilmoitus, yläpalkki:** `tools/rakenna.py`, funktiot `header` ja `footer` sekä `TEKSTIT`.
- **Referenssikuntien logot:** `tools/rakenna.py`, kohta `LOGOT`, ja kuvat kansioon `img/logot/`.
- **Värit ja fontit:** `css/style.css`, kohta 1. Kontrastit on laskettu kommentteihin; tarkista ne, jos vaihdat värejä.
- Sivupohjien merkinnät (`{{root}}`, `{{ikoni:nimi}}`, `{{sivu:avain}}`, `{{lomake}}`, `{{logot}}`, `{{murupolku}}`) on selitetty skriptin alussa.

## Julkaisu

```
git add -A
git commit -m "Kuvaus muutoksesta"
git push --follow-tags
```

Jos push hylätään ("fetch first"), GitHubissa on muutos, jota koneella ei ole (esim. GitHubin luoma `CNAME`):

```
git pull --rebase
git push --follow-tags
```

## Versiointi

- Versio näkyy alatunnisteessa. Numero on tiedostossa `js/menu.js` (`SITE_VERSION`) ja oletusteksti `tools/rakenna.py`:ssä; nosta molemmat.
- Kirjaa muutos `CHANGELOG.md`:hen (uusin ensin, ei päivämääriä).
- Merkitse versio: `git tag -a v2.0.1 -m "Kuvaus"` ja julkaise `git push --follow-tags`.
- Pelkkä README- tai muutoslokimuutos ei nosta versiota.

## Analytiikka ja evästeet

Google Analytics 4 (G-73CPF19H48) ladataan vasta, kun kävijä hyväksyy evästeet (Google Consent Mode v2). Valinta tallennetaan selaimeen (`vlindata-consent`), ja sen voi muuttaa alatunnisteen Evästeasetukset-napista. Peruminen poistaa GA-evästeet.

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

© VLiNdATA Oy. Kaikki oikeudet pidätetään.
