import os
import subprocess
import sys

skills = [
    "accessibility-enforcer",
    "mobile-perf-auditor",
    "mobile-security-auditor",
    "app-store-reviewer",
    "release-orchestrator",
    "deep-link-architect",
    "push-notification-planner",
    "offline-sync-designer",
    "onboarding-designer",
    "crash-analyst"
]

def main():
    print(f"🚀 Installing {len(skills)} Mobile ecosystem skills...")
    for skill in skills:
        print(f"Installing {skill}...")
        cmd = ["skills", "install", skill]
        try:
            subprocess.run(cmd, check=True, shell=True if sys.platform == "win32" else False)
        except subprocess.CalledProcessError:
            print(f"⚠️ Failed to install {skill}. Continuing...")
    print("✅ Mobile Ecosystem installation complete!")

if __name__ == "__main__":
    main()
