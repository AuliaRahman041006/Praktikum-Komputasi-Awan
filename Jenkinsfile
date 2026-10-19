pipeline {
    agent any

    environment {
        IMAGE_NAME           = 'aulia041006/simple-app'
        REGISTRY_CREDENTIALS = 'dockerhub-credentials'
        TAG                  = "${BUILD_NUMBER}"
    }

    stages {
        stage('Checkout') {
            steps { checkout scm }
        }

        stage('Build') {
            steps { bat 'echo Build di Windows, build ke-%BUILD_NUMBER%' }
        }

        stage('Build Docker Image') {
            steps {
                bat(returnStatus: true, script: 'docker logout')
                bat 'docker build -t %IMAGE_NAME%:%BUILD_NUMBER% .'
            }
        }

        stage('Push Docker Image') {
            steps {
                withCredentials([usernamePassword(credentialsId: REGISTRY_CREDENTIALS,
                                                  usernameVariable: 'DH_USER',
                                                  passwordVariable: 'DH_PASS')]) {
                    bat 'echo %DH_PASS%| docker login -u %DH_USER% --password-stdin'
                    bat 'docker push %IMAGE_NAME%:%BUILD_NUMBER%'
                    bat 'docker tag %IMAGE_NAME%:%BUILD_NUMBER% %IMAGE_NAME%:latest'
                    bat 'docker push %IMAGE_NAME%:latest'
                }
            }
        }

        stage('Deploy App + Database') {
            steps { bat 'docker compose -p praktikum up -d --build' }
        }
    }

    post {
        always {
            bat(returnStatus: true, script: 'docker logout')
            echo 'Selesai build'
        }
    }
}
