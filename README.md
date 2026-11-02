# vlindata.fi

VLiNdATA Oy:n kotisivu. Staattinen sivusto: tavallisia HTML-, CSS- ja JavaScript-tiedostoja, ei julkaisutyökalua eikä käännösvaihetta. Ylläpito tehdään muokkaamalla tiedostoja (Clauden kanssa).

## Julkaisu

Kopioi kaikki tiedostot palvelimen juureen niin, että `index.html` on osoitteessa `https://vlindata.fi/`. `404.html` toimii virhesivuna, jos palvelin on asetettu käyttämään sitä (esim. GitHub Pages tekee sen itse).

Tiedostoja `LUEMINUT.md` ja `CHANGELOG.md` ei tarvitse julkaista, mutta niistä ei ole haittaa.

## Tiedostot

| Polku | Sisältö |
|---|---|
| `index.html` | etusivu suomeksi |
| `evasteet.html` | evästesivu suomeksi |
| `en/index.html`, `en/cookies.html` | samat englanniksi |
| `404.html` | "sivua ei löytynyt" molemmilla kielillä |
| `css/style.css` | kaikki tyylit, värit muuttujina alussa |
| `css/fonts.css`, `fonts/` | Lexend-fontti ja sen lisenssi |
| `js/consent.js` | evästeilmoitus ja Google Analytics 4 (G-73CPF19H48) |
| `js/menu.js` | mobiilivalikko, aktiivinen osio, versionumero |
| `img/` | kuvat, logot, jakokuvat (`og-kuva.jpg`, `og-kuva-en.jpg`) |
| `favicon.*`, `apple-touch-icon.png`, `img/icons/`, `site.webmanifest` | kuvakkeet |
| `robots.txt`, `sitemap.xml`, `llms.txt` | hakukoneille ja tekoälyhauille |

## Muistettavaa muutoksissa

- Tekstimuutos tehdään molempiin kieliversioihin (`index.html` ja `en/index.html`).
- Nosta versiota `js/menu.js`:ssä ja kirjaa muutos `CHANGELOG.md`:hen.
- Päivitä `sitemap.xml`:n `lastmod`, kun sisältö muuttuu isosti.
- Jos herokuva tai pääteksti muuttuu, jakokuvat tehdään uudelleen.

## Lisenssit

| Osa | Lähde | Lisenssi |
|---|---|---|
| Lexend-fontti | @fontsource-variable/lexend 5.3.0 | SIL Open Font License 1.1 (`fonts/OFL-Lexend.txt`) |
| Ikonit (palvelut, yhteystiedot) | Lucide (lucide-static 1.66.0) | ISC (`LICENSE-lucide.txt`) |
| Kuntien logot | kuntien omat tunnukset | kuntien tavaramerkkejä, käytössä referensseinä |
