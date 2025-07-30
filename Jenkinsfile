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
                    pip install flake8 selenium webdriver-manager
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
                    start /B python -m flask run
                    timeout /T 10 >nul
                    pytest tests/test_ui_selenium.py -v
                    taskkill /IM "python.exe" /F
                '''
            }
        }
    }

    post {
        always {
            echo 'Cleaning up workspace...'
            bat 'taskkill /IM "python.exe" /F 2>nul || echo "No python processes to kill"'
        }
        success {
            echo 'Pipeline completed successfully!'
        }
        failure {
            echo 'Pipeline failed. Please check the logs for error.'
        }
    }
}