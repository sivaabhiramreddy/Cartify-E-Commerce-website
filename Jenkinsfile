pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                sh 'pip3 install -r requirements.txt'
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