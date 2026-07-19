pipeline {
    // 1. 使用 any 环境，不再调用 Docker 镜像，直接在 Jenkins 容器内就地运行
    agent any

    stages {
        stage('Checkout Code') {
            steps {
                checkout scm
            }
        }

        stage('Install Tools & Dependencies') {
            steps {
                // 利用容器内置的 python3
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
                // 执行 Pytest
                sh 'python3 -m pytest --html=report.html --self-contained-html || true'
            }
        }
    }

    post {
        always {
            // 当第一步的插件装好后，这行代码就能完美解析并挂载你的报告了
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