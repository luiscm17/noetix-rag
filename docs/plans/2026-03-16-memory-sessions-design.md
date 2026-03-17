# Memory and Sessions Design - Multi-Agent Orchestrator

**Date**: 2026-03-16  
**Status**: Approved

## Overview

Add persistent memory and session management to the multi-agent orchestrator using Redis. This enables:
- Multi-turn conversations with persistent history
- Long-term memory for user preferences and learned facts

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      /api/chat                              │
│                   (session_id: str)                        │
└─────────────────────────┬───────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                   AgentOrchestrator                         │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Session (AgentSession)                             │   │
│  │  ├─ RedisChatMessageStore (historial)              │   │
│  │  └─ RedisProvider (memoria a largo plazo)          │   │
│  └─────────────────────────────────────────────────────┘   │
│                          │                                  │
│         ┌───────────────┼───────────────┐                  │
│         ▼               ▼               ▼                  │
│   TriageAgent    RAGAgent      TeacherAgent   SocraticAgent │
└─────────────────────────────────────────────────────────────┘
```

## Redis Storage

### Short-Term Memory (Conversation History)

| Key Pattern | Type | Description |
|-------------|------|-------------|
| `chat:{session_id}` | Redis List | Mensajes de la conversación (JSON) |

### Long-Term Memory (User Context)

| Key Pattern | Type | Description |
|-------------|------|-------------|
| `context:{user_id}` | Redis Search + Hash | Memories con embedding vectorial |

## Components

### 1. Session Manager (`session_manager.py`)

- Creates/retrieves sessions based on `session_id`
- Initializes RedisChatMessageStore per session
- Handles session lifecycle

### 2. Updated Orchestrator

- Accepts `session_id` parameter
- Uses Redis-backed session with history provider
- Attaches RedisProvider for long-term memory

### 3. Updated API Endpoint

- Accepts `session_id` in request body
- Passes session to orchestrator
- Maintains conversation across requests

## Dependencies

```bash
uv add redis
```

## Implementation Order

1. Install Redis dependency
2. Create session manager
3. Update orchestrator to use session
4. Update chat endpoint to accept session_id
5. Test multi-turn conversations

## Notes

- Single user (development mode)
- Local Redis instance
- All context providers managed by orchestrator only
