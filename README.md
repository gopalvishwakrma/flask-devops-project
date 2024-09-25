# DevOps Project Showcase

## Docker + Flask + NGINX + Jenkins on AlmaLinux

This project demonstrates a robust DevOps pipeline using Docker, Flask, NGINX, and Jenkins, deployed on AlmaLinux. It's designed to showcase the skills of a DevOps fresher in containerization, web development, reverse proxy configuration, and continuous integration/continuous deployment (CI/CD).

![Project Architecture](assets/project_architecture.png)

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Project Structure](#project-structure)
3. [Setup and Installation](#setup-and-installation)
4. [Running the Application](#running-the-application)
5. [CI/CD with Jenkins](#cicd-with-jenkins)
6. [Monitoring and Logging](#monitoring-and-logging)
7. [Troubleshooting](#troubleshooting)
8. [Future Improvements](#future-improvements)

## Prerequisites

- AlmaLinux 8 or later
- Docker and Docker Compose
- Git
- Jenkins

## Project Structure

```
.
├── app.py
├── docker-compose.yaml
├── Dockerfile
├── nginx.conf
├── requirements.txt
└── templates
    └── index.html
```

## Setup and Installation

### 1. Install Docker and Docker Compose

```bash
sudo dnf config-manager --add-repo=https://download.docker.com/linux/centos/docker-ce.repo
sudo dnf install docker-ce docker-ce-cli containerd.io docker-compose-plugin
sudo systemctl start docker
sudo systemctl enable docker
```

### 2. Install Git

```bash
sudo dnf install git
```

### 3. Clone the Repository

```bash
git clone https://github.com/your-username/devops-project-showcase.git
cd devops-project-showcase
```

### 4. Set Up Environment Variables

Create a `.env` file in the project root:

```bash
DB_USER=admin
DB_PASSWORD=admin
POSTGRES_DB=myapp
REDIS_HOST=redis
MAIL_USERNAME=your-email@example.com
MAIL_PASSWORD=your-email-password
```

## Running the Application

1. Build and start the containers:

```bash
docker-compose up -d --build
```

2. Check the status of the containers:

```bash
docker-compose ps
```

![Docker Compose Status](assets/docker_compose_status.png)

3. Access the application at `http://your-server-ip:8082`

![Application Screenshot](assets/application_screenshot.png)

## CI/CD with Jenkins

### Setting up Jenkins

1. Install Jenkins on AlmaLinux:

```bash
sudo wget -O /etc/yum.repos.d/jenkins.repo https://pkg.jenkins.io/redhat-stable/jenkins.repo
sudo rpm --import https://pkg.jenkins.io/redhat-stable/jenkins.io.key
sudo dnf install jenkins
sudo systemctl start jenkins
sudo systemctl enable jenkins
```

2. Access Jenkins at `http://your-server-ip:8080` and complete the setup

### Creating a Jenkins Pipeline

1. Create a new Jenkins Pipeline job
2. Configure the pipeline to use the Jenkinsfile in your repository
3. Set up webhook in your Git repository to trigger the Jenkins job on push

![Jenkins Pipeline](assets/jenkins_pipeline.png)

### Jenkins Build Status

![Jenkins Status](assets/jenkins_status.png)

## Monitoring and Logging

### Viewing Logs

To view logs for a specific service:

```bash
docker-compose logs -f service_name
```

### Monitoring Container Health

```bash
docker-compose ps
```

## Troubleshooting

- If the application is not accessible, check NGINX logs:

```bash
docker-compose logs nginx
```

- For database connection issues, verify PostgreSQL logs:

```bash
docker-compose logs db
```

## Future Improvements

1. Implement Prometheus and Grafana for advanced monitoring
2. Add unit and integration tests to the CI/CD pipeline
3. Implement blue-green deployment strategy
4. Set up ELK stack for centralized logging

---

This project was created by Gopal Vishwakarma, a passionate DevOps fresher. For any questions or collaborations, please reach out at gopalvish@supporthives.com.
