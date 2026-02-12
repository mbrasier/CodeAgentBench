# CodeAgentBench

A benchmark suite for evaluating coding agent capabilities across multiple programming languages and software engineering tasks.

## Structure

```
CodeAgentBench/
├── README.md               # This file
├── run_benchmarks.py       # Master benchmark runner
├── tasks/                  # Task definitions and starter code (agents work here)
│   └── task_NN_name/
│       ├── instructions.md # What the agent must implement
│       └── <starter files> # Code stubs to fill in
└── evaluators/             # Automated test scripts (separate from tasks)
    └── task_NN_name/
        └── evaluate.*      # Runs tests and reports results
```

## Tasks

| #  | Task                    | Language   | Topic                    |
|----|-------------------------|------------|--------------------------|
| 01 | Caesar Cipher           | Python     | String Manipulation      |
| 02 | LRU Cache               | JavaScript | Data Structures          |
| 03 | Binary Search Tree      | Python     | Trees / OOP              |
| 04 | Generic Stack           | TypeScript | Generics / Type Safety   |
| 05 | Dynamic Programming     | Python     | DP Algorithms            |
| 06 | Event Emitter           | JavaScript | Event-Driven / Closures  |
| 07 | CSV Data Analysis       | Python     | File I/O / Data Analysis |
| 08 | SQL Analytics           | SQL        | Database Queries         |
| 09 | Debug & Fix             | Python     | Debugging                |
| 10 | Graph Algorithms        | Python     | Graph Theory             |
| 11 | Performance Optimization | Python     | Algorithmic Complexity   |
| 12 | Multi-Bug System Debug   | Python     | Debugging (no hints)     |
| 13 | Spec Violations          | Python     | Requirements Conformance |
| 14 | Async Error Handling     | JavaScript | Async / Promises         |
| 15 | Decorator Pitfalls       | Python     | Python-Specific Patterns |

## Running Benchmarks

Run all benchmarks:
```bash
python run_benchmarks.py
```

Run a single task:
```bash
python run_benchmarks.py --task task_01_caesar_cipher
```

Run with verbose output (shows all test lines):
```bash
python run_benchmarks.py --verbose
```

Run an evaluator directly:
```bash
python evaluators/task_01_caesar_cipher/evaluate.py
node evaluators/task_02_lru_cache/evaluate.js
```

## Evaluator Output Format

All evaluators print lines in this format and exit with code 0 (all pass) or 1 (any fail):

```
[PASS] test name
[FAIL] test name: expected <X>, got <Y>
```

Exit code `2` means the evaluator could not run (missing runtime, missing solution file, etc.).

## Adding New Tasks

1. Pick the next task number `NN` and a short name.
2. Create `tasks/task_NN_name/instructions.md` — describe what the agent must implement.
3. Add starter file(s) with function stubs and docstrings (e.g. `solution.py`, `solution.js`).
4. Create `evaluators/task_NN_name/evaluate.<ext>` that:
   - Imports/requires the solution from the task directory.
   - Runs test cases and prints `[PASS]` / `[FAIL]` lines.
   - Exits with code 0 (success) or 1 (failure).
5. Add the task to the table above.

## Requirements

- **Python tasks**: Python 3.8+
- **JavaScript tasks**: Node.js 14+
- **TypeScript task**: `ts-node` + `typescript` (`npm install -g ts-node typescript`) — skipped gracefully if unavailable
- **SQL task**: Uses Python's built-in `sqlite3` module (no extra deps)
