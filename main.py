import os
from flask import Flask, request, jsonify
import requests
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/"

app = Flask(__name__)


# --- 辅助函数：发送消息 ---
def send_telegram_message(chat_id, text):
    method = 'sendMessage'
    url = TELEGRAM_API_URL + method

    payload = {
        'chat_id': chat_id,
        'text': text,
        'parse_mode': 'Markdown'  # 可以使用 Markdown 格式
    }

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()  # 如果响应状态码不是 2xx，则抛出异常
        return True
    except requests.exceptions.RequestException as e:
        print(f"发送消息失败: {e}")
        return False


# --- Webhook 入口点 ---
@app.route('/webhook', methods=['POST'])
def webhook():
    if request.method == 'POST':
        # 获取 Telegram 发送的 JSON 数据
        update = request.get_json()

        # 检查是否是消息更新
        if 'message' in update:
            message = update['message']
            chat_id = message['chat']['id']
            text = message.get('text', '')  # 提取用户发送的文本，如果没有则为空字符串

            print(f"收到来自 Chat ID {chat_id} 的消息: {text}")

            # --- 简单的 Bot 逻辑 ---
            if text == '/start':
                reply_text = "*欢迎使用本 Bot！*\n请随便输入一些文字，我会原样回复给你。"
            elif text.startswith('/'):
                reply_text = "抱歉，我不明白这个命令。请尝试输入文字或 `/start`。"
            else:
                reply_text = f"你输入了: `{text}`"

            # 发送回复
            send_telegram_message(chat_id, reply_text)

        # 必须返回一个 200 OK 状态码，告诉 Telegram 你已成功接收更新
        return jsonify({'status': 'ok'}), 200

    # 非 POST 请求（例如浏览器访问），返回一个简单的信息
    return "Telegram Webhook Endpoint", 200


if __name__ == '__main__':
    # Flask 默认运行在 http://127.0.0.1:5000
    app.run(host='0.0.0.0', port=os.environ.get('PORT', 5000), debug=True)