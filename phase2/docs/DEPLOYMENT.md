# Deployment Guide

This guide explains how to deploy the Hackathon Todo application to production.

## Architecture Overview

The application consists of two separate services:
- **Frontend**: Next.js application deployed to Vercel
- **Backend**: FastAPI application deployed to Google Cloud Run

## Deploying the Backend to Google Cloud Run

### Prerequisites
- Google Cloud account with billing enabled
- Google Cloud SDK installed and configured
- Docker installed

### Steps

1. **Prepare the backend for deployment**

   Update your `.env.production` file with production settings:
   ```env
   DATABASE_URL=postgresql://username:password@ep-xxx.us-east-1.aws.neon.tech/dbname?sslmode=require
   JWT_SECRET=a-very-long-and-secure-random-string
   JWT_ALGORITHM=HS256
   JWT_EXPIRATION_HOURS=24
   API_HOST=0.0.0.0
   API_PORT=8080
   DEBUG=false
   ENVIRONMENT=production
   ALLOWED_ORIGINS=https://your-frontend-domain.vercel.app
   ```

2. **Build and push the Docker image**

   Create a `Dockerfile` in the backend directory if not already present:
   ```dockerfile
   FROM python:3.10-slim
   
   WORKDIR /app
   
   COPY requirements.txt .
   RUN pip install --no-cache-dir -r requirements.txt
   
   COPY . .
   
   EXPOSE 8080
   
   CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
   ```

   Build and push the image to Google Container Registry:
   ```bash
   gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/todo-backend
   ```

3. **Deploy to Cloud Run**

   ```bash
   gcloud run deploy todo-backend \
     --image gcr.io/YOUR_PROJECT_ID/todo-backend \
     --platform managed \
     --region YOUR_REGION \
     --port 8080 \
     --set-env-vars DATABASE_URL=YOUR_DATABASE_URL \
     --set-env-vars JWT_SECRET=YOUR_JWT_SECRET \
     --set-env-vars ALLOWED_ORIGINS=YOUR_FRONTEND_URL \
     --memory 512Mi \
     --cpu 1 \
     --timeout 300s \
     --concurrency 80 \
     --max-instances 10 \
     --min-instances 0
   ```

4. **Set up SSL certificate** (if using custom domain)

   Follow Google Cloud documentation to map your custom domain and obtain SSL certificate.

## Deploying the Frontend to Vercel

### Prerequisites
- Vercel account
- Vercel CLI installed (optional)

### Steps

1. **Prepare the frontend for deployment**

   Update your `.env.production` file with production settings:
   ```env
   NEXT_PUBLIC_API_URL=https://your-backend-url.run.app/api
   ```

2. **Deploy to Vercel**

   Using Vercel CLI:
   ```bash
   cd frontend
   vercel --prod
   ```

   Or push to a connected Git repository (GitHub, GitLab, Bitbucket) with Vercel integration enabled.

3. **Configure environment variables in Vercel dashboard**

   Go to your project settings in Vercel and add the environment variables:
   - `NEXT_PUBLIC_API_URL`: Your deployed backend URL

## Environment-Specific Configuration

### Production Environment Variables

#### Backend
- `DATABASE_URL`: Production Neon PostgreSQL connection string
- `JWT_SECRET`: Strong, randomly generated secret key
- `DEBUG`: `false`
- `ENVIRONMENT`: `production`
- `ALLOWED_ORIGINS`: Your frontend domain (e.g., `https://your-app.vercel.app`)

#### Frontend
- `NEXT_PUBLIC_API_URL`: Your deployed backend API URL

## Monitoring and Logs

### Backend (Cloud Run)
- Access logs through Google Cloud Console > Cloud Run > your service > Logs
- Set up custom dashboards and alerts in Google Cloud Monitoring

### Frontend (Vercel)
- Access logs through Vercel dashboard
- Set up custom analytics and error tracking

## Scaling Configuration

### Backend Scaling
The deployment command above sets up:
- Min instances: 0 (to save costs when idle)
- Max instances: 10 (adjust based on expected load)
- Concurrency: 80 requests per instance
- Memory: 512MB per instance

Adjust these values based on your traffic patterns and performance requirements.

### Frontend Scaling
Vercel automatically scales your Next.js application globally with edge caching.

## Security Considerations

1. **JWT Secret**: Use a strong, randomly generated secret and rotate periodically
2. **Database Connection**: Always use SSL connections to your database
3. **CORS Policy**: Restrict allowed origins to only your frontend domains
4. **API Rate Limiting**: Consider implementing rate limiting for public endpoints
5. **Secret Management**: Use Google Secret Manager for sensitive configuration

## Backup and Recovery

### Database Backups
- Neon PostgreSQL provides automated backups
- Configure backup retention policies in your Neon dashboard
- Test recovery procedures regularly

### Application Rollback
- Maintain versioned deployments
- Use Git tags for release versions
- Have a rollback plan ready

## Post-Deployment Checklist

- [ ] Verify the backend API is accessible at the deployed URL
- [ ] Test the API documentation at `/api/docs`
- [ ] Verify the frontend can communicate with the backend
- [ ] Test user registration and login flows
- [ ] Verify task CRUD operations work end-to-end
- [ ] Check that user isolation is working correctly
- [ ] Verify SSL certificates are properly configured
- [ ] Set up monitoring and alerting
- [ ] Document the deployment for team members
- [ ] Update DNS records if using custom domains

## Troubleshooting Common Issues

### CORS Errors
- Verify that `ALLOWED_ORIGINS` includes your frontend domain
- Check that the domain includes the protocol (https://)

### Database Connection Issues
- Verify the database connection string is correct
- Ensure the database allows connections from Cloud Run region
- Check that SSL mode is properly configured

### JWT Validation Issues
- Ensure the JWT secret is identical between frontend and backend
- Check that tokens are not expired
- Verify that the algorithm matches between services

### Performance Issues
- Monitor Cloud Run instance scaling
- Check database query performance
- Consider adding caching for frequently accessed data