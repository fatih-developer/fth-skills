# Command Blacklist

This file lists shell commands that adaptive-guard and security-auditor will **always reject**. Any skill containing or executing these commands will be flagged with STRICT REJECT.

## Tier 1 — STRICT REJECT (Instant Block, No Override)

```bash
rm -rf          # Mass / recursive deletion
dd if=/dev/zero # Disk wipe / fill
:(){ :|:& };:   # Fork bomb
mkfs            # Disk format
> /dev/sda      # Raw disk overwrite
wget|curl ... | bash   # Remote Code Execution (RCE)
nc -e /bin/sh   # Reverse shell
chmod 777 /     # System-wide open permissions
chown -R root   # Root ownership takeover
iptables -F     # Firewall flush
```

## Tier 2 — HIGH RISK (Require Checkpoint)

```bash
kill -9 -1         # Kill all processes
find / -delete     # Recursive unbounded deletion
truncate -s 0      # Empty all files in scope
mv /* /dev/null    # Mass file relocation/deletion
sudo ...           # Any privilege escalation
cat /etc/passwd    # System credentials
env | grep -i key  # Full environment dump
find / -type f     # Entire filesystem scan
curl ... | bash    # Piped remote execution
eval(...)          # Arbitrary code evaluation
exec(...)          # Arbitrary process spawning
```

## Tier 3 — DYNAMIC RISK (Sanitize or Reject)

Any command that concatenates user-supplied input directly:

```python
# These patterns MUST be rejected or sanitized before execution
cmd = f"ls {user_input}"    # REJECT — user may inject ; rm -rf /
os.system(user_path)        # REJECT — path traversal risk
eval(user_code)             # STRICT REJECT
exec(user_input)            # STRICT REJECT
subprocess.run(user_cmd)    # REJECT unless input is validated & escaped
```
