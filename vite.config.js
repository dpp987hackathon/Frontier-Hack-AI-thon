import { defineConfig } from 'vite'

export default defineConfig({
  // Serve from project root
  root: './',
  
  // Public directory for static assets
  publicDir: 'Data',
  
  server: {
    port: 8000,
    open: '/UI/index.html',
    cors: true
  },
  
  build: {
    outDir: 'dist',
    emptyOutDir: true
  },
  
  resolve: {
    alias: {
      '@': '/UI'
    }
  }
})

