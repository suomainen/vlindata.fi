"""Rakentaa vlindata.fi-sivuston HTML-sivut.

Tekstit ovat kansiossa tools/sivut/fi ja tools/sivut/en (yksi tiedosto per sivu).
Tämä skripti lisää jokaiseen sivuun yhteisen <head>-osan, yläpalkin, alatunnisteen
ja evästeilmoituksen sekä kirjoittaa sivut oikeisiin kansioihin.

Aja sivuston juurikansiosta tai mistä tahansa:  python tools/rakenna.py

Sivupohjien merkinnät:
  {{root}}        polku sivuston juureen (./, ../ tai ../../)
  {{ikoni:nimi}}  Lucide-ikoni kansiosta tools/ikonit (esim. {{ikoni:arrow-right}})
  {{sivu:avain}}  linkki saman kielen sivulle (esim. {{sivu:yhteystiedot}})
  {{lomake}}      yhteydenottolomake
  {{logot}}       referenssikuntien logot
  {{murupolku}}   murupolku
  {{versio}}      sivuston versionumero
"""
import json
import re
from pathlib import Path

JUURI = Path(__file__).resolve().parent.parent
TYOKALUT = JUURI / "tools"
DOMAIN = "https://vlindata.fi/"
VUOSI = "2026"
VERSIO = "2.6.0"   # sama kuin js/menu.js:n SITE_VERSION; nosta molemmat

# ---------------------------------------------------------------------------
# Sivut: avain -> polku kummallakin kielellä. Navigaation järjestys on tämä.
# ---------------------------------------------------------------------------
POLUT = {
    "etusivu":        {"fi": "",                           "en": "en/"},
    "kiinteistovero": {"fi": "kiinteistoveroselvitykset/", "en": "en/property-tax-audits/"},
    "paikkatieto":    {"fi": "paikkatietopalvelut/",       "en": "en/gis-services/"},
    "jatkuvuus":      {"fi": "paikkatiedon-jatkuvuus/",    "en": "en/gis-continuity/"},
    "yritys":         {"fi": "yritys/",                    "en": "en/company/"},
    "referenssit":    {"fi": "referenssit/",               "en": "en/references/"},
    "yhteystiedot":   {"fi": "yhteystiedot/",              "en": "en/contact/"},
    "evasteet":       {"fi": "evasteet/",                  "en": "en/cookies/"},
}
NAVIGAATIO = ["etusivu", "kiinteistovero", "paikkatieto", "jatkuvuus", "yritys", "referenssit", "yhteystiedot"]

SIVUT = {
    "fi": {
        "etusivu": {
            "nav": "Etusivu",
            "title": "VLiNdATA Oy – paikkatieto ja kiinteistöveroselvitykset kunnille",
            "description": "VLiNdATA Oy auttaa kuntia kiinteistöveroselvityksissä, rakennusrekisterien laadun parantamisessa ja paikkatietoaineistojen tuottamisessa. Yli 20 vuoden kokemus.",
        },
        "kiinteistovero": {
            "nav": "Kiinteistöveroselvitykset",
            "title": "Kiinteistöveroselvitykset ja rakennusrekisterit – VLiNdATA Oy",
            "description": "Kiinteistöveroselvitys tunnistaa rekistereistä puuttuvat ja virheelliset rakennukset. Työ etenee vaiheittain kunnan resurssien mukaan.",
            "service": "Kiinteistöveroselvitykset ja rakennusrekisterien laadun parantaminen",
        },
        "paikkatieto": {
            "nav": "Paikkatietopalvelut",
            "title": "Paikkatietopalvelut kunnille – VLiNdATA Oy",
            "description": "Paikkatietoaineistojen tuottaminen, päivittäminen ja analysointi sekä asiantuntija-apu järjestelmiin, rekistereihin ja tiedonhallintaan.",
            "service": "Paikkatietopalvelut",
        },
        "jatkuvuus": {
            "nav": "Varautuminen",
            "title": "Paikkatiedon jatkuvuus ja varautuminen – VLiNdATA Oy",
            "description": "Paikallinen varajärjestelmä kunnan paikkatietoaineistoille: kartta toimii selaimessa ja QGISissä myös silloin, kun ulkoinen rajapinta tai verkkoyhteys katkeaa.",
            "service": "Paikkatiedon jatkuvuus ja varajärjestelmä",
        },
        "yritys": {
            "nav": "Yritys",
            "title": "Yritys ja Virpi Lindvall – VLiNdATA Oy",
            "description": "VLiNdATA Oy:n yrittäjä Virpi Lindvall on paikkatietoalan asiantuntija, jolla on yli 20 vuoden kokemus kuntien paikkatiedosta ja rakennusrekistereistä.",
        },
        "referenssit": {
            "nav": "Referenssit",
            "title": "Referenssit – VLiNdATA Oy",
            "description": "VLiNdATA Oy on tehnyt yhteistyötä kuntien kanssa rakennusrekisteritietojen selvittämiseksi ja laadun parantamiseksi.",
        },
        "yhteystiedot": {
            "nav": "Yhteystiedot",
            "title": "Yhteystiedot – VLiNdATA Oy",
            "description": "Ota yhteyttä Virpi Lindvalliin: puhelin +358 44 301 2471, sähköposti virpi@vlindata.fi.",
        },
        "evasteet": {
            "nav": "Evästeet",
            "title": "Evästeet – VLiNdATA Oy",
            "description": "Mitä evästeitä vlindata.fi käyttää ja miten voit muuttaa valintaasi.",
            "robots": "noindex, follow",
        },
    },
    "en": {
        "etusivu": {
            "nav": "Home",
            "title": "VLiNdATA Oy – GIS and property tax audits for municipalities",
            "description": "VLiNdATA Oy helps Finnish municipalities with property tax audits, building register quality and GIS datasets. Over 20 years of experience.",
        },
        "kiinteistovero": {
            "nav": "Property tax audits",
            "title": "Property tax audits and building registers – VLiNdATA Oy",
            "description": "A property tax audit identifies buildings that are missing or incorrect in the registers. The work proceeds in stages to suit the municipality's resources.",
            "service": "Property tax audits and building register quality",
        },
        "paikkatieto": {
            "nav": "GIS services",
            "title": "GIS services for municipalities – VLiNdATA Oy",
            "description": "Producing, updating and analysing GIS datasets, and expert help with systems, registers and information management.",
            "service": "GIS services",
        },
        "jatkuvuus": {
            "nav": "Preparedness",
            "title": "GIS continuity and preparedness – VLiNdATA Oy",
            "description": "A local backup system for municipal GIS data: the map works in the browser and in QGIS even when an external interface or network connection is down.",
            "service": "GIS continuity and backup system",
        },
        "yritys": {
            "nav": "Company",
            "title": "Company and Virpi Lindvall – VLiNdATA Oy",
            "description": "Virpi Lindvall, founder of VLiNdATA Oy, is a GIS specialist with over 20 years of experience in municipal GIS and building registers.",
        },
        "referenssit": {
            "nav": "References",
            "title": "References – VLiNdATA Oy",
            "description": "VLiNdATA Oy has worked with Finnish municipalities to investigate and improve the quality of building register data.",
        },
        "yhteystiedot": {
            "nav": "Contact",
            "title": "Contact – VLiNdATA Oy",
            "description": "Contact Virpi Lindvall: phone +358 44 301 2471, email virpi@vlindata.fi.",
        },
        "evasteet": {
            "nav": "Cookies",
            "title": "Cookies – VLiNdATA Oy",
            "description": "Which cookies vlindata.fi uses and how to change your choice.",
            "robots": "noindex, follow",
        },
    },
}

# Kieliriippuvat yhteiset tekstit
TEKSTIT = {
    "fi": {
        "skip": "Siirry sisältöön",
        "brand_small": "Paikkatieto · Kiinteistövero",
        "brand_label": "VLiNdATA Oy, etusivulle",
        "menu": "Valikko",
        "nav_label": "Päävalikko",
        "lang_label": "Kieli – Language",
        "crumbs_label": "Murupolku",
        "og_alt": "VLiNdATA Oy: paikkatietoa ja rakennustietoja, joista kunta hyötyy. Kuvassa Virpi Lindvall.",
        "og_locale": "fi_FI", "og_locale_alt": "en_GB",
        "toteutus": "Tekninen toteutus", "f_cookies": "Evästeet", "f_cookie_settings": "Evästeasetukset", "f_version": "versio",
        "consent_label": "Evästeilmoitus",
        "consent_text": "Käytän evästeitä kävijämäärän analysoimiseen. Google Analytics ladataan vain, jos hyväksyt.",
        "consent_more": "Lisätietoja evästeistä",
        "consent_deny": "Hylkää", "consent_accept": "Hyväksy",
        "new_tab": " (avautuu uuteen välilehteen)",
        "ytunnus": "Y-tunnus",
    },
    "en": {
        "skip": "Skip to content",
        "brand_small": "GIS · Property tax",
        "brand_label": "VLiNdATA Oy, home",
        "menu": "Menu",
        "nav_label": "Main menu",
        "lang_label": "Kieli – Language",
        "crumbs_label": "Breadcrumb",
        "og_alt": "VLiNdATA Oy: GIS and building data that benefit municipalities. Photo of Virpi Lindvall.",
        "og_locale": "en_GB", "og_locale_alt": "fi_FI",
        "toteutus": "Technical implementation", "f_cookies": "Cookies", "f_cookie_settings": "Cookie settings", "f_version": "version",
        "consent_label": "Cookie notice",
        "consent_text": "I use cookies to analyse visitor numbers. Google Analytics is loaded only if you accept.",
        "consent_more": "More about cookies",
        "consent_deny": "Decline", "consent_accept": "Accept",
        "new_tab": " (opens in a new tab, in Finnish)",
        "ytunnus": "Business ID",
    },
}

# Referenssikunnat: (tiedosto, leveys, korkeus, nimi fi, nimi en, osoite, korkea logo)
LOGOT = [
    ("aura.webp", 240, 87, "Auran kunta", "Municipality of Aura",
     "https://www.aura.fi/kunta-ja-paatoksenteko/ajankohtaista/tiedotteet/-rakennusrekisterin-paivitys-ja-kiinteistokysely-kesalla-2025/#news_anchor", False),
    ("rusko.webp", 240, 44, "Ruskon kunta", "Municipality of Rusko", "https://rusko.fi/", False),
    ("sauvo.webp", 182, 160, "Sauvon kunta", "Municipality of Sauvo",
     "https://www.sauvo.fi/asuminen-ja-ymparisto/rakennusvalvonta/kiinteistokartoitus/", True),
    ("oripaa.webp", 240, 100, "Oripään kunta", "Municipality of Oripää",
     "https://oripaa.fi/asukkaalle/tekninen-toimi/kiinteistoselvitys/", False),
    ("lieto.webp", 240, 240, "Liedon kaupunki", "City of Lieto",
     "https://lieto.fi/palvelut-ja-asiointi/rakentaminen/rakennusrekisterin-paivitys/", True),
    ("naantali.svg", 2675, 1066, "Naantalin kaupunki", "City of Naantali", "https://www.naantali.fi/fi", False),
    ("masku.webp", 308, 121, "Maskun kunta", "Municipality of Masku", "https://www.masku.fi/", False),
    ("sakyla.svg", 398, 244, "Säkylän kunta", "Municipality of Säkylä", "https://www.sakyla.fi/", True),
]

LOMAKE = {
    "fi": {
        "title": "Lähetä viesti",
        "intro": "Täytä kentät, niin viesti avautuu valmiiksi sähköpostiohjelmaasi.",
        "required": "pakollinen",
        "name": "Nimi", "org": "Kunta tai organisaatio", "email": "Sähköpostiosoite", "message": "Viesti",
        "button": "Lähetä viesti",
        "note": "Lomake ei tallenna tietoja sivustolle. Viesti lähtee omasta sähköpostistasi, kun painat siellä Lähetä.",
    },
    "en": {
        "title": "Send a message",
        "intro": "Fill in the fields and the message opens ready in your email app.",
        "required": "required",
        "name": "Name", "org": "Municipality or organisation", "email": "Email address", "message": "Message",
        "button": "Send message",
        "note": "The form does not store anything on this site. The message is sent from your own email when you press Send there.",
    },
}


# ---------------------------------------------------------------------------
# Apufunktiot
# ---------------------------------------------------------------------------
def ikoni(nimi):
    svg = (TYOKALUT / "ikonit" / f"{nimi}.svg").read_text(encoding="utf-8")
    svg = re.sub(r"<!--.*?-->", "", svg, flags=re.S)
    svg = re.sub(r'\s+class="[^"]*"', "", svg)
    svg = re.sub(r"\s*\n\s*", " ", svg).strip()
    svg = svg.replace("<svg ", '<svg aria-hidden="true" focusable="false" ', 1)
    return svg.replace(" >", ">").replace(" />", "/>")


def juuri(polku):
    syvyys = polku.count("/")
    return "./" if syvyys == 0 else "../" * syvyys


def href(root, polku):
    return root if not polku else root + polku


def lomake(kieli):
    t = LOMAKE[kieli]
    def kentta(id_, nimi, label, tyyppi="text", pakollinen=True, auto=""):
        merkki = f' <span class="muted">({t["required"]})</span>' if pakollinen else ""
        req = " required" if pakollinen else ""
        ac = f' autocomplete="{auto}"' if auto else ""
        virhe = f'\n        <p class="field__error" id="{id_}-virhe" hidden></p>' if pakollinen else ""
        desc = f' aria-describedby="{id_}-virhe"' if pakollinen else ""
        if tyyppi == "textarea":
            ohjain = f'<textarea id="{id_}" name="{nimi}" rows="6"{req}{desc}></textarea>'
        else:
            ohjain = f'<input id="{id_}" name="{nimi}" type="{tyyppi}"{ac}{req}{desc}>'
        return (f'      <div class="field">\n        <label for="{id_}">{label}{merkki}</label>\n'
                f'        {ohjain}{virhe}\n      </div>')
    return "\n".join([
        '<form class="form" action="mailto:virpi@vlindata.fi" method="post" enctype="text/plain" data-contact-form novalidate>',
        f'      <h3 class="h3">{t["title"]}</h3>',
        f'      <p class="form__note">{t["intro"]}</p>',
        kentta("lomake-nimi", "nimi", t["name"], auto="name"),
        kentta("lomake-organisaatio", "organisaatio", t["org"], pakollinen=False, auto="organization"),
        kentta("lomake-sahkoposti", "sahkoposti", t["email"], "email", auto="email"),
        kentta("lomake-viesti", "viesti", t["message"], "textarea"),
        f'      <button class="btn btn--ensisijainen" type="submit">{t["button"]} {ikoni("arrow-right")}</button>',
        f'      <p class="form__note">{t["note"]}</p>',
        '      <p class="form__status" data-form-status role="status" aria-live="polite"></p>',
        '    </form>',
    ])


def logot(kieli, root):
    rivit = ['<ul class="logos">']
    for tiedosto, w, h, nimi_fi, nimi_en, url, korkea in LOGOT:
        nimi = nimi_fi if kieli == "fi" else nimi_en
        luokka = ' class="korkea"' if korkea else ""
        rivit.append(
            f'        <li><a href="{url}" target="_blank" rel="noopener">'
            f'<img src="{root}img/logot/{tiedosto}" alt="{nimi}" width="{w}" height="{h}"{luokka} loading="lazy" decoding="async">'
            f'<span class="sr-only">{TEKSTIT[kieli]["new_tab"]}</span></a></li>')
    rivit.append("      </ul>")
    return "\n".join(rivit)


def jsonld(kieli, avain):
    meta = SIVUT[kieli][avain]
    url = DOMAIN + POLUT[avain][kieli]
    kuvaus_org = ("Kiinteistöveroselvitykset, rakennusrekisterien laadun parantaminen ja paikkatietopalvelut kunnille."
                  if kieli == "fi" else
                  "Property tax audits, building register quality and GIS services for municipalities.")
    graph = [
        {
            "@type": "WebSite", "@id": DOMAIN + "#website", "url": DOMAIN,
            "name": "VLiNdATA Oy", "inLanguage": ["fi", "en"],
            "publisher": {"@id": DOMAIN + "#organization"},
            "creator": {"@id": "https://summanen.org/#oskari-summanen"},
        },
        {
            "@type": "Person", "@id": "https://summanen.org/#oskari-summanen", "name": "Oskari Summanen",
            "url": "https://summanen.org/",
            "description": ("VLiNdATA Oy:n kumppani ja sivuston tekninen toteuttaja (summanen.org)" if kieli == "fi"
                            else "Partner of VLiNdATA Oy and technical builder of this website (summanen.org)"),
        },
        {
            "@type": "Organization", "@id": DOMAIN + "#organization", "name": "VLiNdATA Oy",
            "url": DOMAIN, "logo": DOMAIN + "img/vlindata-logo.webp", "image": DOMAIN + "img/og-kuva.jpg",
            "description": kuvaus_org, "email": "virpi@vlindata.fi", "telephone": "+358443012471",
            "areaServed": {"@type": "Country", "name": "Finland"},
            "identifier": {"@type": "PropertyValue", "propertyID": "Y-tunnus", "value": "3410053-6"},
            "founder": {"@id": DOMAIN + "#virpi-lindvall"},
            "knowsAbout": ["Paikkatieto", "Kiinteistöveroselvitys", "Rakennusrekisteri",
                           "Paikkatietoanalyysi", "Tiedonhallinta"],
        },
        {
            "@type": "Person", "@id": DOMAIN + "#virpi-lindvall", "name": "Virpi Lindvall",
            "jobTitle": "Yrittäjä, paikkatietoalan asiantuntija" if kieli == "fi" else "Founder, GIS specialist",
            "image": DOMAIN + "img/virpi-metsa-pysty-1000.jpg",
            "worksFor": {"@id": DOMAIN + "#organization"},
        },
        {
            "@type": "WebPage", "@id": url + "#webpage", "url": url, "name": meta["title"],
            "description": meta["description"], "inLanguage": kieli,
            "isPartOf": {"@id": DOMAIN + "#website"},
        },
    ]
    if avain != "etusivu":
        graph[-1]["breadcrumb"] = {"@id": url + "#breadcrumb"}
        graph.append({
            "@type": "BreadcrumbList", "@id": url + "#breadcrumb",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": SIVUT[kieli]["etusivu"]["nav"],
                 "item": DOMAIN + POLUT["etusivu"][kieli]},
                {"@type": "ListItem", "position": 2, "name": meta["nav"], "item": url},
            ],
        })
    if "service" in meta:
        graph.append({
            "@type": "Service", "@id": url + "#service", "name": meta["service"],
            "description": meta["description"], "provider": {"@id": DOMAIN + "#organization"},
            "areaServed": {"@type": "Country", "name": "Finland"}, "url": url,
        })
    teksti = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, indent=2)
    return "\n".join("  " + rivi for rivi in teksti.splitlines())


def head(kieli, avain, root):
    meta = SIVUT[kieli][avain]
    t = TEKSTIT[kieli]
    url = DOMAIN + POLUT[avain][kieli]
    url_fi = DOMAIN + POLUT[avain]["fi"]
    url_en = DOMAIN + POLUT[avain]["en"]
    og = DOMAIN + ("img/og-kuva.jpg" if kieli == "fi" else "img/og-kuva-en.jpg")
    robots = meta.get("robots", "index, follow")
    return f"""<head>
  <meta charset="utf-8">
  <meta name="color-scheme" content="light">
  <script src="{root}js/consent.js" defer></script>
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
  <meta name="description" content="{meta['description']}">
  <title>{meta['title']}</title>
  <link rel="canonical" href="{url}">
  <link rel="alternate" hreflang="fi" href="{url_fi}">
  <link rel="alternate" hreflang="en" href="{url_en}">
  <link rel="alternate" hreflang="x-default" href="{url_fi}">
  <meta name="robots" content="{robots}">
  <meta name="author" content="Virpi Lindvall, VLiNdATA Oy">
  <meta name="theme-color" content="#f7f4ec">
  <link rel="icon" href="{root}favicon.ico" sizes="48x48">
  <link rel="icon" href="{root}favicon.svg" type="image/svg+xml">
  <link rel="apple-touch-icon" href="{root}apple-touch-icon.png">
  <link rel="manifest" href="{root}site.webmanifest">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="VLiNdATA Oy">
  <meta property="og:locale" content="{t['og_locale']}">
  <meta property="og:locale:alternate" content="{t['og_locale_alt']}">
  <meta property="og:url" content="{url}">
  <meta property="og:title" content="{meta['title']}">
  <meta property="og:description" content="{meta['description']}">
  <meta property="og:image" content="{og}">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:image:alt" content="{t['og_alt']}">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{meta['title']}">
  <meta name="twitter:description" content="{meta['description']}">
  <meta name="twitter:image" content="{og}">
  <meta name="twitter:image:alt" content="{t['og_alt']}">
  <script type="application/ld+json">
{jsonld(kieli, avain)}
  </script>
  <link rel="preload" href="{root}fonts/manrope-latin-wght.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="preload" href="{root}fonts/inter-latin-wght.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="stylesheet" href="{root}css/fonts.css">
  <link rel="stylesheet" href="{root}css/style.css">
  <script src="{root}js/menu.js" defer></script>
</head>"""


def header(kieli, avain, root):
    t = TEKSTIT[kieli]
    linkit = []
    for k in NAVIGAATIO:
        nykyinen = ' aria-current="page"' if k == avain else ""
        linkit.append(f'        <li><a class="nav__link" href="{href(root, POLUT[k][kieli])}"{nykyinen}>{SIVUT[kieli][k]["nav"]}</a></li>')
    fi_href = href(root, POLUT[avain]["fi"])
    en_href = href(root, POLUT[avain]["en"])
    fi_cur = ' aria-current="page"' if kieli == "fi" else ""
    en_cur = ' aria-current="page"' if kieli == "en" else ""
    return f"""  <a class="skip" href="#sisalto">{t['skip']}</a>
  <header class="topbar">
    <div class="topbar__inner">
      <a class="brand" href="{href(root, POLUT['etusivu'][kieli])}" aria-label="{t['brand_label']}">
        <img src="{root}img/vlindata-logo.webp" alt="" width="40" height="44">
        <span>VLiNdATA Oy<small>{t['brand_small']}</small></span>
      </a>
      <button class="menu-toggle" type="button" aria-expanded="false" aria-controls="paavalikko">
        <span></span><span></span><span></span>
        <span class="sr-only">{t['menu']}</span>
      </button>
      <nav class="nav" id="paavalikko" aria-label="{t['nav_label']}">
        <ul class="nav__list">
{chr(10).join(linkit)}
          <li class="nav__evasteet"><a class="nav__link nav__link--pieni" href="{href(root, POLUT['evasteet'][kieli])}"{' aria-current="page"' if avain == 'evasteet' else ''}>{t['f_cookies']}</a></li>
          <li class="nav__meta">
            <button class="nav__meta-nappi" type="button" id="consent-open">{t['f_cookie_settings']}</button>
            <span>© {VUOSI} VLiNdATA Oy · {t['f_version']} <span data-site-version>{VERSIO}</span></span>
            <span class="nav__toteutus">{t['toteutus']}: <a href="https://summanen.org/" target="_blank" rel="noopener">summanen.org<span class="sr-only"> {t['new_tab']}</span></a></span>
          </li>
        </ul>
      </nav>
      <div class="lang" role="group" aria-label="{t['lang_label']}">
        <a href="{fi_href}" hreflang="fi" lang="fi"{fi_cur} aria-label="FI – suomeksi">FI</a>
        <a href="{en_href}" hreflang="en" lang="en"{en_cur} aria-label="EN – in English">EN</a>
      </div>
    </div>
  </header>"""


def evasteilmoitus(kieli, root):
    """Evästeilmoitus (sivun alalaidassa kiinteänä, näkyy kunnes kävijä valitsee)."""
    t = TEKSTIT[kieli]
    p = lambda k: href(root, POLUT[k][kieli])
    return f"""  <div class="consent" id="consent" role="region" aria-label="{t['consent_label']}" hidden>
    <p class="consent__text">{t['consent_text']} <a href="{p('evasteet')}">{t['consent_more']}</a></p>
    <div class="consent__actions">
      <button class="btn btn--reuna" type="button" data-consent="deny">{t['consent_deny']}</button>
      <button class="btn btn--toissijainen" type="button" data-consent="accept">{t['consent_accept']}</button>
    </div>
  </div>"""


def murupolku(kieli, avain, root):
    t = TEKSTIT[kieli]
    return f"""<nav class="crumbs" aria-label="{t['crumbs_label']}">
        <ol>
          <li><a href="{href(root, POLUT['etusivu'][kieli])}">{SIVUT[kieli]['etusivu']['nav']}</a></li>
          <li><span aria-current="page">{SIVUT[kieli][avain]['nav']}</span></li>
        </ol>
      </nav>"""


def tayta(sisalto, kieli, avain, root):
    sisalto = sisalto.replace("{{lomake}}", lomake(kieli))
    sisalto = sisalto.replace("{{logot}}", logot(kieli, root))
    sisalto = sisalto.replace("{{murupolku}}", murupolku(kieli, avain, root))
    sisalto = re.sub(r"\{\{ikoni:([a-z0-9-]+)\}\}", lambda m: ikoni(m.group(1)), sisalto)
    sisalto = re.sub(r"\{\{sivu:([a-z]+)\}\}", lambda m: href(root, POLUT[m.group(1)][kieli]), sisalto)
    sisalto = sisalto.replace("{{versio}}", f'<span data-site-version>{VERSIO}</span>')
    sisalto = sisalto.replace("{{root}}", root)
    jaljella = re.findall(r"\{\{[^}]*\}\}", sisalto)
    if jaljella:
        raise SystemExit(f"Tuntematon merkintä sivulla {kieli}/{avain}: {jaljella}")
    return sisalto


def rakenna_sivu(kieli, avain):
    polku = POLUT[avain][kieli]
    root = juuri(polku)
    lahde = TYOKALUT / "sivut" / kieli / f"{avain}.html"
    runko = tayta(lahde.read_text(encoding="utf-8").rstrip(), kieli, avain, root)
    skriptit = f'  <script src="{root}js/contact-form.js" defer></script>\n' if "data-contact-form" in runko else ""
    if "data-hz=" in runko:
        skriptit += f'  <script src="{root}js/vaakavieritys.js" defer></script>\n'
    html = f"""<!doctype html>
<html lang="{kieli}">
{head(kieli, avain, root)}
<body>
{header(kieli, avain, root)}
  <main id="sisalto">
{runko}
  </main>
{evasteilmoitus(kieli, root)}
{skriptit}</body>
</html>
"""
    kohde = JUURI / polku / "index.html"
    kohde.parent.mkdir(parents=True, exist_ok=True)
    kohde.write_text(html, encoding="utf-8")
    return kohde


def uudelleenohjaus(vanha, uusi_polku):
    """Vanhat osoitteet (esim. evasteet.html) ohjataan uusiin, jotta vanhat linkit toimivat."""
    syvyys = vanha.count("/")
    root = "./" if syvyys == 0 else "../" * syvyys
    kohde = root + uusi_polku
    html = f"""<!doctype html>
<html lang="fi">
<head>
  <meta charset="utf-8">
  <title>VLiNdATA Oy</title>
  <meta name="robots" content="noindex">
  <link rel="canonical" href="{DOMAIN}{uusi_polku}">
  <meta http-equiv="refresh" content="0; url={kohde}">
</head>
<body>
  <p><a href="{kohde}">{DOMAIN}{uusi_polku}</a></p>
</body>
</html>
"""
    (JUURI / vanha).write_text(html, encoding="utf-8")


def sitemap():
    rivit = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">']
    for avain in POLUT:
        if SIVUT["fi"][avain].get("robots", "").startswith("noindex"):
            continue
        for kieli in ("fi", "en"):
            rivit.append("  <url>")
            rivit.append(f"    <loc>{DOMAIN}{POLUT[avain][kieli]}</loc>")
            for k in ("fi", "en"):
                rivit.append(f'    <xhtml:link rel="alternate" hreflang="{k}" href="{DOMAIN}{POLUT[avain][k]}"/>')
            rivit.append(f'    <xhtml:link rel="alternate" hreflang="x-default" href="{DOMAIN}{POLUT[avain]["fi"]}"/>')
            rivit.append("  </url>")
    rivit.append("</urlset>")
    (JUURI / "sitemap.xml").write_text("\n".join(rivit) + "\n", encoding="utf-8")


if __name__ == "__main__":
    for kieli in ("fi", "en"):
        for avain in POLUT:
            print("kirjoitettu", rakenna_sivu(kieli, avain).relative_to(JUURI))
    uudelleenohjaus("evasteet.html", POLUT["evasteet"]["fi"])
    uudelleenohjaus("en/cookies.html", POLUT["evasteet"]["en"])
    sitemap()
    print("kirjoitettu sitemap.xml ja vanhojen osoitteiden ohjaukset")
