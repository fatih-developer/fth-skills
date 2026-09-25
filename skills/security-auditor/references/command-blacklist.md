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

---

## Extended Catalog

The detailed entries below were merged from the former `skill-security` skill. They use the same tiers as the summary above; when an entry appears in both, the stricter tier wins.

### Tier 1 — STRICT REJECT (extended list)

#### System Destruction
```bash
rm -rf /
rm -rf /*
rm -rf ~
dd if=/dev/zero of=/dev/sda
dd if=/dev/random of=/dev/sda
mkfs /dev/sda
mkfs.ext4 /dev/sda
> /dev/sda
shred /dev/sda
wipefs /dev/sda
```

#### Fork Bomb / Resource Exhaustion
```bash
:(){ :|:& };:
fork_bomb() { fork_bomb | fork_bomb & }
while true; do ./ & done
python3 -c "import os; [os.fork() for _ in iter(int,1)]"
```

#### Remote Code Execution (RCE)
```bash
curl http://... | bash
curl http://... | sh
wget -O- http://... | bash
wget -O- http://... | sh
eval $(curl ...)
eval $(wget ...)
```

#### Reverse Shell
```bash
nc -e /bin/sh
nc -e /bin/bash
ncat -e /bin/sh
bash -i >& /dev/tcp/
python3 -c "import socket..."  # reverse shell pattern
```

#### Privilege Escalation
```bash
sudo su -
sudo bash
sudo -i
chmod 4755 /bin/bash  # SUID bash
chown root:root /tmp/x && chmod +s /tmp/x
```

#### Mass Data Deletion
```bash
find / -delete
find / -exec rm {} \;
find . -type f -delete
truncate -s 0 $(find / -type f)
```

---

### Tier 2 — HIGH RISK (extended list)

#### Broad System Access
```bash
find / -type f               # Full filesystem scan
ls -laR /                    # Recursive root list
cat /etc/shadow              # Password hashes
cat /etc/passwd              # User list
cat ~/.ssh/id_rsa            # Private SSH key
env                          # Full environment (may contain secrets)
printenv                     # Full environment
set                          # All shell variables
```

#### Process Management
```bash
kill -9 -1                   # Kill all processes
killall -9                   # Kill all processes
pkill -9 -u root             # Kill root processes
```

#### Network Security
```bash
iptables -F                  # Flush firewall rules
ufw disable                  # Disable firewall
nmap -sS                     # Stealth scan
tcpdump                      # Listen to network traffic
wireshark                    # Capture network traffic
```

#### Critical System Files
```bash
cat /etc/sudoers
cat /etc/crontab
crontab -r                   # Delete all cron jobs
```

#### Potential Data Loss
```bash
mv /* /dev/null
cp /dev/null important_file
truncate -s 0 *.db
```

---

### Tier 3 — DYNAMIC RISK / Under Surveillance (extended list)

#### Dynamic Code Execution (Input Dependent)
```bash
eval "$user_input"
bash -c "$user_input"
sh -c "$user_input"
python3 -c "$user_code"
node -e "$user_script"
```

#### High Resource Usage
```bash
yes > /dev/null              # CPU exhaustion
cat /dev/urandom > file      # Fill disk
stress --cpu 8               # CPU stress
```

#### Service Management
```bash
systemctl stop              # Stop service
service stop                # Stop service
reboot                      # Reboot system
halt                        # Halt system
shutdown                    # Shutdown system
```

---

### SAFE — No Approval Required

```bash
# Read operations
ls, cat, head, tail, grep, find (limited directory), wc
# Text processing
awk, sed, cut, tr, sort, uniq
# Information gathering
pwd, whoami, date, uname
# Development
git status, git log, git diff (read-only)
# File creation (in specific directories)
mkdir, touch, cp (to tmp directory)
```

---

### Dynamic Command Detection

If the following patterns exist, approval is required regardless of command contents:

```python
# Python
os.system(variable)
subprocess.run(variable, shell=True)
exec(variable)
eval(variable)
__import__(variable)

# JavaScript/Node
eval(variable)
new Function(variable)
child_process.exec(variable)

# Shell
$()  # command substitution + variable
``   # backtick + variable
```
