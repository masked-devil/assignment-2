pipeline {
    agent any

    environment {
        DOCKER_REGISTRY = "maskeddevil"  //Docker Hub username
        DOCKER_IMAGE_NAME = "assignment-2"              //image name
        DOCKER_IMAGE_TAG = "${BUILD_NUMBER}"         // Using Jenkins build number as tag
        REMOTE_DEPLOY_PATH = "/tmp/assignment-2-deploy"      // Path  where you deploy 
        COMPOSE_FILE_NAME = "docker-compose.yml"   // Name of docker-compose file in the repo
    }

    stages {
        stage('Checkout Code') {
            steps {
                git credentialsId: 'git-credentials-id',  //Git credentials ID in Jenkins
                    url: 'https://github.com/masked-devil/assignment-2',        //Git repository URL
                    branch: 'main'                         // Branch
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
                    docker.image("${DOCKER_REGISTRY}/${DOCKER_IMAGE_NAME}:${DOCKER_IMAGE_TAG}").inside {
                        sh 'pip install -r requirements.txt' // Install app dependencies (adjust if needed)
                        sh 'pytest'                         // Run your unit tests (adjust command if needed)
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
                    docker.withRegistry('https://index.docker.io/v1/', 'dockerhub-credentials-id') { //Docker Hub credentials ID
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
                    sshagent (credentials: ['remote-server-credentials-id']) { //remote server SSH credentials ID
                        sh """
                            ssh -o StrictHostKeyChecking=no ${REMOTE_SERVER_USERNAME}@${REMOTE_SERVER_HOST} << EOF
                                cd ${REMOTE_DEPLOY_PATH}
                                docker-compose pull
                                docker-compose up -d
                                echo "Application deployed successfully!"
                            EOF
                        """
                    }
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

        }
        success {
            echo 'Pipeline completed successfully!'

        }
    }
}