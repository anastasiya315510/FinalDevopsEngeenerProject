

# Flask CI/CD & Kubernetes Orchestration

This repository demonstrates a **full CI/CD pipeline for a Flask application**, containerized with Docker, orchestrated with **Kubernetes**, and monitored using **Prometheus** and **Grafana**. The pipeline also uses **ArgoCD** for GitOps-style deployments.

---

## 🚀 Features

* **Flask Application**: Lightweight "Hello World" web app.
* **CI/CD with GitHub Actions**: Build, lint, test, and deploy automatically.
* **Kubernetes Deployment**: Supports Namespaces, Deployments, Services, and HPA.
* **GitOps with ArgoCD**: Automates application delivery from Git repository.
* **Monitoring**: Prometheus for metrics, Grafana for dashboards.
* **Containerized**: Runs locally with Docker or in Kubernetes clusters.

---

## 🗂 Project Structure

```
.
├── app/                        # Flask application code
├── flask-chart/                # Helm chart for Flask app
├── manifests/
│   ├── argocd/                 # ArgoCD manifests
│   └── grafana/                # Grafana Helm chart overrides (values.yaml)
├── requirements.txt            # Python dependencies
├── Dockerfile                  # Docker build instructions
├── .github/workflows/ci-cd.yml # GitHub Actions pipeline
└── README.md
```

---

## 🧑‍💻 Local Development

### Clone & Install

```bash
git clone https://github.com/anastasiya315510/Phase_1.git
cd Phase_1

python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

pip install -r requirements.txt
```

### Run Flask App

```bash
python app.py
```

Visit: [http://localhost:8000](http://localhost:8000)

### Docker (Optional)

```bash
docker build -t flask_final_project:latest .
docker run -d -p 8000:8000 flask_final_project:latest
```

---

## 🐳 CI/CD with GitHub Actions

The pipeline (`.github/workflows/ci-cd.yml`) does:

1. **Build Stage**: Sets up Python, installs dependencies, and caches pip.
2. **Lint Stage**: Runs `pylint` for code quality.
3. **Test Stage**: Runs `pytest`.
4. **Deploy Stage**:

   * Creates namespaces for `dev`, `prod`, `argocd`, and `monitoring`.
   * Installs Prometheus CRDs.
   * Deploys ArgoCD via manifests.
   * Deploys Grafana using the **official Helm chart**.
   * Deploys your Flask Helm chart (`flask-chart/`) to the corresponding namespace.

> The deployment automatically picks the namespace based on the branch (`dev` or `master`).

---

## 🏗 Kubernetes Deployment

### 1. Cluster Setup

* Using **Kind**, **Minikube**, or any Kubernetes cluster.

```bash
kind create cluster --name flask-ci-cluster
kubectl cluster-info
```

### 2. Namespaces

```bash
kubectl create ns dev
kubectl create ns prod
kubectl create ns argocd
kubectl create ns monitoring
```

### 3. Deploy Prometheus CRDs

```bash
kubectl apply --validate=false -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/main/example/prometheus-operator-crd/monitoring.coreos.com_servicemonitors.yaml
kubectl apply --validate=false -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/main/example/prometheus-operator-crd/monitoring.coreos.com_podmonitors.yaml
kubectl apply --validate=false -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/main/example/prometheus-operator-crd/monitoring.coreos.com_prometheusrules.yaml
```

### 4. ArgoCD Deployment

```bash
kubectl apply -n argocd -f manifests/argocd/argo-cd/templates --recursive
```

* Access ArgoCD UI:

```bash
kubectl port-forward svc/argocd-server -n argocd 8080:443
```

* Login:

```bash
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d
```

---

### 5. Grafana Deployment

* Using Helm:

```bash
helm repo add grafana https://grafana.github.io/helm-charts
helm repo update
helm upgrade --install grafana grafana/grafana \
  --namespace monitoring \
  --values manifests/grafana/values.yaml \
  --wait
```

* Access Grafana UI:

```bash
kubectl port-forward svc/grafana -n monitoring 3000:80
```

* Default login: `admin` / password from `values.yaml`.

---

### 6. Flask App Deployment

* Dev:

```bash
helm upgrade --install flask-app-dev flask-chart/ --namespace dev -f flask-chart/values-dev.yaml --wait
```

* Prod:

```bash
docker build -t 315510/flask_final_project:latest .
docker push 315510/flask_final_project:latest

helm upgrade --install flask-app-prod flask-chart/ --namespace prod -f flask-chart/values-prod.yaml --wait
```

---

## 🔧 Monitoring & Observability

* **Prometheus**: Scrapes metrics from your Flask pods and services.
* **Grafana**: Dashboards for metrics, CPU/memory usage, request rates.
* **HPA**: Horizontal Pod Autoscaler can scale Flask pods based on CPU.

---

## ✅ Notes & Tips

* Use **Helm** for all deployments; avoids broken raw manifests.
* Keep branch-specific overrides in `values-dev.yaml` and `values-prod.yaml`.
* GitHub Actions automates full build → test → deploy flow.
* Always check pods status:

```bash
kubectl get pods -n dev
kubectl get pods -n prod
kubectl get pods -n monitoring
kubectl get pods -n argocd
```


