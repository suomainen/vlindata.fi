/* Evästeilmoitus ja Google Analytics 4 (Consent Mode v2)
   - Kaikki analytiikka on oletuksena kielletty.
   - gtag.js ladataan vasta, kun kävijä painaa "Hyväksy".
   - Valinta tallennetaan selaimen localStorageen.
   - Valinnan voi muuttaa alatunnisteen "Evästeasetukset"-napista (id consent-open). */
(() => {
  const GA_ID = 'G-73CPF19H48';
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
  };

  // Poistaa Google Analyticsin evästeet (_ga, _ga_XXXX) tältä ja ylätason verkkotunnukselta
  const removeAnalyticsCookies = () => {
    const host = location.hostname;
    const domains = ['', host, `.${host}`, `.${host.split('.').slice(-2).join('.')}`];
    document.cookie.split(';').map((c) => c.split('=')[0].trim())
      .filter((name) => name === '_ga' || name.startsWith('_ga_'))
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

    const show = () => {
      banner.hidden = false;
      const first = banner.querySelector('button');
      if (first) first.focus({ preventScroll: true });
    };
    const hide = () => { banner.hidden = true; };

    banner.addEventListener('click', (event) => {
      const button = event.target.closest('[data-consent]');
      if (!button) return;
      const previous = readChoice();
      if (button.dataset.consent === 'accept') {
        saveChoice('granted');
        hide();
        loadAnalytics();
      } else {
        saveChoice('denied');
        hide();
        if (previous === 'granted') {
          // Aiempi hyväksyntä perutaan: evästeet pois ja sivu uudelleen ilman analytiikkaa
          removeAnalyticsCookies();
          location.reload();
        }
      }
    });

    document.querySelectorAll('#consent-open, [data-consent-open]').forEach((button) => {
      button.addEventListener('click', show);
    });

    if (!readChoice()) banner.hidden = false;
  });
})();
