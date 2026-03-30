import os
from openai import AzureOpenAI
from flask import Flask, request, render_template

app = Flask(__name__)

# --- Azure OpenAI の設定 (あなたのコードを反映) ---
endpoint = os.getenv('OpenAI_ENDPOINT')
model_name = os.getenv('OpenAI_DEPLOY_NAME') # Renderの設定画面で登録する名前
subscription_key = os.getenv('OpenAI_API_KEY')
api_version = "2024-12-01-preview"

client = AzureOpenAI(
    api_version=api_version,
    azure_endpoint=endpoint,
    api_key=subscription_key,
)

# --- 1. 辞書データ (課題の要件) ---
zh_ko_dict = {
    "你好": "안녕하세요", "謝謝": "감사합니다", "對不起": "죄송합니다",
    "老師": "선생님", "學生": "학생", "朋友": "친구",
    "家人": "가족", "愛": "사랑", "早安": "좋은 ア침", "晚安": "안녕히 주무세요"
}

zh_en_dict = {
    "你好": "Hello", "蘋果": "apple", "香蕉": "banana",
    "電腦": "computer", "字典": "dictionary", "科學": "science",
    "學習": "learning", "快樂": "happy", "世界": "world", "程式": "program"
}

# --- 2. ページ表示のロジック ---
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['GET', 'POST'])
def ask():
    answer = ""
    question = ""
    dict_type = "zh_ko"

    if request.method == 'POST':
        question = request.form.get('question', '').strip()
        dict_type = request.form.get('dict_type', 'zh_ko')
        
        # 1. まず自前辞書から探す (75点レベル)
        if dict_type == "zh_ko":
            answer = zh_ko_dict.get(question)
            target_lang = "韓文"
        else:
            answer = zh_en_dict.get(question)
            target_lang = "英文"

        # 2. 辞書になければAIに聞く (90点レベルの処理)
        if not answer and question:
            try:
                response = client.chat.completions.create(
                    model=model_name,
                    messages=[
                        {"role": "system", "content": "你是一個專業の翻訳助手。"},
                        {"role": "user", "content": f"請把「{question}」翻訳成{target_lang}，並提供簡短解釋(30字以内)及一個例句。"}
                    ],
                    max_tokens=150
                )
                answer = response.choices[0].message.content.strip()
            except Exception as e:
                answer = f"AI 暫時無法回應，錯誤：{str(e)}"
                
    return render_template('ask.html', question=question, answer=answer, dict_type=dict_type)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False)
