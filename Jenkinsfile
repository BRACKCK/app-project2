pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                git 'https://github.com/BRACKCK/app-project2.git'
            }
        }

        stage('Set up Python') {
            steps {
                bat '''
                    python -m venv venv
                    call venv\\Scripts\\activate
                    python -m pip install --upgrade pip
                    pip install -r requirements.txt
                    pip install pytest pytest-benchmark flake8
                '''
            }
        }

        stage('Functional Tests') {
            steps {
                bat '''
                    call venv\\Scripts\\activate
                    coverage run -m unittest discover -s . -p "test_*.py"
                    coverage report
                '''
            }
        }

        stage('Performance Benchmark') {
            steps {
                bat '''
                    call venv\\Scripts\\activate
                    pytest test_perf.py --benchmark-only
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
                    pytest tests\\test_ui_selenium.py
                '''
            }
        }
    }
}
