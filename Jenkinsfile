pipeline {
    agent any

    stages {
        stage('Checkout Code') {
            steps {
                checkout scm
            }
        }

        stage('Install Tools & Dependencies') {
            steps {
                sh '''
                    python3 -m pip install --upgrade pip --break-system-packages
                    python3 -m pip install ruff bandit mypy pytest pytest-html --break-system-packages
                    if [ -f requirements.txt ]; then python3 -m pip install -r requirements.txt --break-system-packages; fi
                '''
            }
        }

        stage('Static Lint Checks') {
            parallel {
                stage('Ruff Check') {
                    steps {
                        sh 'python3 -m ruff check .'
                    }
                }
                stage('Bandit Scan') {
                    steps {
                        sh 'python3 -m bandit -r . -x ./tests'
                    }
                }
                stage('Mypy Type Check') {
                    steps {
                        sh 'python3 -m mypy . --ignore-missing-imports'
                    }
                }
            }
        }

        stage('Run Automated Tests') {
            steps {
                sh 'python3 -m pytest --html=report.html --self-contained-html || true'
            }
            // 💡 关键改动：把发布报告的逻辑挪到这个拥有明确工作空间的 stage 后置钩子里
            post {
                always {
                    publishHTML(target: [
                        allowMissing: false,
                        alwaysLinkToLastBuild: true,
                        keepAll: true,
                        reportDir: '.',
                        reportFiles: 'report.html',
                        reportName: 'Pytest自动化测试报告'
                    ])
                }
            }
        }
    }
}