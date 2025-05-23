pipeline {
    agent any

    environment {
        DOCKER_IMAGE_NAME = 'substobeme/spe_project'
        GITHUB_REPO_URL = 'https://github.com/substobeme/spe_project.git'
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: "${GITHUB_REPO_URL}"
            }
        }

        stage('Build Docker Images') {
            steps {
                script {
                    sh "docker build -t ${DOCKER_IMAGE_NAME}:training -f Dockerfile.training ."
                    sh "docker build -t ${DOCKER_IMAGE_NAME}:recognition -f Dockerfile.recognition ."
                    sh "docker build -t ${DOCKER_IMAGE_NAME}:frontend -f Dockerfile.frontend ."
                }
            }
        }

        stage('Push Docker Images') {
            steps {
                script {
                    docker.withRegistry('', 'mydocker') {
                        sh "docker push ${DOCKER_IMAGE_NAME}:training"
                        sh "docker push ${DOCKER_IMAGE_NAME}:recognition"
                        sh "docker push ${DOCKER_IMAGE_NAME}:frontend"
                    }
                }
            }
        }

        stage('Deploy with Ansible (Local)') {
            steps {
                sh 'ansible-playbook -i inventory.ini deploy.yml'
            }
        }
    }
}
