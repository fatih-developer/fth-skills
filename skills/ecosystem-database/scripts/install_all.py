import os
import subprocess
import sys

skills = [
    "schema-architect",
    "access-policy-designer",
    "seed-data-generator",
    "query-explainer",
    "index-advisor",
    "query-budget-enforcer",
    "schema-diff-analyzer",
    "migration-strategist",
    "data-masker",
    "data-lineage-tracer"
]

def main():
    print(f"🚀 Installing {len(skills)} Database ecosystem skills...")
    for skill in skills:
        print(f"Installing {skill}...")
        cmd = ["skills", "install", skill]
        try:
            subprocess.run(cmd, check=True, shell=True if sys.platform == "win32" else False)
        except subprocess.CalledProcessError:
            print(f"⚠️ Failed to install {skill}. Continuing...")
    print("✅ Database Ecosystem installation complete!")

if __name__ == "__main__":
    main()
