from flask import Flask, render_template, request, jsonify, send_file
from iching import IChing
from ai_interpreter import AIInterpreter
import io
import datetime
import os
import logging
import markdown2  # 添加markdown2库
import sys
import requests
import json
from openai import OpenAI

# 配置日志
logging.basicConfig(
    level=logging.ERROR,  # 只显示错误级别的日志
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
# 完全禁用所有日志输出
logging.getLogger('werkzeug').disabled = True
logging.getLogger('flask.app').disabled = True
app.logger.disabled = True
# 禁用Flask的访问日志
sys.stdout = open('/dev/null', 'w')
sys.stderr = open('/dev/null', 'w')

iching = IChing()

class AIInterpreter:
    def __init__(self):
        self.api_key = os.getenv('DEEPSEEK_API_KEY')
        if not self.api_key:
            raise ValueError("DEEPSEEK_API_KEY not found in environment variables")
        self.client = OpenAI(
            api_key=self.api_key,
            base_url="https://api.deepseek.com/v1"
        )
        logger.info("AI解释器初始化完成")

ai_interpreter = AIInterpreter()

@app.route('/')
def index():
    logger.info("访问主页")
    empty_result = {
        "question": "",
        "name": "请输入问题进行求卦",
        "description": "暂无卦辞",
        "meaning": "暂无卦义",
        "hexagram": [],
        "upper_trigram": {
            "name": "暂无",
            "nature": "暂无",
            "characteristic": "暂无",
            "element": "暂无"
        },
        "lower_trigram": {
            "name": "暂无",
            "nature": "暂无",
            "characteristic": "暂无",
            "element": "暂无"
        },
        "yao_texts": {
            "1": {"type": "暂无", "symbol": "暂无", "description": "暂无爻辞", "meaning": "暂无爻义"},
            "2": {"type": "暂无", "symbol": "暂无", "description": "暂无爻辞", "meaning": "暂无爻义"},
            "3": {"type": "暂无", "symbol": "暂无", "description": "暂无爻辞", "meaning": "暂无爻义"},
            "4": {"type": "暂无", "symbol": "暂无", "description": "暂无爻辞", "meaning": "暂无爻义"},
            "5": {"type": "暂无", "symbol": "暂无", "description": "暂无爻辞", "meaning": "暂无爻义"},
            "6": {"type": "暂无", "symbol": "暂无", "description": "暂无爻辞", "meaning": "暂无爻义"}
        },
        "changing_count": 0,
        "changing_lines": [],
        "changed_hexagram": {
            "name": "暂无",
            "description": "暂无",
            "meaning": "暂无"
        },
        "interpretation": "请输入问题进行求卦"
    }
    return render_template('index.html', result=empty_result)

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
        
        # 生成文本内容
        text_content = f"""周易卦象解析结果

所问问题：
{data.get('question', '无')}

本卦：
卦名：{data.get('name', '无')}
卦辞：{data.get('description', '无')}
卦义：{data.get('meaning', '无')}

上下卦：
上卦（{data.get('upper_trigram', {}).get('name', '无')}）：
性质：{data.get('upper_trigram', {}).get('nature', '无')}
特性：{data.get('upper_trigram', {}).get('characteristic', '无')}
五行：{data.get('upper_trigram', {}).get('element', '无')}

下卦（{data.get('lower_trigram', {}).get('name', '无')}）：
性质：{data.get('lower_trigram', {}).get('nature', '无')}
特性：{data.get('lower_trigram', {}).get('characteristic', '无')}
五行：{data.get('lower_trigram', {}).get('element', '无')}

爻位：
"""
        # 添加爻位信息
        yao_texts = data.get('yao_texts', {})
        if yao_texts:
            for position in sorted(yao_texts.keys(), key=lambda x: int(x) if x.isdigit() else 0, reverse=True):
                yao = yao_texts[position]
                yao_type = yao.get('type', '')  # 获取爻的类型（老阳、老阴、少阳、少阴）
                text_content += f"""第{position}爻（{yao_type}）：
符号：{yao.get('symbol', '无')}
描述：{yao.get('description', '无')}
含义：{yao.get('meaning', '无')}"""
                
                if yao.get('change_meaning'):
                    text_content += f"\n变爻：{yao.get('change_meaning', '无')}"
                text_content += "\n\n"

        # 添加变卦信息
        if data.get('changed_hexagram'):
            changed = data['changed_hexagram']
            text_content += f"""变卦：
卦名：{changed.get('name', '无')}
卦辞：{changed.get('description', '无')}
卦义：{changed.get('meaning', '无')}
"""

        # 添加AI解读内容
        if data.get('ai_interpretation'):
            ai_data = data['ai_interpretation']
            text_content += f"""
AI解读：

整体形势：
{ai_data.get('sections', {}).get('整体形势', '无')}

具体建议：
{ai_data.get('sections', {}).get('具体建议', '无')}

注意事项：
{ai_data.get('sections', {}).get('注意事项', '无')}

发展方向：
{ai_data.get('sections', {}).get('发展方向', '无')}

行动建议：
{ai_data.get('sections', {}).get('行动建议', '无')}
"""

        # 添加生成时间
        text_content += f"\n---\n生成时间：{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

        # 创建内存文件对象
        buffer = io.BytesIO()
        buffer.write(text_content.encode('utf-8'))
        buffer.seek(0)

        # 生成文件名
        filename = f"易经解析_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        logger.info(f"文件生成完成: {filename}")
        
        return send_file(
            buffer,
            as_attachment=True,
            download_name=filename,
            mimetype='text/plain'
        )

    except Exception as e:
        logger.error(f"生成下载文件失败: {str(e)}", exc_info=True)
        return jsonify({'error': str(e)}), 500

@app.route('/ai_interpret', methods=['POST'])
def ai_interpret():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'error': 'No data provided'})
        
        # 获取卦象信息
        hexagram = data.get('hexagram', {})
        changing_count = data.get('changing_count', 0)
        changing_lines = data.get('changing_lines', [])
        changed_hexagram = data.get('changed_hexagram', {})
        question = data.get('question', '')
        
        # 根据变爻数量应用不同的解卦规则
        interpretation_rules = {
            0: "六爻皆不变：占本卦彖辞，而以内卦为贞，外卦为悔。根据这个卦的卦辞，并结合卦象推论方法对内、外卦之间的关系进行分析。其中内卦代表问卦者，外卦代表问卦者的对方。",
            1: "一爻变：以本卦变爻辞占。根据本卦中的这一变爻的爻辞推论所问事项的吉凶。",
            2: "二爻变：以本卦二变爻辞占，仍以上爻为主。根据本卦的两个变爻辞进行推论，并以上位的那个爻辞为主要依据。",
            3: "三爻变：占本卦及之卦之彖辞，而以本卦为贞，之卦为悔。前十卦主贞，后十卦主悔。应以本卦和之卦的卦辞作为推论依据。其中，本卦卦辞代表问卦者，之卦卦辞代表问卦者对方；初爻不变的十个卦体（即 '前十卦'），以本卦卦辞为主要依据；初爻变化的十个卦体（即 '后十卦'），以之卦卦辞为主要依据。",
            4: "四爻变：以之卦二不变爻占，仍以下爻为主。推论的依据是之卦中的两个不变爻，其中处于下位的不变爻为主，上位的不变爻为次。",
            5: "五爻变：以之卦不变爻占。推论的依据是之卦中的不变爻。",
            6: "六爻变：若为《乾》之《坤》或《坤》之《乾》，则占 '二用'，即《乾・用九》的 '群龙无首，吉' 和《坤・用六》的 '利永贞'；余卦占之卦彖辞。如果遇其他卦体，则以之卦卦辞为推论依据。"
        }
        
        # 构建提示词
        prompt = f"""
        问题：{question}
        
        卦象信息：
        - 本卦：{hexagram.get('name', '')}
        - 本卦卦辞：{hexagram.get('description', '')}
        - 本卦卦义：{hexagram.get('meaning', '')}
        - 变爻数量：{changing_count}
        - 变爻位置：{', '.join(map(str, changing_lines)) if changing_lines else '无'}
        - 变卦：{changed_hexagram.get('name', '')}
        - 变卦卦辞：{changed_hexagram.get('description', '')}
        - 变卦卦义：{changed_hexagram.get('meaning', '')}
        
        解卦规则：
        {interpretation_rules.get(changing_count, '')}
        
        请根据以上信息，结合传统易经解卦规则，对问题进行解读。解读应包含以下方面：
        1. 整体形势：分析当前的整体情况
        2. 具体建议：根据卦象给出的具体建议
        3. 注意事项：需要注意的关键点
        4. 发展方向：未来的可能发展方向
        5. 行动建议：具体的行动建议
        """
        
        # 调用 AI 进行解读
        response = ai_interpreter.client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "你是一位精通易经的专家，请根据提供的卦象信息和传统解卦规则，对问题进行深入解读。"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1000
        )
        
        # 解析 AI 返回的结果
        ai_response = response.choices[0].message.content
        sections = {
            '整体形势': '',
            '具体建议': '',
            '注意事项': '',
            '发展方向': '',
            '行动建议': ''
        }
        
        # 解析各个部分的内容
        current_section = None
        for line in ai_response.split('\n'):
            if '整体形势' in line:
                current_section = '整体形势'
            elif '具体建议' in line:
                current_section = '具体建议'
            elif '注意事项' in line:
                current_section = '注意事项'
            elif '发展方向' in line:
                current_section = '发展方向'
            elif '行动建议' in line:
                current_section = '行动建议'
            elif current_section and line.strip():
                sections[current_section] += line.strip() + '\n'
        
        return jsonify({
            'success': True,
            'sections': sections
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    # 从环境变量获取端口号，默认为5005
    port = int(os.environ.get('PORT', 5005))
    logger.info(f"启动服务器，端口: {port}")
    app.run(host='0.0.0.0', port=port, debug=True) 