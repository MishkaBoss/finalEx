pipeline {
    agent any
    parameters {
        string defaultValue: 'https://github.com/MishkaBoss/finalEx.git', 
        name: 'REPO_URL'
    }
    stages {
        stage('Clone GitHub repository') {
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
        stage('Run docker container locally') {
            steps {
                script {
                    def containerExists = sh(script: 'docker ps -a -q -f "publish=5000"', returnStdout: true).trim()
                    if (containerExists) {
                        sh 'docker stop $(containerExists)'
                        sh 'docker remove $(containerExists)'
                    }
                }
                sh 'docker run -d -p 5000:5000 final-ex-todo-app'
            }
        }
        stage('curl test') {
            steps {
                timeout(time: 10, unit: 'SECONDS') {
                    sh 'curl -f http://localhost:5000'
                }
            }
        }
        stage('Stop and remove local container') {
            steps {
                        sh 'docker stop final-ex-todo-app'
                        sh 'docker remove final-ex-todo-app'
                }
            }
        stage('Login to Docker Hub') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerHubCredentials', passwordVariable: 'DOCKER_HUB_PASSWORD', usernameVariable: 'DOCKER_HUB_USERNAME')]) {
                    sh 'docker login -u $DOCKER_HUB_USERNAME -p $DOCKER_HUB_PASSWORD'
                }
            }
        }
        stage('Tag image') {
            steps {
                sh 'docker tag final-ex-todo-app:latest devoops93/todo-app:latest'
            }
        }
        stage('Push image to Docker Hub') {
            steps {
                sh 'docker push devoops93/todo-app:latest'
            }
        }
        stage('test') {
            steps {
                script {
                    dir('/var/lib/jenkins/workspace/terraform') {
                        def public_ip = sh(script: 'terraform output public_ip', returnStdout: true).trim()
                        echo "The public IP is: ${public_ip}"
                    }
                }   
                 
            }
        }

    }
}