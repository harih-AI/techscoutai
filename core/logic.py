from core.llm import call_llm
from core.prompts import SYSTEM_PROMPT, TECH_QUESTION_PROMPT

def generate_questions(tech_stack, experience):
    questions = []
    for tech in tech_stack:
        q = call_llm(
            SYSTEM_PROMPT,
            TECH_QUESTION_PROMPT.format(
                tech=tech,
                exp=experience,
                n=3
            )
        )
        questions.append((tech, q))
    return questions
