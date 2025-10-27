#### Phase 4: Advanced Automation – GitOps & Monitoring
Objective:
Enhance your QuakeWatch deployment by implementing GitOps practices for
continuous deployment and setting up comprehensive monitoring using Prometheus
and Grafana.
Tasks:
● GitOps with ArgoCD:
○ ArgoCD Setup:
■ Install ArgoCD on your Kubernetes (k3s) cluster.
■ Configure ArgoCD to track a Git repository containing your
Kubernetes manifests (or Helm charts) for QuakeWatch.

```bazaar
# Create ArgoCD namespace
kubectl create namespace argocd

# Install ArgoCD
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
kubectl get pods -n argocd

kubectl port-forward svc/argocd-server -n argocd 8085:443


```
#Got it! Here’s a concise, practical way to document your Argo CD setup and usage for your QuakeWatch project. You can include this in your project repo as `docs/ARGOCD.md` or similar.

---

# **Argo CD Configuration & Usage Guide**

## **1️⃣ Prerequisites**

* Kubernetes cluster running (k3s, minikube, etc.)
* Argo CD installed in `argocd` namespace:

```bash
kubectl get pods -n argocd
```

You should see pods like:

* `argocd-server`

* `argocd-repo-server`

* `argocd-application-controller`

* `kubectl` configured to talk to your cluster

* Git repository containing your Kubernetes manifests or Helm charts

---

## **2️⃣ Accessing Argo CD**

### **Port-forward Argo CD server**

```bash
kubectl port-forward svc/argocd-server -n argocd 8085:443
```

> Access Argo CD UI at: [https://localhost:8085](https://localhost:8085)

### **Login via CLI**

```bash
argocd login localhost:8085 \
  --username admin \
  --password $(kubectl get secret argocd-initial-admin-secret -n argocd -o jsonpath="{.data.password}" | base64 -d) \
  --insecure
```

---

## **3️⃣ Create an Application**

Assume you have a Helm chart in Git under `flask-chart`:

```bash
argocd app create flask-app \
  --repo https://github.com/anastasiya315510/FinalDevopsEngeenerProject.git \
  --path flask-chart \
  --dest-server https://kubernetes.default.svc \
  --dest-namespace quakewatch \
  --sync-policy automated \
  --self-heal \
  --auto-prune
```

**Explanation of flags:**

* `--sync-policy automated` → auto-sync on Git changes
* `--self-heal` → automatically correct drift
* `--auto-prune` → remove resources no longer in Git

---

#### **4️⃣ Synchronize & Monitor**

* Sync manually (if needed):

```bazaar
argocd app sync flask-app
```

* Check status:

```bazaar
argocd app get flask-app
```

* Watch logs/events:

```bazaar
kubectl get events -n quakewatch
kubectl logs -l app=flask-app-dev -n quakewatch
```

---

#### **5️⃣ Sync Waves (Advanced)**

To control deployment order in Helm charts, use `argocd.argoproj.io/sync-wave` annotation in your manifests:

```yaml
metadata:
  annotations:
    argocd.argoproj.io/sync-wave: "1"
```



### Monitoring with Prometheus & Grafana:

○ Prometheus Installation:
■ Deploy Prometheus into your cluster to collect metrics from
QuakeWatch and the cluster itself.
■ Configure Prometheus to scrape metrics from your application and
Kubernetes components.
Got it! Let’s outline a practical way to deploy Prometheus in your Kubernetes cluster and collect metrics from both QuakeWatch and cluster components. I’ll give you a step-by-step approach with recommended YAMLs and Helm options.

---

# **Prometheus Setup for QuakeWatch**

## **1️⃣ Install Prometheus**

The easiest way is via the official Helm chart (`prometheus-community/prometheus`):

```bash
# Add the Helm repo
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update

# Create namespace for monitoring
kubectl create namespace monitoring

# Install Prometheus in the monitoring namespace
helm install prometheus prometheus-community/prometheus \
  --namespace monitoring \
  --set alertmanager.persistentVolume.enabled=false \
  --set server.persistentVolume.enabled=false
```

> This installs Prometheus server, alertmanager, and exporters for Kubernetes metrics.

---

## **2️⃣ Expose Prometheus Server (Optional)**

For local access, you can port-forward:

```bash
kubectl port-forward svc/prometheus-server -n monitoring 9090:80
```

Then open [http://localhost:9090](http://localhost:9090) to access the Prometheus UI.

---

## **3️⃣ Configure Scraping for QuakeWatch**

Prometheus scrapes metrics from pods via **annotations** or ServiceMonitors.

### **Option A: Annotations on the Service**

If your Flask app exposes metrics (e.g., via `/metrics`):

```yaml
apiVersion: v1
kind: Service
metadata:
  name: flask-final-project-service
  namespace: quakewatch
  annotations:
    prometheus.io/scrape: "true"
    prometheus.io/port: "8000"   # or your metrics port
    prometheus.io/path: "/metrics"
spec:
  type: NodePort
  selector:
    app: flask-final-project
  ports:
    - protocol: TCP
      port: 8000
      targetPort: 8000
```

Prometheus will automatically scrape this service if configured with `kubernetes_sd_configs`.

### **Option B: Use ServiceMonitor (Recommended)**

If using the **Prometheus Operator**, create a `ServiceMonitor`:

```yaml
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: flask-service-monitor
  namespace: monitoring
spec:
  selector:
    matchLabels:
      app: flask-final-project
  endpoints:
    - port: http
      path: /metrics
      interval: 15s
```

* `path` → endpoint for metrics
* `interval` → scrape frequency

---

## **4️⃣ Scraping Cluster Metrics**

Prometheus already comes with node-exporter and kube-state-metrics. Make sure:

```bash
kubectl get pods -n monitoring
```

You should see:

* `prometheus-server`
* `kube-state-metrics`
* `node-exporter`
* `alertmanager`

These collect metrics from nodes, pods, deployments, and kube components.

---

## **5️⃣ Validate Metrics**

1. Access Prometheus UI via port-forward or ingress
2. Run queries like:

```promql
up                # Shows which targets are up
kube_pod_info     # Pod metadata
flask_request_total  # If your app exposes custom metrics
```

---

## **6️⃣ Optional: Alerting**

You can configure Prometheus alerts in `alertmanager` and tie them to Slack, email, or webhook notifications.

Example alert for high CPU on QuakeWatch pods:

```yaml
groups:
- name: quakewatch-alerts
  rules:
  - alert: HighCPUUsage
    expr: sum(rate(container_cpu_usage_seconds_total{namespace="quakewatch"}[5m])) > 0.5
    for: 5m
    labels:
      severity: critical
    annotations:
      summary: "High CPU usage in QuakeWatch"
```



○ Grafana Setup:
■ Install Grafana and connect it to Prometheus.
■ Create custom dashboards that visualize application metrics (e.g.,
CPU/memory usage, request rates, error rates) and cluster health.

Here’s a structured approach to set up **Grafana** and connect it to Prometheus, along with custom dashboards for your QuakeWatch application:

---

## **1️⃣ Install Grafana**

You have several options: Helm chart, kubectl manifests, or using a managed Grafana service. Using Helm is simplest in your cluster:

```bash
# Add Grafana Helm repo
helm repo add grafana https://grafana.github.io/helm-charts
helm repo update

# Install Grafana in monitoring namespace
helm upgrade --install grafana grafana/grafana \
  --namespace monitoring --create-namespace \
  --set adminUser=admin \
  --set adminPassword='StrongPassword123' \
  --set service.type=LoadBalancer \
  --wait
```

> This will expose Grafana with a LoadBalancer IP (or NodePort if your cluster doesn’t support LoadBalancer).

---

## **2️⃣ Access Grafana**

```bash
kubectl get svc -n monitoring
```

* Find the Grafana service (type LoadBalancer or NodePort).
* Open in browser: `http://<EXTERNAL-IP>:3000`
* Login with:

  * **User:** admin
  * **Password:** the one you set (`StrongPassword123`)

---

## **3️⃣ Connect Grafana to Prometheus**

1. Go to **Configuration → Data Sources → Add Data Source**
2. Select **Prometheus**
3. Set URL to your Prometheus service, e.g.:

```text
http://prometheus-operated.monitoring.svc.cluster.local:9090
```

4. Click **Save & Test** → should succeed

---

## **4️⃣ Create Dashboards**

### **Basic Panels to Monitor QuakeWatch**

* **CPU/Memory Usage:**

  * Query for your Flask pods:

```promql
sum(rate(container_cpu_usage_seconds_total{namespace="quakewatch", pod=~"flask-app-.*"}[1m])) by (pod)
sum(container_memory_usage_bytes{namespace="quakewatch", pod=~"flask-app-.*"}) by (pod)
```

* **Request Rates / Error Rates:**

  * If your app exposes metrics via **Prometheus client** (`/metrics` endpoint):

```promql
sum(rate(http_requests_total{namespace="quakewatch"}[1m])) by (status)
sum(rate(http_requests_total{namespace="quakewatch", status=~"5.."}[1m])) by (pod)
```

* **Cluster Health:**

  * Node CPU:

```promql
sum(rate(node_cpu_seconds_total{mode!="idle"}[1m])) by (instance)
```

* Node Memory:

```promql
node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes * 100
```

---

## **5️⃣ Optional: Import Pre-made Dashboards**

Grafana provides dashboards for Kubernetes and Prometheus metrics:

* Go to **Dashboards → Manage → Import**
* Use Dashboard IDs:

  * Kubernetes cluster monitoring: `6417`
  * Node Exporter Full: `1860`

---

## **6️⃣ Automate with Helm / GitOps**

If you want Grafana deployed automatically via ArgoCD:

1. Add Grafana Helm chart to your repo as an app.
2. Configure `values.yaml` for:

```yaml
adminUser: admin
adminPassword: YOUR_SECRET
service:
  type: ClusterIP
datasources:
  datasources.yaml:
    apiVersion: 1
    datasources:
    - name: Prometheus
      type: prometheus
      url: http://prometheus-operated.monitoring.svc.cluster.local:9090
      access: proxy
```

3. ArgoCD will sync Grafana + dashboards automatically.

---

If you want, I can create a **ready-to-use `values-grafana.yaml`** for Helm with QuakeWatch dashboards preconfigured, so you can just deploy via ArgoCD.

Do you want me to do that?


○ Alerting:
■ Configure alerting rules in Prometheus to notify you when critical
issues arise (e.g., high error rates or pod failures).

○ Documentation:
■ Document the Prometheus and Grafana setup along with sample
dashboards and alerting configurations.

Deliverables:
● ArgoCD configuration files and a documented guide for GitOps deployment.
● Prometheus and Grafana configuration manifests (or Helm charts) along with
sample dashboards.
● Documentation on the GitOps and monitoring setup, including screenshots of
dashboards and descriptions of alerting rules.
● Git repository with all the code