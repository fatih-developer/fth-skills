import os
import subprocess
import sys

skills = [
    "claw-integration-design",
    "tool-selector",
    "context-compressor",
    "task-decomposer",
    "parallel-planner",
    "memory-ledger",
    "error-recovery",
    "multi-brain",
    "multi-brain-experts",
    "multi-brain-debate",
    "assumption-checker",
    "output-critic",
    "multi-brain-score",
    "checkpoint-guardian",
    "agent-reviewer"
]

def main():
    print(f"🚀 Installing {len(skills)} Orchestration ecosystem skills...")
    for skill in skills:
        print(f"Installing {skill}...")
        cmd = ["skills", "install", skill]
        try:
            subprocess.run(cmd, check=True, shell=True if sys.platform == "win32" else False)
        except subprocess.CalledProcessError:
            print(f"⚠️ Failed to install {skill}. Continuing...")
    print("✅ Orchestration Ecosystem installation complete!")

if __name__ == "__main__":
    main()
