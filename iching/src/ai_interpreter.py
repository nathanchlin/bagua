import os
import logging
from dotenv import load_dotenv
from openai import OpenAI

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='ai_interpreter.log'
)
logger = logging.getLogger(__name__)

# 加载环境变量
load_dotenv()

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
        
    def interpret_hexagram(self, hexagram_data, question=None):
        """
        使用AI解读卦象
        
        Args:
            hexagram_data: 卦象数据，包含卦名、卦辞、爻辞等信息
            question: 用户的问题（可选）
        
        Returns:
            dict: AI的解读结果
        """
        try:
            logger.info(f"开始解读卦象: {hexagram_data.get('name', '未知卦象')}")
            if question:
                logger.info(f"问题: {question}")
                
            # 构建提示信息
            prompt = self._build_prompt(hexagram_data, question)
            logger.debug(f"生成的提示信息: {prompt}")
            
            logger.info("正在请求AI解读...")
            response = self.client.chat.completions.create(
                model="deepseek-chat",
                messages=[
                    {
                        "role": "system",
                        "content": """你是一位精通易经的专家，擅长解读卦象并给出切实可行的建议。
请根据以下规则进行解卦：

1. 六爻皆不变：占本卦彖辞，而以内卦为贞，外卦为悔。根据这个卦的卦辞，并结合卦象推论方法对内、外卦之间的关系进行分析。其中内卦代表问卦者，外卦代表问卦者的对方。

2. 一爻变：以本卦变爻辞占。根据本卦中的这一变爻的爻辞推论所问事项的吉凶。

3. 二爻变：以本卦二变爻辞占，仍以上爻为主。根据本卦的两个变爻辞进行推论，并以上位的那个爻辞为主要依据。

4. 三爻变：占本卦及之卦之彖辞，而以本卦为贞，之卦为悔。前十卦主贞，后十卦主悔。应以本卦和之卦的卦辞作为推论依据。其中，本卦卦辞代表问卦者，之卦卦辞代表问卦者对方；初爻不变的十个卦体（即 "前十卦"），以本卦卦辞为主要依据；初爻变化的十个卦体（即 "后十卦"），以之卦卦辞为主要依据。

5. 四爻变：以之卦二不变爻占，仍以下爻为主。推论的依据是之卦中的两个不变爻，其中处于下位的不变爻为主，上位的不变爻为次。

6. 五爻变：以之卦不变爻占。推论的依据是之卦中的不变爻。

7. 六爻变：若为《乾》之《坤》或《坤》之《乾》，则占 "二用"，即《乾・用九》的 "群龙无首，吉" 和《坤・用六》的 "利永贞"；余卦占之卦彖辞。如果遇其他卦体，则以之卦卦辞为推论依据。

请从以下几个方面进行解读：
1. 整体形势
2. 具体建议
3. 注意事项
4. 发展方向
5. 行动建议

输出为txt格式，每一句话结束后用回车换行。"""
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.7,
                max_tokens=2000,
                stream=False
            )
            
            interpretation = response.choices[0].message.content
            logger.info("AI解读完成")
            return {
                "success": True,
                "interpretation": interpretation,
                "sections": self._parse_sections(interpretation)
            }
                
        except Exception as e:
            error_msg = f"解读过程出错: {str(e)}"
            logger.error(error_msg, exc_info=True)
            return {
                "success": False,
                "error": error_msg
            }
    
    def _build_prompt(self, hexagram_data, question=None):
        """构建AI提示信息"""
        logger.info("开始构建提示信息")
        
        # 数据验证
        if not isinstance(hexagram_data, dict):
            logger.error(f"无效的卦象数据格式: {type(hexagram_data)}")
            raise ValueError("卦象数据必须是字典格式")
            
        prompt = "请对以下卦象进行详细解读：\n\n"
        
        if question:
            prompt += f"问题：{question}\n\n"
            
        # 获取本卦信息
        original_hexagram = hexagram_data.get('original_hexagram', {})
        name = str(original_hexagram.get('name', '未知卦名'))
        description = str(original_hexagram.get('description', '无卦辞'))
        meaning = str(original_hexagram.get('meaning', '无卦义'))
        
        # 获取变爻信息
        num_changes = hexagram_data.get('num_changes', 0)
        changing_yao_positions = hexagram_data.get('changing_yao_positions', [])
        interpretation_rules = hexagram_data.get('interpretation_rules', [])
        interpretation = hexagram_data.get('interpretation', [])
        
        # 获取变卦信息
        changing_hexagram = hexagram_data.get('changing_hexagram', {})
        
        # 构建基本信息
        prompt += f"""卦象信息：
- 卦名：{name}
- 卦辞：{description}
- 卦义：{meaning}

变爻信息：
- 变爻数量：{num_changes}
- 变爻位置：{', '.join(map(str, changing_yao_positions))}
- 解卦规则：{', '.join(interpretation_rules)}
- 解卦内容：{', '.join(interpretation)}

上下卦：
- 上卦：{original_hexagram.get('upper_trigram', {}).get('name', '未知上卦')}
- 下卦：{original_hexagram.get('lower_trigram', {}).get('name', '未知下卦')}

爻位信息：
"""
        
        # 添加爻位信息，包含错误处理
        yao_texts = original_hexagram.get('yao_texts', {})
        if isinstance(yao_texts, dict) and yao_texts:
            # 按照从上到下的顺序处理爻位（6->1）
            for position in sorted(yao_texts.keys(), key=lambda x: int(str(x)) if str(x).isdigit() else 0, reverse=True):
                yao = yao_texts[position]
                if isinstance(yao, dict):
                    is_changing = int(position) in changing_yao_positions
                    prompt += f"\n第{position}爻{'（变爻）' if is_changing else ''}："
                    
                    # 获取爻的符号
                    if 'symbol' in yao:
                        prompt += f"\n符号：{yao['symbol']}"
                        
                    # 获取爻的描述
                    if 'description' in yao:
                        prompt += f"\n描述：{yao['description']}"
                        
                    # 获取爻的含义
                    if 'meaning' in yao:
                        prompt += f"\n含义：{yao['meaning']}"
                        
                    prompt += "\n"
                else:
                    logger.warning(f"爻位 {position} 的数据格式无效")
                    prompt += f"\n第{position}爻：数据格式无效\n"
        else:
            logger.warning("爻位数据格式无效或为空")
            prompt += "（爻位信息缺失或格式无效）\n"
            
        # 添加变卦信息
        if changing_hexagram:
            prompt += f"""
变卦信息：
- 卦名：{changing_hexagram.get('name', '未知卦名')}
- 卦辞：{changing_hexagram.get('description', '无卦辞')}
- 卦义：{changing_hexagram.get('meaning', '无卦义')}
"""
                
        logger.info("提示信息构建完成")
        return prompt
    
    def _parse_sections(self, interpretation):
        """将AI解读分解为不同部分"""
        logger.info("开始解析AI解读结果")
        sections = {
            "整体形势": "",
            "具体建议": "",
            "注意事项": "",
            "发展方向": "",
            "行动建议": ""
        }
        
        current_section = None
        lines = interpretation.split('\n')
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # 检查是否是新的部分标题
            for section in sections.keys():
                if section in line or f"{len(str(list(sections.keys()).index(section) + 1))}." in line:
                    current_section = section
                    logger.debug(f"找到新的部分: {section}")
                    break
                    
            if current_section and line not in sections.keys():
                sections[current_section] += line + "\n"
                
        logger.info("AI解读结果解析完成")
        return sections 