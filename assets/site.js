'use strict';
(() => {
  // The former GitHub Pages address keeps visitors on the current canonical site.
  if (location.hostname === 'eslamelshikh-dev.github.io' && location.pathname.toLowerCase().startsWith('/moblethamamt')) {
    const path = location.pathname.slice('/MOBLETHamamt'.length) || '/';
    location.replace('https://moblet-hamamat.vercel.app' + path + location.search + location.hash);
    return;
  }
  const menu = document.querySelector('.mobile-nav');
  const header = document.querySelector('.header');
  if (header) {
    const reflectScroll = () => header.classList.toggle('is-scrolled', window.scrollY > 25);
    reflectScroll();
    window.addEventListener('scroll', reflectScroll, { passive: true });
  }
  if (menu) {
    menu.querySelectorAll('a').forEach(a => a.addEventListener('click', () => { menu.open = false; }));
    document.addEventListener('keydown', event => {
      if (event.key === 'Escape' && menu.open) {
        menu.open = false;
        menu.querySelector('summary').focus();
      }
    });
    document.addEventListener('click', event => {
      if (!menu.contains(event.target)) menu.open = false;
    });
  }
  const form = document.getElementById('request-form');
  if (form) {
    form.addEventListener('submit', event => {
      event.preventDefault();
      if (!form.reportValidity()) return;
      const data = new FormData(form);
      const service = String(data.get('service') || '').trim();
      const district = String(data.get('district') || '').trim();
      const details = String(data.get('details') || '').trim();
      const message = ['السلام عليكم، أرغب في الاستفسار عن خدمات مبلط حمامات في الرياض.', 'الخدمة: ' + service, district && 'الحي: ' + district, details && 'التفاصيل: ' + details].filter(Boolean).join('\n');
      location.href = 'https://wa.me/966546562621?text=' + encodeURIComponent(message);
    });
  }
  const gallery = document.querySelector('.gallery-browser');
  if (gallery) {
    const controls = gallery.querySelector('.gallery-filters');
    const cards = Array.from(gallery.querySelectorAll('[data-group]'));
    const status = gallery.querySelector('.gallery-result');
    const section = gallery.closest('.full-gallery');
    const count = new Intl.NumberFormat('ar-SA');
    controls.hidden = false;
    const filter = category => {
      let visible = 0;
      cards.forEach(card => {
        card.hidden = category !== 'all' && card.dataset.group !== category;
        if (!card.hidden) visible += 1;
      });
      controls.querySelectorAll('button').forEach(button => {
        button.setAttribute('aria-pressed', String(button.dataset.galleryFilter === category));
      });
      section.classList.toggle('is-filtered', category !== 'all');
      status.textContent = 'عرض ' + count.format(visible) + ' من ' + count.format(cards.length) + ' صور';
    };
    controls.addEventListener('click', event => {
      const button = event.target.closest('[data-gallery-filter]');
      if (button) filter(button.dataset.galleryFilter);
    });
    filter('all');
  }
  const dialog = document.querySelector('.lightbox');
  if (dialog && typeof dialog.showModal === 'function') {
    let opener;
    const close = () => dialog.close();
    document.querySelectorAll('[data-lightbox]').forEach(link => {
      link.addEventListener('click', event => {
        event.preventDefault();
        opener = link;
        const source = link.querySelector('img');
        const image = dialog.querySelector('img');
        image.src = link.href;
        image.alt = source.alt;
        image.width = source.width;
        image.height = source.height;
        dialog.querySelector('figcaption').textContent = link.dataset.caption;
        dialog.showModal();
      });
    });
    dialog.querySelector('.lightbox-close').addEventListener('click', close);
    dialog.addEventListener('click', event => { if (event.target === dialog) close(); });
    dialog.addEventListener('close', () => { if (opener) opener.focus(); });
  }
})();
