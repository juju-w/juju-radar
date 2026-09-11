/* The English paragraphs are editorial summaries, not excerpts of the report. */
(() => {
 const guide = document.querySelector('[data-reading-guide]');
 if (!guide) return;
 const controls = guide.querySelector('[data-language-controls]');
 controls.hidden = false;
 controls.addEventListener('click', event => {
  const button = event.target.closest('[data-language]');
  if (!button) return;
  const mode = button.dataset.language;
  if (!['both', 'zh', 'en'].includes(mode)) return;
  guide.dataset.language = mode;
  for (const option of controls.querySelectorAll('[data-language]')) {
   option.setAttribute('aria-pressed', String(option === button));
  }
 });
})();
