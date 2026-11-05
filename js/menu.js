/* Valikko, yläpalkin reunaviiva ja versionumero */
(() => {
  // Sivuston versio: nosta jokaisessa muutoksessa ja kirjaa CHANGELOG.md-tiedostoon
  const SITE_VERSION = '2.2.0';
  // Tätä leveämmällä näytöllä valikko on aina auki (vastaa CSS:n 1180 px rajaa)
  const DESKTOP_MIN_WIDTH = 1180;

  document.querySelectorAll('[data-site-version]').forEach((el) => { el.textContent = SITE_VERSION; });

  const toggle = document.querySelector('.menu-toggle');
  const nav = document.getElementById(toggle ? toggle.getAttribute('aria-controls') : '');

  const setOpen = (open, { returnFocus = false } = {}) => {
    if (!toggle || !nav) return;
    toggle.setAttribute('aria-expanded', String(open));
    nav.classList.toggle('is-open', open);
    if (!open && returnFocus) toggle.focus();
  };

  if (toggle && nav) {
    toggle.addEventListener('click', () => {
      setOpen(toggle.getAttribute('aria-expanded') !== 'true');
    });
    // Ankkurilinkin valinta sulkee valikon puhelimella
    nav.addEventListener('click', (event) => {
      if (event.target.closest('a') && window.innerWidth < DESKTOP_MIN_WIDTH) setOpen(false);
    });
    document.addEventListener('keydown', (event) => {
      if (event.key === 'Escape' && toggle.getAttribute('aria-expanded') === 'true') {
        setOpen(false, { returnFocus: true });
      }
    });
    window.addEventListener('resize', () => {
      if (window.innerWidth >= DESKTOP_MIN_WIDTH) setOpen(false);
    });
  }

  // Yläpalkkiin ohut viiva, kun sivua on vieritetty
  const topbar = document.querySelector('.topbar');
  if (topbar) {
    const onScroll = () => topbar.classList.toggle('is-scrolled', window.scrollY > 8);
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();
  }
})();
