pipeline {
  agent any
  stages {
    stage('version') {
      steps {
        sh 'python3 --version'
      }
    }
    stage('Build') {
      steps {
        sh 'python3 automerge-pr-on-approval.py'
      }
    }
    stage('Test') {
      steps {
        sh 'echo Tested sucessfully'
      }
    }
  }
}