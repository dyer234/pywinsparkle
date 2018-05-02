pipeline {
  agent {
    node {
      label 'ubuntu docker 1'
    }

  }
  stages {
    stage('build') {
      steps {
        sh '''cd BuildScripts;





./create_wheels.sh'''
      }
    }
  }
}