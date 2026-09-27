"""Collect and manage user feedback for model improvement."""
import json
from pathlib import Path
from datetime import datetime


class FeedbackCollector:
    """Collects user ratings and feedback for model retraining."""
    
    def __init__(self):
        self.feedback_dir = Path("src/data/feedback")
        self.feedback_file = self.feedback_dir / "feedback.jsonl"
        self.feedback_dir.mkdir(parents=True, exist_ok=True)
    
    def log_feedback(self, prompt, generated_text, rating, notes=""):
        """Log a user rating for a model generation.
        
        Args:
            prompt: User's input prompt
            generated_text: Model's generated response
            rating: User rating (1-5, where 5 is best)
            notes: Optional user feedback text
        """
        feedback = {
            "prompt": prompt,
            "generated_text": generated_text,
            "rating": max(1, min(5, rating)),  # Clamp to 1-5
            "notes": notes,
            "timestamp": datetime.now().isoformat()
        }
        
        with open(self.feedback_file, "a") as f:
            json.dump(feedback, f)
            f.write("\n")
    
    def get_high_quality_samples(self, min_rating=4):
        """Retrieve high-quality samples for retraining.
        
        Args:
            min_rating: Minimum rating threshold (1-5)
            
        Returns:
            List of high-quality prompt-response pairs
        """
        if not self.feedback_file.exists():
            return []
        
        samples = []
        try:
            with open(self.feedback_file) as f:
                for line in f:
                    entry = json.loads(line)
                    if entry["rating"] >= min_rating:
                        samples.append((entry["prompt"], entry["generated_text"]))
        except (json.JSONDecodeError, IOError):
            pass
        
        return samples
    
    def get_statistics(self):
        """Get feedback statistics.
        
        Returns:
            Dict with avg_rating, total_samples, distribution
        """
        if not self.feedback_file.exists():
            return {"avg_rating": 0, "total_samples": 0, "distribution": {}}
        
        ratings = []
        try:
            with open(self.feedback_file) as f:
                for line in f:
                    entry = json.loads(line)
                    ratings.append(entry["rating"])
        except (json.JSONDecodeError, IOError):
            pass
        
        if not ratings:
            return {"avg_rating": 0, "total_samples": 0, "distribution": {}}
        
        distribution = {i: ratings.count(i) for i in range(1, 6)}
        return {
            "avg_rating": sum(ratings) / len(ratings),
            "total_samples": len(ratings),
            "distribution": distribution
        }
