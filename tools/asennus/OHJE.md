# vlindata.fi – sivujen päivitys omalta koneelta

Tällä työkalulla voit muuttaa sivujen tekstejä, katsoa muutokset ennen julkaisua ja julkaista ne osoitteeseen vlindata.fi. Versionumero, muutoshistoria ja tallennus GitHubiin hoituvat automaattisesti.

## Asennus (kerran)

Ennen asennusta:

- Luo itsellesi GitHub-tunnus osoitteessa github.com ja kerro käyttäjänimesi Oskarille. Oskari lisää sinut sivuston repoon, ja saat siitä kutsun sähköpostiisi. Hyväksy kutsu.
- Pidä Domainhotellin FTP-tunnukset käsillä. Ne tallennetaan vain omalle koneellesi WinSCP-ohjelmaan.

Asennus:

1. Pura zip-paketti esimerkiksi työpöydälle ja kaksoisnapsauta **asenna.bat**.
2. Asennus asentaa Gitin, Pythonin ja WinSCP:n. Hyväksy Windowsin kysymykset.
3. Asennus kysyy kansion sivustolle. Paina Enter, niin sivusto tallentuu Tiedostot-kansioon.
4. GitHub pyytää kirjautumaan: valitse **Sign in with your browser** ja kirjaudu.
5. Kirjoita nimesi ja sähköpostiosoitteesi. Ne näkyvät muutoshistoriassa.
6. Lopuksi WinSCP aukeaa. Tallenna palvelinyhteys ohjeen mukaan nimellä **vlindata** ja ruksi **Tallenna salasana**.

Työpöydälle tulee kuvake **VLiNdATA-sivut**. Jos jokin vaihe ei onnistu, käynnistä kone uudelleen ja aja asenna.bat uudestaan. Jo tehdyt vaiheet ohitetaan.

## Käyttö

Avaa työkalu työpöydän kuvakkeesta **VLiNdATA-sivut** ja etene numerojärjestyksessä.

1. **Hae uusin versio.** Paina aina ensin, jotta saat Oskarin tekemät muutokset.
2. **Avaa tekstit.** Avaa kansion, jossa sivujen tekstit ovat. Kansiossa *fi* ovat suomenkieliset ja kansiossa *en* englanninkieliset sivut. Avaa tiedosto Muistiolla (hiiren oikea painike → Avaa sovelluksessa → Muistio), muuta tekstiä ja tallenna.
3. **Esikatsele.** Avaa sivut selaimeen. Vain sinä näet esikatselun. Jos muutit tekstiä uudelleen, paina Esikatsele uudestaan.
4. **Mitä muutit?** Kirjoita lyhyesti, esimerkiksi "Yritys-sivun esittelyteksti päivitetty", ja paina **Julkaise**. Työkalu kysyy vielä varmistuksen ennen kuin sivut menevät verkkoon.

Valmis sivu näkyy osoitteessa vlindata.fi. Jos näet vanhan version, paina selaimessa **Ctrl + F5**.

**Tee zip työpöydälle** tallentaa koko sivuston zip-pakettina esimerkiksi varmuuskopioksi.

## Mikä tiedosto on mikäkin sivu

| Sivu | Tiedosto (fi ja en) |
|---|---|
| Etusivu | etusivu.html |
| Kiinteistövero | kiinteistovero.html |
| Paikkatieto | paikkatieto.html |
| Varautuminen | jatkuvuus.html |
| Yritys | yritys.html |
| Referenssit | referenssit.html |
| Yhteystiedot | yhteystiedot.html |
| Evästeet | evasteet.html |

Muuta vain tekstiä merkkien `>` ja `<` välissä. Esimerkiksi rivillä

`<p>Olen VLiNdATA Oy:n yrittäjä.</p>`

muutetaan vain kohtaa *Olen VLiNdATA Oy:n yrittäjä.*

- Älä poista tai muuta kulmasulkeiden sisältöä (`<p>`, `</p>`, `class="..."`).
- Merkinnät kaksoisaaltosulkeissa, esimerkiksi `{{ikoni:phone}}` ja `{{sivu:yritys}}`, ovat työkalun omia. Jätä ne paikalleen.
- `&shy;` pitkän sanan keskellä on piilotavuviiva puhelinta varten. Sen voi jättää paikalleen.
- Muista muuttaa sama asia myös englanninkieliselle sivulle (kansio *en*) tai pyydä Oskaria kääntämään.

## Jos jokin menee pieleen

- **"Oskari on muuttanut samoja kohtia kuin sinä"**: muutoksesi ovat tallessa. Älä tee uusia muutoksia, vaan soita Oskarille.
- **"Sivujen kokoaminen epäonnistui"**: viimeksi muutetusta tiedostosta on luultavasti poistunut vahingossa merkki `<`, `>` tai `}`. Tarkista muutos tai kysy Oskarilta.
- **"Yhteys palvelimeen ei onnistunut"**: tarkista, että WinSCP:ssä on tallennettu yhteys nimeltä *vlindata* ja salasana on oikein.
- Tarkempi loki on tiedostossa `%TEMP%\vlindata-sivutyokalu.log`. Sen voi lähettää Oskarille.
