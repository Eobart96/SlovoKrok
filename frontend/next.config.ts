import { PHASE_DEVELOPMENT_SERVER } from "next/constants";
import type { NextConfig } from "next";

const backendUrl = process.env.BACKEND_URL ?? "http://127.0.0.1:8000";

export default function nextConfig(phase: string): NextConfig {
  return {
    devIndicators: false,
    distDir:
      process.env.NEXT_DIST_DIR ??
      (phase === PHASE_DEVELOPMENT_SERVER ? ".next-dev" : ".next"),
    async rewrites() {
      return [
        { source: "/api/:path*", destination: `${backendUrl}/api/:path*` },
        { source: "/health", destination: `${backendUrl}/health` },
        { source: "/docs", destination: `${backendUrl}/docs` },
        { source: "/openapi.json", destination: `${backendUrl}/openapi.json` },
      ];
    },
  };
}
