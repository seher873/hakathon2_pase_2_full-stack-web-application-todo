/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'export', // Enable static site generation
  trailingSlash: true,

  // Handle the dynamic routes that use client-side hooks
  async redirects() {
    return [
      // Redirect any problematic routes if needed
    ]
  }
};

module.exports = nextConfig;