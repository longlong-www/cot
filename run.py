"""Run the recommended simple three-step pipeline."""
import argparse
import subprocess
import sys
from pathlib import Path

def main():
    parser = argparse.ArgumentParser(); parser.add_argument('--input', required=True); parser.add_argument('--output', required=True); parser.add_argument('--goal-column', default='goal'); args = parser.parse_args()
    root = Path(__file__).parent; output = Path(args.output); output.parent.mkdir(parents=True, exist_ok=True)
    def call(script, *extra): subprocess.run([sys.executable, str(root / script), *map(str, extra)], check=True)
    goals = output.with_name('normalized_goals.json'); refined = output.with_name('refined.json'); badman = output.with_name('badman.json')
    call('step1_load_goals.py', '--input', args.input, '--output', goals, '--goal-column', args.goal_column)
    call('step1_refine.py', '--input', goals, '--output', refined)
    call('step2_badman.py', '--input', goals, '--output', badman)
    call('step3_build_prompt.py', '--refined', refined, '--badman', badman, '--output', output)

if __name__ == '__main__': main()
