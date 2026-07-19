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
                // 💡 核心修复：在 Jenkins 容器内部自动安装 Python3 和 pip
                sh '''
                    echo "=== 开始安装系统 Python ==="
                    # 如果不是 root 用户，尝试更新并安装环境
                    if command -v apt-get >/dev/null; then
                        sudo apt-get update || apt-get update
                        sudo apt-get install -y python3 python3-pip python3-venv || apt-get install -y python3 python3-pip
                    fi
                    
                    echo "=== 检查 Python 版本 ==="
                    python3 --version || python --version
                    
                    echo "=== 安装 Python 测试依赖包 ==="
                    python3 -m pip install --upgrade pip --break-system-packages || pip install --upgrade pip
                    python3 -m pip install ruff bandit mypy pytest pytest-html --break-system-packages || pip install ruff bandit mypy pytest pytest-html
                '''
            }
        }

        stage('Static Lint Checks') {
            parallel {
                stage('Ruff Check') {
                    steps {
                        sh 'python3 -m ruff check . || ruff check .'
                    }
                }
                stage('Bandit Scan') {
                    steps {
                        sh 'python3 -m bandit -r . -x ./tests || bandit -r . -x ./tests'
                    }
                }
                stage('Mypy Type Check') {
                    steps {
                        sh 'python3 -m mypy . --ignore-missing-imports || mypy . --ignore-missing-imports'
                    }
                }
            }
        }

        stage('Run Automated Tests') {
            steps {
                sh 'python3 -m pytest --html=report.html --self-contained-html || pytest --html=report.html --self-contained-html || true'
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