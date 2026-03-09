/** @type {import('next').NextConfig} */
const nextConfig = {
  // Disable image optimization for Netlify deployment
  images: {
    unoptimized: true,
  },

  // WSL compatibility settings
  webpack: (config, { isServer }) => {
    if (!isServer) {
      config.resolve.fallback = {
        ...(config.resolve.fallback || {}),
        fs: false,
      };
    }

    return config;
  }
};

module.exports = nextConfig;