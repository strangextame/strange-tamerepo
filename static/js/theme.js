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

  // Adjust body padding-bottom dynamically to account for the fixed watermark
  const watermarkContainer = document.getElementById('scryfall-watermark-container');
  if (watermarkContainer) {
      const watermarkHeight = watermarkContainer.offsetHeight;
      document.body.style.paddingBottom = `${watermarkHeight}px`;
  }
});