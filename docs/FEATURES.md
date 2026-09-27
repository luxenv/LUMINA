# Lumina-1 Features

## Model Improvements

### 1. Context Window (32 characters)
The model now uses a rolling context window of 32 previous characters to understand context better than just the last character.

### 2. Proper Softmax Normalization
Generated probabilities are now correctly normalized to sum to 1.0, ensuring valid probability distributions.

### 3. Model Caching
The model is loaded once at server startup and cached in memory, eliminating disk reads on every request.

## Memory & Persistence

### Session-Based Memory
- Each browser session gets a unique ID (stored in localStorage)
- Conversation history is saved to `src/data/sessions/{session_id}.jsonl`
- Memory can be retrieved to provide context for future turns
- Supports multi-turn conversations with coherent context

### Knowledge Base (SQLite)
- Local SQLite database at `src/data/lumina.db`
- Three tables: facts, documents, queries
- Persistent storage for:
  - Facts: key-value pairs with categories
  - Documents: full documents with tagging
  - Queries: logged interactions for analytics

## Feedback Loop

### User Ratings
- Rate each response (1-5 stars)
- Feedback logged to `src/data/feedback/feedback.jsonl`
- Tracks: prompt, generated text, rating, user notes, timestamp

### Statistics
- `GET /api/stats` returns average rating and distribution
- High-quality samples (rating >= 4) can be extracted for retraining
- Enables iterative model improvement

## Tool Router & Function Calling

### Available Tools
- **calculator**: Evaluate math expressions
- **knowledge**: Look up facts from knowledge base
- **time**: Get current time
- **memory_lookup**: Store and recall memories
- **document_search**: Search indexed documents

### Auto-Detection
Tools are automatically detected from user queries:
- "calculate 2 + 3" → calculator tool
- "what is the capital of france" → knowledge tool
- "current time" → time tool
- "search for climate change" → document_search tool

## API Endpoints

### Chat
```
POST /api/chat
{
  "message": "your prompt",
  "session_id": "unique_session_id",
  "use_tools": true
}
```

### Feedback
```
POST /api/feedback
{
  "prompt": "original prompt",
  "generated_text": "model output",
  "rating": 4,
  "notes": "optional feedback"
}
```

### Knowledge Base
```
POST /api/knowledge/add
{"key": "capital_france", "value": "Paris", "category": "geography"}

POST /api/knowledge/search
{"query": "france"}
```

### Statistics
```
GET /api/stats
```

## Offline Capability

All features work fully offline:
- Model runs locally
- Memory persists to local files
- Knowledge base uses local SQLite
- No external API calls
- Feedback and ratings stored locally
- Tool router runs client-side logic

## Online Deployment

The same code works online with:
- ThreadingHTTPServer handles concurrent requests
- Model cache prevents memory bloat
- Sessions persist across server restarts (files on disk)
- Knowledge base is portable (single .db file)
- Ready for containerization (Docker)
