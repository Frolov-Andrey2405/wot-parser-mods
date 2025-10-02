import subprocess
import sys

commands = [
    [sys.executable, "parser.py"],
    [sys.executable, "downloads.py"],
    [sys.executable, "unpacking.py"]
]

for cmd in commands:
    print(f"\n🚀 Running: {' '.join(cmd)}")
    result = subprocess.run(cmd)
    if result.returncode != 0:
        print(f"❌ Error during execution: {' '.join(cmd)}. Stopping the chain.")
        break
