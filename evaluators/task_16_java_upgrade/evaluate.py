#!/usr/bin/env python3
"""Evaluator for Task 16: Java Version Upgrade"""
import sys
import os
import shutil
import subprocess
import tempfile

TASK_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        '..', '..', 'tasks', 'task_16_java_upgrade')
EVAL_DIR = os.path.dirname(os.path.abspath(__file__))

ALL_TESTS = [
    "findFirst present",
    "findFirst value",
    "findFirst absent",
    "countLongerThan 3",
    "countLongerThan 4",
    "countLongerThan 5",
    "countLongerThan 10",
    "sortByLength first",
    "sortByLength second",
    "sortByLength third",
    "joinStrings comma",
    "joinStrings single",
    "joinStrings two",
]


def main():
    if not shutil.which('javac'):
        print("[SKIP] Java runtime not found (javac not on PATH)")
        sys.exit(2)

    solution_path = os.path.join(TASK_DIR, 'StringUtils.java')
    if not os.path.exists(solution_path):
        print("[FAIL] StringUtils.java not found in task directory")
        sys.exit(1)

    tmpdir = tempfile.mkdtemp()
    try:
        shutil.copy(solution_path, tmpdir)
        shutil.copy(os.path.join(EVAL_DIR, 'TestStringUtils.java'), tmpdir)

        result = subprocess.run(
            ['javac', 'StringUtils.java', 'TestStringUtils.java'],
            cwd=tmpdir,
            capture_output=True,
            text=True,
        )

        if result.returncode != 0:
            for name in ALL_TESTS:
                print(f"[FAIL] {name}: compile error")
            sys.exit(1)

        result = subprocess.run(
            ['java', 'TestStringUtils'],
            cwd=tmpdir,
        )
        sys.exit(result.returncode)

    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)


if __name__ == "__main__":
    main()
