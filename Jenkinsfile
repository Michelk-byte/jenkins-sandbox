pipeline {
  agent {
    docker { image 'python:3.11-slim' }
  }
  options { timestamps() }
  stages {
    stage('Checkout') {
      steps { checkout scm }
    }
    stage('Install deps') {
      steps {
        sh 'python -V'
        sh 'pip install -r requirements.txt'
      }
    }
    stage('Test') {
      steps { sh 'pytest -q' }
      post {
        always {
          junit allowEmptyResults: true, testResults: '**/junit*.xml'
        }
      }
    }
  }
}