### Phase 3: Automation - Package Management, Version
Control & CI/CD
Objective:
Phase 3 focuses on automating the deployment process and improving version control
practices. You will create Helm charts, set up Git repositories, and implement CI/CD pipelines
using GitHub Actions.
Tasks:
1. Package Management with Helm:
○ Create a Helm chart for your Kubernetes application.
```bazaar
helm create flask-chart
```
○ Publish the Helm chart to an artifact repository.
```bazaar
helm package flask-chart

# You can run this anywhere
helm repo add mycharts https://anastasiya315510.github.io/flask-chart
helm repo update

# Install the chart
helm install flask-app mycharts/flask-chart


mkdir -p docs
mv flask-chart-1.0.0.tgz docs/
cd docs
helm repo index . --url https://anastasiya315510.github.io/flask-chart
git add docs/
git commit -m "Add Helm chart package and index"
git push origin main

helm install flask-app mycharts/flask-chart


```
2. Version Control with Git:
○ Set up a Git repository for your project.
○ Create multiple branches and demonstrate common Git workflows.
○ Resolve conflicts and manage pull requests.
3. CI/CD Pipeline:
○ Use GitHub Actions to create a CI/CD pipeline.
○ Implement different stages in the pipeline (build, test, deploy).
○ Use matrix builds to test your application with pylint on multiple environments .

Deliverables:
● A Helm chart published to an artifact repository.
● A Git repository with a clear branching strategy and documented workflows.
● A working CI/CD pipeline configured in GitHub Actions.