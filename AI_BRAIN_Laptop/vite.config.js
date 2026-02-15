import { defineConfig } from "vite";
import { resolve } from "path";

export default defineConfig({
    root: resolve(__dirname, 'src'),
    build: {
        outDir: resolve(__dirname, 'static/dist'),
        emptyOutDir: true,
        rollupOptions: {
            input: resolve(__dirname, 'src/main.js'),
            output: {
                entryFileNames: 'bundle.js'
            }
        },
    },
    server: {
        port: 5173,
        host: '0.0.0.0',
        cors: true
    }
})