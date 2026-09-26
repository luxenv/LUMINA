"""Session-based conversation memory and context management."""
import json
from pathlib import Path
from datetime import datetime
import uuid


class ConversationMemory:
    """Stores and retrieves conversation history for offline persistence."""
    
    def __init__(self, session_id=None):
        self.session_id = session_id or str(uuid.uuid4())
        self.memory_dir = Path("src/data/sessions")
        self.memory_file = self.memory_dir / f"{self.session_id}.jsonl"
        self.memory_dir.mkdir(parents=True, exist_ok=True)
    
    def save_turn(self, prompt, response, metadata=None):
        """Persist a conversation turn.
        
        Args:
            prompt: User input
            response: Model output
            metadata: Optional dict with extra info (confidence, tools_used, etc)
        """
        turn = {
            "prompt": prompt,
            "response": response,
            "timestamp": datetime.now().isoformat(),
            "metadata": metadata or {}
        }
        with open(self.memory_file, "a") as f:
            json.dump(turn, f)
            f.write("\n")
    
    def get_context(self, max_turns=5):
        """Retrieve recent conversation turns for context.
        
        Args:
            max_turns: Maximum number of recent turns to retrieve
            
        Returns:
            List of turn dicts in chronological order
        """
        if not self.memory_file.exists():
            return []
        
        try:
            with open(self.memory_file) as f:
                turns = [json.loads(line) for line in f.readlines()]
            return turns[-max_turns:]
        except (json.JSONDecodeError, IOError):
            return []
    
    def get_formatted_context(self, max_turns=3):
        """Format context as a string for prompt augmentation.
        
        Format: "User: prompt\nAssistant: response\n..."
        """
        turns = self.get_context(max_turns)
        if not turns:
            return ""
        
        parts = []
        for turn in turns:
            parts.append(f"User: {turn['prompt']}")
            parts.append(f"Assistant: {turn['response']}")
        return "\n".join(parts) + "\n"
    
    def clear_session(self):
        """Delete this session's memory."""
        if self.memory_file.exists():
            self.memory_file.unlink()
    
    def list_all_sessions():
        """List all available sessions (static method)."""
        memory_dir = Path("src/data/sessions")
        if not memory_dir.exists():
            return []
        return [f.stem for f in memory_dir.glob("*.jsonl")]
