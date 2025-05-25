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
      def workspace = env.WORKSPACE

      sh "mkdir -p ${workspace}/ansible-logs"

      // Remove old containers if any
      sh "docker rm -f loki || true"
      sh "docker rm -f promtail || true"

      // Start Loki container
      sh """
        docker run -d --name loki -p 3100:3100 \
          -v ${workspace}/loki-config.yaml:/etc/loki/local-config.yaml \
          grafana/loki:2.8.2 \
          -config.file=/etc/loki/local-config.yaml
      """

      // Start Promtail container mounting ansible-logs and config
      sh """
        docker run -d --name promtail \
          -v ${workspace}/ansible-logs:/ansible-logs:ro \
          -v ${workspace}/promtail-config.yaml:/etc/promtail/config.yaml \
          --network host \
          grafana/promtail:2.8.2 \
          -config.file=/etc/promtail/config.yaml
      """

      // Run ansible playbook and output logs into monitored folder
      sh "ansible-playbook -i ${workspace}/inventory.ini ${workspace}/deploy.yml | tee ${workspace}/ansible-logs/deploy.log"
    }
            }
        }
    }
}
