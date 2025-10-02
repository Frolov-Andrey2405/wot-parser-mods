import subprocess
import sys

commands = [
    [sys.executable, "./app/parser.py"],
    [sys.executable, "./app/downloads.py"],
    [sys.executable, "./app/unpacking.py"]
]

for cmd in commands:
    print(f"\n🚀 Running: {' '.join(cmd)}")
    result = subprocess.run(cmd)
    if result.returncode != 0:
        print(f"❌ Error during execution: {' '.join(cmd)}. Stopping the chain.")
        break
