module.exports = {
  content: [
    './templates/**/*.{html,js}',
    './core/templates/**/*.{html,js}',
    './node_modules/flowbite/**/*.{html,js}',
  ],
  safelist: [
    'mt-4',
    'bg-gray-900/50',
    'dark:bg-gray-900/80',
    'fixed',
    'inset-0',
    'z-30',
  ],
  theme: {
    extend: {
      colors: {
        primary: {"50":"#ecfdf5","100":"#d1fae5","200":"#a7f3d0","300":"#6ee7b7","400":"#34d399","500":"#10b981","600":"#059669","700":"#047857","800":"#065f46","900":"#064e3b","950":"#022c22"},
        skyblue: '#F2F6FF',
        darkblue: '#3B39A7',
        bgdarkblue: '#0F1F45',
        bglightblue: '#1F2873',
        navy: '#4456A2',
        bggray: '#F8F9FB'
      },
      fontFamily: {
        'body': [
          'Inter',
          'ui-sans-serif',
          'system-ui',
          '-apple-system',
          'Segoe UI',
          'Roboto',
          'Helvetica Neue',
          'Arial',
          'Noto Sans',
          'sans-serif',
          'Apple Color Emoji',
          'Segoe UI Emoji',
          'Segoe UI Symbol',
          'Noto Color Emoji'
        ],
        'sans': [
          'Inter',
          'ui-sans-serif',
          'system-ui',
          '-apple-system',
          'Segoe UI',
          'Roboto',
          'Helvetica Neue',
          'Arial',
          'Noto Sans',
          'sans-serif',
          'Apple Color Emoji',
          'Segoe UI Emoji',
          'Segoe UI Symbol',
          'Noto Color Emoji'
          // other fallback fonts
        ]
      }
    },
  },
  plugins: [
    require('flowbite/plugin')
  ],
}
