EXIT_WORDS = ["exit", "quit", "bye", "stop"]

def is_exit(text: str) -> bool:
    return text.lower().strip() in EXIT_WORDS

def is_valid(text: str) -> bool:
    return text is not None and text.strip() != ""
