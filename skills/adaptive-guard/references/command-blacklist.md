# Command Blacklist (adaptive-guard)

This file is the K1 execution blacklist for adaptive-guard. Any message or tool call matching these patterns is **instantly blocked** without escalating to K2 or K3.

## Tier 1 — STRICT REJECT

```bash
rm -rf
dd if=/dev/zero
:(){ :|:& };:
mkfs
wget|curl ... | bash
nc -e /bin/sh
chmod 777 /
chown -R root
iptables -F
> /dev/sda
```

## Tier 2 — HIGH RISK (Auto-escalate to K3)

```bash
kill -9 -1
find / -delete
truncate -s 0
sudo
cat /etc/passwd
env | grep -i key
eval(
exec(
```

## Dynamic Injection Patterns

```regex
(;\s*rm\s+-rf)             # Semicolon-chained deletion
(\|\s*bash)                # Piped shell execution
(\$\(.+\))                 # Command substitution
(`[^`]+`)                  # Backtick execution
(&&\s*rm|&&\s*curl)        # Chained destructive commands
```
