import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables from .env file
load_dotenv()

# Set the OPENAI_API_KEY from the .env file
os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')

client = OpenAI()

try:
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  # 修正模型名稱
        messages=[
            {"role": "system", "content": "你是一位智能助理，請使用繁體中文回覆"},
            {"role": "user", "content": "您好！"}
        ]
    )
    print(response.choices[0].message.content)
except Exception as e:
    print(f"發生錯誤: {str(e)}")