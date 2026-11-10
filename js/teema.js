/* Vaalea ja tumma ulkoasu
   Oletuksena sivu on aina vaalea. Yläpalkin kuu/aurinko-nappi vaihtaa tumman
   ulkoasun päälle ja pois, ja valinta jää selaimen muistiin.

   Tiedosto ladataan <head>-osassa ilman deferiä, jotta tallennettu valinta
   ehtii html-elementtiin ennen kuin sivu piirretään (ei vaaleaa välähdystä).
   Värit ovat css/style.css:n osiossa 1. */
(() => {
  const AVAIN = 'vlindata-teema';
  const VARIT = { vaalea: '#f7f4ec', tumma: '#18201b' };  // theme-color (selaimen palkki)
  const juuri = document.documentElement;

  const lue = () => { try { return localStorage.getItem(AVAIN); } catch (e) { return null; } };
  const tallenna = (tumma) => {
    try {
      if (tumma) localStorage.setItem(AVAIN, 'tumma');
      else localStorage.removeItem(AVAIN);
    } catch (e) { /* yksityinen ikkuna: valinta pätee vain tällä sivulla */ }
  };

  const aseta = (tumma) => {
    if (tumma) juuri.dataset.teema = 'tumma';
    else delete juuri.dataset.teema;
  };
  aseta(lue() === 'tumma');
  juuri.classList.add('teema-js');  // nappi näkyy vain, kun skripti toimii

  const onTumma = () => juuri.dataset.teema === 'tumma';

  const paivita = () => {
    const tumma = onTumma();
    document.querySelectorAll('[data-teema-nappi]').forEach((nappi) => {
      nappi.setAttribute('aria-pressed', String(tumma));
    });
    document.querySelectorAll('meta[name="theme-color"]').forEach((meta) => {
      meta.content = tumma ? VARIT.tumma : VARIT.vaalea;
    });
  };

  document.addEventListener('click', (e) => {
    if (!e.target.closest('[data-teema-nappi]')) return;
    const tumma = !onTumma();
    aseta(tumma);
    tallenna(tumma);
    paivita();
  });

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', paivita);
  else paivita();
})();
