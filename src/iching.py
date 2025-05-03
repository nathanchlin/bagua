import os
import sys
import random
import readline  # 添加readline支持
from typing import List, Dict, Tuple
from hexagram_data import (HEXAGRAMS_DATA, TRIGRAM_ATTRIBUTES, 
                         HEXAGRAM_NAMES, HEXAGRAM_PINYIN, HEXAGRAM_MAPS)

# Add the current directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

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
        # 老阳(9): 3/16, 少阳(7): 5/16, 少阴(8): 7/16, 老阴(6): 1/16
        # 为了调试，暂时增加变爻的概率
        rand = random.random()
        print(f"随机数: {rand}")  # 调试日志
        
        if rand < 0.3:    # 增加老阴的概率
            print("生成老阴(6)")  # 调试日志
            return 6       # 老阴
        elif rand < 0.5:  # 减少少阴的概率
            print("生成少阴(8)")  # 调试日志
            return 8       # 少阴
        elif rand < 0.7:  # 减少少阳的概率
            print("生成少阳(7)")  # 调试日志
            return 7       # 少阳
        else:             # 增加老阳的概率
            print("生成老阳(9)")  # 调试日志
            return 9       # 老阳

    def is_changing_line(self, value: int) -> bool:
        """
        判断是否是变爻（老阳或老阴）
        """
        is_changing = value in [6, 9]
        yao_type = self.YAO_TYPES.get(value, ('未知', '未知'))[0]
        print(f"判断变爻: 值={value}, 类型={yao_type}, 是否变爻={is_changing}")  # 调试日志
        return is_changing

    def get_line_value(self, value: int) -> int:
        """
        获取爻的阴阳值（0为阴，1为阳）
        """
        result = 1 if value in [7, 9] else 0
        print(f"爻值: {value} -> 阴阳值: {result}")  # 调试日志
        return result

    def generate_hexagram(self) -> List[int]:
        """
        生成完整的六爻卦象
        """
        print("\n=== 开始生成六爻 ===")  # 调试日志
        hexagram = []
        for i in range(6):
            value = self.cast_yarrow_stalks()
            hexagram.append(value)
            yao_type, yao_symbol = self.YAO_TYPES.get(value, ('未知', '未知'))
            print(f"生成第{i+1}爻: 值={value}, 类型={yao_type}, 符号={yao_symbol}")  # 调试日志
        
        print(f"生成的完整卦象: {hexagram}")  # 调试日志
        return hexagram

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

    def get_hexagram_info(self, hexagram_key: str) -> dict:
        """根据卦象键获取卦象的详细信息"""
        print(f"获取卦象信息，键: {hexagram_key}")  # 调试日志
        hexagram_name = HEXAGRAM_MAPS.get(hexagram_key)
        print(f"卦名: {hexagram_name}")  # 调试日志
        if not hexagram_name:
            print("未找到卦名")  # 调试日志
            return {
                "name": "未知卦",
                "description": "暂无卦辞",
                "meaning": "暂无卦义"
            }
        
        # 从HEXAGRAMS_DATA中获取卦象的详细信息
        hexagram_data = HEXAGRAMS_DATA.get(hexagram_key, {})  # 使用原始键查找
        print(f"卦象数据: {hexagram_data}")  # 调试日志
        
        return {
            "name": hexagram_name,
            "description": hexagram_data.get("description", "暂无卦辞"),
            "meaning": hexagram_data.get("meaning", "暂无卦义")
        }

    def get_trigram_info(self, trigram_values: List[int]) -> dict:
        """根据三爻值获取八卦的详细信息"""
        trigram = tuple(trigram_values)
        trigram_name = self.TRIGRAMS.get(trigram)
        if not trigram_name:
            return {
                "name": "未知",
                "nature": "暂无",
                "characteristic": "暂无",
                "element": "暂无"
            }
        
        # 从TRIGRAM_ATTRIBUTES中获取八卦的详细信息
        trigram_attr = TRIGRAM_ATTRIBUTES.get(trigram_name, {})
        
        return {
            "name": trigram_name,
            "nature": trigram_attr.get("nature", "暂无"),
            "characteristic": trigram_attr.get("characteristic", "暂无"),
            "element": trigram_attr.get("element", "暂无")
        }

    def get_yao_type(self, value: int) -> str:
        """根据爻值获取爻的类型"""
        return self.YAO_TYPES.get(value, ("未知", "未知"))[0]

    def get_yao_symbol(self, value: int) -> str:
        """根据爻值获取爻的符号"""
        return self.YAO_TYPES.get(value, ("未知", "未知"))[1]

    def get_yao_text(self, hexagram_key: str, position: int) -> str:
        """获取爻辞"""
        hexagram_name = HEXAGRAM_MAPS.get(hexagram_key)
        if not hexagram_name:
            return "暂无爻辞"
        
        hexagram_data = HEXAGRAMS_DATA.get(hexagram_key, {})
        yao_texts = hexagram_data.get("yao_texts", {})
        yao_data = yao_texts.get(str(position), {})
        return yao_data.get("description", "暂无爻辞")

    def get_yao_meaning(self, hexagram_key: str, position: int) -> str:
        """获取爻义"""
        hexagram_name = HEXAGRAM_MAPS.get(hexagram_key)
        if not hexagram_name:
            return "暂无爻义"
        
        hexagram_data = HEXAGRAMS_DATA.get(hexagram_key, {})
        yao_texts = hexagram_data.get("yao_texts", {})
        yao_data = yao_texts.get(str(position), {})
        return yao_data.get("meaning", "暂无爻义")

    def get_changed_hexagram(self, hexagram: List[int]) -> List[int]:
        """
        获取变卦的爻值
        规则：
        - 老阳（9）变为老阴（6）
        - 老阴（6）变为老阳（9）
        - 少阳（7）和少阴（8）保持不变
        """
        print(f"原始卦象: {hexagram}")  # 调试日志
        changed = [6 if v == 9 else 9 if v == 6 else v for v in hexagram]
        print(f"变卦结果: {changed}")   # 调试日志
        return changed

    def interpret_hexagram(self, question):
        """根据问题生成卦象并解释
        
        变爻规则：
        1. 六爻皆不变：占本卦彖辞，而以内卦为贞，外卦为悔
        2. 一爻变：以本卦变爻辞占
        3. 二爻变：以本卦二变爻辞占，仍以上爻为主
        4. 三爻变：占本卦及之卦之彖辞，而以本卦为贞，之卦为悔
        5. 四爻变：以之卦二不变爻占，仍以下爻为主
        6. 五爻变：以之卦不变爻占
        7. 六爻变：若为《乾》之《坤》或《坤》之《乾》，则占"二用"；余卦占之卦彖辞
        """
        # 生成卦象
        hexagram = self.generate_hexagram()
        print(f"原始卦象: {hexagram}")
        
        # 获取变卦
        changed_hexagram = self.get_changed_hexagram(hexagram)
        print(f"变卦结果: {changed_hexagram}")
        
        # 计算变爻数量
        changing_lines = []
        for i, value in enumerate(hexagram):
            if self.is_changing_line(value):
                changing_lines.append(i + 1)  # 爻位从1开始计数
        changing_count = len(changing_lines)
        print(f"变爻数量: {changing_count}")
        print(f"变爻位置: {changing_lines}")
        
        # 获取本卦信息
        binary_values = [self.get_line_value(v) for v in hexagram]
        print(f"二进制值: {binary_values}")
        upper_trigram = tuple(binary_values[3:])  # 上卦是第4-6爻
        lower_trigram = tuple(binary_values[:3])  # 下卦是第1-3爻
        print(f"上卦三爻: {upper_trigram}")
        print(f"下卦三爻: {lower_trigram}")
        upper_name = self.TRIGRAMS.get(upper_trigram)
        lower_name = self.TRIGRAMS.get(lower_trigram)
        print(f"上卦名称: {upper_name}")
        print(f"下卦名称: {lower_name}")
        hexagram_key = f"{upper_name}{lower_name}"
        print(f"卦象键: {hexagram_key}")
        hexagram_info = self.get_hexagram_info(hexagram_key)
        print(f"卦象信息: {hexagram_info}")
        
        # 获取变卦信息
        changed_binary_values = [self.get_line_value(v) for v in changed_hexagram]
        print(f"变卦二进制值: {changed_binary_values}")
        changed_upper_trigram = tuple(changed_binary_values[3:])  # 上卦是第4-6爻
        changed_lower_trigram = tuple(changed_binary_values[:3])  # 下卦是第1-3爻
        print(f"变卦上卦三爻: {changed_upper_trigram}")
        print(f"变卦下卦三爻: {changed_lower_trigram}")
        changed_upper_name = self.TRIGRAMS.get(changed_upper_trigram)
        changed_lower_name = self.TRIGRAMS.get(changed_lower_trigram)
        print(f"变卦上卦名称: {changed_upper_name}")
        print(f"变卦下卦名称: {changed_lower_name}")
        changed_hexagram_key = f"{changed_upper_name}{changed_lower_name}"
        print(f"变卦卦象键: {changed_hexagram_key}")
        changed_hexagram_info = self.get_hexagram_info(changed_hexagram_key)
        print(f"变卦卦象信息: {changed_hexagram_info}")
        
        # 获取上下卦信息
        upper_trigram_info = self.get_trigram_info(list(upper_trigram))
        lower_trigram_info = self.get_trigram_info(list(lower_trigram))
        print(f"上卦信息: {upper_trigram_info}")
        print(f"下卦信息: {lower_trigram_info}")
        
        # 获取爻辞信息
        yao_texts = {}
        for i, value in enumerate(hexagram):
            position = i + 1
            yao_type = self.get_yao_type(value)
            yao_texts[str(position)] = {
                'type': yao_type,
                'symbol': self.get_yao_symbol(value),
                'description': self.get_yao_text(hexagram_key, position),
                'meaning': self.get_yao_meaning(hexagram_key, position),
                'change_meaning': self.get_yao_meaning(changed_hexagram_key, position) if self.is_changing_line(value) else None
            }
        print(f"爻辞信息: {yao_texts}")
        
        # 根据变爻规则生成解卦信息
        interpretation = ""
        if changing_count == 0:
            # 六爻皆不变：占本卦彖辞，而以内卦为贞，外卦为悔
            interpretation = f"本卦六爻皆不变，以内卦为贞，外卦为悔。\n"
            interpretation += f"内卦（下卦）代表问卦者：{lower_trigram_info['name']}（{lower_trigram_info['nature']}）\n"
            interpretation += f"外卦（上卦）代表问卦者的对方：{upper_trigram_info['name']}（{upper_trigram_info['nature']}）"
        elif changing_count == 1:
            # 一爻变：以本卦变爻辞占
            interpretation = "本卦一爻变，以变爻辞占。\n"
            for position in changing_lines:
                yao = yao_texts[str(position)]
                interpretation += f"变爻位置：第{position}爻\n"
                interpretation += f"爻辞：{yao['description']}\n"
                interpretation += f"解释：{yao['meaning']}\n"
                interpretation += f"变爻解释：{yao['change_meaning']}\n"
        elif changing_count == 2:
            # 二爻变：以本卦二变爻辞占，仍以上爻为主
            interpretation = "本卦二爻变，以二变爻辞占，以上爻为主。\n"
            for position in sorted(changing_lines, reverse=True):
                yao = yao_texts[str(position)]
                interpretation += f"变爻位置：第{position}爻\n"
                interpretation += f"爻辞：{yao['description']}\n"
                interpretation += f"解释：{yao['meaning']}\n"
                interpretation += f"变爻解释：{yao['change_meaning']}\n"
        elif changing_count == 3:
            # 三爻变：占本卦及之卦之彖辞，而以本卦为贞，之卦为悔
            interpretation = "本卦三爻变，占本卦及之卦之彖辞。\n"
            interpretation += f"本卦（贞）代表问卦者：{hexagram_info['name']}\n"
            interpretation += f"之卦（悔）代表问卦者的对方：{changed_hexagram_info['name']}\n"
            interpretation += f"本卦卦辞：{hexagram_info['meaning']}\n"
            interpretation += f"之卦卦辞：{changed_hexagram_info['meaning']}"
        elif changing_count == 4:
            # 四爻变：以之卦二不变爻占，仍以下爻为主
            interpretation = "本卦四爻变，以之卦二不变爻占，以下爻为主。\n"
            interpretation += f"之卦：{changed_hexagram_info['name']}\n"
            for position in range(1, 7):
                if position not in changing_lines:
                    yao = yao_texts[str(position)]
                    interpretation += f"不变爻位置：第{position}爻\n"
                    interpretation += f"爻辞：{yao['description']}\n"
                    interpretation += f"解释：{yao['meaning']}\n"
        elif changing_count == 5:
            # 五爻变：以之卦不变爻占
            interpretation = "本卦五爻变，以之卦不变爻占。\n"
            interpretation += f"之卦：{changed_hexagram_info['name']}\n"
            for position in range(1, 7):
                if position not in changing_lines:
                    yao = yao_texts[str(position)]
                    interpretation += f"不变爻位置：第{position}爻\n"
                    interpretation += f"爻辞：{yao['description']}\n"
                    interpretation += f"解释：{yao['meaning']}\n"
        elif changing_count == 6:
            # 六爻变：若为《乾》之《坤》或《坤》之《乾》，则占"二用"；余卦占之卦彖辞
            if (hexagram_info['name'] == '乾' and changed_hexagram_info['name'] == '坤') or \
               (hexagram_info['name'] == '坤' and changed_hexagram_info['name'] == '乾'):
                interpretation = "本卦六爻全变，且为乾之坤或坤之乾，占'二用'。\n"
                interpretation += "特殊解释：用九，见群龙无首，吉。用六，利永贞。"
            else:
                interpretation = "本卦六爻全变，占之卦彖辞。\n"
                interpretation += f"之卦：{changed_hexagram_info['name']}\n"
                interpretation += f"之卦卦辞：{changed_hexagram_info['meaning']}"
        
        print(f"解卦信息: {interpretation}")
        
        return {
            'question': question,
            'name': hexagram_info['name'],
            'description': hexagram_info['description'],
            'meaning': hexagram_info['meaning'],
            'hexagram': hexagram,
            'changing_count': changing_count,
            'changing_lines': changing_lines,
            'changed_hexagram': changed_hexagram_info,
            'upper_trigram': upper_trigram_info,
            'lower_trigram': lower_trigram_info,
            'yao_texts': yao_texts,
            'interpretation': interpretation
        }

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