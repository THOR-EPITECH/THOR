import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  output: "standalone",
  // Configuration pour les appels API
  async rewrites() {
    return [
      {
        source: '/api/backend/:path*',
        destination: `${process.env.API_URL || 'http://localhost:8000'}/api/:path*`,
      },
    ];
  },
};

export default nextConfig;
