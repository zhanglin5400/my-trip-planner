FROM python:3.11-slim

WORKDIR /app

# 复制依赖文件并安装
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install uv
# 应用修复 MCP JSON 解析问题
#COPY fix_mcp.py /app/fix_mcp.py
#RUN python /app/fix_mcp.py

# 复制整个 backend 目录
COPY backend/ .

# 暴露端口（Railway 会自动映射）
EXPOSE 8000

# 启动命令
CMD uvicorn app.api.main:app --host 0.0.0.0 --port $PORT