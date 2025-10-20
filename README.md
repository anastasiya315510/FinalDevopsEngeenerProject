
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

## ✅ License

MIT License. Free to use for personal or commercial projects.

