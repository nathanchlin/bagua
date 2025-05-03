"""
测试易经数据模块的功能
"""
from hexagram_data import HEXAGRAM_NAMES, HEXAGRAM_PINYIN, HEXAGRAMS_DATA, TRIGRAM_ATTRIBUTES

def test_data_consistency():
    """测试数据一致性"""
    print("测试数据一致性...")
    
    # 测试卦名数量
    assert len(HEXAGRAM_NAMES) == 64, f"卦名数量应为64，实际为{len(HEXAGRAM_NAMES)}"
    print("✓ 卦名数量正确")
    
    # 测试拼音对照完整性
    assert len(HEXAGRAM_PINYIN) == len(HEXAGRAM_NAMES), "拼音对照表与卦名数量不一致"
    for name in HEXAGRAM_NAMES:
        assert name in HEXAGRAM_PINYIN, f"卦名 {name} 缺少拼音对照"
    print("✓ 拼音对照完整")
    
    # 测试八卦属性
    assert len(TRIGRAM_ATTRIBUTES) == 8, "八卦属性数量不正确"
    for trigram in TRIGRAM_ATTRIBUTES:
        assert all(key in TRIGRAM_ATTRIBUTES[trigram] for key in ["nature", "character", "element"]), \
            f"八卦 {trigram} 属性不完整"
    print("✓ 八卦属性完整")
    
    # 打印一些示例数据
    print("\n示例数据:")
    print(f"第一卦: {HEXAGRAM_NAMES[0]} ({HEXAGRAM_PINYIN[HEXAGRAM_NAMES[0]]})")
    if HEXAGRAMS_DATA.get("乾乾"):
        print(f"卦辞: {HEXAGRAMS_DATA['乾乾']['description']}")
        print(f"含义: {HEXAGRAMS_DATA['乾乾']['meaning']}")
        if 'yao_texts' in HEXAGRAMS_DATA['乾乾']:
            print("\n爻辞示例:")
            for yao_num, yao_data in HEXAGRAMS_DATA['乾乾']['yao_texts'].items():
                print(f"{yao_data['symbol']}: {yao_data['description']}")

if __name__ == "__main__":
    test_data_consistency() 