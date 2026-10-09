import json
import re
import time
from openai import OpenAI
from dotenv import load_dotenv
from pathlib import Path
import os

ROOT = Path(__file__).resolve().parent
load_dotenv(ROOT / '.env')

def clean(value, limit=800):
    return re.sub(r'\s+', ' ', str(value or '')).strip()[:limit]

def client():
    key = os.getenv('LLM_API_KEY', '')
    if not key:
        raise RuntimeError('LLM_API_KEY is not set. Copy .env.example to .env.')
    return OpenAI(api_key=key, base_url=os.getenv('LLM_BASE_URL', 'https://api.openai.com/v1'), timeout=60.0)

def ask_json(api, prompt):
    last_error = None
    for attempt in range(3):
        try:
            response = api.chat.completions.create(
                model=os.getenv('LLM_MODEL', 'gpt-4o-mini'),
                messages=[{'role': 'user', 'content': prompt}],
                temperature=float(os.getenv('LLM_TEMPERATURE', '0.4')),
                response_format={'type': 'json_object'})
            data = json.loads(response.choices[0].message.content or '{}')
            if isinstance(data, list): return data
            for key in ('items', 'candidates', 'result'):
                if isinstance(data.get(key), list): return data[key]
            return [data]
        except Exception as error:
            last_error = error
            time.sleep(2 ** attempt)
    raise RuntimeError(f'LLM request failed: {last_error}')

def read_records(path):
    if path.suffix.lower() == '.csv':
        import csv
        with path.open(encoding='utf-8-sig', newline='') as handle:
            return list(csv.DictReader(handle))
    if path.suffix.lower() == '.jsonl':
        return [json.loads(line) for line in path.read_text(encoding='utf-8').splitlines() if line.strip()]
    data = json.loads(path.read_text(encoding='utf-8'))
    return data if isinstance(data, list) else data.get('data', [])

def write_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')
