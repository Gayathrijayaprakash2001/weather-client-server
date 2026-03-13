pipeline {
agent any

```
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
            bat 'docker build -t weather-mcp -f weather-mcp/Dockerfile ./weather-mcp'
        }
    }

    stage('Test Stage') {
        steps {
            echo "Running tests..."
        }
    }

}
```

}
