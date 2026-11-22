/* Evästeilmoitus, Google Analytics 4 (Consent Mode v2) ja Microsoft Clarity
   - Kaikki analytiikka on oletuksena kielletty.
   - gtag.js ja Clarity ladataan vasta, kun kävijä painaa "Hyväksy".
   - Valinta tallennetaan selaimen localStorageen.
   - Valinnan voi muuttaa Analytiikkaevästeet-kytkimestä (Evästeet-sivu ja puhelimen valikko). */
(() => {
  const GA_ID = 'G-73CPF19H48';
  const CLARITY_ID = 'zho2cm3xyq';           // Microsoft Clarity: lämpökartat ja istuntotallenteet
  const STORAGE_KEY = 'vlindata-consent';   // arvo 'granted' tai 'denied'

  window.dataLayer = window.dataLayer || [];
  // gtag käyttää arguments-oliota, joten se on tavallinen funktio (ei nuolifunktio)
  function gtag() { window.dataLayer.push(arguments); }
  window.gtag = gtag;

  gtag('consent', 'default', {
    analytics_storage: 'denied',
    ad_storage: 'denied',
    ad_user_data: 'denied',
    ad_personalization: 'denied'
  });

  const readChoice = () => {
    try { return localStorage.getItem(STORAGE_KEY); } catch (e) { return null; }
  };
  const saveChoice = (value) => {
    try { localStorage.setItem(STORAGE_KEY, value); } catch (e) { /* yksityinen tila: valinta ei säily */ }
  };

  let analyticsLoaded = false;
  const loadAnalytics = () => {
    if (analyticsLoaded) return;
    analyticsLoaded = true;
    gtag('consent', 'update', { analytics_storage: 'granted' });
    const script = document.createElement('script');
    script.async = true;
    script.src = `https://www.googletagmanager.com/gtag/js?id=${GA_ID}`;
    document.head.appendChild(script);
    gtag('js', new Date());
    gtag('config', GA_ID);
    loadClarity();
  };

  // Microsoft Clarity; sama latauskoodi kuin Clarityn ohjeessa, suostumus kerrotaan consentv2:lla
  const loadClarity = () => {
    window.clarity = window.clarity || function () { (window.clarity.q = window.clarity.q || []).push(arguments); };
    window.clarity('consentv2', { ad_Storage: 'denied', analytics_Storage: 'granted' });
    const script = document.createElement('script');
    script.async = true;
    script.src = `https://www.clarity.ms/tag/${CLARITY_ID}`;
    document.head.appendChild(script);
  };

  // Poistaa Google Analyticsin (_ga, _ga_XXXX) ja Clarityn (_clck, _clsk) evästeet tältä ja ylätason verkkotunnukselta
  const removeAnalyticsCookies = () => {
    const host = location.hostname;
    const domains = ['', host, `.${host}`, `.${host.split('.').slice(-2).join('.')}`];
    document.cookie.split(';').map((c) => c.split('=')[0].trim())
      .filter((name) => name === '_ga' || name.startsWith('_ga_') || name === '_clck' || name === '_clsk')
      .forEach((name) => {
        domains.forEach((d) => {
          document.cookie = `${name}=; expires=Thu, 01 Jan 1970 00:00:00 GMT; path=/${d ? `; domain=${d}` : ''}`;
        });
      });
  };

  if (readChoice() === 'granted') loadAnalytics();

  document.addEventListener('DOMContentLoaded', () => {
    const banner = document.getElementById('consent');
    if (!banner) return;

    // Ilmoitus pysyy näkyvissä, kunnes kävijä valitsee (myös Evästeet-sivulla). Sivun alalaitaan
    // varataan ilmoituksen korkuinen tila, jotta sen alle ei jää tekstiä, jota ei voi vierittää esiin.
    const varaaTila = () => {
      document.body.style.paddingBottom = banner.hidden ? '' : `${banner.offsetHeight + 24}px`;
    };
    window.addEventListener('resize', varaaTila);

    const hide = () => { banner.hidden = true; varaaTila(); };


    // Kytkin näyttää nykyisen tilan: päällä = hyväksytty, pois = hylätty tai ei valintaa
    const TILAT = document.documentElement.lang === 'en'
      ? { granted: 'On', denied: 'Off', none: 'Off (not chosen)' }
      : { granted: 'Päällä', denied: 'Pois', none: 'Pois (ei valittu)' };
    const switches = document.querySelectorAll('[data-consent-kytkin]');
    const updateSwitches = () => {
      const choice = readChoice();
      const avain = choice === 'granted' || choice === 'denied' ? choice : 'none';
      switches.forEach((kytkin) => {
        kytkin.setAttribute('aria-checked', String(avain === 'granted'));
        kytkin.dataset.tila = avain;
        kytkin.querySelector('.kytkin__tila').textContent = TILAT[avain];
      });
    };
    updateSwitches();

    const accept = () => {
      saveChoice('granted');
      hide();
      loadAnalytics();
      updateSwitches();
    };
    const deny = () => {
      const previous = readChoice();
      saveChoice('denied');
      hide();
      if (window.clarity) window.clarity('consentv2', { ad_Storage: 'denied', analytics_Storage: 'denied' });
      updateSwitches();
      if (previous === 'granted') {
        // Aiempi hyväksyntä perutaan: evästeet pois ja sivu uudelleen ilman analytiikkaa
        removeAnalyticsCookies();
        location.reload();
      }
    };

    document.addEventListener('click', (event) => {
      const button = event.target.closest('[data-consent]');
      if (button) {
        if (button.dataset.consent === 'accept') accept(); else deny();
        return;
      }
      if (event.target.closest('[data-consent-kytkin]')) {
        if (readChoice() === 'granted') deny(); else accept();
      }
    });

    if (!readChoice()) { banner.hidden = false; varaaTila(); }
  });
})();
