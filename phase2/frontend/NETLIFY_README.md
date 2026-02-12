# Phase-2 Frontend for Netlify Deployment

This repository contains the Phase-2 frontend application deployed to Netlify.

## Overview

This is a Next.js application that serves as the frontend for the Todo application. It provides:
- User authentication (login/signup)
- Dashboard for managing tasks
- Integration with the backend API
- Responsive UI built with Tailwind CSS

## Deployment

This application is designed to be deployed to Netlify with the following configuration:

### Build Settings:
- Build command: `npm run build`
- Publish directory: `out`

### Environment Variables:
- `NEXT_PUBLIC_API_BASE_URL`: Base URL for the backend API

## Features

- Authentication flow (login/signup)
- Task management dashboard
- Responsive design for all device sizes
- Modern UI with Tailwind CSS and shadcn/ui components

## Local Development

To run locally:
```bash
npm install
npm run dev
```

The application will be available at `http://localhost:3000`.

## License

MIT