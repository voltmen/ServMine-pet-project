# ServMine Pet Project

Ласкаво просимо до проєкту **ServMine**! Це вебдодаток для ігрового сервера Minecraft із власною системою авторизації, новинами, відгуками та магазином послуг.

Увесь проєкт повністю контейнеризований за допомогою **Docker** та **Docker Compose**, що дозволяє розгорнути всю інфраструктуру (Backend, Frontend, Database) однією командою.

---

## 🛠 Технологічний стек

* **Frontend:** React.js
* **Backend:** Python (FastAPI, SQLAlchemy)
* **Database:** PostgreSQL 15
* **DevOps:** Docker, Docker Compose

---

## 📋 Попередні вимоги

Переконайся, що на твоєму комп'ютері встановлено:
* [Docker Desktop](https://www.docker.com/products/docker-desktop/) (з підтримкою Docker Compose V2)
* [Git](https://git-scm.com/)

---

## 🚀 Швидкий запуск

### Крок 1. Клонування репозиторію

Завантажте проєкт на свій комп'ютер та перейдіть у його директорію:

```bash
git clone https://github.com/voltmen/ServMine-pet-project.git
cd ServMine-pet-project
```

---

### Крок 2. Налаштування змінного оточення (.env)
Створіть файл .env на основі готового шаблону:

```bash
cp .env.example .env
(або просто скопіюйте вміст .env.example у новий файл .env у корені проєкту)
```

💡 Примітка: Усі дефолтні значення у .env.example вже налаштовані для локальної роботи з Docker.

---

### Крок 3. Запуск та доступ до сервісів
Зберіть та запустіть усі контейнери однією командою:

```Bash
docker compose up -d --build
🌐 Доступ до додатку в браузері:

Frontend: http://localhost:3000

Backend API (Swagger Docs): http://localhost:8000/docs