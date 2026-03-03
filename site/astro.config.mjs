import { defineConfig } from 'astro/config';
import tailwind from '@astrojs/tailwind';

export default defineConfig({
  integrations: [tailwind()],
  output: 'static',
  // Update this when deploying to GitHub Pages
  site: 'https://silkyrich.github.io',
  base: '/uk-curriculum-as-graph',
});
