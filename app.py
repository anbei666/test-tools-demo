# ==========================================
# 示例：一个最基础的测试平台 Web 服务 (app.py)
# ==========================================
# 🚨 注意：为了让这个文件运行，请务必确保你的 requirements.txt
#    里已经包含了 flask（比如直接写一行：flask）

from flask import Flask

# 1. 创建 Flask 应用实例
app = Flask(__name__)


# 2. 定义根路由 (/)，当浏览器访问 http://localhost:8000 时触发
@app.route('/')
def home():
    # 返回一个简单的 HTML 页面内容
    return """
    <html>
        <head>
            <title>自动化测试平台 - 首页</title>
            <style>
                body { font-family: Arial, sans-serif; text-align: center; margin-top: 100px; background-color: #f4f4f9; }
                h1 { color: #333; }
                p { font-size: 1.2em; color: #666; }
                .status-block { margin: 20px auto; padding: 20px; width: 300px; background: white; border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); }
                .success { color: #2ecc71; font-weight: bold; }
            </style>
        </head>
        <body>
            <h1>欢迎使用自动化测试平台！</h1>
            <div class="status-block">
                <p>Web 服务状态：</p>
                <p class="success">正在运行中... ✅</p>
            </div>
            <p>这个页面是由 Docker 容器内部启动的 Flask 服务生成的。</p>
        </body>
    </html>
    """

# 3. 如果直接运行这个脚本
if __name__ == '__main__':
    # 🌟 关键点：必须设置 host='0.0.0.0'
    #    这样 Docker 引擎才能把宿主机的请求转交给容器内的服务。
    # 🌟 关键点：port 必须与 Dockerfile 中的 EXPOSE 和 docker run 中的映射端口一致 (8000)。
    app.run(host='0.0.0.0', port=8000)  # nosec
