/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './entry/templates/landing/*.html',
    './entry/templates/login/*.html',
    './entry/templates/registration/*.html',
    './feedback/templates/active/*.html',
    './feedback/templates/dashboard/*.html',
    './feedback/templates/guides/*.html',
    './feedback/templates/initial/*.html',
    './templates/*.html',
  ],
  darkMode: 'media', // or 'media' or 'class'
  theme: {
    extend: {},
    fontFamily: {
      'sans': ['ui-sans-serif', 'system-ui', '-apple-system', 'BlinkMacSystemFont', 'Segoe UI', 'Roboto', 'Helvetica Neue', 'Arial', 'Noto Sans', 'sans-serif', 'Apple Color Emoji', 'Segoe UI Emoji', 'Segoe UI Symbol', 'Noto Color Emoji'],
      'serif': ['ui-serif', 'Georgia', 'Cambria', '"Times New Roman"', 'Times', 'serif'],
      'mono': ['ui-monospace', 'SFMono-Regular', 'Menlo', 'Monaco', 'Consolas', '"Liberation Mono"', '"Courier New"', 'monospace']
    },
  },
  variants: {
    extend: {},
  },
  plugins: [],
  mode: 'jit',
}

