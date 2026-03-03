---
name: protocol-selector
description: Projenin gereksinimlerine göre (latency, real-time beklentisi, payload boyutu) en uygun API protokolünü (REST, GraphQL, gRPC, WebSocket, SSE) seçer. Tradeoff analizleri yapar ve duruma göre hibrit mimari önerileri geliştirir.
---

# Protocol Selector Protocol

This skill prevents the "Golden Hammer" anti-pattern (where every problem is solved with GraphQL just because it's trendy, or REST just because it's familiar). It selects the correct transport layer based on the actual consumer needs.

**Core assumption:** There is no single "best" protocol. Picking gRPC for a public frontend is a disaster; picking REST for high-frequency microservice-to-microservice communication is inefficient.

---

## 1. Requirement Analysis (Static)
Analyze the system context based on user inputs:
- **Clients:** Web Browser? Mobile App? Internal Microservices? IoT Devices?
- **Data Shape:** Highly relational/graph-like? Binary files? Simple CRUD?
- **Delivery Expectation:** Request/Response? Server-to-Client Push? Bi-directional streams?

## 2. Trade-Off Evaluation

Map requirements to the strengths of specific protocols:
- 🌐 **REST (HTTP/JSON):** Best for public external APIs. Easy to cache, ubiquitous, simple tooling. Bad for over-fetching.
- 🕸️ **GraphQL:** Best for complex frontends and mobile apps needing to aggregate data from multiple sources. Prevents over-fetching. Hard to cache, risk of N+1 problems.
- ⚡ **gRPC / Protocol Buffers:** Best for internal microservices. Binary, heavily compressed, strongly typed, fast. Extremely difficult for browsers to consume natively.
- 📡 **WebSockets:** Best for true bi-directional real-time communication (e.g., Chat, Multiplayer Games). Stateful, difficult to scale and load balance.
- 📥 **Server-Sent Events (SSE):** Best for uni-directional real-time updates (e.g., Live sports scores, progress bars, notifications). Simpler to scale than WebSockets, runs over standard HTTP.

## 3. Output Generation

**Required Outputs (Must write BOTH to `docs/api-report/`):**

1. **Human-Readable Markdown (`docs/api-report/protocol-selection-report.md`)**
```markdown
### 🏛️ API Protocol Selection

**Context:** Building a live-updating dashboard for IoT sensor data and an internal admin CRUD panel.

#### 🎯 Recommended Architecture: Hybrid (REST + SSE)

**1. CRUD Operations: REST**
- **Why:** The admin panel performs standard Create/Read/Update/Delete operations on devices. Caching is useful here. Predictable tooling.
- **Trade-off:** Potential over-fetching on the dashboard list view, but acceptable for admin use.

**2. Live Sensor Data: Server-Sent Events (SSE)**
- **Why:** The dashboard only needs to *receive* live updates from the sensors. It doesn't need to push data back constantly. SSE is much lighter on infrastructure than WebSockets.
- **Trade-off:** Uni-directional only. If the frontend needs to send a command, it must use a standard REST `POST`.
```

2. **Machine-Readable JSON (`docs/api-report/protocol-selection-output.json`)**
```json
{
  "skill": "protocol-selector",
  "primary_protocol": "REST",
  "secondary_protocol": "SSE",
  "reasoning": "Standard CRUD best served by REST, live read-only dashboard best served by SSE to avoid WS overhead.",
  "rejected_protocols": ["gRPC (Ext. facing)", "GraphQL (No complex joins req)"]
}
```

---

## Guardrails
- **Beware the gRPC Web Trap:** If suggesting gRPC for a web frontend, you MUST mention `grpc-web` and Envoy proxies as a major infrastructure overhead.
- **GraphQL Caching:** If suggesting GraphQL, explicitly mention that standard HTTP caching (CDN) will not work easily; application-level caching (e.g., Apollo Client) is required.
