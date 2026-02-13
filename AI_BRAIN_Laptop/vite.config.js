import { defineConfig } from "vite";

export default defineConfig({
    root: '/src',
    build: {
        outDir: '../static/dist',
        emptyOutDir: true,
        rollupOptions: {
            input: './main.js',
            output: {
                entryFileNames: 'bundle.js'
            }
        },
    },
    server: {
        port: 5173,
        cors: true,
        origin: 'http://localhost:5173',
        headers: {
            'access-control-allow-origin': '*'
        }
    }
})