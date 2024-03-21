pipeline {
    agent any
    parameters {
        string defaultValue: 'https://github.com/MishkaBoss/finalEx.git', 
        name: 'REPO_URL'
    }
    stages {
        stage('git clone') {
            steps {
                sh 'rm -rf summaryEx'
                sh "git clone ${REPO_URL}"
            }
        }
        stage('Delete previous image if exists and build docker image') {
            steps {
                script {
                    def imageExists = sh(script: 'docker images -q summary-ex-flask-app', returnStdout: true).trim()
                    if (imageExists) {
                        sh 'docker rmi summary-ex-flask-app'
                    }
                }
        sh 'docker build -t summary-ex-flask-app ./summaryEx'
            }
        }

        stage('Run docker dontainer') {
            steps {
                sh 'docker run -d -p 5000:5000 summary-ex-flask-app'
            }
        }

    }
}