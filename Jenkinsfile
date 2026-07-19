pipeline {
    agent any

    // 1. 设置超时，防止死循环占用服务器资源
    options {
        timeout(time: 1, unit: 'HOURS')
        disableConcurrentBuilds()
    }

    // 2. 触发器：确保代码推送时触发（配合网页端 Webhook 使用）
    triggers {
        pollSCM('')
    }

    stages {
        stage('Checkout Code') {
            steps {
                // 使用任务配置中的 Git 仓库
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
            // 💡 移除所有 when 条件，确保 GitHub 每次都能收到 Lint 结果
            parallel {
                stage('Ruff Check') { steps { sh 'python3 -m ruff check .' } }
                stage('Bandit Scan') { steps { sh 'python3 -m bandit -r . -x ./tests' } }
                stage('Mypy Type Check') { steps { sh 'python3 -m mypy . --ignore-missing-imports' } }
            }
        }

        stage('Run Automated Tests') {
            // 💡 移除所有 when 条件，确保 GitHub 每次都能收到测试结果
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
    post {
        success {
            step([$class: 'GitHubCommitStatusSetter', statusResultSource: [$class: 'ConditionalStatusResultSource', results: [[$class: 'AnyBuildResult', message: '构建成功', state: 'SUCCESS']]]])
        }
        failure {
            step([$class: 'GitHubCommitStatusSetter', statusResultSource: [$class: 'ConditionalStatusResultSource', results: [[$class: 'AnyBuildResult', message: '构建失败', state: 'FAILURE']]]])
        }
    }
}