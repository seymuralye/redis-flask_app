<h1 align="center">Redis Flask App</h1>

**Table of Contents:**

- [About The Project](#about-the-project)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Running the Application](#running-the-application)
- [Important Notification](#important-notification)
- [Contributing](#contributing)
- [Contact](#contact)

---

## About The Project

This project demonstrates a Flask-based web application that integrates with Redis for caching. It leverages **Docker Compose** to simplify deployment and configuration.

Repository Link: **[Redis Flask App](https://gitlab.com/seymuralye/redis-flask_app)**.

---

## Getting Started

Follow these steps to set up and run the application.

### Prerequisites

Ensure you have the following installed:
- **Docker**
- **Docker Compose**
- **Git**

To verify the installations, run the following commands:
```bash
docker --version
docker-compose --version
git --version
```

### Installation

Clone the repository:
```bash
git clone https://gitlab.com/seymuralye/redis-flask_app
cd redis-flask_app
```
Build and start the Docker containers:
```bash
docker-compose up -d --build
```

Verify that all containers are running:
```bash
docker-compose ps
```
You should see the following containers:
- **flask-app**
- **redis**
- **postgresql**
- **pgadmin**

### Running the Application
Restart the flask-app container to ensure proper initialization:
```bash
docker restart flask-app
```
Test the application:
```bash
curl http://localhost:5000/countries
```
- On the first request, data will be fetched from the **PostgreSQL** database.
- On subsequent requests, data will be retrieved from **Redis** for faster responses.
