# React Flow Audit Checklist

## 1. Discovery

- Confirm `@xyflow/react` version and TypeScript usage.
- Locate all components rendering `<ReactFlow />`.
- Locate all custom node and edge implementations.

## 2. Types And Data Contracts

- Ensure node and edge types are declared in one shared module.
- Ensure `Node<Data, Type>` and `Edge<Data, Type>` generics are used.
- Ensure each custom node's `data` shape is explicit and stable.
- Ensure id format is deterministic enough for updates and persistence.

## 3. State And Handlers

- Ensure `useNodesState` and `useEdgesState` (or a single external store) are wired correctly.
- Ensure `onNodesChange` and `onEdgesChange` pass through unchanged unless intentionally wrapped.
- Ensure `onConnect` uses `addEdge` and preserves required edge metadata.
- Ensure no stale closure issues in callbacks.

## 4. Rendering And Performance

- Ensure `nodeTypes` and `edgeTypes` are stable references.
- Ensure large inline objects/functions are not recreated in render loops.
- Ensure heavy custom nodes are memoized when appropriate.
- Ensure expensive layout recalculation is not triggered on every render.

## 5. UX And Behavior

- Ensure controls (`Background`, `Controls`, `MiniMap`) are configured intentionally.
- Ensure invalid connections are blocked if domain rules require it.
- Ensure selection, drag, and zoom behavior matches product expectation.

## 6. Persistence And Serialization

- Ensure save/load path serializes both nodes and edges.
- Ensure schema/version for persisted graph data is documented.
- Ensure migration path exists if node data shape changed.

## 7. Validation

- Run project tests/checks if available.
- If no tests exist, run manual scenario checks:
  - create node
  - connect nodes
  - delete node/edge
  - reload persisted graph