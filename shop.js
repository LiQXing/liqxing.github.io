(() => {
  'use strict';
  const theme = document.querySelector('#theme');
  function updateTheme() {
    const dark = document.documentElement.dataset.theme === 'dark';
    theme.textContent = dark ? '☀' : '◐';
    theme.setAttribute('aria-label', dark ? '切换到日间模式' : '切换到夜间模式');
    theme.setAttribute('aria-pressed', String(dark));
  }
  theme.addEventListener('click', () => {
    const value = document.documentElement.dataset.theme === 'dark' ? 'light' : 'dark';
    document.documentElement.dataset.theme = value;
    try { localStorage.setItem('liqxing-theme', value); } catch {}
    updateTheme();
  });
  updateTheme();
  const dialog = document.querySelector('#consult-dialog');
  const request = document.querySelector('#request');
  const status = document.querySelector('#copy-status');
  document.querySelectorAll('[data-service]').forEach(button => {
    button.addEventListener('click', () => {
      document.querySelector('#service-name').textContent = button.dataset.service;
      request.value = `你好，我想咨询「${button.dataset.service}」。\n\n主要用途：\n期望服务期限：\n预算范围：\n期望办理时间：\n\n想了解具体费用、交付方式与售后约定，谢谢。`;
      status.textContent = '';
      dialog.showModal();
    });
  });
  dialog.querySelector('.dialog-close').addEventListener('click', () => dialog.close());
  dialog.addEventListener('click', event => { if (event.target === dialog) {
    const r = dialog.getBoundingClientRect();
    if (event.clientX < r.left || event.clientX > r.right || event.clientY < r.top || event.clientY > r.bottom) dialog.close();
  }});
  document.querySelector('#copy-request').addEventListener('click', async () => {
    try {
      await navigator.clipboard.writeText(request.value);
      status.textContent = '已复制。请前往私信，粘贴并发送给我。';
    } catch {
      request.focus(); request.select();
      status.textContent = '请手动复制已选中的内容，再前往私信发送。';
    }
  });
})();
