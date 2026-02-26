POSITIVE_WORDS = {"great", "good", "interested", "yes", "sure", "okay"}
NEGATIVE_WORDS = {"no", "stop", "busy", "not interested", "angry", "frustrated"}


def score_sentiment(text: str) -> float:
    t = text.lower()
    score = 0
    for w in POSITIVE_WORDS:
        if w in t:
            score += 1
    for w in NEGATIVE_WORDS:
        if w in t:
            score -= 1
    return max(-1.0, min(1.0, score / 3.0))
