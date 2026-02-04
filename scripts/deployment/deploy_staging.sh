#!/bin/bash
# Deploy to staging environment

set -e

echo "Deploying JARVIS to staging..."

# Build Docker images
echo "Building Docker images..."
docker-compose -f docker-compose.prod.yml build

# Tag images for registry
echo "Tagging images..."
docker tag jarvis-api:prod registry.example.com/jarvis-api:staging
docker tag jarvis-web:prod registry.example.com/jarvis-web:staging

# Push to registry
echo "Pushing images to registry..."
docker push registry.example.com/jarvis-api:staging
docker push registry.example.com/jarvis-web:staging

# Deploy to Kubernetes
echo "Deploying to Kubernetes..."
kubectl apply -f infrastructure/kubernetes/overlays/staging/

# Wait for rollout
echo "Waiting for deployment to complete..."
kubectl rollout status deployment/jarvis-api -n staging
kubectl rollout status deployment/jarvis-web -n staging

echo "✅ Deployment to staging complete!"
echo ""
echo "Check status:"
echo "  kubectl get pods -n staging"
echo ""
echo "View logs:"
echo "  kubectl logs -f deployment/jarvis-api -n staging"
