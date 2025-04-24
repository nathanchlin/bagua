from flask import Flask, render_template, request, jsonify
from iching import IChing

app = Flask(__name__)
iching = IChing()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/cast', methods=['POST'])
def cast():
    question = request.form.get('question', '').strip()
    if not question:
        return jsonify({'error': '问题不能为空'}), 400
    
    try:
        result = iching.interpret_hexagram(question)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/hexagrams')
def hexagrams():
    """返回所有可用的卦象列表"""
    from hexagram_data import HEXAGRAM_MAPS, HEXAGRAM_PINYIN
    hexagrams_list = []
    for i, (key, name) in enumerate(HEXAGRAM_MAPS.items(), 1):
        hexagrams_list.append({
            'id': i,
            'key': key,
            'name': name,
            'pinyin': HEXAGRAM_PINYIN.get(name, '')
        })
    return jsonify(hexagrams_list)

if __name__ == '__main__':
    app.run(debug=True, port=5000) 