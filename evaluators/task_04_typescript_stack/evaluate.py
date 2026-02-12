#!/usr/bin/env python3
"""
Evaluator for Task 04: TypeScript Generic Stack.

Tries to run test_stack.ts using ts-node (local then global).
Exits with code 2 if TypeScript tooling is not available.
"""
import subprocess
import sys
import os

EVAL_DIR = os.path.dirname(os.path.abspath(__file__))
TEST_FILE = os.path.join(EVAL_DIR, 'test_stack.ts')
TASK_DIR = os.path.join(EVAL_DIR, '..', '..', 'tasks', 'task_04_typescript_stack')
SOLUTION_FILE = os.path.join(TASK_DIR, 'stack.ts')


def solution_exists():
    if not os.path.exists(SOLUTION_FILE):
        print("[FAIL] stack.ts not found")
        return False
    return True


def try_run(cmd):
    """Run cmd and return CompletedProcess, or None if the binary is missing."""
    try:
        return subprocess.run(cmd, capture_output=True, text=True, timeout=60,
                              cwd=EVAL_DIR)
    except FileNotFoundError:
        return None
    except subprocess.TimeoutExpired:
        print("[FAIL] ts-node timed out after 60s")
        sys.exit(1)


def main():
    if not solution_exists():
        sys.exit(1)

    result = None

    # 1. Try local ts-node (project node_modules)
    local_tsnode = os.path.join(EVAL_DIR, '..', '..', 'node_modules', '.bin', 'ts-node')
    if os.path.exists(local_tsnode):
        result = try_run([local_tsnode, TEST_FILE])

    # 2. Try global ts-node
    if result is None:
        result = try_run(['ts-node', TEST_FILE])

    # 3. Try via npx (downloads if missing, slower)
    if result is None:
        result = try_run(['npx', '--yes', 'ts-node', TEST_FILE])

    if result is None:
        print("[SKIP] ts-node not found. Install with:  npm install -g ts-node typescript")
        sys.exit(2)

    print(result.stdout, end='')
    if result.stderr.strip() and result.returncode != 0:
        for line in result.stderr.strip().splitlines()[:10]:
            print(f"STDERR: {line}", file=sys.stderr)

    sys.exit(result.returncode)


if __name__ == "__main__":
    main()
