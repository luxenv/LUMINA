import json
import uuid
from datetime import datetime
from pathlib import Path


class ConversationMemory:

    def __init__(self, session_id=None):
        self.session_id = session_id or str(uuid.uuid4())

        # Find the project root.
        # context.py is:
        # src/features/memory/context.py
        root = Path(__file__).resolve().parents[2]

        self.memory_dir = root / "data" / "sessions"
        self.memory_file = (
            self.memory_dir / f"{self.session_id}.jsonl"
        )

        self.memory_dir.mkdir(
            parents=True,
            exist_ok=True
        )

    def save_turn(self, prompt, response, metadata=None):

        turn = {
            "prompt": prompt,
            "response": response,
            "timestamp": datetime.now().isoformat(),
            "metadata": metadata or {}
        }

        with open(
            self.memory_file,
            "a",
            encoding="utf-8"
        ) as f:

            json.dump(
                turn,
                f,
                ensure_ascii=False
            )

            f.write("\n")

    def get_context(self, max_turns=5):

        if not self.memory_file.exists():
            return []

        try:

            with open(
                self.memory_file,
                "r",
                encoding="utf-8"
            ) as f:

                turns = [
                    json.loads(line)
                    for line in f
                    if line.strip()
                ]

            return turns[-max_turns:]

        except (json.JSONDecodeError, IOError):
            return []

    def search_memory(
        self,
        query,
        max_results=5
    ):

        if not query:
            return []

        query = str(query).lower().strip()

        if not self.memory_file.exists():
            return []

        try:

            with open(
                self.memory_file,
                "r",
                encoding="utf-8"
            ) as f:

                turns = [
                    json.loads(line)
                    for line in f
                    if line.strip()
                ]

        except (json.JSONDecodeError, IOError):
            return []

        results = []

        for turn in reversed(turns):

            prompt = str(
                turn.get("prompt", "")
            )

            response = str(
                turn.get("response", "")
            )

            if (
                query in prompt.lower()
                or query in response.lower()
            ):

                results.append(turn)

                if len(results) >= max_results:
                    break

        return results

    def get_formatted_context(
        self,
        max_turns=3
    ):

        turns = self.get_context(
            max_turns
        )

        if not turns:
            return ""

        parts = []

        for turn in turns:

            parts.append(
                f"User: {turn.get('prompt', '')}"
            )

            parts.append(
                f"Assistant: {turn.get('response', '')}"
            )

        return "\n".join(parts) + "\n"

    def clear_session(self):

        if self.memory_file.exists():
            self.memory_file.unlink()

    @staticmethod
    def list_all_sessions():

        root = Path(__file__).resolve().parents[2]
        memory_dir = root / "data" / "sessions"

        if not memory_dir.exists():
            return []

        return [
            file.stem
            for file in memory_dir.glob("*.jsonl")
        ]
