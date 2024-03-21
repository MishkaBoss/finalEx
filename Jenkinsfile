pipeline {
    agent any
    parameters {
        string defaultValue: 'https://github.com/MishkaBoss/finalEx.git', 
        name: 'REPO_URL'
    }
    stages {
        stage('git clone') {
            steps {
                sh 'rm -rf finalEx'
                sh "git clone ${REPO_URL}"
            }
        }
        stage('Delete previous image if exists and build docker image') {
            steps {
                script {
                    def imageExists = sh(script: 'docker images -q final-ex-todo-app', returnStdout: true).trim()
                    if (imageExists) {
                        sh 'docker rmi final-ex-todo-app'
                    }
                }
        sh 'docker build -t final-ex-todo-app ./finalEx'
            }
        }

        stage('Run docker container') {
            steps {
                sh 'docker run -d -p 5000:5000 final-ex-todo-app'
            }
        }

    }
}