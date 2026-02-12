#!/usr/bin/env python3
"""Evaluator for Task 17: C# Version Upgrade"""
import sys
import os
import shutil
import subprocess
import tempfile

TASK_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        '..', '..', 'tasks', 'task_17_csharp_upgrade')
EVAL_DIR = os.path.dirname(os.path.abspath(__file__))

ALL_TESTS = [
    "GetLengths count",
    "GetLengths values",
    "CountByFirstLetter distinct keys",
    "CountByFirstLetter all ones",
    "CountByFirstLetter a=2",
    "CountByFirstLetter b=1",
    "CountShorterThan 5",
    "CountShorterThan 10",
    "FormatEntry basic",
    "FormatEntry zero",
]

CSPROJ_TEMPLATE = """\
<Project Sdk="Microsoft.NET.Sdk">
  <PropertyGroup>
    <OutputType>Exe</OutputType>
    <TargetFramework>{framework}</TargetFramework>
    <Nullable>disable</Nullable>
    <ImplicitUsings>disable</ImplicitUsings>
  </PropertyGroup>
</Project>
"""


def detect_target_framework():
    """Return 'netN.0' for the highest installed .NET SDK >= 6, or None."""
    try:
        result = subprocess.run(
            ['dotnet', '--list-sdks'],
            capture_output=True, text=True, timeout=15,
        )
        if result.returncode != 0:
            return None
        highest = 0
        for line in result.stdout.splitlines():
            line = line.strip()
            if not line:
                continue
            # Lines look like: "8.0.100 [/usr/share/dotnet/sdk]"
            version_str = line.split()[0]
            major = int(version_str.split('.')[0])
            if major >= 6 and major > highest:
                highest = major
        if highest == 0:
            return None
        return f"net{highest}.0"
    except Exception:
        return None


def main():
    if not shutil.which('dotnet'):
        print("[SKIP] .NET runtime not found (dotnet not on PATH)")
        sys.exit(2)

    framework = detect_target_framework()
    if framework is None:
        print("[SKIP] No .NET 6+ SDK found")
        sys.exit(2)

    solution_path = os.path.join(TASK_DIR, 'TextProcessor.cs')
    if not os.path.exists(solution_path):
        print("[FAIL] TextProcessor.cs not found in task directory")
        sys.exit(1)

    tmpdir = tempfile.mkdtemp()
    try:
        proj_path = os.path.join(tmpdir, "task17.csproj")
        with open(proj_path, 'w') as f:
            f.write(CSPROJ_TEMPLATE.format(framework=framework))

        shutil.copy(solution_path, tmpdir)
        shutil.copy(os.path.join(EVAL_DIR, 'TestRunner.cs'), tmpdir)

        result = subprocess.run(
            ['dotnet', 'build', '-v', 'quiet', '--nologo'],
            cwd=tmpdir,
            capture_output=True,
            text=True,
        )

        if result.returncode != 0:
            for name in ALL_TESTS:
                print(f"[FAIL] {name}: build error")
            sys.exit(1)

        result = subprocess.run(
            ['dotnet', 'run', '--no-build', '--nologo'],
            cwd=tmpdir,
        )
        sys.exit(result.returncode)

    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)


if __name__ == "__main__":
    main()
