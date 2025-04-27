import os
import logging
from dotenv import load_dotenv
from openai import OpenAI

# 配置日志
logging.basicConfig(
    level=logging.CRITICAL,  # 只显示严重错误级别的日志
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class AIInterpreter:
    def __init__(self):
        load_dotenv()
        # 使用环境变量中的API密钥
        self.api_key = os.getenv("OPENAI_API_KEY", "sk-e1a39e17a78c4ee3aa5151ac9b08b135")
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
请按照以下固定格式进行解读，每个部分都需要以标题开头：

一、整体形势分析
[在这里详细分析当前整体形势]

二、具体建议
[在这里提供具体可行的建议]

三、需要注意的事项
[在这里列出需要特别注意的要点]

四、发展方向
[在这里分析未来可能的发展方向]

五、行动建议
[在这里给出具体的行动建议]

请确保每个部分都有实质性的内容，避免空泛的表述。回答要具体、务实、有针对性。"""
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
            
        # 安全地获取数据，提供默认值
        name = str(hexagram_data.get('name', '未知卦名'))
        description = str(hexagram_data.get('description', '无卦辞'))
        meaning = str(hexagram_data.get('meaning', '无卦义'))
        
        # 获取上下卦信息
        upper_trigram = hexagram_data.get('upper_trigram')
        lower_trigram = hexagram_data.get('lower_trigram')
        
        # 构建基本信息
        prompt += f"""卦象信息：
- 卦名：{name}
- 卦辞：{description}
- 卦义：{meaning}

上下卦：
- 上卦：{upper_trigram if upper_trigram else '未知上卦'}
- 下卦：{lower_trigram if lower_trigram else '未知下卦'}

爻位信息：
"""
        
        # 添加爻位信息，包含错误处理
        yao_texts = hexagram_data.get('yao_texts', {})
        if isinstance(yao_texts, dict) and yao_texts:
            # 按照从上到下的顺序处理爻位（6->1）
            for position in sorted(yao_texts.keys(), key=lambda x: int(str(x)) if str(x).isdigit() else 0, reverse=True):
                yao = yao_texts[position]
                if isinstance(yao, dict):
                    prompt += f"\n第{position}爻："
                    
                    # 获取爻的符号
                    if 'symbol' in yao:
                        prompt += f"\n符号：{yao['symbol']}"
                        
                    # 获取爻的描述
                    if 'description' in yao:
                        prompt += f"\n描述：{yao['description']}"
                        
                    # 获取爻的含义
                    if 'meaning' in yao:
                        prompt += f"\n含义：{yao['meaning']}"
                        
                    # 获取爻的变化含义
                    if 'change_meaning' in yao:
                        prompt += f"\n变爻：{yao['change_meaning']}"
                        
                    prompt += "\n"
                else:
                    logger.warning(f"爻位 {position} 的数据格式无效")
                    prompt += f"\n第{position}爻：数据格式无效\n"
        else:
            logger.warning("爻位数据格式无效或为空")
            prompt += "（爻位信息缺失或格式无效）\n"
                
        logger.info("提示信息构建完成")
        return prompt
    
    def _parse_sections(self, interpretation):
        """将AI解读分解为不同部分"""
        logger.info("开始解析AI解读结果")
        sections = {
            "整体形势": "暂无分析",
            "具体建议": "暂无建议",
            "注意事项": "暂无注意事项",
            "发展方向": "暂无方向",
            "行动建议": "暂无建议"
        }
        
        # 定义可能的部分标题变体
        section_variants = {
            "整体形势": ["整体形势", "整体分析", "形势分析", "1.", "一、"],
            "具体建议": ["具体建议", "建议", "2.", "二、"],
            "注意事项": ["注意事项", "需要注意", "3.", "三、"],
            "发展方向": ["发展方向", "未来方向", "4.", "四、"],
            "行动建议": ["行动建议", "具体行动", "5.", "五、"]
        }
        
        current_section = None
        content_buffer = []
        lines = interpretation.split('\n')
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # 检查是否是新的部分标题
            found_section = False
            for section, variants in section_variants.items():
                for variant in variants:
                    if variant.lower() in line.lower():
                        # 如果有累积的内容，保存到当前部分
                        if current_section and content_buffer:
                            sections[current_section] = ' '.join(content_buffer).strip()
                            content_buffer = []
                        
                        current_section = section
                        found_section = True
                        break
                if found_section:
                    break
            
            # 如果不是标题且有当前部分，添加到内容缓冲区
            if not found_section and current_section:
                # 去掉可能的序号前缀
                cleaned_line = line
                for prefix in ["1.", "2.", "3.", "4.", "5.", "一、", "二、", "三、", "四、", "五、"]:
                    if cleaned_line.startswith(prefix):
                        cleaned_line = cleaned_line[len(prefix):].strip()
                content_buffer.append(cleaned_line)
        
        # 保存最后一个部分的内容
        if current_section and content_buffer:
            sections[current_section] = ' '.join(content_buffer).strip()
        
        # 确保所有部分都有内容
        for section in sections:
            if not sections[section] or sections[section].isspace():
                sections[section] = f"暂无{section}信息"
        
        logger.info("AI解读结果解析完成")
        return sections 