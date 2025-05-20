minikube start --driver=docker --force

kubectl apply -f k8s/namespace.yaml


kubectl apply -f k8s/pvcs.yaml


kubectl apply -f k8s/copy-pod.yaml


kubectl cp /home/aayushi/Desktop/spe_project/models/encodings.pkl face-recognition/copy-models:/app/models/encodings.pkl


kubectl exec -n face-recognition -it copy-models -- ls -l /app/models


kubectl delete pod copy-models -n face-recognition


# Build images
docker build -t recognition:latest -f Dockerfile.recognition .
docker build -t frontend:latest -f Dockerfile.frontend .

# Load images into minikube
minikube image load recognition:latest
minikube image load frontend:latest

kubectl apply -f k8s/recognition-deployment.yaml

eval $(minikube docker-env)  # So it builds inside Minikube's Docker daemon
kubectl apply -f k8s/frontend-deployment.yaml
kubectl apply -f k8s/services.yaml

# Check pods
kubectl get pods -n face-recognition

# Check services
kubectl get services -n face-recognition

# Get the frontend URL
minikube service frontend -n face-recognition --url

# Watch pod status
kubectl get pods -n face-recognition -w

# Check logs
kubectl logs -n face-recognition -l app=recognition -f
kubectl logs -n face-recognition -l app=frontend -f

minikube service frontend-service -n face-recognition