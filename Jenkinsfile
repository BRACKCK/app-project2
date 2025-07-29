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
                sh '''
                    python3 -m venv venv
                    source venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                    pip install pytest pytest-benchmark flake8
                '''
            }
        }

        stage('Functional Tests') {
            steps {
                sh '''
                    source venv/bin/activate
                    coverage run -m unittest discover -s . -p 'test_*.py'
                    coverage report
                '''
            }
        }

        stage('Performance Benchmark') {
            steps {
                sh '''
                    source venv/bin/activate
                    pytest test_perf.py --benchmark-only
                '''
            }
        }

        stage('Linting (Maintainability)') {
            steps {
                sh '''
                    source venv/bin/activate
                    flake8 . --exit-zero --max-line-length=100
                '''
            }
        }
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

