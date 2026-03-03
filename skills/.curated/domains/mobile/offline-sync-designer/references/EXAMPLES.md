# Examples

## Example — Note Taking App Sync

**User Request:** 
"I'm building a note-taking app in React Native. Right now, if the user creates a note, I make an API call to `POST /notes` to get the DB ID, then add it to my Redux store. If they have no internet, the app shows an error. I want them to be able to create and edit notes offline, and have it sync when the internet comes back. How do I architect this?"

**Skill Response:**

```markdown
# 🔄 Offline Sync & Local-First Architecture

Your current architecture is "Server-Authoritative". We need to move to a "Local-First" architecture. The client database must become the single source of truth for the UI.

## 🗄 Storage & Domain Strategy
- **Replace Redux with a Local DB:** Redux is in-memory; it clears when the app closes. For offline capability, use a persistent local database.
- **Recommended DB:** **WatermelonDB** is highly recommended for React Native offline-first apps because it is built precisely for this sync pattern and handles background threading efficiently.

## ⚡ UI State Handling (Optimistic Updates)
**Scenario: User creates a new note while in airplane mode.**
1. **Action:** Generate a `UUIDv4` on the device. Do NOT wait for a backend database ID.
2. **Local DB:** Save the Note locally in WatermelonDB. Mark the record internally with `_status: 'created'`.
3. **UI:** The UI is reactive (tied to the local DB). It instantly shows the new note. No spinners.
4. **Queue:** The app queues a background sync job.

## ⚔️ Conflict Resolution Strategy
**Policy: Last Write Wins (LWW)**
Since users might edit notes on their phone, then edit the same note on their iPad while the phone was offline, you need a mechanism to decide which version to keep.

**Implementation:**
- Add an `updated_at` timestamp column to your Notes table.
- When the phone reconnects, it pushes its changes up. The backend API checks the incoming `updated_at` against the database's `updated_at`.
- If phone `updated_at` > backend `updated_at`, the backend accepts the change.
- If phone is older, the backend rejects the write and forces the phone to pull the newer version.

## 📡 Sync Mechanism
- **Foreground Sync:** Use React Native's `NetInfo` library. When state changes from `offline` to `online`, immediately trigger the sync queue.
- **Background Sync:** Use `react-native-background-actions` or Expo's `BackgroundFetch` to wake up the app periodically every few hours to pull down new notes if the user hasn't opened the app.

## 🚨 Critical Architectural Change: Migrating from Int IDs to UUIDs
Because notes are created offline, your backend must stop relying on PostgreSQL `SERIAL` or MySQL `AUTO_INCREMENT` primary keys for the `Note` entity. You must change your backend schema to accept `UUID` strings as the primary key. This allows the client to dictate the ID and prevents collisions during sync.
```
