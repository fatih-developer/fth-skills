# Resume Checklist

Use after selecting a handoff. Do not continue from Next Recommended Action until reconciliation succeeds.

## Select (low context)

- [ ] Read `.session-transfer/INDEX.md` first when it exists
- [ ] Prefer this agent’s unfinished handoff; otherwise take the latest compatible cross-agent handoff
- [ ] Read only the selected handoff initially — do not open every historical file
- [ ] If the global index is missing or corrupted, recover from agent `INDEX.md` then JSONL/handoff metadata; never delete timestamped files

## Reconcile with the repository

- [ ] Confirm working directory and git branch (understand any mismatch)
- [ ] Run `check_staleness.py` — FRESH / SLIGHTLY_STALE / STALE / VERY_STALE
- [ ] Compare `git status` and recent commits to Files Changed / commit metadata
- [ ] Verify referenced files still exist
- [ ] Treat the live repo as source of truth when the handoff is stale

## Then continue

- [ ] Start from **Next Recommended Action** only after the checks above
- [ ] Use Remaining Work, Issues / Risks, and Resume Instructions as constraints
- [ ] On the next CREATE, record lineage (`resumed_from`, `previous_session`, `source_agent`)

## Red flags — stop

1. Referenced files are gone
2. Branch or architecture has diverged
3. Assumptions in the handoff are clearly false
4. Indexes disagree with files on disk — recover, do not guess
