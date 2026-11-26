"""Tekee muuttuvista fonteista kiinteäpainoiset woff2-tiedostot kansioon fonts/.

Vanhojen iPhonejen Safari tukee muuttuvia fontteja (variable fonts) puutteellisesti,
joten sivu käyttää vain kiinteitä painoja. Lähteet ovat npm-paketeista
(@fontsource-variable/inter ja /manrope, versiot package.json:ssa).

Aja repon juuressa:
    npm install
    pip install fonttools brotli
    python tools/fontit.py

Jos tyyleihin tulee uusi paino, lisää se PAINOT-listaan ja css/fonts.css:ään.
"""
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont

JUURI = Path(__file__).resolve().parent.parent
PAINOT = {
    "inter": ("@fontsource-variable/inter/files/inter-latin-wght-normal.woff2", [400, 500, 600, 700]),
    "manrope": ("@fontsource-variable/manrope/files/manrope-latin-wght-normal.woff2", [600, 700, 800]),
}

for nimi, (lahde, painot) in PAINOT.items():
    src = JUURI / "node_modules" / lahde
    for w in painot:
        f = instantiateVariableFont(TTFont(src), {"wght": w}, updateFontNames=False)
        assert "fvar" not in f, "muuttuva akseli jäi tiedostoon"
        f.recalcTimestamp = False   # sama tulos joka ajolla
        f.flavor = "woff2"
        out = JUURI / "fonts" / f"{nimi}-{w}.woff2"
        f.save(out)
        print(out.relative_to(JUURI), out.stat().st_size, "tavua")
