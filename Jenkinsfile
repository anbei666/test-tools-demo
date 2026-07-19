pipeline {
    agent any

    stages {
        stage('Checkout Code') {
            steps {
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                // 此时 python3 已经是容器原生自带的了，直接装依赖包
                sh '''
                    python3 -m pip install --upgrade pip --break-system-packages
                    python3 -m pip install ruff bandit mypy pytest pytest-html --break-system-packages
                '''
            }
        }

        stage('Static Lint Checks') {
            parallel {
                stage('Ruff Check') { steps { sh 'python3 -m ruff check .' } }
                stage('Bandit Scan') { steps { sh 'python3 -m bandit -r . -x ./tests' } }
                stage('Mypy Type Check') { steps { sh 'python3 -m mypy . --ignore-missing-imports' } }
            }
        }

        stage('Run Automated Tests') {
            steps {
                sh 'python3 -m pytest --html=report.html --self-contained-html || true'
            }
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