/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'export',
  distDir: 'out',
  trailingSlash: true,
  images: {
    unoptimized: true,
  },
  experimental: {
    appDir: true,
    // Enable turbopack explicitly to avoid conflicts
    turbo: {},
  },
  // Remove webpack config for turbopack compatibility
}

module.exports = nextConfig