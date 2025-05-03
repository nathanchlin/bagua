#!/bin/bash

# 构建并启动Docker容器
docker-compose up --build -d

echo "应用已启动，访问 http://localhost:5000"
echo "查看日志: docker-compose logs -f"
echo "停止应用: docker-compose down" 