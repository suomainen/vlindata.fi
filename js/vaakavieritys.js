/* Etusivun vaakavieritys
   Tietokoneella etusivun väripaneelit asettuvat vierekkäin. Kävijä vierittää
   tavallisesti (hiiren rulla, kosketuslevy, näppäimet), ja seuraava paneeli
   laajenee täyttämään näkymän edellisen kaventuessa sivuun.

   - Puhelimella, matalalla näytöllä ja kun kävijä on pyytänyt vähemmän liikettä
     (prefers-reduced-motion) sivu pysyy tavallisena pystyvierityksenä.
   - HTML ei muutu: paneelit ovat samassa järjestyksessä hakukoneille ja
     ruudunlukijoille. Skripti vain siirtää ne näyttämöelementin sisään.
   - Jos paneelin sisältö on näkymää korkeampi, vieritys kuljettaa ensin
     sisällön loppuun ja vasta sitten avaa seuraavan paneelin.
   - Näppäimistön fokus avaa paneelin, jossa fokusoitu elementti on. */
(() => {
  // Milloin vaakavieritys on käytössä (vastaa CSS:n .hz-tilaa)
  const KAYTOSSA = '(min-width: 1180px) and (min-height: 620px) and (prefers-reduced-motion: no-preference)';
  const KAISTA_SEURAAVA = 50;   // tulevan paneelin kaistan leveys (px)
  const KAISTA_EDELLINEN = 50;  // ohitetun paneelin kaistan leveys (px), sama kuin tulevilla
  const VALI = 8;               // paneelien väli (px)
  const AVAUS = 0.9;            // paneelin avautumiseen kuluva vieritys näkymän korkeuksina
  const PYSAHDYS = 0.3;         // vähimmäisvieritys avatun paneelin kohdalla

  const main = document.getElementById('sisalto');
  const paneelit = main ? [...main.querySelectorAll(':scope > .panel[data-hz]')] : [];
  if (paneelit.length < 2) return;

  const media = window.matchMedia(KAYTOSSA);
  const N = paneelit.length;
  let nayttamo = null;
  let ilmaisin = null;
  let osat = [];      // jokaisen paneelin vierityssegmentit
  let alku = 0;       // vaakaosuuden alku sivulla (px)
  let paalla = false;
  let tikki = false;

  const rajaa = (x, a, b) => Math.min(b, Math.max(a, x));

  // ---- Rakentaminen ja purku --------------------------------------------
  const rakenna = () => {
    nayttamo = document.createElement('div');
    nayttamo.className = 'hz__nayttamo';
    main.classList.add('hz');
    paneelit.forEach((paneeli, i) => {
      const kaista = document.createElement('a');
      kaista.className = 'hz__kaista';
      kaista.href = `#${paneeli.id}`;
      kaista.tabIndex = -1;                       // näppäimistölle sisältö riittää
      kaista.setAttribute('aria-hidden', 'true'); // ruudunlukija lukee itse paneelin
      kaista.innerHTML = `<span class="hz__nro">${String(i + 1).padStart(2, '0')}</span><span class="hz__nimi"></span>`;
      kaista.querySelector('.hz__nimi').textContent = paneeli.dataset.hz;
      paneeli.prepend(kaista);
      nayttamo.appendChild(paneeli);
    });
    ilmaisin = document.createElement('div');
    ilmaisin.className = 'hz__ilmaisin';
    ilmaisin.setAttribute('aria-hidden', 'true');
    ilmaisin.innerHTML = '<span class="hz__ilmaisin-teksti"></span><span class="hz__palkki"><span></span></span>';
    nayttamo.appendChild(ilmaisin);
    main.appendChild(nayttamo);
    document.documentElement.classList.add('hz-on');
    paalla = true;
    mittaa();
  };

  const pura = () => {
    paneelit.forEach((paneeli) => {
      const kaista = paneeli.querySelector(':scope > .hz__kaista');
      if (kaista) kaista.remove();
      paneeli.style.cssText = '';
      const wrap = paneeli.querySelector(':scope > .wrap');
      if (wrap) wrap.style.cssText = '';
      main.appendChild(paneeli);
    });
    if (nayttamo) nayttamo.remove();
    nayttamo = null;
    main.classList.remove('hz');
    main.style.height = '';
    document.documentElement.classList.remove('hz-on');
    paalla = false;
  };

  // ---- Mittaus: paneelien leveydet ja vierityssegmentit ---------------
  const mittaa = () => {
    if (!paalla) return;
    const topbar = document.querySelector('.topbar');
    const ylaosa = topbar ? topbar.offsetHeight : 0;
    document.documentElement.style.setProperty('--hz-ylaosa', `${ylaosa}px`);
    const leveys = nayttamo.clientWidth - 2 * VALI;
    const korkeus = window.innerHeight - ylaosa;

    osat = [];
    let s = 0;
    paneelit.forEach((paneeli, i) => {
      // Paneelin leveys silloin, kun se on auki: edelliset kapeina, seuraavat kaistoina
      const auki = leveys - i * KAISTA_EDELLINEN - (N - 1 - i) * KAISTA_SEURAAVA - (N - 1) * VALI;
      const wrap = paneeli.querySelector(':scope > .wrap');
      wrap.style.width = `${auki}px`;
      wrap.style.transform = '';
      const yli = Math.max(0, wrap.offsetHeight - (paneeli.clientHeight));
      const avaus = i === 0 ? 0 : AVAUS * korkeus;
      const pysahdys = Math.max(PYSAHDYS * korkeus, yli);
      osat.push({ paneeli, wrap, yli, alku: s, auki: s + avaus, loppu: s + avaus + pysahdys });
      s += avaus + pysahdys;
    });
    main.style.height = `${s + korkeus}px`;
    alku = main.getBoundingClientRect().top + window.scrollY - ylaosa;
    paivita();
  };

  // ---- Piirto vierityksen mukaan ----------------------------------------
  const paivita = () => {
    tikki = false;
    if (!paalla) return;
    const s = window.scrollY - alku;

    // p = jatkuva sijainti paneelien välillä (0 = ensimmäinen auki, 1 = toinen auki ...)
    let p = 0;
    osat.forEach((o, i) => {
      if (s >= o.alku) p = i === 0 ? 0 : (i - 1) + rajaa((s - o.alku) / (o.auki - o.alku), 0, 1);
    });

    osat.forEach((o, i) => {
      const paino = Math.max(0, 1 - Math.abs(p - i));
      const kaista = KAISTA_EDELLINEN + (KAISTA_SEURAAVA - KAISTA_EDELLINEN) * rajaa(i - p + 1, 0, 1);
      o.paneeli.style.flex = `${paino} 1 ${kaista}px`;
      o.paneeli.classList.toggle('is-auki', paino > 0.5);
      o.paneeli.style.setProperty('--hz-paino', paino.toFixed(3));
      // Pitkä sisältö liikkuu ylöspäin, kun paneeli on auki
      const siirto = o.yli ? rajaa((s - o.auki) / (o.loppu - o.auki), 0, 1) * o.yli : 0;
      o.wrap.style.transform = siirto ? `translateY(${-siirto}px)` : '';
    });

    const nykyinen = Math.round(p);
    ilmaisin.querySelector('.hz__ilmaisin-teksti').textContent =
      `${String(nykyinen + 1).padStart(2, '0')} / ${String(N).padStart(2, '0')}  ${paneelit[nykyinen].dataset.hz}`;
    // Ilmaisin kulkee avoimen paneelin vasemmassa alakulmassa
    ilmaisin.style.left = `${VALI + p * (KAISTA_EDELLINEN + VALI) + KAISTA_SEURAAVA + 16}px`;
    ilmaisin.querySelector('.hz__palkki span').style.transform = `scaleX(${(p / (N - 1)).toFixed(4)})`;
  };

  const pyyda = () => { if (!tikki) { tikki = true; requestAnimationFrame(paivita); } };

  // Vierityskohta, jossa paneeli on kokonaan auki (osuus 0–1 pitkän sisällön matkasta)
  const kohta = (i, osuus = 0) => {
    const o = osat[i];
    return alku + o.auki + osuus * (o.loppu - o.auki);
  };

  const mene = (i, osuus = 0, pehmea = true) => {
    window.scrollTo({ top: kohta(i, osuus), behavior: pehmea ? 'smooth' : 'instant' });
  };

  // ---- Tapahtumat --------------------------------------------------------
  window.addEventListener('scroll', pyyda, { passive: true });
  window.addEventListener('resize', () => { if (paalla) mittaa(); });

  // Sivuttainen pyyhkäisy kosketuslevyllä vierittää samaan suuntaan
  window.addEventListener('wheel', (e) => {
    if (!paalla || Math.abs(e.deltaX) <= Math.abs(e.deltaY)) return;
    const s = window.scrollY - alku;
    if (s < 0 || s > osat[N - 1].loppu) return;
    e.preventDefault();
    window.scrollBy(0, e.deltaX);
  }, { passive: false });

  // Ankkurilinkit (#kiinteistovero ym.) vievät oikean paneelin kohdalle
  document.addEventListener('click', (e) => {
    if (!paalla) return;
    const linkki = e.target.closest('a[href^="#"]');
    if (!linkki) return;
    const i = paneelit.findIndex((pnl) => `#${pnl.id}` === linkki.getAttribute('href'));
    if (i < 0) return;
    e.preventDefault();
    mene(i);
    history.replaceState(null, '', linkki.getAttribute('href'));
  });

  // Näppäimistön fokus avaa paneelin ja tuo fokusoidun kohdan näkyviin
  // Hiiren tai kosketuksen aiheuttama fokus ei siirrä näkymää (vain näppäimistö)
  let osoitin = false;
  document.addEventListener('pointerdown', () => { osoitin = true; setTimeout(() => { osoitin = false; }, 400); });

  main.addEventListener('focusin', (e) => {
    if (!paalla || osoitin) return;
    const i = paneelit.findIndex((pnl) => pnl.contains(e.target));
    if (i < 0) return;
    const o = osat[i];
    let osuus = 0;
    if (o.yli) {
      const y = e.target.getBoundingClientRect().top - o.wrap.getBoundingClientRect().top;
      osuus = rajaa((y - o.paneeli.clientHeight / 3) / o.yli, 0, 1);
    }
    const tavoite = kohta(i, osuus);
    if (Math.abs(window.scrollY - tavoite) > 4) window.scrollTo({ top: tavoite, behavior: 'instant' });
    // Selain voi vierittää paneelin sisältöä fokuksen takia; palautetaan
    [o.paneeli, nayttamo].forEach((el) => { el.scrollLeft = 0; el.scrollTop = 0; });
    paivita();
  });

  const vaihda = () => {
    if (media.matches && !paalla) rakenna();
    else if (!media.matches && paalla) pura();
    if (paalla && location.hash) {
      const i = paneelit.findIndex((pnl) => `#${pnl.id}` === location.hash);
      if (i >= 0) mene(i, 0, false);
    }
  };
  media.addEventListener('change', vaihda);
  vaihda();

  // Fontit ja kuvat voivat muuttaa sisällön korkeutta: mitataan uudelleen
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(mittaa);
  window.addEventListener('load', mittaa);
})();
