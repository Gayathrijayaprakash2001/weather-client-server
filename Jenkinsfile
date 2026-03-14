// pipeline {
//     agent any

//     triggers {
//         githubPush()
//     }

//     stages {
//         stage('Clone Repository') {
//             steps {
//                 git 'https://github.com/Gayathrijayaprakash2001/weather-client-server.git'
//             }
//         }

//         stage('Build travel-agent image') {
//             steps {
//                 bat 'docker build -t travel-agent -f travel-agent/Dockerfile.agent ./travel-agent'
//             }
//         }

//         stage('Build weather-mcp image') {
//             steps {
//                 bat 'docker build -t weather-mcp -f weather-mcp/Dockerfile ./weather-mcp'
//             }
//         }

//         stage('Run Containers') {
//             steps {
//                 bat 'docker run -d -p 8000:8000 --name weather-mcp weather-mcp'
//                 bat 'docker run -d --name travel-agent travel-agent'
//             }
//         }

//         stage('Test Stage') {
//             steps {
//                 echo "Running tests..."
//             }
//         }
//     }
// }

pipeline {
    agent any

    stages {

        stage('Clone Repository') {
            steps {
                git branch: 'main', url: 'https://github.com/Gayathrijayaprakash2001/weather-client-server.git'
            }
        }

        stage('Build travel-agent image') {
            steps {
                bat 'docker build -t travel-agent -f travel-agent/Dockerfile.agent ./travel-agent'
            }
        }

        stage('Build weather-mcp image') {
            steps {
                bat 'docker build -t weather-mcp ./weather-mcp'
            }
        }

        stage('Run Containers') {
            steps {
                bat 'docker run -d -p 8000:8000 --name weather-mcp weather-mcp'
                bat 'docker run -d --name travel-agent travel-agent'
            }
        }

        stage('Test Stage') {
            steps {
                echo "Running tests..."
            }
        }
    }
}