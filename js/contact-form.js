/* Yhteydenottolomake: kokoaa viestin ja avaa sen kävijän omassa sähköpostiohjelmassa.
   Tietoja ei lähetetä sivuston palvelimelle eikä kolmannelle osapuolelle.
   Lomakkeella ei ole mailto-actionia (selain varoittaisi https-sivulla); ilman
   JavaScriptiä näytetään sähköpostiosoite <noscript>-tekstinä. */
(() => {
  const form = document.querySelector('[data-contact-form]');
  if (!form) return;

  const lang = document.documentElement.lang === 'en' ? 'en' : 'fi';
  const T = {
    fi: {
      required: 'Täytä tämä kenttä.',
      email: 'Tarkista sähköpostiosoite, esimerkiksi nimi@kunta.fi.',
      subject: 'Yhteydenotto vlindata.fi-sivulta',
      name: 'Nimi', org: 'Kunta tai organisaatio', mail: 'Sähköposti',
      opened: 'Viesti avautui sähköpostiohjelmaasi. Lähetä se sieltä. Jos mitään ei avautunut, kirjoita osoitteeseen virpi@vlindata.fi.',
      errors: 'Lomakkeessa on puutteita. Korjaa merkityt kentät.'
    },
    en: {
      required: 'Please fill in this field.',
      email: 'Please check the email address, for example name@company.com.',
      subject: 'Message from vlindata.fi',
      name: 'Name', org: 'Municipality or organisation', mail: 'Email',
      opened: 'The message opened in your email app. Please send it from there. If nothing opened, write to virpi@vlindata.fi.',
      errors: 'Some fields need attention. Please correct the marked fields.'
    }
  }[lang];

  const status = form.querySelector('[data-form-status]');
  const fields = [...form.querySelectorAll('input[required], textarea[required]')];
  const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

  const setError = (field, message) => {
    const error = document.getElementById(`${field.id}-virhe`);
    if (message) {
      field.setAttribute('aria-invalid', 'true');
      if (error) { error.textContent = message; error.hidden = false; }
    } else {
      field.removeAttribute('aria-invalid');
      if (error) { error.textContent = ''; error.hidden = true; }
    }
  };

  const validate = (field) => {
    const value = field.value.trim();
    if (!value) return T.required;
    if (field.type === 'email' && !EMAIL_RE.test(value)) return T.email;
    return '';
  };

  fields.forEach((field) => {
    field.addEventListener('blur', () => {
      if (field.hasAttribute('aria-invalid')) setError(field, validate(field));
    });
  });

  form.addEventListener('submit', (event) => {
    event.preventDefault();
    let firstInvalid = null;
    fields.forEach((field) => {
      const message = validate(field);
      setError(field, message);
      if (message && !firstInvalid) firstInvalid = field;
    });
    if (firstInvalid) {
      if (status) status.textContent = T.errors;
      firstInvalid.focus();
      return;
    }

    const get = (name) => (form.elements[name] ? form.elements[name].value.trim() : '');
    const body = [
      get('viesti'),
      '',
      '—',
      `${T.name}: ${get('nimi')}`,
      `${T.org}: ${get('organisaatio') || '–'}`,
      `${T.mail}: ${get('sahkoposti')}`
    ].join('\r\n');

    const href = `mailto:virpi@vlindata.fi?subject=${encodeURIComponent(T.subject)}&body=${encodeURIComponent(body)}`;
    if (status) status.textContent = T.opened;
    window.location.href = href;
  });
})();
