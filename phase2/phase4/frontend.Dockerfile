FROM node:20-alpine

WORKDIR /app

# Copy package files from Phase3 frontend
COPY ./phase3/frontend/package*.json ./

RUN npm ci --only=production

# Copy source code
COPY ./phase3/frontend/src ./src
COPY ./phase3/frontend/public ./public

EXPOSE 3000

CMD ["npm", "start"]