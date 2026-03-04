/** @type {import('tailwindcss').Config} */
export default {
  content: ['./src/**/*.{astro,html,js,jsx,md,mdx,svelte,ts,tsx,vue}'],
  theme: {
    extend: {
      colors: {
        // Graph node colors from the visualization layer
        'ks-blue': '#3B82F6',
        'concept-teal': '#14B8A6',
        'cluster-indigo': '#6366F1',
        'lens-violet': '#7C3AED',
        'difficulty-amber': '#F59E0B',
        'cpa-cyan': '#06B6D4',
        'delivery-emerald': '#10B981',
        // Delivery mode colors
        'dm-ai-direct': '#10B981',
        'dm-ai-facilitated': '#3B82F6',
        'dm-guided': '#F59E0B',
        'dm-specialist': '#EF4444',
      },
    },
  },
  plugins: [],
};
