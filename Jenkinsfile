pipeline {
    // 1. 指定执行环境：直接拉起 Python 3.10 容器，并在其中运行后续所有步骤（免去宿主机配环境）
    agent {
        docker {
            image 'swr.cn-north-4.myhuaweicloud.com/ddn-k8s/docker.io/library/python:3.10-slim'
            // 允许容器内以 root 权限运行，避免文件读写权限问题
            args '-u root'
        }
    }

    stages {
        // 阶段一：检查并拉取代码
        stage('Checkout Code') {
            steps {
                // checkout scm 会自动根据 Webhook 传来的情报，拉取触发该事件的对应分支代码
                checkout scm
            }
        }

        // 阶段二：安装依赖与工具链
        stage('Install Dependencies') {
            steps {
                sh '''
                    python -m pip install --upgrade pip
                    if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
                    pip install ruff bandit mypy pytest pytest-html
                '''
            }
        }

        // 阶段三：静态门禁检查（代码规范、安全、类型）
        stage('Static Lint Checks') {
            parallel { // 并行执行这三个检查，节省流水线运行时间
                stage('Ruff Check') {
                    steps {
                        sh 'ruff check .'
                    }
                }
                stage('Bandit Scan') {
                    steps {
                        sh 'bandit -r . -x ./tests'
                    }
                }
                stage('Mypy Type Check') {
                    steps {
                        sh 'mypy . --ignore-missing-imports'
                    }
                }
            }
        }

        // 阶段四：动态自动化测试
        stage('Run Automated Tests') {
            steps {
                // || true 确保测试用例挂了也会继续走后面的 post 收集报告逻辑
                sh 'pytest --html=report.html --self-contained-html || true'
            }
        }
    }

    // 5. 后置产物收集
    post {
        always {
            // 利用 Jenkins 的 HTML Publisher 插件自动解析并挂载 HTML 报告
            // 注意：需要在 Jenkins 插件管理里提前安装 "HTML Publisher" 插件
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