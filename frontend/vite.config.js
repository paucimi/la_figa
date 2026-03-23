import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import path from 'path';

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
  build: {
    // Evita conflicto con el mount /assets del backend (logo, etc.)
    assetsDir: 'react-assets',
    outDir: 'dist',
  },
  server: {
    // En desarrollo: proxy al backend FastAPI
    proxy: {
      '/api': { target: 'http://localhost:8080', changeOrigin: true },
      '/editor': { target: 'http://localhost:8080', changeOrigin: true },
      '/static': { target: 'http://localhost:8080', changeOrigin: true },
      '/assets': { target: 'http://localhost:8080', changeOrigin: true },
    },
  },
});
