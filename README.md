# Milestone 11 — Lumina-1 Website AI

This is the first milestone where the website talks to the LOCAL Lumina-1
model instead of using hard-coded JavaScript responses.

Architecture:

Browser
   |
   | HTTP POST /api/chat
   v
Python local server
   |
   v
Lumina-1 model.json
   |
   v
generated response
   |
   v
Browser

No cloud API is required.

1. First train Milestone 9:
       python3 09-lumina-core/train.py

2. Start the website:
       python3 11-website-ai/server.py

3. Open:
       http://127.0.0.1:8000

This model is intentionally tiny and will not behave like ChatGPT. The goal
is to make the entire pipeline real and understandable.
