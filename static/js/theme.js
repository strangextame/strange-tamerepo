document.addEventListener('DOMContentLoaded', () => {
  // JavaScript for theme switcher functionality
  document.querySelectorAll('[data-bs-theme-value]').forEach(toggle => {
    toggle.addEventListener('click', () => {
      const theme = toggle.getAttribute('data-bs-theme-value');
      localStorage.setItem('theme', theme);
      // Re-evaluate preferred theme for 'auto'
      document.documentElement.setAttribute('data-bs-theme', theme === 'auto' ? (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light') : theme);
    });
  });

  // Dynamic padding adjustment for watermark removed as it's no longer fixed.
  // The flexbox layout in base.html will handle its positioning.
});