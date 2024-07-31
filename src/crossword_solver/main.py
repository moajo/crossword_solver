import openai
import os

# 環境変数からAPIキーの設定
openai.api_key = os.getenv("OPENAI_API_KEY")

# GPTによる応答生成
prompt = "以下の条件の下でおいしい食べ物を教えてください。\n条件1:和食\n条件2:甘い"
response = openai.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": prompt},
    ],
    temperature=0,
)

# 応答の表示
text = response.choices[0].message.content
print(text)

# import requests

# url = "https://example.com"
# response = requests.get(url)
