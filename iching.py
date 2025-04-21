import random
from typing import List, Dict, Tuple
from hexagram_data import (HEXAGRAMS_DATA, TRIGRAM_ATTRIBUTES, 
                         HEXAGRAM_NAMES, HEXAGRAM_PINYIN)

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
        rand = random.random()
        if rand < 1/16:    # 1/16
            return 6       # 老阴
        elif rand < 8/16:  # 7/16
            return 8       # 少阴
        elif rand < 13/16: # 5/16
            return 7       # 少阳
        else:             # 3/16
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
        """
        根据二进制值获取卦名
        """
        binary_str = ''.join(map(str, binary_values))
        hexagram_name = self.trigram_pairs.get(binary_str, "未知")
        if hexagram_name in HEXAGRAM_NAMES:
            return f"{hexagram_name} ({HEXAGRAM_PINYIN[hexagram_name]})"
        return hexagram_name

    def get_changed_hexagram(self, hexagram: List[int]) -> List[int]:
        """
        获取变卦的爻值
        """
        return [7 if v == 9 else 8 if v == 6 else v for v in hexagram]

    def interpret_hexagram(self, question: str) -> Dict:
        """
        根据问题生成并解释卦象
        """
        hexagram = self.generate_hexagram()
        binary_hexagram = [self.get_line_value(v) for v in hexagram]
        upper, lower = self.get_trigrams(hexagram)
        
        # 获取卦名（包含拼音）
        hexagram_name = self.get_hexagram_name(binary_hexagram)
        
        # 获取变卦
        changed_hexagram = self.get_changed_hexagram(hexagram)
        changed_binary = [self.get_line_value(v) for v in changed_hexagram]
        changed_upper, changed_lower = self.get_trigrams(changed_hexagram)
        changed_hexagram_name = self.get_hexagram_name(changed_binary)
        
        # 获取卦象详细信息
        hexagram_info = HEXAGRAMS_DATA.get(f"{upper}{lower}", {
            "name": hexagram_name,
            "description": "无描述",
            "meaning": "无解释"
        })
        
        # 获取变卦详细信息
        changed_hexagram_info = HEXAGRAMS_DATA.get(f"{changed_upper}{changed_lower}", {
            "name": changed_hexagram_name,
            "description": "无描述",
            "meaning": "无解释"
        })
        
        # 获取上下卦的属性
        upper_attributes = TRIGRAM_ATTRIBUTES.get(upper, {})
        lower_attributes = TRIGRAM_ATTRIBUTES.get(lower, {})
        
        # 生成爻位信息，包含变爻标记和传统符号
        lines = []
        for i, v in enumerate(hexagram):
            yao_type, yao_symbol = self.YAO_TYPES[v]
            line_info = {
                "position": 6 - i,  # 从下往上数
                "type": yao_type,
                "symbol": yao_symbol,
                "is_changing": self.is_changing_line(v)
            }
            lines.append(line_info)
        
        result = {
            "question": question,
            "hexagram": hexagram,
            "upper_trigram": {
                "name": upper,
                **upper_attributes
            },
            "lower_trigram": {
                "name": lower,
                **lower_attributes
            },
            "hexagram_name": hexagram_name,
            "description": hexagram_info["description"],
            "meaning": hexagram_info["meaning"],
            "lines": lines,
            "has_changes": any(self.is_changing_line(v) for v in hexagram),
            "changed_hexagram": {
                "name": changed_hexagram_name,
                "description": changed_hexagram_info["description"],
                "meaning": changed_hexagram_info["meaning"]
            } if any(self.is_changing_line(v) for v in hexagram) else None
        }
        
        return result

def print_divider():
    print("=" * 50)

def print_available_hexagrams():
    """
    打印所有可用的卦象名称及其拼音
    """
    print("\n可用的六十四卦：")
    print_divider()
    for i, name in enumerate(HEXAGRAM_NAMES, 1):
        pinyin = HEXAGRAM_PINYIN.get(name, "")
        print(f"{i:2d}. {name} ({pinyin})", end="\t")
        if i % 4 == 0:
            print()  # 换行
    print("\n")

if __name__ == "__main__":
    iching = IChing()
    
    # 显示所有可用的卦象
    print_available_hexagrams()
    
    question = input("请输入你想问的问题：")
    result = iching.interpret_hexagram(question)
    
    print("\n周易卦象解析")
    print_divider()
    print(f"问题：{result['question']}")
    print_divider()
    print(f"本卦：{result['hexagram_name']}")
    print(f"卦辞：{result['description']}")
    print(f"卦义：{result['meaning']}")
    print_divider()
    print("上卦：")
    print(f"  本卦：{result['upper_trigram']['name']}")
    print(f"  性质：{result['upper_trigram'].get('nature', '未知')}")
    print(f"  特性：{result['upper_trigram'].get('character', '未知')}")
    print(f"  五行：{result['upper_trigram'].get('element', '未知')}")
    print("\n下卦：")
    print(f"  本卦：{result['lower_trigram']['name']}")
    print(f"  性质：{result['lower_trigram'].get('nature', '未知')}")
    print(f"  特性：{result['lower_trigram'].get('character', '未知')}")
    print(f"  五行：{result['lower_trigram'].get('element', '未知')}")
    print_divider()
    print("爻位：")
    # 从上往下打印爻位
    for line in sorted(result['lines'], key=lambda x: x['position'], reverse=True):
        print(f"{line['symbol']}  第{line['position']}爻: {line['type']}")
    
    if result['has_changes']:
        print_divider()
        print("变卦：")
        print(f"卦名：{result['changed_hexagram']['name']}")
        print(f"卦辞：{result['changed_hexagram']['description']}")
        print(f"卦义：{result['changed_hexagram']['meaning']}") 