"""
Typing Takedown — High Score Manager
Saves and loads high scores per game mode to a JSON file.
"""

import json
import os
from datetime import datetime

SCORES_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "scores.json")
MAX_SCORES_PER_MODE = 10


def _load_all() -> dict:
    """Load all scores from the JSON file."""
    if not os.path.exists(SCORES_FILE):
        return {}
    try:
        with open(SCORES_FILE, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return {}


def _save_all(data: dict):
    """Save all scores to the JSON file."""
    with open(SCORES_FILE, "w") as f:
        json.dump(data, f, indent=2)


def save_score(mode: str, stats_summary: dict):
    """
    Save a new score entry for a game mode.
    Keeps only the top MAX_SCORES_PER_MODE scores per mode.
    """
    data = _load_all()

    entry = {
        "score": stats_summary.get("score", 0),
        "wpm": stats_summary.get("wpm", 0),
        "accuracy": stats_summary.get("accuracy", 0),
        "max_combo": stats_summary.get("max_combo", 0),
        "enemies_defeated": stats_summary.get("enemies_defeated", 0),
        "time_played": stats_summary.get("time_played", 0),
        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
    }

    if mode not in data:
        data[mode] = []

    data[mode].append(entry)
    # Sort by score descending, keep top N
    data[mode] = sorted(data[mode], key=lambda x: x["score"], reverse=True)[
        :MAX_SCORES_PER_MODE
    ]

    _save_all(data)


def get_high_scores(mode: str) -> list:
    """Get the list of high scores for a given mode."""
    data = _load_all()
    return data.get(mode, [])


def get_all_high_scores() -> dict:
    """Get all high scores organized by mode."""
    return _load_all()


def get_top_score(mode: str) -> int:
    """Get the highest score for a mode, or 0 if none."""
    scores = get_high_scores(mode)
    if scores:
        return scores[0].get("score", 0)
    return 0


def is_new_high_score(mode: str, score: int) -> bool:
    """Check if a score would be a new record for the mode."""
    return score > get_top_score(mode)
