node {
  stage('SCM') {
    checkout scm
  }
  stage('SonarQube Analysis') {
    def scannerHome = tool 's';
    withSonarQubeEnv() {
       def sonarRunner = tool name: 'SonarQubeScanner', type: 'hudson.plugins.sonar.SonarRunnerInstallation'
      sh "${scannerHome}/bin/s"
    }
  }
}
