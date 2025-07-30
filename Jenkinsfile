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
                script{
                    //For Unix-like systems
                    if (isUnix()) {
                        sh 'python3 -m venv venv'
                        sh 'source venv/bin/activate'
                        sh 'pip install --upgrade pip'
                        sh 'pip install -r requirements.txt'
            }
                    //For Windows systems
                    else {
                        bat 'python -m venv venv'
                        bat 'call venv \\Scripts\\activate'
                        bat 'python -m pip install --upgrade pip'
                        bat 'pip install -r requirements.txt'
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
