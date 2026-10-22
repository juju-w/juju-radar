/* Progressive article controls. All rendering libraries are versioned, local assets. */
(() => {
  const assets = document.currentScript?.dataset || {};
  const enhance = async () => {
  await window.jujuReadingReady;
  // The persistent player replaces its initial document with a reading iframe.
  if (window.self === window.top && document.querySelector('iframe#site')) return;
  const load = source => new Promise((resolve, reject) => {
    const url = new URL(source, location.href);
    if (url.origin !== location.origin || !url.pathname.startsWith('/juju-radar/assets/vendor/')) {
      reject(new Error('Unexpected article asset')); return;
    }
    const script = document.createElement('script');
    script.src = url.href; script.onload = resolve; script.onerror = reject;
    document.head.append(script);
  });
  let status;
  const announce = text => {
    if (!status) {
      status = document.createElement('div'); status.className = 'format-status';
      status.setAttribute('role', 'status'); document.body.append(status);
    }
    status.textContent = text; status.hidden = false;
    clearTimeout(status.timer); status.timer = setTimeout(() => { status.hidden = true; }, 2200);
  };
  for (const button of document.querySelectorAll('.copy-code')) {
    button.hidden = false;
    button.addEventListener('click', async () => {
      const code = button.closest('.code-block, .mermaid-block').querySelector('pre code');
      const text = code.textContent;
      let copied = false;
      try { await navigator.clipboard.writeText(text); copied = true; } catch {
        const field = document.createElement('textarea'); field.value = text;
        field.readOnly = true; field.style.cssText = 'position:fixed;left:-10000px;top:0';
        document.body.append(field); field.select();
        try { copied = document.execCommand('copy'); } catch {}
        field.remove(); button.focus();
      }
      if (copied) announce('已复制');
      else {
        const range = document.createRange(); range.selectNodeContents(code);
        const selection = window.getSelection(); selection.removeAllRanges(); selection.addRange(range);
        announce('复制未完成，代码已选中，可手动复制');
      }
    });
  }
  for (const region of document.querySelectorAll('.table-scroll')) {
    const hint = region.parentElement.querySelector('.table-hint');
    const update = () => { if (hint) hint.hidden = region.scrollWidth <= region.clientWidth + 1; };
    update();
    if (window.ResizeObserver) {
      const observer = new ResizeObserver(update); observer.observe(region); observer.observe(region.querySelector('table'));
    } else window.addEventListener('resize', update);
  }
  const snippets = [...document.querySelectorAll('.code-block pre code')];
  if (snippets.length && assets.highlightSrc) {
    load(assets.highlightSrc).then(() => {
      for (const code of snippets) {
        const language = [...code.classList].find(name => name.startsWith('language-'))?.slice(9);
        if (language && window.hljs?.getLanguage(language)) window.hljs.highlightElement(code);
      }
    }).catch(() => {}); // Escaped, readable source remains when highlighting is unavailable.
  }

  const expand = (svg, trigger) => {
    const home = svg.parentElement, originalStyle = svg.getAttribute('style');
    const dialog = document.createElement('dialog'); dialog.className = 'diagram-dialog';
    dialog.setAttribute('aria-label', '图示放大');
    const toolbar = document.createElement('div'); toolbar.className = 'diagram-dialog-toolbar';
    const title = document.createElement('strong'); title.textContent = '图示放大'; toolbar.append(title);
    const controls = document.createElement('div'); controls.className = 'diagram-zoom-controls'; toolbar.append(controls);
    const viewport = document.createElement('div'); viewport.className = 'diagram-dialog-viewport';
    viewport.tabIndex = 0; viewport.setAttribute('aria-label', '图示，可滚动查看');
    dialog.append(toolbar, viewport); document.body.append(dialog);
    const label = document.createElement('span'); label.className = 'diagram-zoom-label';
    label.setAttribute('aria-live', 'polite');
    const width = svg.viewBox.baseVal.width || svg.getBoundingClientRect().width || 640;
    let scale = 1;
    const resize = value => {
      scale = Math.max(.25, Math.min(4, value));
      svg.style.width = `${width * scale}px`; svg.style.maxWidth = 'none'; svg.style.height = 'auto';
      dialog.style.height = `${Math.min(window.innerHeight - 28, Math.max(320,
        svg.viewBox.baseVal.height * scale + toolbar.offsetHeight + 40))}px`;
      label.textContent = `${Math.round(scale * 100)}%`;
    };
    const button = (name, action) => {
      const control = document.createElement('button'); control.type = 'button'; control.textContent = name;
      control.addEventListener('click', action); controls.append(control); return control;
    };
    button('缩小', () => resize(scale / 1.25)); controls.append(label);
    button('放大', () => resize(scale * 1.25));
    const fit = () => resize(Math.min(1, (viewport.clientWidth - 32) / width));
    button('适应宽度', fit); button('关闭', () => dialog.close());
    dialog.addEventListener('close', () => {
      home.append(svg);
      if (originalStyle === null) svg.removeAttribute('style'); else svg.setAttribute('style', originalStyle);
      dialog.remove(); trigger.focus();
    }, {once: true});
    viewport.append(svg); dialog.showModal(); resize(1);
  };

  const diagrams = [...document.querySelectorAll('.mermaid-block')];
  if (!diagrams.length) return;
  const fail = block => {
    block.dataset.renderState = 'error';
    const status = block.querySelector('.diagram-status'); status.hidden = false;
    status.textContent = '图示暂时无法显示，可展开下方源码查看。';
    block.querySelector('details').open = true;
  };
  (async () => {
    try { await load(assets.mermaidSrc); } catch { diagrams.forEach(fail); return; }
    if (!window.mermaid) { diagrams.forEach(fail); return; }
    await document.fonts.ready;
    window.mermaid.initialize({
      startOnLoad: false, securityLevel: 'strict', theme: 'neutral', logLevel: 5,
      suppressErrorRendering: true, maxTextSize: 50000, maxEdges: 500,
      htmlLabels: false, flowchart: {htmlLabels: false},
      fontFamily: '-apple-system, BlinkMacSystemFont, PingFang SC, Microsoft YaHei, sans-serif',
      secure: ['secure', 'securityLevel', 'startOnLoad', 'maxTextSize', 'maxEdges',
        'suppressErrorRendering', 'dompurifyConfig', 'themeCSS', 'htmlLabels'],
    });
    for (const [index, block] of diagrams.entries()) {
      const source = block.querySelector('pre code').textContent;
      const id = `radar-diagram-${index}`;
      try {
        const {svg} = await window.mermaid.render(id, source);
        const viewport = block.querySelector('.diagram-viewport'); viewport.innerHTML = svg;
        const diagram = viewport.querySelector('svg');
        if (!diagram) throw new Error('No diagram');
        diagram.setAttribute('role', 'img');
        if (!diagram.hasAttribute('aria-label') && !diagram.hasAttribute('aria-labelledby')) diagram.setAttribute('aria-label', '文章图示');
        viewport.hidden = false; block.querySelector('.diagram-status').hidden = true;
        block.querySelector('details').open = false; block.dataset.renderState = 'ready';
        const control = block.querySelector('.diagram-expand'); control.hidden = false;
        control.addEventListener('click', () => expand(diagram, control));
      } catch {
        document.getElementById('d' + id)?.remove(); fail(block);
      }
    }
  })().catch(() => diagrams.filter(block => block.dataset.renderState !== 'ready').forEach(fail));
  };
  if (document.readyState === 'complete') void enhance();
  else document.addEventListener('DOMContentLoaded', () => { void enhance(); }, {once: true});
})();
