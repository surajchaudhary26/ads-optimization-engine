def label_badge(label: str) -> str:
    if label == "Best Choice":
        return "BEST"
    if label == "Good Choice":
        return "GOOD"
    return "REVIEW"
