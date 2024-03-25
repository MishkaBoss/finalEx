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
                        sh 'docker rmi -f final-ex-todo-app'
                    }
                }
        sh 'docker build -t final-ex-todo-app ./finalEx'
            }
        }
        stage('Login to Docker Hub') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerHubCredentials', passwordVariable: 'DOCKER_HUB_PASSWORD', usernameVariable: 'DOCKER_HUB_USERNAME')]) {
                    sh 'docker login -u $DOCKER_HUB_USERNAME -p $DOCKER_HUB_PASSWORD'
                }
            }
        }
        stage('Push image to docker hub') {
            steps {
                sh 'docker tag final-ex-todo-app:latest devoops93/todo-app:v${BUILD_NUMBER}'
                sh 'docker push devoops93/todo-app:v${BUILD_NUMBER}'
            }
        }

        // stage('Connect to EC2 ') {
        //     steps {
        //         sshagent(['ec2-ssh']) 
        //     }
        // }
        stage('Pull image from docker hub') {
            steps {
                sh 'docker pull devoops93/todo-app:v${BUILD_NUMBER}'
            }
        }

        stage('Run docker container') {
             steps {
                script {
                    def containerExists = sh(script: 'docker ps -a -q -f "publish=5000"', returnStdout: true).trim()
                    if (containerExists) {
                        sh 'docker stop $(containerExists)'
                        sh 'docker remove $(containerExists)'
                        // sh 'docker stop $(docker ps -a -q -f "publish=5000")'
                        // sh 'docker rm $(docker ps -a -q -f "publish=5000")'
                    }
                }
                sh 'docker run -d -p 5000:5000 devoops93/todo-app:v${BUILD_NUMBER}'
            }
        }

    }
}