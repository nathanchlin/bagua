# 易经占卜应用

这是一个基于 Flask 的易经占卜应用，支持传统解卦和 AI 智能解读。

## 功能特点

- 传统易经六十四卦占卜
- AI 智能解读（使用 DeepSeek API）
- 支持变爻分析
- 支持卦象可视化
- 支持导出占卜记录

## 安装方式

### 方式一：直接运行

1. 克隆仓库：
```bash
git clone https://github.com/yourusername/iching.git
cd iching
```

2. 安装依赖：
```bash
pip install -r requirements.txt
```

3. 设置环境变量：
```bash
export DEEPSEEK_API_KEY=your_api_key_here
```

4. 运行应用：
```bash
python app.py
```

### 方式二：使用 Docker（推荐）

1. 克隆仓库：
```bash
git clone https://github.com/yourusername/iching.git
cd iching
```

2. 创建环境变量文件：
```bash
echo "DEEPSEEK_API_KEY=your_api_key_here" > .env
```

3. 构建并启动容器：
```bash
# 构建镜像
docker-compose build

# 启动容器
docker-compose up -d
```

4. 查看容器状态：
```bash
docker-compose ps
```

5. 查看容器日志：
```bash
docker-compose logs -f
```

6. 停止容器：
```bash
docker-compose down
```

## 访问应用

应用启动后，打开浏览器访问：
- 直接运行：http://localhost:5000
- Docker 运行：http://localhost:5000

## 环境变量

- `DEEPSEEK_API_KEY`：DeepSeek API 密钥（必需）

## 注意事项

- 确保在启动应用前已设置 `DEEPSEEK_API_KEY` 环境变量
- 默认情况下，应用运行在 5000 端口
- 如需更改端口，请修改 `docker-compose.yml` 文件中的端口映射
- 应用数据存储在容器内，如需持久化存储，请根据需要配置 volumes

## 更新应用

### 直接运行方式
```bash
git pull
pip install -r requirements.txt
```

### Docker 方式
```bash
git pull
docker-compose up -d --build
```

## 常见问题

1. 如何修改端口？
   - 直接运行：修改 `app.py` 中的 `port` 参数
   - Docker 运行：修改 `docker-compose.yml` 中的端口映射

2. 如何查看日志？
   - 直接运行：查看控制台输出
   - Docker 运行：使用 `docker-compose logs -f` 命令

3. 如何备份数据？
   - 直接运行：备份 `data` 目录
   - Docker 运行：配置 volumes 持久化存储

## 贡献指南

欢迎提交 Issue 和 Pull Request 来帮助改进这个项目。

## 许可证

MIT License 