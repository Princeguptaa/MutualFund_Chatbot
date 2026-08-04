import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    host: '127.0.0.1', // explicitly use IPv4 localhost
    port: 5173,
    open: true // this will automatically open your browser!
  }
})
