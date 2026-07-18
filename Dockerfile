# 1. 基础环境：使用官方的 Python 3.10 轻量版
FROM python:3.10-slim

# 2. 容器内部署目录：后续操作都在容器内的 /app 目录下进行
WORKDIR /app

# 3. 复制依赖清单并安装
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. 把当前目录下的所有代码复制到容器的 /app 目录里
COPY . .

# 5. 告诉容器默认运行 pytest 自动化测试
CMD ["pytest"]