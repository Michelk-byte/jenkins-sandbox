pipeline {
  agent { docker { image 'python:3.13-slim' } }
  options { skipDefaultCheckout(); timestamps() }   // stop the automatic checkout
  stages {
    stage('Checkout') {
      steps {
        deleteDir()            // nuke anything stale in the workspace
        checkout scm           // full clone of your repo here
      }
    }
    stage('Install deps') {
      steps {
        sh 'python --version'
        sh 'pip install --upgrade pip'
        sh 'pip install -r requirements.txt'
      }
    }
    stage('Test') {
      steps {
        sh 'pytest -q --junitxml=reports/junit.xml'
      }
      post {
        always {
          junit allowEmptyResults: true, testResults: 'reports/junit.xml'
        }
      }
    }
  }
}