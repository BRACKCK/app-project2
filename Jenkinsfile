pipeline {
    agent any

    environment {
        // Define environment variables
        APP_NAME = "energy-advisor"
        FLASK_APP = "app.py"
        FLASK_ENV = "development"
        DATABASE_URL = "sqlite:///home_energy.db"
        PYTHON_VERSION = "3.9"
    }

     stages {
        stage('Setup Environment') {
            steps {
                echo 'Setting up the environment...'
                // Install required system dependencies
                sh 'sudo apt-get update && sudo apt-get install -y python3 python3-pip python3-venv sqlite3'
                
                // Create and activate virtual environment
                sh 'python3 -m venv venv'
                sh '. venv/bin/activate'
                
                // Install Python dependencies
                sh 'pip install -r requirements.txt'
                
                // Initialize database
                sh 'python init_db.py'
                sh 'python seed_data.py'
            }
        }

                stage('Unit Tests') {
            steps {
                echo 'Running unit tests...'
                sh '. venv/bin/activate && python -m pytest tests/unit -v --cov=app --cov-report=xml'
            }
            post {
                always {
                    // Publish test coverage report
                    publishHTML(target: [
                        allowMissing: false,
                        alwaysLinkToLastBuild: false,
                        keepAll: false,
                        reportDir: 'htmlcov',
                        reportFiles: 'index.html',
                        reportName: 'Coverage Report'
                    ])
                    junit '**/junit.xml'
                }
            }
        }


