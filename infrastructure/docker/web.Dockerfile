# Multi-stage build for JARVIS Web Dashboard
FROM node:18-alpine as builder

WORKDIR /app

# Copy package files
COPY apps/web/dashboard/package*.json ./
RUN npm ci

# Copy source
COPY apps/web/dashboard/ ./
RUN npm run build

# Production stage
FROM nginx:alpine

# Copy built files
COPY --from=builder /app/dist /usr/share/nginx/html

# Copy nginx configuration
COPY infrastructure/docker/nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
