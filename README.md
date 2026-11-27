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
sv/                              ruotsinkieliset sivut (piilossa, ks. Ruotsinkielinen versio)
luottamus/, tietosuojaseloste/   Luottamus ja tietoturva sekä tietosuojaseloste (piilossa; en/trust-center/, en/privacy-notice/)
404.html                         "sivua ei löytynyt" molemmilla kielillä
evasteet.html, en/cookies.html   vanhojen osoitteiden ohjaukset
css/style.css                    kaikki tyylit, värit muuttujina alussa
css/fonts.css, fonts/            Manrope ja Inter sekä lisenssit
js/consent.js                    evästeilmoitus, Google Analytics 4 ja Microsoft Clarity
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
Sivutyokalu.bat, tools/sivutyokalu.ps1   päivitystyökalu (ikkuna): hae, esikatsele, julkaise, zip
tools/asennus/                   työkalun asennus toiselle koneelle ja käyttöohje (OHJE.md, OHJE.pdf)
package.json, package-lock.json  fonttien ja ikonien versiot (Dependabot), ei julkaista
SECURITY.md                      haavoittuvuuksien ilmoittaminen
.github/dependabot.yml           Dependabotin viikkotarkistus (npm ja pip)
.htaccess                        palvelimen asetukset (https, 404, välimuisti)
tools/sivut/fi/, en/, sv/        sivujen tekstit (yksi tiedosto per sivu ja kieli)
tools/fontit.py, tools/requirements.txt   kiinteät fontit npm-paketeista (vain ylläpitoon)
tools/ikonit/                    Lucide-ikonit, jotka skripti upottaa sivuille
```

## Esikatselu

```
python tools/rakenna.py
python -m http.server 8000
```

Avaa selaimessa http://localhost:8000/.

## Muokkaaminen

- **Tekstit:** muokkaa tiedostoa `tools/sivut/fi/<sivu>.html` ja vastaavia `tools/sivut/en/<sivu>.html` ja `tools/sivut/sv/<sivu>.html`, aja sitten `python tools/rakenna.py`. Älä muokkaa koottuja `index.html`-tiedostoja käsin, koska skripti kirjoittaa ne yli.
- **Sivujen otsikot, kuvaukset ja valikko:** `tools/rakenna.py`, kohta `SIVUT`.
- **Yläpalkki ja valikko (myös Evästeet, Analytiikkaevästeet-kytkin ja versio), evästeilmoitus:** `tools/rakenna.py`, funktiot `header` ja `evasteilmoitus` sekä `TEKSTIT`. Sivustolla ei ole erillistä alatunnistetta.
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

### Sivutyökalu (Virpi)

`Sivutyokalu.bat` avaa ikkunan (`tools/sivutyokalu.ps1`, PowerShell + Windows Forms), jolla sivuja voi päivittää ilman komentoriviä:

- **Hae uusin versio**: `git pull --rebase`. Omat muutokset pannaan hetkeksi sivuun (`git stash`) ja palautetaan; kootut sivut palautetaan ensin ennalleen ja kootaan lopuksi uudelleen, jotta ne eivät aiheuta ristiriitoja. Jos sama kohta on muuttunut molemmilla, muutokset jäävät `git stash`iin ja työkalu pyytää ottamaan yhteyttä Oskariin.
- **Julkaise**: hakee uusimman, kokoaa sivut, nostaa korjausversiota (2.8.2 → 2.8.3, ohittaa varatut tagit), kirjaa muutoslokiin kävijän kirjoittaman kuvauksen, tekee commitin `vlindata.fi X.Y.Z: kuvaus`, vie GitHubiin, tekee tagin ja julkaisee `tools/julkaise.ps1`:llä esikatselun ja vahvistuksen jälkeen. Jos joku ehti viedä muutoksia väliin, versionnosto kumotaan ja kaikki tehdään uudelleen uusimman päälle.
- **Avaa tekstit**, **Esikatsele** (paikallinen palvelin portissa 8765), **Tee zip työpöydälle**, **Avaa vlindata.fi**.

Loki: `%TEMP%\vlindata-sivutyokalu.log`. Funktioita voi testata ilman ikkunaa: `. .\tools\sivutyokalu.ps1 -EiIkkunaa`.

Asennus toiselle koneelle: `tools/asennus/asenna.bat` (Git, Python ja WinSCP wingetillä, repon haku, nimi muutoshistoriaan, työpöydän pikakuvake, WinSCP-yhteyden ohje). Käyttäjä tarvitsee GitHub-tunnuksen, jolla on pääsy repoon. Käyttöohje: `tools/asennus/OHJE.pdf`.

### Palvelimen asetukset (`.htaccess`)

`.htaccess` julkaistaan muiden tiedostojen mukana. Se ohjaa osoitteet muotoon `https://vlindata.fi/` (myös www- ja http-osoitteet), ottaa käyttöön 404-sivun, estää kansiolistauksen ja ylläpitotiedostojen näkymisen, asettaa tiedostotyypit, pakkauksen, välimuistin ja tietoturvaotsakkeet.

Jos push GitHubiin hylätään ("fetch first"): `git pull --rebase` ja uudelleen `git push --follow-tags`.

## Versiointi

- Versio näkyy puhelimen valikossa ja Evästeet-sivulla. Numero on tiedostossa `js/menu.js` (`SITE_VERSION`) ja `tools/rakenna.py`:n vakiossa `VERSIO`; nosta molemmat.
- Kirjaa muutos `CHANGELOG.md`:hen (uusin ensin, ei päivämääriä).
- Merkitse versio: `git tag -a v2.0.1 -m "Kuvaus"` ja julkaise `git push --follow-tags`.
- Pelkkä README- tai muutoslokimuutos ei nosta versiota.

## Ruotsinkielinen versio

Ruotsinkieliset sivut ovat osoitteessa https://vlindata.fi/sv/, mutta ne ovat piilossa, kunnes ruotsia äidinkielenään puhuva on tarkistanut käännöksen:

- sivut ovat `noindex, nofollow`, eivät ole sitemapissa eikä suomen- ja englanninkielisten sivujen kielivalinnassa tai hreflang-linkeissä
- ruotsinkielisellä sivulla on kielivalinta FI · EN · SV, joten tarkistaja voi vertailla kieliä
- sanasto on tarkistettu kaksikielisten kuntien sivuilta ([Kimitoön](https://www.kimitoon.fi/boende-och-miljo/), [Pargas](https://www.pargas.fi/sv/kartor-och-geografisk-information)): paikkatieto = geografisk information / GIS (ei geodata), byggnadstillsyn, planläggning och markanvändning, säkerhet och beredskap; valikossa Fastighetsskatt, Kartor och GIS, Beredskap

Julkaisu, kun käännös on tarkistettu:

1. `tools/rakenna.py`: lisää `"sv"` listaan `JULKAISTUT` ja aja `python tools/rakenna.py`. Kielivalinta, hreflang ja sitemap päivittyvät kaikille sivuille.
2. `404.html`: lisää ruotsinkielinen teksti ja linkki `/sv/`.
3. `llms.txt`: lisää ruotsinkielinen osio.
4. Jakokuva: ruotsinkieliset sivut käyttävät nyt englanninkielistä `img/og-kuva-en.jpg`; tee tarvittaessa `img/og-kuva-sv.jpg` ja vaihda se funktioon `head`.

## Luottamus ja tietoturva (trust center)

Sivut `luottamus/` (Luottamus ja tietoturva) ja `tietosuojaseloste/` sekä englanniksi `en/trust-center/` ja `en/privacy-notice/` ovat piilossa: `"piilossa": True` kohdassa `SIVUT` tekee niistä noindex-sivuja, jotka eivät ole valikossa eivätkä sitemapissa. Ruotsinkielistä versiota ei vielä ole (sivut puuttuvat `POLUT`-kohdan sv-sarakkeesta, joten kielivalinta näyttää vain FI ja EN).

Henkilötietojen käsittelytoimien kuvaus tulee ERPin tarjoustyökalusta (JYSE/JIT Henkilötiedot 2025), ja sivun tekstit vastaavat sitä.

Julkaisu: poista `"piilossa": True` molemmista kielistä, lisää linkit esimerkiksi valikon alaosaan (`nav__evasteet`) ja Evästeet-sivulle, aja `python tools/rakenna.py`.

## Etusivun vaakavieritys

`js/vaakavieritys.js` asettaa etusivun paneelit (`<section class="panel" data-hz="Nimi">`) vierekkäin, kun näyttö on vähintään 1180 × 620 px eikä kävijä ole pyytänyt vähemmän liikettä. Muuten sivu on tavallinen pystysivu. Asetukset (kaistojen leveys 50 px, avautumisen pituus) ovat tiedoston alussa; kaistan leveys on myös `css/style.css`:ssä (`.hz__kaista`) ja tyylit `css/style.css`:n kohdassa 17. Uusi paneeli lisätään etusivun tekstitiedostoon `data-hz`-nimen kanssa, ja se tulee vaakavieritykseen automaattisesti.

## Tietoturva

Haavoittuvuuksien ilmoittaminen: ks. [SECURITY.md](SECURITY.md).

### Mitä suojattavaa on

Sivusto on staattinen: ei tietokantaa, kirjautumista eikä palvelinpuolen ohjelmia. Yhteydenottolomake avaa viestin kävijän omassa sähköpostiohjelmassa eikä lähetä mitään palvelimelle. Analytiikka (Google Analytics ja Microsoft Clarity) latautuu vasta evästehyväksynnän jälkeen.

| Riski | Miten hoidettu |
| --- | --- |
| GitHub-tili ja repo | Repo on yksityinen; tilin kaksivaiheinen tunnistautuminen on ylläpitäjän vastuulla. |
| Palvelimen FTP-tunnukset | Tallennettu vain WinSCP:hen ylläpitäjien koneille, ei repoon. |
| Vieras koodi sivulla | Sisältöturvakäytäntö (`CSP` tiedostossa `tools/rakenna.py` ja `404.html`): selain lataa vain sivuston omat tiedostot sekä Googlen ja Clarityn skriptit. Uusi ulkoinen palvelu pitää lisätä käytäntöön. Sivulla ei ole inline-skriptejä eikä `style`-attribuutteja. |
| Ylläpitotiedostot palvelimella | `julkaise.ps1` ei siirrä niitä, ja `.htaccess` estää `tools/`-kansion, `.md`-, `.py`-, `.ps1`- ja `package*.json`-tiedostot. |
| Upotus toisen sivun sisään, MIME-arvailu | `.htaccess`: `X-Frame-Options`, `X-Content-Type-Options`, `Referrer-Policy`, `Permissions-Policy`. |
| Kolmannen osapuolen tiedostot | Versiot `package.json`:ssa ja `tools/requirements.txt`:ssä, Dependabot seuraa (alla). |

### Mitä palvelin hoitaa

Domainhotelli ylläpitää palvelimen ja sen päivitykset sekä HTTPS-varmenteen (uusiutuu automaattisesti, siksi `.well-known` jätetään rauhaan). `.htaccess` ohjaa kaiken liikenteen HTTPS:ään.

### Riippuvuuksien seuranta

Sivu ei käytä JavaScript-kirjastoja eikä tarvitse npm:ää. Kolmannen osapuolen tiedostot ovat valmiina repossa, ja niiden versiot on kirjattu, jotta **Dependabot** näkee ne (`.github/dependabot.yml`, viikoittain maanantaisin; toimii ilman GitHub Actionsia). `package.json`, `package-lock.json` ja `tools/requirements.txt` eivät mene palvelimelle.

- **Fontit** `fonts/inter-400.woff2` … `manrope-800.woff2` ovat kiinteäpainoisia versioita pakettien `@fontsource-variable/inter` ja `@fontsource-variable/manrope` muuttuvista fonteista (vanhojen iPhonejen Safari näyttää muuttuvat fontit huonosti). Päivitys: vaihda versio `package.json`:iin, aja `npm install`, `pip install -r tools/requirements.txt` ja `python tools/fontit.py`. Uusi paino lisätään skriptin `PAINOT`-listaan ja `css/fonts.css`:ään.
- **Ikonit** `tools/ikonit/*.svg` ovat paketista `lucide-static` (LinkedIn-ikoni versiosta 0.460.0, alias `lucide-static-linkedin`).
- **Python-paketit** `fonttools` ja `brotli` (`tools/requirements.txt`) tarvitaan vain fonttien tekoon. `tools/rakenna.py` käyttää vain Pythonin omia kirjastoja.
- **Google Analytics ja Microsoft Clarity** ladataan palveluntarjoajan palvelimelta aina uusimpana versiona, joten niitä ei voi kirjata versioina.

Käsin ajettavat tarkistukset:

```
npm audit
pip install pip-audit
pip-audit -r tools/requirements.txt
```

Jokainen löydetty haavoittuvuus (CVE) verrataan CISA:n KEV-luetteloon (tunnetusti hyödynnetyt haavoittuvuudet, https://www.cisa.gov/known-exploited-vulnerabilities-catalog). KEV-luettelossa oleva korjataan heti, muut seuraavan päivityksen yhteydessä. Luettelosta kannattaa hakea myös ylläpidon ohjelmia: Git, Python, WinSCP ja palvelimen cPanel/LiteSpeed.

## Analytiikka ja evästeet

Google Analytics 4 (G-73CPF19H48) ja Microsoft Clarity (`zho2cm3xyq`, lämpökartat ja istuntotallenteet) ladataan vasta, kun kävijä hyväksyy evästeet (Google Consent Mode v2 ja Clarityn `consentv2`). Valinta tallennetaan selaimeen (`vlindata-consent`), ja sen voi muuttaa Analytiikkaevästeet-kytkimellä (Evästeet-sivulla otsikon alla ja puhelimen valikossa). Peruminen poistaa GA- ja Clarity-evästeet (`_ga*`, `_clck`, `_clsk`).

Yhteydenottolomake ei lähetä tietoja millekään palvelimelle: se avaa viestin kävijän omassa sähköpostiohjelmassa. Siksi lomakkeen kautta ei voi tulla roskapostia eikä tietoja tallennu sivustolle.

## Hakukoneet ja jakaminen

Jokaisella sivulla on otsikko, kuvaus, canonical, kieliversiolinkit (hreflang), Open Graph- ja X-kortti sekä rakenteinen tieto (JSON-LD: WebSite, Organization, Person, WebPage, alasivuilla BreadcrumbList ja palvelusivuilla Service). Jakokuvat: `img/og-kuva.jpg` ja `img/og-kuva-en.jpg`.

## Kolmannen osapuolen tiedostot ja oikeudet

| Tiedosto | Versio | Lisenssi tai oikeus |
|---|---|---|
| Manrope (`fonts/manrope-600/700/800.woff2`) | @fontsource-variable/manrope 5.3.0 | SIL Open Font License 1.1, `fonts/OFL-Manrope.txt` |
| Inter (`fonts/inter-400/500/600/700.woff2`) | @fontsource-variable/inter 5.3.0 | SIL Open Font License 1.1, `fonts/OFL-Inter.txt` |
| Ikonit (`tools/ikonit/`) | lucide-static 1.66.0 | ISC, `LICENSE-lucide.txt` |
| LinkedIn-ikoni (`tools/ikonit/linkedin.svg`) | lucide-static 0.460.0 (brändi-ikonit poistuivat myöhemmistä versioista) | ISC; LinkedIn on LinkedIn Corporationin tavaramerkki |
| Kuntien logot (`img/logot/`) | – | kuntien tavaramerkkejä, käytössä referensseinä |
| Valokuvat (`img/virpi-*.jpg`) | – | kuvaajan tekijänoikeus, käyttölupa VLiNdATA Oy:llä |
| Kuva `img/oskari-summanen.webp` | – | Oskari Summasen kuva, käyttölupa |

© VLiNdATA Oy. Kaikki oikeudet pidätetään.
