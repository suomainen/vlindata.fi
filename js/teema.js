/* Vaalea ja tumma ulkoasu
   Oletuksena sivu seuraa laitteen asetusta (prefers-color-scheme). Yläpalkin
   kuu/aurinko-nappi vaihtaa vaalean ja tumman välillä, ja valinta jää selaimen
   muistiin. Evästesivun "Ulkoasu laitteen asetuksen mukaan" poistaa valinnan.

   Tiedosto ladataan <head>-osassa ilman deferiä, jotta tallennettu valinta
   ehtii html-elementtiin ennen kuin sivu piirretään (ei vaaleaa välähdystä).
   Värit ovat css/style.css:n osiossa 1. */
(() => {
  const AVAIN = 'vlindata-teema';
  const VARIT = { vaalea: '#f7f4ec', tumma: '#18201b' };  // theme-color (selaimen palkki)
  const juuri = document.documentElement;
  const media = window.matchMedia('(prefers-color-scheme: dark)');

  const lue = () => { try { return localStorage.getItem(AVAIN); } catch (e) { return null; } };
  const tallenna = (arvo) => {
    try {
      if (arvo) localStorage.setItem(AVAIN, arvo);
      else localStorage.removeItem(AVAIN);
    } catch (e) { /* yksityinen ikkuna: valinta pätee vain tällä sivulla */ }
  };

  const aseta = (valinta) => {
    if (valinta === 'tumma' || valinta === 'vaalea') juuri.dataset.teema = valinta;
    else delete juuri.dataset.teema;
  };
  aseta(lue());
  juuri.classList.add('teema-js');  // nappi näkyy vain, kun skripti toimii

  const nykyinen = () => juuri.dataset.teema || (media.matches ? 'tumma' : 'vaalea');

  const paivita = () => {
    const tumma = nykyinen() === 'tumma';
    document.querySelectorAll('[data-teema-nappi]').forEach((nappi) => {
      nappi.setAttribute('aria-pressed', String(tumma));
    });
    document.querySelectorAll('[data-teema-auto]').forEach((nappi) => {
      nappi.hidden = !juuri.dataset.teema;
    });
    document.querySelectorAll('meta[name="theme-color"]').forEach((meta) => {
      const oma = (meta.media || '').includes('dark') ? VARIT.tumma : VARIT.vaalea;
      meta.content = juuri.dataset.teema ? VARIT[juuri.dataset.teema] : oma;
    });
  };

  document.addEventListener('click', (e) => {
    if (e.target.closest('[data-teema-nappi]')) {
      const uusi = nykyinen() === 'tumma' ? 'vaalea' : 'tumma';
      aseta(uusi);
      tallenna(uusi);
      paivita();
    } else if (e.target.closest('[data-teema-auto]')) {
      aseta(null);
      tallenna(null);
      paivita();
      // Painettu nappi piiloutuu: fokus yläpalkin teemanappiin
      const nappi = document.querySelector('[data-teema-nappi]');
      if (nappi) nappi.focus();
    }
  });

  media.addEventListener('change', paivita);
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', paivita);
  else paivita();
})();
