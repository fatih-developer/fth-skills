# Legacy To Modern API Mapping

Use this as a quick mapping reference during migration.

## Package Import

- Legacy: `reactflow`
- Target: `@xyflow/react`

## Typical Hook And Utility Targets

- Keep `useNodesState` and `useEdgesState` patterns, but verify import source.
- Keep `addEdge`, but verify the `Connection` and edge type usage.
- Confirm generic usage on `ReactFlow<NodeType, EdgeType>`.

## Common Migration Notes

- Re-check CSS import path and style inclusion.
- Re-check custom node and edge type registration shape.
- Re-check strict typing after package migration.
