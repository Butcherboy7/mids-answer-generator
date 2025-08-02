import json
import os
from datetime import datetime
from typing import List, Dict

class HistoryManager:
    """Manages history of generated answer sets"""
    
    def __init__(self):
        self.history_file = "data/answer_history.json"
        self._ensure_data_directory()
        self._load_history()
    
    def _ensure_data_directory(self):
        """Ensure data directory exists"""
        os.makedirs("data", exist_ok=True)
    
    def _load_history(self):
        """Load history from JSON file"""
        try:
            if os.path.exists(self.history_file):
                with open(self.history_file, 'r') as f:
                    self.history = json.load(f)
            else:
                self.history = []
        except Exception as e:
            self.history = []
    
    def _save_history(self):
        """Save history to JSON file"""
        try:
            with open(self.history_file, 'w') as f:
                json.dump(self.history, f, indent=2)
        except Exception as e:
            print(f"Error saving history: {e}")
    
    def add_entry(self, entry: Dict):
        """Add a new entry to history"""
        
        # Create history entry
        history_entry = {
            "id": len(self.history) + 1,
            "subject": entry["subject"],
            "mode": entry["mode"],
            "question_count": entry["question_count"],
            "generated_at": entry["generated_at"],
            "pdf_path": entry["pdf_path"],
            "timestamp": datetime.now().isoformat()
        }
        
        self.history.append(history_entry)
        self._save_history()
    
    def get_history(self) -> List[Dict]:
        """Get all history entries"""
        return self.history
    
    def get_entry(self, entry_id: int) -> Dict:
        """Get specific history entry by ID"""
        for entry in self.history:
            if entry["id"] == entry_id:
                return entry
        return {}
    
    def delete_entry(self, entry_id: int) -> bool:
        """Delete a history entry"""
        for i, entry in enumerate(self.history):
            if entry["id"] == entry_id:
                # Try to delete the PDF file if it exists
                try:
                    if os.path.exists(entry["pdf_path"]):
                        os.remove(entry["pdf_path"])
                except:
                    pass
                
                # Remove from history
                self.history.pop(i)
                self._save_history()
                return True
        return False
    
    def clear_history(self):
        """Clear all history"""
        # Try to delete all PDF files
        for entry in self.history:
            try:
                if os.path.exists(entry["pdf_path"]):
                    os.remove(entry["pdf_path"])
            except:
                pass
        
        self.history = []
        self._save_history()
