/** @type {import('next').NextConfig} */
const nextConfig = {
  // Use the Netlify plugin for deployment instead of static export
  // The @netlify/next plugin will handle the deployment correctly
  output: undefined, // Let Netlify plugin handle the output

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