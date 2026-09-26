

GitHub Pages can host HTML/CSS/JS, but it cannot run the Python AI server.
A public AI version needs a server/container with Python and enough CPU/RAM.

## Local deployment test

    python3 09-lumina-core/train.py
    python3 17-complete-lumina/app.py

Then open http://127.0.0.1:8000

## Docker

    docker build -f 18-deployment/Dockerfile -t lumina-1 .
    docker run --rm -p 8000:8000 lumina-1

For a real host, use a service that supports a Python container or long-running
Python process. Keep secrets out of Git. Configure the PORT environment variable
when the platform provides one.

Architecture:
Browser -> HTTPS -> hosted Python service -> Lumina-1 model/tools/knowledge/memory

The final model may eventually require much stronger hardware than the Acer.
