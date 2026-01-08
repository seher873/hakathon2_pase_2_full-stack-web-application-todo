/** @type {import('next').NextConfig} */
const nextConfig = {
  // Temporarily remove output: 'export' to see if build works without static generation
  // output: 'export', // This is already set in your netlify.toml
  // trailingSlash: true,

  // Handle the dynamic routes that use client-side hooks
  async redirects() {
    return [
      // Redirect any problematic routes if needed
    ]
  },
};

module.exports = nextConfig;