# 1. 选地基：使用官方的 Python 3.9 轻量版镜像
# (这个镜像里已经装好了 Python，不用你自己装了)
FROM python:3.14-slim
# 2. 设工作区：在容器里建个文件夹叫 /app
WORKDIR /app
# 3. 搬运清单：先把 requirements.txt 拷进去
# (利用缓存机制加速构建)
COPY requirements.txt .
# 4. 安装依赖：让容器根据清单装包
# (使用清华源加速下载，--no-cache-dir 减小体积)
RUN pip install --no-cache-dir -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# 5. 搬运代码：把当前目录下的所有代码拷进容器
COPY . .

# 6. 启动命令：容器启动时，自动运行 pytest
CMD ["pytest", "-vs", "--alluredir=./report/tmp"]
