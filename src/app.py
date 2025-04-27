from flask import Flask, render_template, request, jsonify, send_file
from iching import IChing
from ai_interpreter import AIInterpreter
import io
import datetime
import os
import logging

# 配置日志
logging.basicConfig(
    level=logging.CRITICAL,  # 只显示严重错误级别的日志
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
# 关闭Flask的开发服务器日志
import logging as flask_logging
flask_logging.getLogger('werkzeug').setLevel(logging.CRITICAL)

# 关闭Flask的调试输出
app.logger.setLevel(logging.CRITICAL)

iching = IChing()
ai_interpreter = AIInterpreter()

@app.route('/')
def index():
    logger.info("访问主页")
    return render_template('index.html')

@app.route('/cast', methods=['POST'])
def cast():
    question = request.form.get('question', '').strip()
    if not question:
        logger.warning("收到空问题")
        return jsonify({'error': '问题不能为空'}), 400
    
    try:
        logger.info(f"开始解析问题: {question}")
        result = iching.interpret_hexagram(question)
        logger.info(f"解析完成: {result.get('name', '未知卦象')}")
        return jsonify(result)
    except Exception as e:
        logger.error(f"解析失败: {str(e)}", exc_info=True)
        return jsonify({'error': str(e)}), 500

@app.route('/hexagrams')
def hexagrams():
    """返回所有可用的卦象列表"""
    logger.info("请求卦象列表")
    from hexagram_data import HEXAGRAM_MAPS, HEXAGRAM_PINYIN
    hexagrams_list = []
    for i, (key, name) in enumerate(HEXAGRAM_MAPS.items(), 1):
        hexagrams_list.append({
            'id': i,
            'key': key,
            'name': name,
            'pinyin': HEXAGRAM_PINYIN.get(name, '')
        })
    logger.info(f"返回 {len(hexagrams_list)} 个卦象")
    return jsonify(hexagrams_list)

@app.route('/download_result', methods=['POST'])
def download_result():
    """生成并下载卦象解析结果的Markdown文件"""
    try:
        data = request.json
        if not data:
            logger.warning("下载请求中没有数据")
            return jsonify({'error': '数据不能为空'}), 400
        
        logger.info(f"开始生成下载文件: {data.get('name', '未知卦象')}")
        
        # 生成Markdown内容
        md_content = f"""# 周易卦象解析结果

## 所问问题
{data.get('question', '无')}

## 本卦
- **卦名**：{data.get('name', '无')}
- **卦辞**：{data.get('description', '无')}
- **卦义**：{data.get('meaning', '无')}

## 上下卦
### 上卦（{data.get('upper_trigram', {}).get('name', '无')}）
- **性质**：{data.get('upper_trigram', {}).get('nature', '无')}
- **特性**：{data.get('upper_trigram', {}).get('characteristic', '无')}
- **五行**：{data.get('upper_trigram', {}).get('element', '无')}

### 下卦（{data.get('lower_trigram', {}).get('name', '无')}）
- **性质**：{data.get('lower_trigram', {}).get('nature', '无')}
- **特性**：{data.get('lower_trigram', {}).get('characteristic', '无')}
- **五行**：{data.get('lower_trigram', {}).get('element', '无')}

## 爻位
"""
        # 添加爻位信息
        yao_texts = data.get('yao_texts', {})
        if yao_texts:
            for position in sorted(yao_texts.keys(), key=lambda x: int(str(x)) if str(x).isdigit() else 0, reverse=True):
                yao = yao_texts[position]
                yao_type = yao.get('type', '')  # 获取爻的类型（老阳、老阴、少阳、少阴）
                md_content += f"""### 第{position}爻（{yao_type}）
- **符号**：{yao.get('symbol', '无')}
- **描述**：{yao.get('description', '无')}
- **含义**：{yao.get('meaning', '无')}"""
                
                if yao.get('change_meaning'):
                    md_content += f"\n- **变爻**：{yao.get('change_meaning', '无')}"
                md_content += "\n\n"

        # 添加变卦信息
        if data.get('changed_hexagram'):
            changed = data['changed_hexagram']
            md_content += f"""## 变卦
- **卦名**：{changed.get('name', '无')}
- **卦辞**：{changed.get('description', '无')}
- **卦义**：{changed.get('meaning', '无')}
"""

        # 添加生成时间
        md_content += f"\n\n---\n生成时间：{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

        # 创建内存文件对象
        buffer = io.BytesIO()
        buffer.write(md_content.encode('utf-8'))
        buffer.seek(0)

        # 生成文件名
        filename = f"易经解析_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        logger.info(f"文件生成完成: {filename}")
        
        return send_file(
            buffer,
            as_attachment=True,
            download_name=filename,
            mimetype='text/markdown'
        )

    except Exception as e:
        logger.error(f"生成下载文件失败: {str(e)}", exc_info=True)
        return jsonify({'error': str(e)}), 500

@app.route('/ai_interpret', methods=['POST'])
def ai_interpret():
    """AI解卦接口"""
    try:
        data = request.json
        if not data:
            logger.warning("AI解读请求中没有数据")
            return jsonify({'error': '请求数据不能为空'}), 400
            
        logger.info(f"开始AI解读: {data.get('name', '未知卦象')}")
        # 获取解读结果
        result = ai_interpreter.interpret_hexagram(
            hexagram_data=data,
            question=data.get('question')
        )
        
        if result['success']:
            logger.info("AI解读完成")
            return jsonify(result)
        else:
            logger.error(f"AI解读失败: {result.get('error', '未知错误')}")
            return jsonify({'error': result['error']}), 500
            
    except Exception as e:
        logger.error(f"AI解读过程出错: {str(e)}", exc_info=True)
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # 从环境变量获取端口号，默认为5005
    port = int(os.environ.get('PORT', 5005))
    logger.info(f"启动服务器，端口: {port}")
    app.run(host='0.0.0.0', port=port, debug=True) 