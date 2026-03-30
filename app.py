from flask import Flask, request, render_template
import os
from openai import AzureOpenAI  # 修正：匯入正確的類別

app = Flask(__name__)

# 從環境變數讀取設定
endpoint = os.getenv('OpenAI_ENDPOINT')
model_name = os.getenv('OpenAI_DEPLOY_NAME')
subscription_key = os.getenv('OpenAI_API_KEY')

# 修正：AI客戶端的初期化（補上括號與正確結構）
client = AzureOpenAI(
    api_version="2024-12-01-preview",
    azure_endpoint=endpoint,
    api_key=subscription_key
)

# 1. 中韓字典
zh_ko_dict = {
    "你好": "안녕하세요",
    "謝謝": "감사합니다",
    "對不起": "죄송합니다",
    "老師": "선생님",
    "學生": "학생",
    "朋友": "친구",
    "家人": "가족",
    "愛": "사랑",
    "早安": "좋은 아침",
    "晚安": "안녕히 주무세요"
}

# 2. 中英字典
zh_en_dict = {
    "你好": "Hello",
    "蘋果": "apple",
    "香蕉": "banana",
    "電腦": "computer",
    "字典": "dictionary",
    "科學": "science",
    "學習": "learning",
    "快樂": "happy",
    "世界": "world",
    "程式": "python/program",
    "海洋": "ocean"
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['GET', 'POST'])
def ask():
    answer = ""
    question = ""
    dict_type = "zh_ko"  # 預設選中韓

    if request.method == 'POST':
        question = request.form.get('question', '').strip()
        dict_type = request.form.get('dict_type', 'zh_ko')
        
        # 根據選單選擇對應字典
        if dict_type == "zh_ko":
            answer = zh_ko_dict.get(question)
        else:
            answer = zh_en_dict.get(question)

        # 修正：縮排需在 POST 區塊內
        # 找不到資料時，調用 AI
        if not answer and question:
            try:
                response = client.chat.completions.create(
                    model=model_name,
                    messages=[
                        {"role": "user", "content": f"請翻譯「{question}」並簡短解釋。"}
                    ],
                    max_tokens=100
                )
                answer = response.choices[0].message.content.strip()
            except Exception as e:
                answer = f"AI錯誤: {str(e)}"
                
    return render_template('ask.html', question=question, answer=answer, dict_type=dict_type)

if __name__ == '__main__':
    # Render 部署建議關閉 debug=False
    app.run(host='0.0.0.0', port=5000)
