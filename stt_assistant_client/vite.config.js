import { defineConfig, loadEnv } from "vite";
import react from "@vitejs/plugin-react";
import path from "path";

export default defineConfig(({ mode }) => {
  const envDir = path.resolve(__dirname, "../env");
  const env = loadEnv("client", envDir, "");

  return {
    plugins: [react()],
    server: {
      host: "0.0.0.0",
      port: 3000,
    },
    define: {
      "import.meta.env.VITE_AUTH0_DOMAIN": JSON.stringify(
        env.VITE_AUTH0_DOMAIN
      ),
      "import.meta.env.VITE_AUTH0_CLIENT_ID": JSON.stringify(
        env.VITE_AUTH0_CLIENT_ID
      ),
      "import.meta.env.VITE_AUTH0_AUDIENCE": JSON.stringify(
        env.VITE_AUTH0_AUDIENCE
      ),
    },
  };
});
