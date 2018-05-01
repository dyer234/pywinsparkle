pipeline {
  agent any
  stages {
    stage('build') {
      steps {
        sh 'BuildScripts/create_wheels.sh'
      }
    }
  }
}