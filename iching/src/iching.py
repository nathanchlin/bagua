import os
import sys
import random
import readline  # 添加readline支持
from typing import List, Dict, Tuple
from hexagram_data import (HEXAGRAMS_DATA, TRIGRAM_ATTRIBUTES, 
                         HEXAGRAM_NAMES, HEXAGRAM_PINYIN, HEXAGRAM_MAPS)
import logging

# Add the current directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

logger = logging.getLogger(__name__)

class IChing:
    # 八卦基本属性
    TRIGRAMS = {
        (1, 1, 1): "乾",
        (0, 0, 0): "坤",
        (0, 1, 0): "坎",
        (1, 0, 1): "离",
        (1, 0, 0): "震",
        (0, 0, 1): "巽",
        (1, 1, 0): "兑",
        (0, 1, 1): "艮"
    }

    # 爻的类型
    YAO_TYPES = {
        6: ("老阴", "— — ·"),  # 变爻
        7: ("少阳", "——"),
        8: ("少阴", "— —"),
        9: ("老阳", "—— ·")    # 变爻
    }

    def __init__(self):
        # 初始化时创建卦名查找表
        self.trigram_pairs = {}
        for upper_code, upper_name in self.TRIGRAMS.items():
            for lower_code, lower_name in self.TRIGRAMS.items():
                # 将二进制元组转换为字符串形式
                binary_code = ''.join(map(str, upper_code + lower_code))
                self.trigram_pairs[binary_code] = f"{upper_name}{lower_name}"

    @staticmethod
    def cast_yarrow_stalks() -> int:
        """
        模拟传统的求卦过程，返回爻的数值：6(老阴)、7(少阳)、8(少阴)、9(老阳)
        """
        # 使用概率分布来模拟传统的求卦概率
        # 老阳(9): 4/16, 少阳(7): 4/16, 少阴(8): 4/16, 老阴(6): 4/16
        rand = random.random()
        if rand < 4/16:    # 4/16
            return 6       # 老阴
        elif rand < 8/16:  # 4/16
            return 8       # 少阴
        elif rand < 12/16: # 4/16
            return 7       # 少阳
        else:             # 4/16
            return 9       # 老阳

    def is_changing_line(self, value: int) -> bool:
        """
        判断是否是变爻（老阳或老阴）
        """
        return value in [6, 9]

    def get_line_value(self, value: int) -> int:
        """
        获取爻的阴阳值（0为阴，1为阳）
        """
        return 1 if value in [7, 9] else 0

    def generate_hexagram(self) -> List[int]:
        """
        生成完整的六爻卦象
        """
        return [self.cast_yarrow_stalks() for _ in range(6)]

    def get_trigrams(self, hexagram: List[int]) -> Tuple[str, str]:
        """
        将六爻分解为上下卦
        """
        # 将爻的数值转换为阴阳值
        binary_hexagram = [self.get_line_value(v) for v in hexagram]
        lower = tuple(binary_hexagram[:3])
        upper = tuple(binary_hexagram[3:])
        return (self.TRIGRAMS.get(upper, "未知"), 
                self.TRIGRAMS.get(lower, "未知"))

    def get_hexagram_name(self, binary_values: List[int]) -> str:
        """根据六爻的二进制值获取卦名"""
        if not binary_values or len(binary_values) != 6:
            return "未知卦"
        
        # 获取上下卦的二进制值
        upper_trigram = tuple(binary_values[:3])
        lower_trigram = tuple(binary_values[3:])
        
        # 获取上下卦的名称
        upper_name = self.TRIGRAMS.get(upper_trigram)
        lower_name = self.TRIGRAMS.get(lower_trigram)
        
        if not upper_name or not lower_name:
            return "未知卦"
        
        # 组合上下卦名称
        trigram_key = f"{upper_name}{lower_name}"
        
        # 从HEXAGRAM_MAPS中获取卦名
        hexagram_name = HEXAGRAM_MAPS.get(trigram_key)
        
        return hexagram_name if hexagram_name else "未知卦"
  
    def get_changed_hexagram(self, hexagram: List[int]) -> List[int]:
        """
        获取变卦的爻值
        老阳(9)变少阴(8)，老阴(6)变少阳(7)
        """
        return [8 if v == 9 else 7 if v == 6 else v for v in hexagram]

    def get_hexagram_info(self, hexagram_key: str) -> dict:
        """根据卦象键获取卦象的详细信息"""
        try:
            # 将卦象键转换为爻值
            yao_values = [int(c) for c in hexagram_key]
            if len(yao_values) != 6:
                logger.error(f"无效的卦象键长度: {hexagram_key}")
                return None
            
            # 将爻值转换为二进制值（0为阴，1为阳）
            binary_values = [1 if v in [7, 9] else 0 for v in yao_values]
            logger.info(f"二进制值: {binary_values}")
            
            # 获取上下卦的二进制值
            upper_trigram = tuple(binary_values[:3])
            lower_trigram = tuple(binary_values[3:])
            logger.info(f"上卦二进制: {upper_trigram}, 下卦二进制: {lower_trigram}")
            
            # 获取上下卦的名称
            upper_name = self.TRIGRAMS.get(upper_trigram)
            lower_name = self.TRIGRAMS.get(lower_trigram)
            logger.info(f"上卦: {upper_name}, 下卦: {lower_name}")
            
            if not upper_name or not lower_name:
                logger.error(f"无法识别上下卦: {upper_trigram}, {lower_trigram}")
                return None
            
            # 组合上下卦名称
            trigram_key = f"{upper_name}{lower_name}"
            logger.info(f"卦象键: {trigram_key}")
            
            # 从HEXAGRAMS_DATA中获取卦象的详细信息
            hexagram_data = HEXAGRAMS_DATA.get(trigram_key, {})
            if not hexagram_data:
                logger.error(f"无法找到卦象数据: {trigram_key}")
                return None
            
            # 获取上下卦的属性
            upper_attrs = TRIGRAM_ATTRIBUTES.get(upper_name, {})
            lower_attrs = TRIGRAM_ATTRIBUTES.get(lower_name, {})
            
            # 构建完整的卦象信息
            result = {
                'name': hexagram_data.get('name', '未知卦'),
                'description': hexagram_data.get('description', '无卦辞'),
                'meaning': hexagram_data.get('meaning', '无解释'),
                'upper_trigram': {
                    'name': upper_name,
                    'nature': upper_attrs.get('nature', '未知'),
                    'characteristic': upper_attrs.get('characteristic', '未知'),
                    'element': upper_attrs.get('element', '未知')
                },
                'lower_trigram': {
                    'name': lower_name,
                    'nature': lower_attrs.get('nature', '未知'),
                    'characteristic': lower_attrs.get('characteristic', '未知'),
                    'element': lower_attrs.get('element', '未知')
                },
                'yao_texts': hexagram_data.get('yao_texts', {})
            }
            
            return result
            
        except Exception as e:
            logger.error(f"获取卦象信息失败: {str(e)}", exc_info=True)
            return None

    def interpret_hexagram(self, question):
        """解析卦象"""
        try:
            # 生成卦象
            hexagram = self.generate_hexagram()
            logger.info(f"生成的卦象: {hexagram}")
            
            # 获取本卦信息
            hexagram_key = ''.join(str(yao) for yao in hexagram)
            logger.info(f"本卦键: {hexagram_key}")
            hexagram_info = self.get_hexagram_info(hexagram_key)
            if not hexagram_info:
                logger.error(f"无法获取本卦信息: {hexagram_key}")
                raise ValueError(f"无法获取本卦信息: {hexagram_key}")
            
            # 分析变爻
            changing_yaos = []
            for i, yao in enumerate(hexagram):
                if yao in [6, 9]:  # 老阴或老阳
                    changing_yaos.append(i)
            logger.info(f"变爻位置: {changing_yaos}")
            
            # 生成变卦
            changed_hexagram = self.get_changed_hexagram(hexagram)
            logger.info(f"变卦: {changed_hexagram}")
            
            # 获取变卦信息
            changed_key = ''.join(str(yao) for yao in changed_hexagram)
            logger.info(f"变卦键: {changed_key}")
            changed_info = self.get_hexagram_info(changed_key)
            if not changed_info and len(changing_yaos) > 0:
                logger.error(f"无法获取变卦信息: {changed_key}")
                raise ValueError(f"无法获取变卦信息: {changed_key}")
            
            # 确保每个爻都有正确的类型
            for i, yao_value in enumerate(hexagram):
                position = str(i + 1)
                if position not in hexagram_info['yao_texts']:
                    hexagram_info['yao_texts'][position] = {}
                hexagram_info['yao_texts'][position]['type'] = self.YAO_TYPES[yao_value][0]
                hexagram_info['yao_texts'][position]['symbol'] = self.YAO_TYPES[yao_value][1]
            
            # 如果有变卦，确保变卦的爻位信息也被正确处理
            if changed_info:
                for i, yao_value in enumerate(changed_hexagram):
                    position = str(i + 1)
                    if position not in changed_info['yao_texts']:
                        changed_info['yao_texts'][position] = {}
                    changed_info['yao_texts'][position]['type'] = self.YAO_TYPES[yao_value][0]
                    changed_info['yao_texts'][position]['symbol'] = self.YAO_TYPES[yao_value][1]
            
            # 根据变爻数量选择解释方式
            num_changes = len(changing_yaos)
            interpretation = ""
            interpretation_rules = ""
            
            if num_changes == 0:
                # 六爻皆不变：占本卦彖辞，而以内卦为贞，外卦为悔
                interpretation_rules = "六爻皆不变：占本卦彖辞，而以内卦为贞，外卦为悔。根据这个卦的卦辞，并结合卦象推论方法对内、外卦之间的关系进行分析。其中内卦代表问卦者，外卦代表问卦者的对方。"
                interpretation = f"本卦彖辞：{hexagram_info['description']}\n"
                interpretation += f"内卦（贞）：{hexagram_info['lower_trigram']['name']}，代表问卦者\n"
                interpretation += f"外卦（悔）：{hexagram_info['upper_trigram']['name']}，代表问卦者对方"
            
            elif num_changes == 1:
                # 一爻变：以本卦变爻辞占
                yao_pos = changing_yaos[0] + 1
                yao_text = hexagram_info['yao_texts'].get(str(yao_pos), {})
                interpretation_rules = "一爻变：以本卦变爻辞占。根据本卦中的这一变爻的爻辞推论所问事项的吉凶。"
                interpretation = f"变爻位置：第{yao_pos}爻\n"
                interpretation += f"爻辞：{yao_text.get('description', '无')}\n"
                interpretation += f"含义：{yao_text.get('meaning', '无')}"
            
            elif num_changes == 2:
                # 二爻变：以本卦二变爻辞占，仍以上爻为主
                yao_pos1, yao_pos2 = sorted([p + 1 for p in changing_yaos])
                yao_text1 = hexagram_info['yao_texts'].get(str(yao_pos1), {})
                yao_text2 = hexagram_info['yao_texts'].get(str(yao_pos2), {})
                interpretation_rules = "二爻变：以本卦二变爻辞占，仍以上爻为主。根据本卦中这两个变爻的爻辞推论所问事项的吉凶，其中以上爻的爻辞为主。"
                interpretation = f"变爻位置：第{yao_pos1}爻和第{yao_pos2}爻\n"
                interpretation += f"第{yao_pos1}爻爻辞：{yao_text1.get('description', '无')}\n"
                interpretation += f"第{yao_pos1}爻含义：{yao_text1.get('meaning', '无')}\n"
                interpretation += f"第{yao_pos2}爻爻辞：{yao_text2.get('description', '无')}\n"
                interpretation += f"第{yao_pos2}爻含义：{yao_text2.get('meaning', '无')}"
            
            elif num_changes == 3:
                # 三爻变：以本卦及之卦彖辞占，而以本卦为贞，之卦为悔
                interpretation_rules = "三爻变：以本卦及之卦彖辞占，而以本卦为贞，之卦为悔。根据本卦和变卦的卦辞推论所问事项的吉凶，其中以本卦为主，变卦为辅。"
                interpretation = f"本卦彖辞：{hexagram_info['description']}\n"
                interpretation += f"变卦彖辞：{changed_info['description']}"
            
            elif num_changes == 4:
                # 四爻变：以之卦二不变爻辞占，仍以下爻为主
                unchanged_yaos = [i for i in range(6) if i not in changing_yaos]
                yao_pos1, yao_pos2 = sorted([p + 1 for p in unchanged_yaos])
                yao_text1 = changed_info['yao_texts'].get(str(yao_pos1), {})
                yao_text2 = changed_info['yao_texts'].get(str(yao_pos2), {})
                interpretation_rules = "四爻变：以之卦二不变爻辞占，仍以下爻为主。根据变卦中这两个不变爻的爻辞推论所问事项的吉凶，其中以下爻的爻辞为主。"
                interpretation = f"不变爻位置：第{yao_pos1}爻和第{yao_pos2}爻\n"
                interpretation += f"第{yao_pos1}爻爻辞：{yao_text1.get('description', '无')}\n"
                interpretation += f"第{yao_pos1}爻含义：{yao_text1.get('meaning', '无')}\n"
                interpretation += f"第{yao_pos2}爻爻辞：{yao_text2.get('description', '无')}\n"
                interpretation += f"第{yao_pos2}爻含义：{yao_text2.get('meaning', '无')}"
            
            elif num_changes == 5:
                # 五爻变：以之卦不变爻辞占
                unchanged_yao = [i for i in range(6) if i not in changing_yaos][0] + 1
                yao_text = changed_info['yao_texts'].get(str(unchanged_yao), {})
                interpretation_rules = "五爻变：以之卦不变爻辞占。根据变卦中这个不变爻的爻辞推论所问事项的吉凶。"
                interpretation = f"不变爻位置：第{unchanged_yao}爻\n"
                interpretation += f"爻辞：{yao_text.get('description', '无')}\n"
                interpretation += f"含义：{yao_text.get('meaning', '无')}"
            
            else:  # num_changes == 6
                # 六爻皆变：以之卦彖辞占
                interpretation_rules = "六爻皆变：以之卦彖辞占。根据变卦的卦辞推论所问事项的吉凶。"
                interpretation = f"变卦彖辞：{changed_info['description']}"
            
            # 构建返回结果
            result = {
                'question': question,
                'name': hexagram_info['name'],
                'description': hexagram_info['description'],
                'meaning': hexagram_info['meaning'],
                'upper_trigram': hexagram_info['upper_trigram'],
                'lower_trigram': hexagram_info['lower_trigram'],
                'yao_texts': hexagram_info['yao_texts'],
                'interpretation': interpretation,
                'interpretation_rules': interpretation_rules,
                'changing_yaos': changing_yaos,
                'num_changes': num_changes
            }
            
            # 如果有变卦，添加变卦信息
            if changed_info:
                result['changed_hexagram'] = {
                    'name': changed_info['name'],
                    'description': changed_info['description'],
                    'meaning': changed_info['meaning'],
                    'yao_texts': changed_info['yao_texts']
                }
            
            return result
            
        except Exception as e:
            logger.error(f"解析卦象失败: {str(e)}", exc_info=True)
            raise

    def print_available_hexagrams(self):
        """打印可用的六十四卦"""
        print("\n可用的六十四卦：")
        print_divider()
        for i, (key, name) in enumerate(HEXAGRAM_MAPS.items(), 1):
            pinyin = HEXAGRAM_PINYIN.get(name, "")
            print(f"{i:2d}. {key}->{name} ({pinyin})", end="\t")
            if i % 4 == 0:
                print()
        print("\n")

def print_divider():
    print("=" * 50)

if __name__ == "__main__":
    iching = IChing()
    
    # 配置readline
    readline.parse_and_bind('set editing-mode emacs')  # 使用emacs键绑定
    readline.parse_and_bind('set horizontal-scroll-mode on')
    readline.parse_and_bind('set mark-directories on')
    readline.parse_and_bind('set mark-symlinked-directories on')
    
    # 显示所有可用的卦象
    iching.print_available_hexagrams()
    
    try:
        question = input("请输入你想问的问题：").strip()
        if not question:
            print("\n问题不能为空，请重新运行程序。")
            exit(1)
        result = iching.interpret_hexagram(question)
        
        print("\n周易卦象解析")
        print_divider()
        print(f"问题：{result['question']}")
        print_divider()
        print(f"本卦：{result['name']}")
        print(f"卦辞：{result['description']}")
        print(f"卦义：{result['meaning']}")
        print_divider()
        print("上卦：")
        print(f"  本卦：{result['upper_trigram']['name']}")
        print(f"  性质：{result['upper_trigram']['nature']}")
        print(f"  特性：{result['upper_trigram']['characteristic']}")
        print(f"  五行：{result['upper_trigram']['element']}")
        print("\n下卦：")
        print(f"  本卦：{result['lower_trigram']['name']}")
        print(f"  性质：{result['lower_trigram']['nature']}")
        print(f"  特性：{result['lower_trigram']['characteristic']}")
        print(f"  五行：{result['lower_trigram']['element']}")
        print_divider()
        print("爻位：")
        # 从上往下打印爻位
        for position, yao_info in sorted(result['yao_texts'].items(), key=lambda x: int(x[0]), reverse=True):
            print(f"{yao_info['symbol']}  第{position}爻: {yao_info['type']}")
            print(f"  {yao_info['symbol']}: {yao_info['description']}")
            print(f"  含义: {yao_info['meaning']}")
            if yao_info.get('change_meaning', '无变爻解释') != '无变爻解释':
                print(f"  变爻: {yao_info['change_meaning']}")
            print()
        
        if result.get('changed_hexagram', None):
            print_divider()
            print("变卦：")
            changed_hexagram_info = result['changed_hexagram']
            print(f"卦名：{changed_hexagram_info['name']}")
            print(f"卦辞：{changed_hexagram_info['description']}")
            print(f"卦义：{changed_hexagram_info['meaning']}")
    except Exception as e:
        print(f"\n发生错误：{e}")
        exit(1) 