# ServMine Pet Project

Welcome to **ServMine**! This is a web application for a Minecraft game server featuring a custom authentication system, news feed, user reviews, services store, and automated test coverage.

The entire project is fully containerized using **Docker** and **Docker Compose**, allowing you to spin up the full infrastructure (Backend, Frontend, Database) with a single command.

---

## 🛠 Tech Stack

* **Frontend:** React.js
* **Backend:** Python (FastAPI, SQLAlchemy)
* **Database:** PostgreSQL 15
* **QA & Automation:** Python 3.11+, Pytest, Playwright (E2E & Visual Regression testing), Allure Reports
* **DevOps & CI/CD:** Docker, Docker Compose, GitHub Actions

---

## 📋 Prerequisites

Ensure you have the following installed on your system:
* [Docker Desktop](https://www.docker.com/products/docker-desktop/) (with Docker Compose V2 support)
* [Git](https://git-scm.com/)
* [Python 3.11+](https://www.python.org/) *(for running automated tests locally)*

---

## 🚀 Quick Start

### Step 1. Clone the repository

Download the project to your local machine and navigate into its directory:

```bash
git clone [https://github.com/voltmen/ServMine-pet-project.git](https://github.com/voltmen/ServMine-pet-project.git)
cd ServMine-pet-project 
```

---

### Step 2. Environment Configuration (.env)
Create a .env file based on the provided template:

```Bash
cp .env.example .env
(or manually copy the contents of .env.example into a new .env file in the root directory)

💡 Note: All default values in .env.example are pre-configured for seamless local execution via Docker.
```

---

### Step 3. Launch Services
Build and run all containers with a single command:

```Bash
docker compose up -d --build
🌐 Application Services Access:

Frontend: http://localhost:3000

Backend API (Swagger Docs): http://localhost:8000/docs
```

---

### 🧪 QA Automation Framework
The project is covered with automated E2E tests and visual regression checks for key user journeys and payment gateway integrations.

### 📍 Running Tests Locally

1. **Install testing dependencies:**
   ```bash
   pip install -r tests/requirements.txt
   playwright install --with-deps

### Execute Pytest and generate Allure results:

```Bash 
pytest tests/ --alluredir=allure-results --clean-alluredir
```

### Serve and view the Allure report in your browser:
```Bash 
allure serve allure-results
```

### ⚙️ CI/CD Integration: Automated tests are triggered automatically on every push or pull_request to the main branch via GitHub Actions, ensuring code stability prior to release.