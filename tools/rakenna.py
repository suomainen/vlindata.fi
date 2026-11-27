"""Rakentaa vlindata.fi-sivuston HTML-sivut.

Tekstit ovat kansioissa tools/sivut/fi, tools/sivut/en ja tools/sivut/sv (yksi tiedosto per sivu).
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
VERSIO = "2.11.2"   # sama kuin js/menu.js:n SITE_VERSION; nosta molemmat

# Sisältöturvakäytäntö: sivu saa ladata vain omia tiedostojaan sekä Google Analyticsin
# ja Microsoft Clarityn (vasta evästehyväksynnän jälkeen, js/consent.js). Uusi ulkoinen
# palvelu pitää lisätä tähän, muuten selain estää sen. Sama rivi on 404.html:ssä.
CSP = "default-src 'self'; script-src 'self' https://www.googletagmanager.com https://www.clarity.ms https://*.clarity.ms; style-src 'self'; img-src 'self' data: https://*.google-analytics.com https://*.googletagmanager.com https://*.clarity.ms https://c.bing.com; font-src 'self'; connect-src 'self' https://*.google-analytics.com https://*.analytics.google.com https://*.googletagmanager.com https://*.clarity.ms https://c.bing.com; frame-src 'none'; object-src 'none'; base-uri 'self'; form-action 'self'"

# ---------------------------------------------------------------------------
# Kielet. KIELET kootaan kaikki; JULKAISTUT näkyvät kielivalinnassa, hreflangissa ja
# sitemapissa. Muut (nyt sv) ovat piilossa: sivut ovat olemassa ja niillä on oma
# kielivalinta, mutta ne ovat noindex eikä niihin linkitetä suomen- tai englanninkieliseltä
# sivulta. Kun ruotsinkielinen käännös on tarkistettu, lisää "sv" JULKAISTUT-listaan.
# ---------------------------------------------------------------------------
KIELET = ("fi", "en", "sv")
JULKAISTUT = ("fi", "en")
KIELINIMET = {"fi": "FI – suomeksi", "en": "EN – in English", "sv": "SV – på svenska"}


def nakyvat(kieli, avain="etusivu"):
    """Kielivalinnan ja hreflangin kielet: julkaistut ja piilossa olevalla sivulla myös sen oma kieli.
    Sivu, jolla ei ole jotain kieliversiota (esim. luottamus ruotsiksi), jättää sen pois."""
    return [k for k in KIELET if (k in JULKAISTUT or k == kieli) and k in POLUT[avain]]


# ---------------------------------------------------------------------------
# Sivut: avain -> polku jokaisella kielellä. Navigaation järjestys on tämä.
# ---------------------------------------------------------------------------
POLUT = {
    "etusivu":        {"fi": "",                           "en": "en/",                       "sv": "sv/"},
    "kiinteistovero": {"fi": "kiinteistoveroselvitykset/", "en": "en/property-tax-audits/",   "sv": "sv/fastighetsskatteutredningar/"},
    "paikkatieto":    {"fi": "paikkatietopalvelut/",       "en": "en/gis-services/",          "sv": "sv/gis-tjanster/"},
    "jatkuvuus":      {"fi": "paikkatiedon-jatkuvuus/",    "en": "en/gis-continuity/",        "sv": "sv/beredskap/"},
    "yritys":         {"fi": "yritys/",                    "en": "en/company/",               "sv": "sv/foretaget/"},
    "referenssit":    {"fi": "referenssit/",               "en": "en/references/",            "sv": "sv/referenser/"},
    "yhteystiedot":   {"fi": "yhteystiedot/",              "en": "en/contact/",               "sv": "sv/kontakt/"},
    "evasteet":       {"fi": "evasteet/",                  "en": "en/cookies/",               "sv": "sv/kakor/"},
    # Piilossa (SIVUT: "piilossa": True): ei valikossa eikä sitemapissa, noindex. Ei ruotsiksi vielä.
    "luottamus":      {"fi": "luottamus/",                 "en": "en/trust-center/"},
    "tietosuoja":     {"fi": "tietosuojaseloste/",         "en": "en/privacy-notice/"},
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
            "valikko": "Kiinteistövero",
            "title": "Kiinteistöveroselvitykset ja rakennusrekisterit – VLiNdATA Oy",
            "description": "Kiinteistöveroselvitys tunnistaa rekistereistä puuttuvat ja virheelliset rakennukset. Työ etenee vaiheittain kunnan resurssien mukaan.",
            "service": "Kiinteistöveroselvitykset ja rakennusrekisterien laadun parantaminen",
        },
        "paikkatieto": {
            "nav": "Paikkatietopalvelut",
            "valikko": "Paikkatieto",
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
        "luottamus": {
            "nav": "Luottamus ja tietoturva",
            "title": "Luottamus ja tietoturva – VLiNdATA Oy",
            "description": "Miten VLiNdATA Oy käsittelee kuntien aineistoja ja henkilötietoja: tietoturvakäytännöt, palvelut, varautuminen ja asiakirjat pyynnöstä.",
            "piilossa": True,
        },
        "tietosuoja": {
            "nav": "Tietosuojaseloste",
            "title": "Tietosuojaseloste – VLiNdATA Oy",
            "description": "VLiNdATA Oy:n tietosuojaseloste: mitä henkilötietoja käsittelen, miksi, kuinka kauan ja mitkä ovat oikeutesi.",
            "piilossa": True,
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
            "valikko": "Property tax",
            "title": "Property tax audits and building registers – VLiNdATA Oy",
            "description": "A property tax audit identifies buildings that are missing or incorrect in the registers. The work proceeds in stages to suit the municipality's resources.",
            "service": "Property tax audits and building register quality",
        },
        "paikkatieto": {
            "nav": "GIS services",
            "valikko": "GIS",
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
        "luottamus": {
            "nav": "Trust and security",
            "title": "Trust and security – VLiNdATA Oy",
            "description": "How VLiNdATA Oy handles municipal data and personal data: security practices, services used, preparedness and documents on request.",
            "piilossa": True,
        },
        "tietosuoja": {
            "nav": "Privacy notice",
            "title": "Privacy notice – VLiNdATA Oy",
            "description": "VLiNdATA Oy privacy notice: what personal data I process, why, for how long and what your rights are.",
            "piilossa": True,
        },
    },
    "sv": {
        "etusivu": {
            "nav": "Startsida",
            "title": "VLiNdATA Oy – geografisk information och fastighetsskatteutredningar för kommuner",
            "description": "VLiNdATA Oy hjälper kommuner med fastighetsskatteutredningar, kvaliteten i byggnadsregistren och kart- och GIS-material. Över 20 års erfarenhet.",
        },
        "kiinteistovero": {
            "nav": "Fastighetsskatteutredningar",
            "valikko": "Fastighetsskatt",
            "title": "Fastighetsskatteutredningar och byggnadsregister – VLiNdATA Oy",
            "description": "En fastighetsskatteutredning identifierar byggnader som saknas eller är felaktiga i registren. Arbetet framskrider stegvis enligt kommunens resurser.",
            "service": "Fastighetsskatteutredningar och kvaliteten i byggnadsregistren",
        },
        "paikkatieto": {
            "nav": "GIS-tjänster",
            "valikko": "Kartor och GIS",
            "title": "GIS-tjänster för kommuner – VLiNdATA Oy",
            "description": "Produktion, uppdatering och analys av kart- och GIS-material samt experthjälp med system, register och informationshantering.",
            "service": "GIS-tjänster",
        },
        "jatkuvuus": {
            "nav": "Beredskap",
            "title": "Kontinuitet och beredskap för geografisk information – VLiNdATA Oy",
            "description": "Ett lokalt reservsystem för kommunens kartor och GIS-material: kartan fungerar i webbläsaren och i QGIS även när ett externt gränssnitt eller nätverket ligger nere.",
            "service": "Kontinuitet och reservsystem för geografisk information",
        },
        "yritys": {
            "nav": "Företaget",
            "title": "Företaget och Virpi Lindvall – VLiNdATA Oy",
            "description": "Virpi Lindvall, företagare i VLiNdATA Oy, är expert inom geografisk information med över 20 års erfarenhet av kommunal geografisk information och byggnadsregister.",
        },
        "referenssit": {
            "nav": "Referenser",
            "title": "Referenser – VLiNdATA Oy",
            "description": "VLiNdATA Oy har samarbetat med kommuner för att utreda uppgifterna i byggnadsregistren och förbättra deras kvalitet.",
        },
        "yhteystiedot": {
            "nav": "Kontakt",
            "title": "Kontakt – VLiNdATA Oy",
            "description": "Kontakta Virpi Lindvall: telefon +358 44 301 2471, e-post virpi@vlindata.fi.",
        },
        "evasteet": {
            "nav": "Kakor",
            "title": "Kakor – VLiNdATA Oy",
            "description": "Vilka kakor vlindata.fi använder och hur du kan ändra ditt val.",
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
        "og_locale": "fi_FI",
        "toteutus": "Tekninen toteutus", "kytkin": "Analytiikkaevästeet", "kytkin_pois": "Pois", "teema": "Tumma ulkoasu", "f_cookies": "Evästeet", "f_cookie_settings": "Evästeasetukset", "f_version": "versio",
        "consent_label": "Evästeilmoitus",
        "consent_text": "Käytän Google Analyticsia nähdäkseni, kuinka moni sivulla käy, ja Microsoft Claritya nähdäkseni, miten sivua käytetään (klikkausten lämpökartat ja istuntojen tallenteet). Seuranta alkaa vain, jos hyväksyt sen.",
        "consent_more": "Evästeet ja tietosuoja",
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
        "og_locale": "en_GB",
        "toteutus": "Technical implementation", "kytkin": "Analytics cookies", "kytkin_pois": "Off", "teema": "Dark theme", "f_cookies": "Cookies", "f_cookie_settings": "Cookie settings", "f_version": "version",
        "consent_label": "Cookie notice",
        "consent_text": "I use Google Analytics to see how many people visit the site and Microsoft Clarity to see how it is used (click heatmaps and session recordings). Tracking starts only if you accept it.",
        "consent_more": "Cookies and privacy",
        "consent_deny": "Decline", "consent_accept": "Accept",
        "new_tab": " (opens in a new tab, in Finnish)",
        "ytunnus": "Business ID",
    },
    "sv": {
        "skip": "Gå till innehållet",
        "brand_small": "GIS · Fastighetsskatt",
        "brand_label": "VLiNdATA Oy, till startsidan",
        "menu": "Meny",
        "nav_label": "Huvudmeny",
        "lang_label": "Kieli – Language – Språk",
        "crumbs_label": "Brödsmulor",
        "og_alt": "VLiNdATA Oy: geografisk information och byggnadsuppgifter som kommunen har nytta av. På bilden Virpi Lindvall.",
        "og_locale": "sv_FI",
        "toteutus": "Teknisk implementering", "kytkin": "Analyskakor", "kytkin_pois": "Av", "teema": "Mörkt tema", "f_cookies": "Kakor", "f_cookie_settings": "Kakinställningar", "f_version": "version",
        "consent_label": "Meddelande om kakor",
        "consent_text": "Jag använder Google Analytics för att se hur många som besöker webbplatsen och Microsoft Clarity för att se hur den används (värmekartor över klick och inspelningar av sessioner). Spårningen börjar bara om du godkänner den.",
        "consent_more": "Kakor och dataskydd",
        "consent_deny": "Avvisa", "consent_accept": "Godkänn",
        "new_tab": " (öppnas i en ny flik, på finska)",
        "ytunnus": "FO-nummer",
    },
}
OG_LOCALE = {"fi": "fi_FI", "en": "en_GB", "sv": "sv_FI"}

# Referenssikunnat: (tiedosto, leveys, korkeus, nimi fi, nimi en, osoite, korkea logo).
# Ruotsinkieliset nimet ovat erikseen LOGOT_SV:ssä samassa järjestyksessä.
LOGOT = [
    ("aura.webp", 240, 87, "Auran kunta", "Municipality of Aura",
     "https://www.aura.fi/kunta-ja-paatoksenteko/ajankohtaista/tiedotteet/-rakennusrekisterin-paivitys-ja-kiinteistokysely-kesalla-2025/#news_anchor", False),
    ("rusko.webp", 240, 44, "Ruskon kunta", "Municipality of Rusko", "https://rusko.fi/", False),
    ("sauvo.webp", 182, 160, "Sauvon kunta", "Municipality of Sauvo",
     "https://www.sauvo.fi/asuminen-ja-ymparisto/rakennusvalvonta/kiinteistokartoitus/", True),
    ("oripaa.webp", 240, 100, "Oripään kunta", "Municipality of Oripää",
     "https://oripaa.fi/asukkaalle/tekninen-toimi/kiinteistoselvitys/", False),
    ("lieto.webp", 144, 190, "Liedon kaupunki", "City of Lieto",
     "https://lieto.fi/palvelut-ja-asiointi/rakentaminen/rakennusrekisterin-paivitys/", True),
    ("naantali.svg", 2675, 1066, "Naantalin kaupunki", "City of Naantali", "https://www.naantali.fi/fi", False),
    ("masku.webp", 308, 121, "Maskun kunta", "Municipality of Masku", "https://www.masku.fi/", False),
    ("sakyla.svg", 398, 244, "Säkylän kunta", "Municipality of Säkylä", "https://www.sakyla.fi/", True),
]
LOGOT_SV = ["Aura kommun", "Rusko kommun", "Sagu kommun", "Oripää kommun", "Lundo stad",
            "Nådendals stad", "Masko kommun", "Säkylä kommun"]

LOMAKE = {
    "fi": {
        "title": "Lähetä viesti",
        "intro": "Täytä kentät, niin viesti avautuu valmiiksi sähköpostiohjelmaasi.",
        "required": "pakollinen",
        "name": "Nimi", "org": "Kunta tai organisaatio", "email": "Sähköpostiosoite", "message": "Viesti",
        "button": "Lähetä viesti",
        "noscript": "Lomake tarvitsee JavaScriptin. Voit lähettää viestin myös suoraan osoitteeseen <a href=\"mailto:virpi@vlindata.fi\">virpi@vlindata.fi</a>.",
        "note": "Lomake ei tallenna tietoja sivustolle. Viesti lähtee omasta sähköpostistasi, kun painat siellä Lähetä.",
    },
    "en": {
        "title": "Send a message",
        "intro": "Fill in the fields and the message opens ready in your email app.",
        "required": "required",
        "name": "Name", "org": "Municipality or organisation", "email": "Email address", "message": "Message",
        "button": "Send message",
        "noscript": "The form needs JavaScript. You can also email <a href=\"mailto:virpi@vlindata.fi\">virpi@vlindata.fi</a> directly.",
        "note": "The form does not store anything on this site. The message is sent from your own email when you press Send there.",
    },
    "sv": {
        "title": "Skicka ett meddelande",
        "intro": "Fyll i fälten så öppnas meddelandet färdigt i ditt e-postprogram.",
        "required": "obligatoriskt",
        "name": "Namn", "org": "Kommun eller organisation", "email": "E-postadress", "message": "Meddelande",
        "button": "Skicka meddelande",
        "noscript": "Formuläret behöver JavaScript. Du kan också skicka e-post direkt till <a href=\"mailto:virpi@vlindata.fi\">virpi@vlindata.fi</a>.",
        "note": "Formuläret sparar ingenting på webbplatsen. Meddelandet skickas från din egen e-post när du trycker på Skicka där.",
    },
}


# ---------------------------------------------------------------------------
# Apufunktiot
# ---------------------------------------------------------------------------
def kirjoita(polku, teksti):
    """Kirjoittaa UTF-8:na ja aina LF-rivinvaihdoin, myös Windowsissa.
    Muuten git näkisi jokaisen sivun muuttuneen pelkkien rivinvaihtojen takia."""
    with open(polku, "w", encoding="utf-8", newline="\n") as f:
        f.write(teksti)


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
        # Ei mailto-actionia: selain merkitsee https-sivun lomakkeen, joka lähettää mailto-osoitteeseen,
        # "ei täysin turvalliseksi". Viestin avaa js/contact-form.js; ilman JavaScriptiä näytetään osoite.
        '<form class="form" method="post" data-contact-form novalidate>',
        f'      <noscript><p class="form__note">{t["noscript"]}</p></noscript>',
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
    for i, (tiedosto, w, h, nimi_fi, nimi_en, url, korkea) in enumerate(LOGOT):
        nimi = {"fi": nimi_fi, "en": nimi_en, "sv": LOGOT_SV[i]}[kieli]
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
    kuvaus_org = {
        "fi": "Kiinteistöveroselvitykset, rakennusrekisterien laadun parantaminen ja paikkatietopalvelut kunnille.",
        "en": "Property tax audits, building register quality and GIS services for municipalities.",
        "sv": "Fastighetsskatteutredningar, bättre kvalitet i byggnadsregistren och GIS-tjänster för kommuner.",
    }[kieli]
    graph = [
        {
            "@type": "WebSite", "@id": DOMAIN + "#website", "url": DOMAIN,
            "name": "VLiNdATA Oy", "inLanguage": nakyvat(kieli),
            "publisher": {"@id": DOMAIN + "#organization"},
            "creator": {"@id": "https://summanen.org/#oskari-summanen"},
        },
        {
            "@type": "Person", "@id": "https://summanen.org/#oskari-summanen", "name": "Oskari Summanen",
            "url": "https://summanen.org/",
            "image": DOMAIN + "img/oskari-summanen.webp",
            "description": {
                "fi": "VLiNdATA Oy:n kumppani: yli 20 vuotta IT-alalta ja yli 10 vuotta paikkatiedosta. "
                      "Myös sivuston tekninen toteuttaja.",
                "en": "Partner of VLiNdATA Oy: over 20 years in IT and over 10 years in GIS. "
                      "Also the technical builder of this website.",
                "sv": "Partner till VLiNdATA Oy: över 20 år inom IT och över 10 år inom geografisk information. "
                      "Har också byggt webbplatsen.",
            }[kieli],
            "affiliation": {"@id": DOMAIN + "#organization"},
            "knowsAbout": ["IT", {"fi": "Paikkatieto", "en": "GIS", "sv": "Geografisk information"}[kieli]],
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
            "jobTitle": {"fi": "Yrittäjä, paikkatietoalan asiantuntija", "en": "Founder, GIS specialist",
                         "sv": "Företagare, expert inom geografisk information"}[kieli],
            "image": DOMAIN + "img/virpi-metsa-pysty-1000.jpg",
            "worksFor": {"@id": DOMAIN + "#organization"},
            "sameAs": ["https://www.linkedin.com/in/lindvall-virpi/"],
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
    vaihtoehdot = "\n".join(f'  <link rel="alternate" hreflang="{k}" href="{DOMAIN + POLUT[avain][k]}">' for k in nakyvat(kieli, avain))
    og_alt = "\n".join(f'  <meta property="og:locale:alternate" content="{OG_LOCALE[k]}">' for k in nakyvat(kieli, avain) if k != kieli)
    # Ruotsinkielistä jakokuvaa ei vielä ole: ruotsinkieliset sivut käyttävät englanninkielistä.
    og = DOMAIN + ("img/og-kuva.jpg" if kieli == "fi" else "img/og-kuva-en.jpg")
    robots = meta.get("robots", "index, follow")
    if kieli not in JULKAISTUT or meta.get("piilossa"):
        robots = "noindex, nofollow"
    return f"""<head>
  <meta charset="utf-8">
  <meta http-equiv="Content-Security-Policy" content="{CSP}">
  <meta name="color-scheme" content="only light">
  <script src="{root}js/teema.js"></script>
  <script src="{root}js/consent.js" defer></script>
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
  <meta name="description" content="{meta['description']}">
  <title>{meta['title']}</title>
  <link rel="canonical" href="{url}">
{vaihtoehdot}
  <link rel="alternate" hreflang="x-default" href="{url_fi}">
  <meta name="robots" content="{robots}">
  <meta name="author" content="Virpi Lindvall, VLiNdATA Oy">
  <meta name="theme-color" content="#f7f4ec">
  <link rel="icon" href="{root}favicon.ico" sizes="48x48">
  <link rel="icon" href="{root}img/icons/icon-192.png" type="image/png" sizes="192x192">
  <link rel="apple-touch-icon" href="{root}apple-touch-icon.png">
  <link rel="manifest" href="{root}site.webmanifest">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="VLiNdATA Oy">
  <meta property="og:locale" content="{t['og_locale']}">
{og_alt}
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
  <link rel="preload" href="{root}fonts/manrope-800.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="preload" href="{root}fonts/inter-400.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="stylesheet" href="{root}css/fonts.css">
  <link rel="stylesheet" href="{root}css/style.css">
  <script src="{root}js/menu.js" defer></script>
</head>"""


def header(kieli, avain, root):
    t = TEKSTIT[kieli]
    linkit = []
    for k in NAVIGAATIO:
        nykyinen = ' aria-current="page"' if k == avain else ""
        linkit.append(f'        <li><a class="nav__link" href="{href(root, POLUT[k][kieli])}"{nykyinen}>{SIVUT[kieli][k].get("valikko", SIVUT[kieli][k]["nav"])}</a></li>')
    nykyinen_kieli = ' aria-current="page"'
    kielilinkit = "\n".join(
        f'        <a href="{href(root, POLUT[avain][k])}" hreflang="{k}" lang="{k}"'
        f'{nykyinen_kieli if k == kieli else ""} aria-label="{KIELINIMET[k]}">{k.upper()}</a>'
        for k in nakyvat(kieli, avain))
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
            <button class="kytkin" type="button" role="switch" aria-checked="false" data-consent-kytkin><span class="kytkin__rata" aria-hidden="true"><span class="kytkin__nuppi"></span></span><span class="kytkin__teksti">{t['kytkin']}</span><span class="kytkin__tila" aria-hidden="true">{t['kytkin_pois']}</span></button>
            <span>© {VUOSI} VLiNdATA Oy · {t['f_version']} <span data-site-version>{VERSIO}</span></span>
            <span class="nav__toteutus">{t['toteutus']}: <a href="https://summanen.org/" target="_blank" rel="noopener">summanen.org<span class="sr-only"> {t['new_tab']}</span></a></span>
          </li>
        </ul>
      </nav>
      <button class="teemanappi" type="button" aria-pressed="false" aria-label="{t['teema']}" title="{t['teema']}" data-teema-nappi>{ikoni('moon')}{ikoni('sun')}</button>
      <div class="lang" role="group" aria-label="{t['lang_label']}">
{kielilinkit}
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
    kirjoita(kohde, html)
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
  <meta http-equiv="Content-Security-Policy" content="{CSP}">
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
    kirjoita(JUURI / vanha, html)


def sitemap():
    rivit = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">']
    for avain in POLUT:
        if SIVUT["fi"][avain].get("robots", "").startswith("noindex") or SIVUT["fi"][avain].get("piilossa"):
            continue
        for kieli in JULKAISTUT:
            rivit.append("  <url>")
            rivit.append(f"    <loc>{DOMAIN}{POLUT[avain][kieli]}</loc>")
            for k in JULKAISTUT:
                rivit.append(f'    <xhtml:link rel="alternate" hreflang="{k}" href="{DOMAIN}{POLUT[avain][k]}"/>')
            rivit.append(f'    <xhtml:link rel="alternate" hreflang="x-default" href="{DOMAIN}{POLUT[avain]["fi"]}"/>')
            rivit.append("  </url>")
    rivit.append("</urlset>")
    kirjoita(JUURI / "sitemap.xml", "\n".join(rivit) + "\n")


if __name__ == "__main__":
    for kieli in KIELET:
        for avain in POLUT:
            if kieli not in POLUT[avain]:
                continue
            print("kirjoitettu", rakenna_sivu(kieli, avain).relative_to(JUURI))
    uudelleenohjaus("evasteet.html", POLUT["evasteet"]["fi"])
    uudelleenohjaus("en/cookies.html", POLUT["evasteet"]["en"])
    sitemap()
    print("kirjoitettu sitemap.xml ja vanhojen osoitteiden ohjaukset")
