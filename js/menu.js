/* Valikko, aktiivisen osion merkintä ja versionumero */
(() => {
  // Sivuston versio: nosta jokaisessa muutoksessa ja kirjaa CHANGELOG.md-tiedostoon
  const SITE_VERSION = '1.0.0';
  // Osio lasketaan aktiiviseksi, kun sen yläreuna on ohittanut tämän kohdan näytöstä
  const ACTIVE_OFFSET_PX = 140;
  // Tätä leveämmällä näytöllä valikko on aina auki (vastaa CSS:n 992 px rajaa)
  const DESKTOP_MIN_WIDTH = 992;

  const versionEl = document.getElementById('site-version');
  if (versionEl) versionEl.textContent = SITE_VERSION;

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
    // Linkin valinta sulkee valikon puhelimella
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

  // Aktiivinen osio: lasketaan vierityksestä (IntersectionObserver ei huomioi rootMarginia iframessa)
  const links = [...document.querySelectorAll('.nav__link[href^="#"]')];
  const targets = links
    .map((link) => ({ link, section: document.querySelector(link.getAttribute('href')) }))
    .filter((item) => item.section);

  if (targets.length) {
    let ticking = false;
    const update = () => {
      ticking = false;
      let current = null;
      targets.forEach((item) => {
        if (item.section.getBoundingClientRect().top - ACTIVE_OFFSET_PX <= 0) current = item;
      });
      // Sivun lopussa viimeinen osio on aktiivinen, vaikka sen yläreuna ei ehtisi ylös
      const atBottom = window.innerHeight + window.scrollY >= document.documentElement.scrollHeight - 2;
      if (atBottom) current = targets.reduce((a, b) => (a.section.offsetTop > b.section.offsetTop ? a : b));
      targets.forEach((item) => {
        if (item === current) item.link.setAttribute('aria-current', 'true');
        else item.link.removeAttribute('aria-current');
      });
    };
    window.addEventListener('scroll', () => {
      if (!ticking) { ticking = true; requestAnimationFrame(update); }
    }, { passive: true });
    update();
  }
})();
