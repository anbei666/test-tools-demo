pipeline {
    agent any

    // 💡 正确：triggers 直接作为顶层指令，与 agent、stages 并列
    triggers {
        pollSCM('')
    }

    // 💡 options 用于放置其他流水线级别的配置
    options {
        timeout(time: 1, unit: 'HOURS')
    }

    stages {
        stage('Checkout Code') {
            steps {
                // 这里的 checkout scm 会自动使用任务配置中的 Git 仓库
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                    python3 -m pip install --upgrade pip --break-system-packages
                    python3 -m pip install ruff bandit mypy pytest pytest-html --break-system-packages
                '''
            }
        }

        stage('Static Lint Checks') {
            when { expression { env.CHANGE_ID != null } }
            parallel {
                stage('Ruff Check') { steps { sh 'python3 -m ruff check .' } }
                stage('Bandit Scan') { steps { sh 'python3 -m bandit -r . -x ./tests' } }
                stage('Mypy Type Check') { steps { sh 'python3 -m mypy . --ignore-missing-imports' } }
            }
        }

        stage('Run Automated Tests') {
            when { expression { env.CHANGE_ID != null } }
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
    // 💡 删除了多余的 post 块，状态上报让插件自动完成即可
}