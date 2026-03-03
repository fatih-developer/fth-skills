# Example Requests

## Example 1: Package migration

Request:
- "Migrate this project from legacy `reactflow` import to `@xyflow/react` safely."

Expected outcome:
- Import migration plan.
- Incremental code patches.
- Verification checklist for behavior parity.

## Example 2: Typed migration

Request:
- "Upgrade this flow editor and remove loose `any` types."

Expected outcome:
- Shared node/edge type module.
- Typed handlers and connection flow.
- Typecheck-ready patch set.

## Example 3: Persistence-safe upgrade

Request:
- "Upgrade without breaking old saved graphs."

Expected outcome:
- Serialized payload compatibility review.
- Optional migration adapter.
- Manual test script for load/save parity.
