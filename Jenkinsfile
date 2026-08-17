pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Test') {
            steps {
                sh 'python3 manage.py test'
            }
        }

        stage('Docker Build') {
            steps {
                sh 'docker build -t cartify .'
            }
        }
    }
}