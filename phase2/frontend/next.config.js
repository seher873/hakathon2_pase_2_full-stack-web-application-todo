/** @type {import('next').NextConfig} */
const nextConfig = {
  // Static export for Netlify deployment
  output: 'export',
  
  // Disable image optimization for static export
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