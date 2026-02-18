# Migration Checklist

## 1. Baseline

- Capture current dependency and version.
- Capture all import sites for React Flow.
- Capture current node/edge type definitions.

## 2. API Mapping

- Map each deprecated API to its replacement.
- Confirm event handler signatures match target version.
- Confirm component props still exist or have replacements.

## 3. Type Safety

- Centralize node and edge types.
- Remove implicit `any` from flow data contracts.
- Confirm custom nodes receive typed props.

## 4. Runtime Behavior

- Verify node drag and edge connect behavior.
- Verify delete/select interactions.
- Verify controls, minimap, and background configuration.

## 5. Persistence

- Validate old saved payload can still load.
- Add schema version if missing.
- Add migration transform for legacy payload when necessary.

## 6. Verification

- Run lint/typecheck/tests if available.
- Manually verify create/connect/delete/save/load.
- Record any deferred cleanups.
