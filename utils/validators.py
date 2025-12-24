import re

EXIT_WORDS = ["exit", "quit", "bye", "stop"]

def is_exit(text: str) -> bool:
    return text.lower().strip() in EXIT_WORDS

def is_valid(text: str) -> bool:
    return text is not None and text.strip() != ""

def is_valid_email(email: str) -> bool:
    """Simple regex for email validation."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email.strip()))

def is_valid_phone(phone: str) -> bool:
    """Simple regex for phone validation (allows +, digits, spaces, dashes)."""
    pattern = r'^[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}$'
    # More relaxed for international:
    if not bool(re.match(pattern, phone.strip())):
        # Fallback to checking if it has at least 7 digits
        digits = re.sub(r'\D', '', phone)
        return len(digits) >= 7
    return True

def extract_years(text: str) -> str:
    """Extracts first number found in string, or returns empty if none."""
    numbers = re.findall(r'\d+', text)
    return numbers[0] if numbers else ""
