pipeline {
    agent any

    environment {
        DOCKER_REGISTRY = "maskeddevil"  // Replace with your Docker Hub username
        DOCKER_IMAGE_NAME = "assignment-2"              // Replace with your desired image name
        DOCKER_IMAGE_TAG = "${BUILD_NUMBER}"         // Using Jenkins build number as tag, can be Git commit hash too
        // Removed REMOTE_SERVER_* variables as deploying locally
        REMOTE_DEPLOY_PATH = "/tmp/assignment-2-deploy"      // Path on the Jenkins agent where you deploy (e.g., /tmp/flask-app-deploy, can be adjusted)
        COMPOSE_FILE_NAME = "docker-compose.yml"   // Name of your docker-compose file in the repo
    }

    stages {
        stage('Checkout Code') {
            steps {
                git credentialsId: 'git-credentials-id',  // Replace with your Git credentials ID in Jenkins
                    url: 'https://github.com/masked-devil/assignment-2',        // Replace with your Git repository URL
                    branch: 'main'                         // Or your desired branch
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    dockerImage = docker.build("${DOCKER_REGISTRY}/${DOCKER_IMAGE_NAME}:${DOCKER_IMAGE_TAG}")
                }
            }
        }

        stage('Run Tests') {
            steps {
                script {
                    docker.image("${DOCKER_REGISTRY}/${DOCKER_IMAGE_NAME}:${DOCKER_IMAGE_TAG}").inside() { // Basic inside() call - no dir parameter
                        sh 'pwd'
                        sh 'ls -al'
                        sh 'echo "Inside Docker Container!"' // Simple test command
                    }
                }
            }
        }

        stage('Push Image to Docker Hub') {
            when {
                expression { return currentBuild.result == 'SUCCESS' } // Only run if previous stages were successful
            }
            steps {
                script {
                    docker.withRegistry('https://index.docker.io/v1/', 'dockerhub-credentials-id') { // Replace with your Docker Hub credentials ID
                        dockerImage.push()
                    }
                }
            }
        }

        stage('Deploy Application') {
            when {
                expression { return currentBuild.result == 'SUCCESS' } // Only run if previous stages were successful
            }
            steps {
                script {
                    sh """
                        mkdir -p ${REMOTE_DEPLOY_PATH}  # Create deploy path if it doesn't exist locally
                        cd ${REMOTE_DEPLOY_PATH}
                        docker-compose pull # Still good practice to pull, though image may already be locally available
                        docker-compose up -d
                        echo "Application deployed locally on Jenkins agent successfully!"
                    """
                }
            }
        }
    }

    post {
        always {
            cleanWs() // Clean workspace after each build
        }
        failure {
            echo 'Pipeline failed :('
            // Add failure notifications here (email, Slack, etc.) if needed
        }
        success {
            echo 'Pipeline completed successfully!'
            // Add success notifications here if needed
        }
    }
}