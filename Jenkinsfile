pipeline {
    agent any 

    environment {
        DB_USER = credentials('db_user') // Assume you have these set up in Jenkins credentials
        DB_PASSWORD = credentials('db_password')
        POSTGRES_DB = 'myapp'
        MAIL_USERNAME = credentials('gopalvish@supporthives.com')
        MAIL_PASSWORD = credentials('7kR&CQY%PN')
        REDIS_HOST = 'redis'
    }

    stages {
        stage('Build') {
            steps {
                script {
                    // Clean previous builds
                    sh 'docker-compose down'
                    // Build the Docker images
                    sh 'docker-compose build'
                }
            }
        }
        stage('Test') {
            steps {
                script {
                    // Run your tests here
                    echo 'Running tests...'
                }
            }
        }
        stage('Deploy') {
            steps {
                script {
                    // Start the application
                    sh 'docker-compose up -d'
                }
            }
        }
    }

    post {
        success {
            echo 'Deployment was successful!'
        }
        failure {
            echo 'Deployment failed!'
        }
        always {
            cleanWs() // Clean up the workspace
        }
    }
}

