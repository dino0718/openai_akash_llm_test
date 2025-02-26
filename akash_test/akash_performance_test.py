import os
import time
from dotenv import load_dotenv
from openai import OpenAI
from typing import List, Dict
import json
import pandas as pd
from datetime import datetime

load_dotenv()

def load_models() -> List[str]:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    model_file = os.path.join(current_dir, 'modle.txt')
    with open(model_file, 'r') as f:
        return [line.strip() for line in f if line.strip()]

def test_model_performance(model: str, test_cases: List[str], temperature: float = 0.7) -> Dict:
    client = OpenAI(
        api_key=os.getenv("AKASH_API_KEY"),
        base_url="https://chatapi.akash.network/api/v1"
    )
    
    results = {
        'model': model,
        'temperature': temperature,
        'tests': []
    }
    
    for case in test_cases:
        start_time = time.time()
        try:
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": "你是一位智能助理，請使用繁體中文回覆"},
                    {"role": "user", "content": case}
                ],
                temperature=temperature
            )
            
            end_time = time.time()
            results['tests'].append({
                'prompt': case,
                'response': response.choices[0].message.content,
                'response_time': end_time - start_time,
                'success': True
            })
        except Exception as e:
            results['tests'].append({
                'prompt': case,
                'error': str(e),
                'success': False
            })
            
    return results

def save_results_to_csv(all_results: List[Dict], filename: str = None):
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"akash_test_results_{timestamp}.csv"
    
    current_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(current_dir, filename)
    
    rows = []
    for result in all_results:
        model = result['model']
        temperature = result['temperature']
        
        for test in result['tests']:
            row = {
                'model': model,
                'temperature': temperature,
                'prompt': test['prompt'],
                'success': test['success']
            }
            
            if test['success']:
                row.update({
                    'response': test['response'],
                    'response_time': test['response_time']
                })
            else:
                row.update({
                    'response': test.get('error', 'Unknown error'),
                    'response_time': None
                })
            
            rows.append(row)
    
    df = pd.DataFrame(rows)
    df.to_csv(csv_path, index=False, encoding='utf-8-sig')
    
    print(f"\n測試結果儲存位置:")
    print(f"完整路徑: {csv_path}")

if __name__ == "__main__":
    test_cases = [
        "解釋什麼是人工智能",
        "用台灣俚語翻譯：風雨無阻",
        "寫一個五言絕句",
        "分析台灣的科技產業現況"
    ]
    
    models = load_models()
    all_results = []
    
    for model in models:
        print(f"\n正在測試模型: {model}")
        try:
            results = test_model_performance(model, test_cases)
            all_results.append(results)
            print(f"測試完成: {model}")
            print(json.dumps(results, ensure_ascii=False, indent=2))
        except Exception as e:
            print(f"測試失敗: {model}")
            print(f"錯誤訊息: {str(e)}")
    
    # 儲存結果到 CSV
    save_results_to_csv(all_results)
