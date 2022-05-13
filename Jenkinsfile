 stages {
   stage("SonarQube Analysis") {
      agent any
      steps {
        script {
            def scannerHome = tool 'SonarQube Scanner 2.8';
            withSonarQubeEnv("sonarserver") {
              sh "${scannerHome}/bin/sonar-scanner"
            }
        }
      }
    }
 }
