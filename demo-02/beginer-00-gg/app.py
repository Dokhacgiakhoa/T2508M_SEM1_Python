# chat.py — Gemini version
import os
import sys
import google.generativeai as genai

API_KEY = "AIzaSyBvPnOH52fOEmJ0zrzV8rISGWUig9kqBIk"

genai.configure(api_key=API_KEY)

SYSTEM_PROMPT = "Bạn là trợ lý hữu ích, trả lời ngắn gọn và chính xác."

# Khởi tạo model + system prompt
model = genai.GenerativeModel(
    model_name="gemini-2.5-flash",             
    system_instruction=SYSTEM_PROMPT
)

# Tạo phiên chat có lưu ngữ cảnh
chat_session = model.start_chat(history=[])

def ask_llm(user_message: str) -> str:
    resp = chat_session.send_message(user_message)
    return (resp.text or "").strip()

def main():
    print("=== Simple Chat (Ctrl+C để thoát) ===")
    while True:
        try:
            user = input("\nBạn: ").strip()
            if not user:
                continue
            reply = ask_llm(user)
            print(f"Trợ lý: {reply}")
        except (KeyboardInterrupt, EOFError):
            print("\nTạm biệt!")
            break

if __name__ == "__main__":
    main()
