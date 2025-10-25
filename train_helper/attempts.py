import json
from datetime import datetime
from typing import Dict, List, Optional, Any
import os

DEFAULT_PATH = "train_helper/data/attempts.json"

class AttemptStorage:
    def __init__(self, path: str = DEFAULT_PATH):
        self.path = path
        self._data: Dict[str, List[Dict[str, Any]]] = {}
        self._load()

    def _load(self):
        if os.path.exists(self.path):
            try:
                with open(self.path, "r", encoding="utf-8") as f:
                    self._data = json.load(f)
            except Exception:
                self._data = {}
        else:
            self._data = {}

    def _save(self):
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(self._data, f, ensure_ascii=False, indent=2)

    def add_attempt(self, question_id: str, result: bool, timestamp: Optional[str] = None):
        entry = {
            "ts": timestamp or datetime.utcnow().isoformat(),
            "result": int(result)
        }
        if question_id not in self._data:
            self._data[question_id] = []
        self._data[question_id].append(entry)
        self._save()

    def get_attempts(self, question_id: str) -> List[Dict[str, Any]]:
        return self._data.get(question_id, [])

    def get_all_attempts(self) -> Dict[str, List[Dict[str, Any]]]:
        return self._data

    def get_score(self, question_id: str) -> Optional[float]:
        attempts = self._data.get(question_id)
        if not attempts:
            return None
        return sum(a["result"] for a in attempts) / len(attempts)

    def clear_all(self):
        self._data = {}
        self._save()

# Example usage:
# storage = AttemptStorage()
# storage.add_attempt("abc123", True)
# score = storage.get_score("abc123")
