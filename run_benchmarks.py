#!/usr/bin/env python3
"""Master benchmark runner for CodeAgentBench.

Usage:
    python run_benchmarks.py                      # run all tasks
    python run_benchmarks.py --task task_01       # run a specific task (partial name)
    python run_benchmarks.py --verbose            # show every test line
"""

import argparse
import subprocess
import sys
import os
from pathlib import Path


def find_evaluators(bench_dir: Path, task_filter: str = None):
    """Return list of (task_name, evaluator_path) sorted by task name."""
    evaluators_dir = bench_dir / "evaluators"
    if not evaluators_dir.exists():
        return []

    result = []
    for task_dir in sorted(evaluators_dir.iterdir()):
        if not task_dir.is_dir():
            continue
        if task_filter and task_filter not in task_dir.name:
            continue
        for filename in ["evaluate.py", "evaluate.js", "evaluate.sh"]:
            eval_file = task_dir / filename
            if eval_file.exists():
                result.append((task_dir.name, eval_file))
                break

    return result


def run_evaluator(eval_file: Path):
    """Run an evaluator script, returning (stdout, stderr, returncode)."""
    ext = eval_file.suffix
    if ext == ".py":
        cmd = [sys.executable, str(eval_file)]
    elif ext == ".js":
        cmd = ["node", str(eval_file)]
    elif ext == ".sh":
        cmd = ["bash", str(eval_file)]
    else:
        return "", f"Unknown evaluator extension: {ext}", 2

    try:
        proc = subprocess.run(
            cmd, capture_output=True, text=True,
            cwd=str(eval_file.parent), timeout=60
        )
        return proc.stdout, proc.stderr, proc.returncode
    except FileNotFoundError as e:
        return "", f"Runtime not found: {e}", 2
    except subprocess.TimeoutExpired:
        return "", "Evaluator timed out after 60s", 2


def parse_results(output: str):
    """Parse [PASS] / [FAIL] lines from evaluator output."""
    passed, failed = [], []
    for line in output.splitlines():
        stripped = line.strip()
        if stripped.startswith("[PASS]"):
            passed.append(stripped[7:])
        elif stripped.startswith("[FAIL]"):
            failed.append(stripped[7:])
    return passed, failed


def main():
    parser = argparse.ArgumentParser(description="Run CodeAgentBench evaluations")
    parser.add_argument("--task", help="Filter to tasks whose name contains this string")
    parser.add_argument("--verbose", "-v", action="store_true",
                        help="Show every [PASS]/[FAIL] line")
    args = parser.parse_args()

    bench_dir = Path(__file__).parent
    evaluators = find_evaluators(bench_dir, args.task)

    if not evaluators:
        print("No evaluators found" + (f" matching '{args.task}'" if args.task else "") + ".")
        sys.exit(1)

    print(f"Running {len(evaluators)} task(s)...\n")

    summary_rows = []
    total_passed = total_failed = 0

    for task_name, eval_file in evaluators:
        print(f"  {task_name}")
        stdout, stderr, returncode = run_evaluator(eval_file)

        if returncode == 2:
            # Runtime unavailable or hard error
            msg = stderr.strip().splitlines()[0] if stderr.strip() else "could not run"
            print(f"    [SKIP] {msg}")
            summary_rows.append((task_name, 0, 0, "SKIP"))
            continue

        passed, failed = parse_results(stdout)

        if args.verbose or failed:
            for line in stdout.strip().splitlines():
                print(f"    {line}")
            if stderr.strip() and (args.verbose or returncode != 0):
                for line in stderr.strip().splitlines()[:5]:
                    print(f"    STDERR: {line}")
        else:
            print(f"    {len(passed)} passed, {len(failed)} failed")

        total_passed += len(passed)
        total_failed += len(failed)
        status = "OK" if not failed else "FAIL"
        summary_rows.append((task_name, len(passed), len(failed), status))

    # Summary table
    print("\n" + "=" * 65)
    print("SUMMARY")
    print("=" * 65)
    print(f"{'Task':<38} {'Pass':>6} {'Fail':>6} {'Status':>8}")
    print("-" * 65)
    for name, p, f, status in summary_rows:
        print(f"{name:<38} {p:>6} {f:>6} {status:>8}")
    print("-" * 65)
    print(f"{'TOTAL':<38} {total_passed:>6} {total_failed:>6}")
    print()

    sys.exit(0 if total_failed == 0 else 1)


if __name__ == "__main__":
    main()
