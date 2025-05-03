# IChing (易经) 预测系统

这是一个基于Python实现的易经预测系统，可以通过传统的筮法模拟卜卦过程，并提供详细的卦象解读。

## 功能特点

- 支持完整的64卦解读
- 包含卦名、卦辞和详细含义
- 提供中文和拼音对照
- 显示上下卦的五行属性
- 支持变卦的解读
- 展示完整的爻位信息
- 提供Web界面
- 支持AI智能解读
- 支持变爻分析
- 支持卦象可视化
- 支持导出占卜记录

## 安装要求

- Python 3.6+
- 依赖包（见 requirements.txt）

## 使用方法

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 环境变量设置

1. 在 `iching/src` 目录下创建 `.env` 文件
2. 在 `.env` 文件中设置你的 DeepSeek API 密钥：
   ```
   DEEPSEEK_API_KEY=your_api_key_here
   ```
3. 注意：不要将 `.env` 文件提交到 Git 仓库

### 3. 启动 Web 应用

#### 方法一：使用 Flask 命令

```bash
# 进入项目目录
cd iching/src

# 设置环境变量
export FLASK_APP=app.py
export FLASK_ENV=development  # 可选：启用开发模式

# 启动服务器
python3 -m flask run --port 5005
```

#### 方法二：直接运行 Python 脚本

```bash
# 进入项目目录
cd iching/src

# 启动服务器
python3 app.py
```

#### 方法三：使用脚本启动（推荐）

1. 在项目根目录创建启动脚本 `run_web.sh`：
   ```bash
   #!/bin/bash
   cd iching/src
   export FLASK_APP=app.py
   python3 -m flask run --port 5005
   ```

2. 给脚本添加执行权限：
   ```bash
   chmod +x run_web.sh
   ```

3. 运行脚本：
   ```bash
   ./run_web.sh
   ```

### 4. 访问 Web 界面

启动成功后，在浏览器中访问：
```
http://localhost:5005
```

## 项目结构

```
iching/
├── src/
│   ├── app.py            # Web应用主程序
│   ├── ai_interpreter.py # AI解读模块
│   ├── iching.py         # 核心逻辑
│   ├── hexagram_data.py  # 卦象数据
│   └── templates/        # Web模板
├── tests/                # 测试文件
└── README.md            # 项目说明文档
```

## 注意事项

- 本程序仅供娱乐和参考
- 卦象解释基于传统周易理论
- 建议在使用时保持平和心态
- 重要决策请理性对待
- 确保已正确设置 DeepSeek API 密钥
- 如果遇到端口占用问题，可以修改 `--port` 参数使用其他端口

## 后续开发计划

- [ ] 添加更详细的卦象解释
- [ ] 实现更准确的筊杯算法
- [ ] 添加变卦分析
- [ ] 添加单元测试
- [ ] 优化Web界面
- [ ] 增加更多AI解读功能 
