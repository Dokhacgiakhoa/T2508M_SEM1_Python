# app.py
from flask import Flask, request, jsonify, make_response
from flask_cors import CORS, cross_origin
import google.generativeai as genai
import os, sys, traceback

app = Flask(__name__)
app.url_map.strict_slashes = False  # tránh redirect /chat <-> /chat/

# CORS cho riêng /chat, /ping
CORS(
    app,
    resources={r"/chat": {"origins": "*"}, r"/ping": {"origins": "*"}},
    methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"],
    supports_credentials=False,
    max_age=86400,
)

SYSTEM_PROMPT = "Bạn là trợ lý hữu ích, trả lời ngắn gọn và chính xác."

API_KEY = "AIzaSyBvPnOH52fOEmJ0zrzV8rISGWUig9kqBIk"

genai.configure(api_key=API_KEY)

model = genai.GenerativeModel(
    model_name="gemini-2.5-flash",    
    system_instruction=SYSTEM_PROMPT
)

# Tạo phiên chat có lưu ngữ cảnh
chat_session = model.start_chat(history=[])

@app.route("/ping", methods=["GET", "OPTIONS"])
@cross_origin(origins="*")
def ping():
    if request.method == "OPTIONS":
        return ("", 204)
    return jsonify({"ok": True})

@app.route("/chat", methods=["POST", "OPTIONS"])
@cross_origin(origins="*")
def chat():
    if request.method == "OPTIONS":
        return ("", 204)

    data = request.get_json(silent=True) or {}
    user_message = (data.get("message") or "").strip()

    if not user_message:
        return jsonify({"reply": "Bạn hãy nhập nội dung cần hỏi nhé."})

    # Gọi Gemini
    try:
        resp = chat_session.send_message(
            user_message
        )
        reply_text = (resp.text or "").strip()
        print(f"User: {user_message}\nAI: {reply_text}\n")
        return jsonify({"reply": reply_text})
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

# đảm bảo kể cả khi có exception vẫn trả JSON + header CORS
@app.errorhandler(Exception)
def handle_error(e):
    traceback.print_exc()
    resp = make_response(jsonify({"error": str(e)}), 500)
    resp.headers["Access-Control-Allow-Origin"] = "*"
    resp.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    resp.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    return resp

if __name__ == "__main__":
    # đổi port tại đây nếu 5001 bận
    app.run(host="127.0.0.1", port=5001, debug=True)
