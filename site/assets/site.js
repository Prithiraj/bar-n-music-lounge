/* Enhancement only: core pages, calendar, directions and image links work without JS. */
'use strict';
(() => {
  const menus = [...document.querySelectorAll('.mobile-nav')];
  menus.forEach(menu => {
    menu.addEventListener('click', event => {
      if (event.target.closest('nav a')) menu.open = false;
    });
  });
  document.addEventListener('keydown', event => {
    if (event.key !== 'Escape') return;
    menus.filter(menu => menu.open).forEach(menu => {
      menu.open = false;
      menu.querySelector('summary').focus();
    });
  });
  document.addEventListener('click', event => {
    menus.filter(menu => menu.open && !menu.contains(event.target)).forEach(menu => { menu.open = false; });
  });

  // Expire date-only listings at the end of the venue's local date, not the
  // visitor's date. This does not invent a start time or imply a live data feed.
  const refreshDates = () => {
    try {
      const parts = new Intl.DateTimeFormat('en-US', {timeZone:'America/New_York', year:'numeric', month:'2-digit', day:'2-digit'}).formatToParts(new Date());
      const value = type => parts.find(p => p.type === type).value;
      const today = `${value('year')}-${value('month')}-${value('day')}`;
      const rows = [...document.querySelectorAll('[data-event-date]')];
      rows.forEach(row => { row.hidden = row.dataset.eventDate < today; });
      document.querySelectorAll('[data-event-empty]').forEach(node => { node.hidden = rows.some(row => !row.hidden); });
      document.querySelectorAll('.schedule-heading, .later-heading').forEach(heading => {
        const list = heading.nextElementSibling;
        if (list?.classList.contains('event-list')) heading.hidden = ![...list.children].some(row => !row.hidden);
      });
    } catch { /* Retain the explicitly dated static listing in older browsers. */ }
  };
  refreshDates();
  document.addEventListener('visibilitychange', () => { if (!document.hidden) refreshDates(); });

  // Third-party imagery can fail; never substitute an unrelated stock picture.
  document.querySelectorAll('.photo img').forEach(img => {
    const fail = () => {
      if (img.closest('.photo-link').querySelector('.image-fallback')) return;
      img.hidden = true;
      const note = document.createElement('span');
      note.className = 'image-fallback';
      note.textContent = 'This archive photo is temporarily unavailable. View the original ↗';
      img.parentElement.append(note);
    };
    img.addEventListener('error', fail, {once:true});
    if (img.complete && !img.naturalWidth) fail();
  });

  const copy = document.querySelector('[data-copy-address]');
  if (copy && navigator.clipboard?.writeText && window.isSecureContext) {
    copy.hidden = false;
    copy.addEventListener('click', async () => {
      const status = document.querySelector('.copy-status');
      try {
        await navigator.clipboard.writeText('Out-n-About Bar and Music Lounge, 28390 US-27, Dundee, FL 33838');
        status.textContent = 'Address copied.';
      } catch {
        status.textContent = 'Copy was not available. Select the address above to copy it.';
      }
    });
  }

  // Native modal provides focus containment and Escape dismissal. Each original
  // image link remains usable without JS; modified clicks retain browser behavior.
  const data = document.querySelector('#photo-data');
  if (!data || !('HTMLDialogElement' in window)) return;
  let photos;
  try { photos = JSON.parse(data.textContent); } catch { return; }
  if (!Array.isArray(photos) || !photos.length) return;
  const dialog = document.createElement('dialog');
  dialog.className = 'photo-dialog';
  dialog.setAttribute('aria-labelledby', 'dialog-title');
  dialog.innerHTML = '<div class="dialog-top"><h2 id="dialog-title">Around Out-n-About</h2><button class="dialog-close" type="button" aria-label="Close photo viewer" autofocus>✕</button></div><img class="dialog-image" alt=""><p class="dialog-error" role="status" hidden>The archive photo could not load. <a href="#">Open the original photo ↗</a></p><div class="dialog-bottom"><p class="dialog-caption"></p><div class="dialog-controls"><button class="dialog-arrow" type="button" data-prev aria-label="Previous photo">←</button><span class="dialog-count" aria-live="polite"></span><button class="dialog-arrow" type="button" data-next aria-label="Next photo">→</button></div></div><p class="dialog-source">Venue photo archive · <a href="https://usarestaurants.info/explore/united-states/florida/polk-county/dundee/out-n-about-bar-and-music-lounge-863-439-1537.htm" rel="noopener">Source listing ↗</a>. Photos may show earlier appearances; drinks pictured are not a current menu.</p>';
  document.body.append(dialog);
  const image = dialog.querySelector('.dialog-image');
  const error = dialog.querySelector('.dialog-error');
  let current = 0;
  let trigger = null;
  const show = index => {
    current = (index + photos.length) % photos.length;
    const photo = photos[current];
    error.hidden = true;
    image.hidden = false;
    image.alt = photo.alt;
    image.src = photo.src;
    error.querySelector('a').href = photo.src;
    dialog.querySelector('.dialog-caption').textContent = photo.caption;
    dialog.querySelector('.dialog-count').textContent = `${current + 1} / ${photos.length}`;
  };
  image.addEventListener('error', () => { image.hidden = true; error.hidden = false; });
  document.querySelectorAll('[data-photo]').forEach(link => {
    link.addEventListener('click', event => {
      if (event.ctrlKey || event.metaKey || event.shiftKey || event.altKey || event.button !== 0) return;
      const index = Number(link.dataset.photo);
      if (!Number.isInteger(index) || !photos[index] || link.querySelector('.image-fallback')) return;
      event.preventDefault();
      trigger = link;
      show(index);
      dialog.showModal();
    });
  });
  dialog.querySelector('.dialog-close').addEventListener('click', () => dialog.close());
  dialog.querySelector('[data-prev]').addEventListener('click', () => show(current - 1));
  dialog.querySelector('[data-next]').addEventListener('click', () => show(current + 1));
  dialog.addEventListener('keydown', event => {
    if (event.key === 'ArrowLeft') { event.preventDefault(); show(current - 1); }
    if (event.key === 'ArrowRight') { event.preventDefault(); show(current + 1); }
  });
  dialog.addEventListener('click', event => {
    if (event.target !== dialog) return;
    const rect = dialog.getBoundingClientRect();
    if (event.clientX < rect.left || event.clientX > rect.right || event.clientY < rect.top || event.clientY > rect.bottom) dialog.close();
  });
  dialog.addEventListener('close', () => { if (trigger?.isConnected) trigger.focus({preventScroll:true}); });
})();
