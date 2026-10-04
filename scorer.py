"""
scorer.py — Evaluates whether the retrieved chunks or model answer meet expectations.
"""

def judge(question: str, expects: str, answer: str, results) -> bool:
    """
    Check if the retrieved chunks contain the expected text.
    Milestone 1 uses this to judge retrieval against criterion 1.
    """
    if not expects or not results:
        return False
    exp = expects.lower().strip()
    return any(exp in r.text.lower() for r in results)
