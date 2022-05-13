node {
  stage('SCM') {
    checkout scm
  }
  stage('SonarQube Analysis') {
    def scannerHome = tool 's';
    withSonarQubeEnv() {
      sh "${scannerHome}/bin/s"
    }
  }
}
