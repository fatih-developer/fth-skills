# Common Fix Patterns

## Broken node or edge updates

Symptom:
- Drag or connect events fire but UI state does not update reliably.

Fix pattern:
- Use functional updates from `useNodesState` and `useEdgesState`.
- Keep handler signatures aligned with `@xyflow/react` types.

## Type drift in `data` payload

Symptom:
- Runtime errors in custom nodes due to missing `data` fields.

Fix pattern:
- Define a shared `NodeData` union/type map.
- Use typed nodes (`Node<NodeData, NodeType>`) and remove `any`.

## Performance degradation on medium/large graphs

Symptom:
- Laggy drag, zoom, and selection.

Fix pattern:
- Stabilize `nodeTypes` and `edgeTypes`.
- Memoize heavy custom nodes.
- Move expensive layout runs behind explicit triggers.

## Inconsistent ids and persistence issues

Symptom:
- Loaded graphs break edge links or duplicate nodes.

Fix pattern:
- Enforce deterministic id creation strategy.
- Validate edge source/target ids after load.
- Add schema version to persisted payload.

## Uncontrolled behavior drift after quick fixes

Symptom:
- One bug fix introduces side effects elsewhere.

Fix pattern:
- Apply small isolated patches.
- Verify core interactions after each patch.
- Record behavior changes and migration notes.