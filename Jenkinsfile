node {
  stage('SCM') {
    checkout scm
  }
  stage('SonarQube Analysis') {
    def scannerHome = tool 's';
    withSonarQubeEnv() {
       "C:\Users\SYS\Downloads\sonar-scanner-cli-4.7.0.2747-windows\sonar-scanner-4.7.0.2747-windows\bin\sonar-scanner.bat"
    }
  }
}
