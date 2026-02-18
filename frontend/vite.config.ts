import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vite.dev/config/
export default defineConfig({
  plugins: [vue()],
  server: {
    host: true, // bind sur 0.0.0.0 — nécessaire en mode Docker
    hmr: process.env.VITE_HMR_CLIENT_PORT
      ? { clientPort: parseInt(process.env.VITE_HMR_CLIENT_PORT) }
      : {},
    proxy: {
      // Utilisé uniquement hors Docker (dev local direct)
      '/upload': 'http://localhost:8000',
      '/split': 'http://localhost:8000',
      '/thumbs': 'http://localhost:8000',
    },
  },
})
