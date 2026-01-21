/** @type {import('next').NextConfig} */
const nextConfig = {
  // Enable server-side rendering for dynamic functionality like auth and API calls
  output: undefined, // Use default SSR mode instead of static export
  trailingSlash: true,

  // Handle the dynamic routes that use client-side hooks
  async redirects() {
    return [
      // Redirect any problematic routes if needed
    ]
  }
};

module.exports = nextConfig;