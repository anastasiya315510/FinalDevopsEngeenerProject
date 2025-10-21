
# 🌍 Phase_1 (Flask Hello World)

**Flask Hello World** is a lightweight, containerized web application built with Flask and served via Gunicorn. It’s ideal as a beginner-friendly example of production-ready container deployment using Docker and Docker Compose.



---

## 🚀 Features

- **Minimal Flask App:** Basic route returning `Hello, World!`
- **Production-Ready:** Uses Gunicorn instead of Flask’s development server
- **Dockerized:** Easily deployable using Docker and Docker Compose
- **Cross-platform Setup:** Works on Linux, macOS, and Windows
- **Clean Structure:** Simple and extensible project layout



## 🗂 Project Structure

```
Phase_1/
├── app.py                # Main Flask application
├── Dockerfile            # Docker image build instructions
├── docker-compose.yml    # Compose service definition
├── requirements.txt      # Python dependencies


````

---

## 🧑‍💻 Installation

### Locally

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/anastasiya315510/Phase_1.git
   cd Phase_1
    ```


2. **Set Up a Virtual Environment (optional but recommended):**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

---

## ▶️ Running the Application Locally

1. **Start the Flask App:**

   ```bash
   python app.py
   ```

2. **Access the App:**

   Open your browser and visit: [ http://localhost:8000](http://127.0.0.1:8000)

---

## 🐳 Running with Docker Compose

### Build the Image

```bash
docker compose build
```

### Start the Container

```bash
docker compose up
```

### Stop the Container

```bash
docker compose down
```

---

## 🐙 Manual Docker Commands

If not using Compose:

```bash
docker build -t flask_final_project:latest .
docker run -d -p 8000:8000 --name flask-app flask_final_project:latest
```

Visit the app at: [http://localhost:8000](http://localhost:8000)

---

## 📌 Notes

* This is a basic example app—feel free to extend it with more routes, templates, or database support.
* Gunicorn is used in place of Flask’s built-in server for production readiness.
* If using volumes for persistent data, define them in `docker-compose.yml`.

---

### Phase 2: Orchestration - Kubernetes Basics & Advanced
Objective:
In Phase 2, you will build upon your containerization knowledge by orchestrating your
application using Kubernetes. The goal is to deploy a scalable and highly available application.
Tasks:
#### 1. Kubernetes Cluster Setup:
○ Set up a Kubernetes cluster using Minikube or k3s.
```bazaar
minikube start --driver=docker
minikube status

```
○ Deploy your Dockerized web application as a Kubernetes Pod.
```bazaar
kubectl apply -f  k8s/flask-final-project-pod.yaml
pod/flask-final-project-pod created
```



#### 2. Basic Kubernetes Resources:
○ Create a Deployment and ReplicaSet for managing the application.
```bazaar
kubectl apply -f k8s/flask-final-project-deployment.yaml

kubectl get deployments
kubectl get replicaset
kubectl get pods


```
○ Expose the application externally using a Kubernetes Service.

```bazaar
kubectl apply -f k8s/flask-final-project-service.yaml

kubectl get service flask-final-project-service

```
○ Implement Horizontal Pod Autoscaling (HPA) based on CPU usage.
   - add Metrics Server:
```bazaar
minikube addons enable metrics-server
kubectl get deployment metrics-server -n kube-system

kubectl apply -f k8s/flask-final-project-deployment.yaml

```

- Add autoscaling
```
kubectl autoscale deployment flask-final-project-deployment \
  --cpu=50% \
  --min=2 \
  --max=5
  
  
  kubectl get hpa
```
#### 3. Advanced Kubernetes Concepts:
○ Use ConfigMaps and Secrets to manage configuration.
```bazaar
kubectl apply -f k8s/configmap.yaml
kubectl apply -f  k8s/secret.yaml
kubectl apply -f k8s/flask-final-project-deployment.yaml
```
○ Set up Kubernetes CronJobs to automate periodic tasks.
```bazaar
kubectl apply -f k8s/cronjob.yaml
kubectl describe cronjob flask-final-project-cronjob
```
○ Implement Liveness and Readiness Probes for monitoring application health.



