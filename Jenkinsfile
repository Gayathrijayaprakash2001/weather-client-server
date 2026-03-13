pipeline {
    agent any

    stages {

        stage('Clone Repository') {
            steps {
                git 'https://github.com/Gayathrijayaprakash2001/weather-client-server.git'
            }
        }

        stage('Build travel-agent image') {
            steps {
                sh 'docker build -t travel-agent ./travel-agent'
            }
        }

        stage('Build weather-mcp image') {
            steps {
                sh 'docker build -t weather-mcp ./weather-mcp'
            }
        }

        stage('Test Stage') {
            steps {
                echo "Running tests..."
            }
        }
    }
}