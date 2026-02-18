"""
Claude (Anthropic) integration for defect analysis, report summaries, and retraining suggestions.
"""
import os
from pathlib import Path
from typing import Optional

# Load .env for ANTHROPIC_API_KEY
try:
    from dotenv import load_dotenv
    env_path = Path(__file__).resolve().parent.parent.parent / ".env"
    load_dotenv(env_path)
except ImportError:
    pass

try:
    import anthropic
    HAS_ANTHROPIC = True
except ImportError:
    HAS_ANTHROPIC = False


def _get_client():
    """Get Anthropic client if API key is configured."""
    if not HAS_ANTHROPIC:
        return None
    key = os.getenv("ANTHROPIC_API_KEY", "").strip()
    if not key or key.startswith("sk-ant-your"):
        return None
    return anthropic.Anthropic(api_key=key)


def analyze_defect_report(stats: dict) -> str:
    """Use Claude to analyze quality inspection report and suggest actions."""
    client = _get_client()
    if not client:
        return "Set ANTHROPIC_API_KEY in .env to enable AI analysis."
    try:
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=500,
            messages=[
                {
                    "role": "user",
                    "content": f"Analyze this quality inspection report and suggest actions. Keep it concise with bullet points.\n\n{stats}",
                }
            ],
        )
        return response.content[0].text
    except Exception as e:
        return f"Error: {e}"


def suggest_retrain(stats: dict, recent_fail_rate: float) -> str:
    """Claude suggests when to retrain based on defect trends."""
    client = _get_client()
    if not client:
        return "Set ANTHROPIC_API_KEY in .env for retraining suggestions."
    try:
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=300,
            messages=[
                {
                    "role": "user",
                    "content": f"Quality stats: {stats}. Recent fail rate: {recent_fail_rate:.1%}. Should we retrain the defect model? Reply with Yes/No and brief reasoning.",
                }
            ],
        )
        return response.content[0].text
    except Exception as e:
        return f"Error: {e}"


def generate_defect_description(defect_class: str, confidence: float) -> str:
    """Generate a human-readable defect description using Claude."""
    client = _get_client()
    if not client:
        return f"Defect: {defect_class} ({confidence:.0%} confidence)"
    try:
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=150,
            messages=[
                {
                    "role": "user",
                    "content": f"One-line manufacturing defect description for class '{defect_class}' at {confidence:.0%} confidence. Be concise and actionable for a QA engineer.",
                }
            ],
        )
        return response.content[0].text.strip()
    except Exception:
        return f"Defect: {defect_class} ({confidence:.0%} confidence)"
