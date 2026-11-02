# Muutosloki

Sivuston versio näkyy alatunnisteessa. Versio on määritelty tiedostossa `js/menu.js` (`SITE_VERSION`). Nosta versiota jokaisessa muutoksessa ja kirjaa muutos tähän.

## 1.0.0

Ensimmäinen versio ilman Mobirisea. Ulkoasu ja tekstit ovat samat kuin aiemmalla vlindata.fi-sivulla.

### Perusta
- Sivu rakennettu uudelleen puhtaaksi HTML-, CSS- ja JavaScript-koodiksi ilman Mobirisea ja Bootstrapia.
- Lexend-fontti omalta palvelimelta (ei Google Fontsia), ikonit Lucide-kirjastosta.
- Kuvat oikeisiin tiedostomuotoihin; valokuvat JPG, logot WebP tai SVG.
- Rikkinäinen tiedosto `tausta.webp` ja Mobirise-merkki poistettu.
- Alatunniste: "© 2026 VLiNdATA Oy", evästeet ja evästeasetukset, versionumero.
- Ruskon referenssilinkki osoittaa kunnan etusivulle (vanha kiinteistökartoitussivu on poistunut).

### Saavutettavuus
- Otsikkotasot järjestykseen (h1 → h2 → h3), palvelujen kuvaukset kappaleiksi.
- Kontrastit WCAG AA -tasolle: harmaa leipäteksti ja vihreät painikkeet hieman tummemmiksi.
- "Siirry sisältöön" -linkki, näkyvä fokus, valikko toimii näppäimistöllä (Esc sulkee).
- Logon alt-teksti korjattu, ulkoisissa linkeissä tieto uudesta välilehdestä.
- Mobiilivalikko toimii myös ilman evästeiden hyväksyntää.

### Evästeet ja Google Analytics
- Uusi evästeilmoitus (Google Consent Mode v2). GA4 latautuu vasta hyväksynnän jälkeen.
- Valinnan voi muuttaa alatunnisteesta tai evästesivulta; peruminen poistaa GA-evästeet.
- Evästesivulle taulukko sivun evästeistä.

### Hakukoneet ja jakaminen
- Otsikko, kuvaus, canonical, Open Graph ja X-kortti, rakenteinen yritystieto (JSON-LD).
- Jakokuvat suomeksi ja englanniksi, favicon ja kotivalikon kuvakkeet, manifesti.
- robots.txt, sitemap.xml, llms.txt ja oma 404-sivu.

### Kieliversiot
- Englanninkielinen etusivu (`/en/`) ja evästesivu (`/en/cookies.html`), kielivalinta FI | EN.
