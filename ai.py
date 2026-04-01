import requests

API_KEY = "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"

def chat_with_ai(message):
    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "openai/gpt-3.5-turbo",
                "messages": [
                    {"role": "system", "content": "You are a professional gym trainer."},
                    {"role": "user", "content": message}
                ]
            }
        )

        # 🔥 DEBUG PRINT (important)
        print("STATUS:", response.status_code)
        print("RESPONSE:", response.text)

        if response.status_code != 200:
            return f"HTTP Error: {response.status_code} | {response.text}"

        data = response.json()

        return data["choices"][0]["message"]["content"]
    
    except Exception as e:
        return f"Error: {str(e)}"
    