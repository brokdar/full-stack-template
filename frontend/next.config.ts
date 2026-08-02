import type { NextConfig } from "next";

// Validate environment at build time — a bad deploy fails here, not at runtime.
import "./env";

const nextConfig: NextConfig = {
  // Self-contained server bundle for the Docker runtime image.
  output: "standalone",
};

export default nextConfig;
