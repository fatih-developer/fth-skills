import os
import subprocess
import sys

skills = [
    "contract-first-designer",
    "api-mock-designer",
    "sdk-scaffolder",
    "protocol-selector",
    "auth-flow-designer",
    "rate-limit-strategist",
    "breaking-change-detector",
    "changelog-generator",
    "webhook-architect",
    "api-observability-planner"
]

def main():
    print(f"🚀 Installing {len(skills)} API ecosystem skills...")
    for skill in skills:
        print(f"Installing {skill}...")
        # Cross platform invocation
        cmd = ["skills", "install", skill]
        try:
            subprocess.run(cmd, check=True, shell=True if sys.platform == "win32" else False)
        except subprocess.CalledProcessError:
            print(f"⚠️ Failed to install {skill}. Continuing...")
    print("✅ API Ecosystem installation complete!")

if __name__ == "__main__":
    main()
