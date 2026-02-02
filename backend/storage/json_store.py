import json
import os
from typing import Dict, Any

# Get the project root directory (go up from backend/storage/ to project root)
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
DATA_FILE = os.path.join(PROJECT_ROOT, "data", "bank_data.json")

class JsonStore:
    """
    Low-level file handler.
    Responsibility: Read/Write raw JSON data safely.
    """

    @staticmethod
    def _initialize_if_missing():
        """Creates the data file if it doesn't exist."""
        if not os.path.exists(DATA_FILE):
            os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
            with open(DATA_FILE, "w") as f:
                json.dump({"users": [], "accounts": [], "transactions": []}, f, indent=2)

    @staticmethod
    def load_data() -> Dict[str, Any]:
        """Reads the entire JSON DB."""
        JsonStore._initialize_if_missing()
        try:
            with open(DATA_FILE, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            # Fallback if file is corrupted
            return {"users": [], "accounts": [], "transactions": []}

    @staticmethod
    def save_data(data: Dict[str, Any]):
        """Overwrites the JSON DB with new data."""
        JsonStore._initialize_if_missing()
        with open(DATA_FILE, "w") as f:
            json.dump(data, f, indent=2)
