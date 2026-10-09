"""Normalize CSV, JSON, or JSONL input into a list of goals."""
import argparse, json, csv
from pathlib import Path
from common import clean, write_json

def main():
    parser=argparse.ArgumentParser(); parser.add_argument('--input',required=True); parser.add_argument('--output',required=True); parser.add_argument('--goal-column',default='goal'); args=parser.parse_args(); path=Path(args.input)
    if path.suffix.lower()=='.csv':
        with path.open(encoding='utf-8-sig',newline='') as f: rows=list(csv.DictReader(f))
    elif path.suffix.lower()=='.jsonl': rows=[json.loads(x) for x in path.read_text(encoding='utf-8').splitlines() if x.strip()]
    else: rows=json.loads(path.read_text(encoding='utf-8'))
    if isinstance(rows,dict): rows=rows.get('data',[])
    write_json(Path(args.output), [{'index':r.get('index',i),'text':clean(r.get(args.goal_column) or r.get('forbidden_prompt') or r.get('goal'))} for i,r in enumerate(rows) if clean(r.get(args.goal_column) or r.get('forbidden_prompt') or r.get('goal'))])

if __name__=='__main__': main()
