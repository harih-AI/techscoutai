from core.llm import call_llm
from core.prompts import SYSTEM_PROMPT, TECH_QUESTION_PROMPT, VALIDATION_PROMPT, EXTRACTION_PROMPT
import re

def generate_questions(tech_stack, experience):
    """
    Generates technical interview questions for each technology in the stack.
    """
    questions = []
    for tech in tech_stack:
        q = call_llm(
            SYSTEM_PROMPT,
            TECH_QUESTION_PROMPT.format(
                tech=tech,
                exp=experience,
                n=1 # Reduced to 1 for brevity in this demo flow
            )
        )
        questions.append((tech, q))
    return questions

def validate_answer(tech, question, answer):
    """
    Validates a technical answer using the LLM.
    """
    feedback = call_llm(
        SYSTEM_PROMPT,
        VALIDATION_PROMPT.format(
            tech=tech,
            question=question,
            answer=answer
        )
    )
    return feedback

def clean_tech_stack(input_str):
    """
    Cleans messy tech stack input into a proper list.
    """
    # Split by comma or semicolon
    items = re.split(r'[,;]+', input_str)
    # Strip whitespace and title case, filter out empty strings
    cleaned = [t.strip().title() for t in items if t.strip()]
    return cleaned

def extract_info_with_llm(context, user_input):
    """
    Uses LLM to extract specific information from a conversational user input.
    """
    result = call_llm(
        SYSTEM_PROMPT,
        EXTRACTION_PROMPT.format(
            context=context,
            user_input=user_input
        )
    )
    if result.upper() == "NONE":
        return None
    return result
