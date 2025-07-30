pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/BRACKCK/app-project2.git'
            }
        }

        stage('Set up Python') {
            steps {
                bat '''
                    python -m venv venv
                    call venv\\Scripts\\activate
                    python -m pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Functional Tests') {
            steps {
                bat '''
                    call venv\\Scripts\\activate
                    coverage run -m unittest discover -s tests -p "test_*.py"
                    coverage report
                '''
            }
        }

        stage('Performance Test') {
            steps {
                bat '''
                    call venv\\Scripts\\activate
                    set PYTHONPATH=%cd%
                    pytest tests/test_perf.py -v
                '''
            }
        }

        stage('Linting (Maintainability)') {
            steps {
                bat '''
                    call venv\\Scripts\\activate
                    flake8 . --exit-zero --max-line-length=100
                '''
            }
        }

        stage('Run UI Tests with Selenium') {
            steps {
                bat '''
                    call venv\\Scripts\\activate
                    start /B flask run
                    timeout /T 5 >nul
                    pytest tests/test_ui_selenium.py
                '''
            }
        }
    }

    post {
        always {
            echo 'Cleaning up workspace...'
        }
        success {
            echo 'Pipeline completed successfully!'
        }
        failure {
            echo 'Pipeline failed. Please check the logs for error.'
        }
    }
}