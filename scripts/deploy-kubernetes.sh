#!/bin/bash
# Kubernetes Deployment Script

set -e

PROJECT_NAME="$1"
NAMESPACE="${2:-default}"
REPLICAS="${3:-3}"

if [ -z "$PROJECT_NAME" ]; then
    echo "Usage: ./deploy-kubernetes.sh <project-name> [namespace] [replicas]"
    exit 1
fi

echo "🚀 Deploying $PROJECT_NAME to Kubernetes..."

# Check kubectl
if ! command -v kubectl &> /dev/null; then
    echo "❌ kubectl not found. Please install Kubernetes CLI."
    exit 1
fi

# Create namespace
echo "📦 Creating namespace..."
kubectl create namespace $NAMESPACE 2>/dev/null || true

# Create ConfigMap
echo "⚙️  Creating ConfigMap..."
kubectl create configmap $PROJECT_NAME-config --from-env-file=.env --namespace=$NAMESPACE -o yaml --dry-run=client | kubectl apply -f - 2>/dev/null || true

# Create deployment
echo "🚀 Creating Kubernetes deployment..."
cat << EOF | kubectl apply -f -
apiVersion: apps/v1
kind: Deployment
metadata:
  name: $PROJECT_NAME
  namespace: $NAMESPACE
  labels:
    app: $PROJECT_NAME
spec:
  replicas: $REPLICAS
  selector:
    matchLabels:
      app: $PROJECT_NAME
  template:
    metadata:
      labels:
        app: $PROJECT_NAME
    spec:
      containers:
      - name: $PROJECT_NAME
        image: gcr.io/PROJECT_ID/$PROJECT_NAME:latest
        ports:
        - containerPort: 8000
        envFrom:
        - configMapRef:
            name: $PROJECT_NAME-config
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5
EOF

# Create Service
echo "🌐 Creating Kubernetes service..."
cat << EOF | kubectl apply -f -
apiVersion: v1
kind: Service
metadata:
  name: $PROJECT_NAME-service
  namespace: $NAMESPACE
spec:
  selector:
    app: $PROJECT_NAME
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8000
  type: LoadBalancer
EOF

# Create Ingress
echo "🔗 Creating Ingress..."
cat << EOF | kubectl apply -f -
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: $PROJECT_NAME-ingress
  namespace: $NAMESPACE
spec:
  rules:
  - host: $PROJECT_NAME.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: $PROJECT_NAME-service
            port:
              number: 80
EOF

echo "✅ Kubernetes deployment complete!"
echo "📍 Service URL: $(kubectl get service $PROJECT_NAME-service -n $NAMESPACE -o jsonpath='{.status.loadBalancer.ingress[0].hostname}')"
kubectl get all -n $NAMESPACE
