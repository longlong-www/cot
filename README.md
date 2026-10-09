#  Prompt Construction

This repository provides a lightweight implementation of the prompt-construction procedure described in the accompanying paper. It is designed for transparent safety research and public reproducibility.


The repository contains:

1. **Simple implementation**: the executable pipeline. It constructs one prompt per benchmark goal using one actor label, one benign carrier task, and a fixed analytical template.
2. **Paper-faithful construction recipe**: the `prompts/` directory contains the auxiliary prompts needed to extend the simple pipeline into the paper's full candidate-generation and matching procedure.


## Simple implementation

```text
raw benchmark goal
        |
        +--> one benign carrier task
        |
        +--> one broad actor label
                     |
                     v
             fixed analytical template
                     |
                     v
                final prompt
```

The construction stages are:

- `step1_refine.py`: rewrites one raw goal as one benign, defensive, or educational carrier task;
- `step2_badman.py`: assigns one broad actor label related to the raw goal;
- `step3_build_prompt.py`: combines both fields into the final three-stage analytical prompt.

Run the complete pipeline with:

```bash
python run.py --input goals.json --output output/final_prompts.json --goal-column goal
```

The input may be CSV, JSON, or JSONL. The output contains the source index, original goal, generated carrier task, actor label, and final prompt.

## Paper-faithful construction

The paper describes a more complete procedure in which an auxiliary model performs candidate generation and selection:

```text
G -> generate candidate roles R -> select R*
  -> generate carrier-task candidates T conditioned on R*
  -> select (R*, T*) by narrative matching
  -> apply the three-stage template
```

Here, `G` is the original goal, `R` is the role candidate set, `R*` is the selected role, `T` is the carrier-task candidate set, and `T*` is the selected task.

The corresponding English auxiliary prompts are in `prompts/`:

```text
prompts/
├── 01_generate_role_candidates.txt
├── 02_select_best_role.txt
├── 03_generate_carrier_tasks.txt
└── 04_select_matched_task.txt
```

## Setup

```bash
python -m pip install -r requirements.txt
copy .env.example .env
```

Set `LLM_API_KEY` in `.env`. Never commit `.env` or real API keys.

## Scope and safety

The public templates are written for defensive safety analysis and exclude operational harmful instructions, evasion methods, payloads, recipes, code, target selection, and executable wrongdoing.
