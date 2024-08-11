import { defineConfig, loadEnv } from "vite";
import vue from "@vitejs/plugin-vue";
import { createRequire } from "node:module";
const require = createRequire(import.meta.url);

// https://vitejs.dev/config/
export default defineConfig(({ mode }) => {
    const env = loadEnv(mode, process.cwd());
    return {
        plugins: [
            vue(),
        ],
        base: env.VITE_BASE_URL,
        build: {
            rollupOptions: {
                input: ["./index.html", "./displayer.html"],
            },
        },
    };
});
