pipeline {
    agent any

    triggers {
        // 💡 强行在内存注册 SCM 监听器，配合 Webhook 的 Poked 信号实现秒级自动触发
        pollSCM('') 
    }

    stages {
        stage('Checkout Code') {
            steps {
                // 动态拉取当前触发分支或 PR 虚拟合并分支的代码
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
            // 💡 双重保险：只有当环境变量中存在 PR 编号（说明是真 PR 触发）时才执行静态检查
            when {
                expression { env.CHANGE_ID != null }
            }
            parallel {
                stage('Ruff Check') { steps { sh 'python3 -m ruff check .' } }
                stage('Bandit Scan') { steps { sh 'python3 -m bandit -r . -x ./tests' } }
                stage('Mypy Type Check') { steps { sh 'python3 -m mypy . --ignore-missing-imports' } }
            }
        }

        stage('Run Automated Tests') {
            // 💡 双重保险：只有当环境变量中存在 PR 编号时才执行自动化业务测试
            when {
                expression { env.CHANGE_ID != null }
            }
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