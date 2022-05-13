 stages {
   stage("SonarQube Analysis") {
      agent any
      steps {
        script {
            def scannerHome = tool 'SonarQube Scanner 2.8';
            withSonarQubeEnv("foo") {
              sh "${scannerHome}/bin/sonar-scanner"
            }
        }
      }
    }
