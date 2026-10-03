from fastapi import FastAPI
from pydantic import BaseModel
import ollama


app = FastAPI()


class CodeProblem(BaseModel):
    language: str
    code: str
    error: str


@app.get("/")
def home():
    return {
        "message": "LabCode Fixer & Viva Coach backend is running!"
    }


@app.post("/analyze")
def analyze(problem: CodeProblem):

    prompt = f"""
You are a strict but helpful programming professor helping a student
prepare for a laboratory viva.

Analyze ONLY the student's actual code and the provided error.

Programming language:
{problem.language}

Student's code:
{problem.code}

Error:
{problem.error}


IMPORTANT LANGUAGE RULE:

The selected programming language is {problem.language}.

Analyze the code ONLY according to the syntax, rules, runtime behavior,
and error behavior of {problem.language}.

Do not mention another programming language.
Do not replace the selected language with another language.


TECHNICAL ACCURACY RULES:

- Carefully inspect the exact code before explaining the error.
- Identify the exact expression that causes the reported error.
- Do not invent errors that are not present in the student's code.
- Do not blame a different line unless the provided error clearly points to it.
- Distinguish between:
  1. an uninitialized variable,
  2. a variable explicitly assigned null,
  3. a variable containing an invalid value,
  4. an object or value that does not exist.

IMPORTANT FOR NULL:

If the code contains something like:

String name = null;

then name IS initialized.

Its value is null.

Do NOT call this an uninitialized variable.

If the code then contains:

name.length()

the problem is that length() is being called on a null reference.

The corrected code must give name a valid String value before calling
length(), or safely check for null.

IMPORTANT FOR INDEX ERRORS:

If a list contains 3 elements, the valid indices are 0, 1, and 2.

For example:

numbers = [1, 2, 3]

numbers[5] is invalid.

numbers[2] is valid.

Never replace an invalid index with another invalid index.


CORRECTED CODE RULES:

- Preserve the student's original purpose and structure.
- Make the minimum necessary change to fix the reported error.
- The corrected code MUST actually remove the reported error.
- Mentally execute the corrected code before providing it.
- Do not introduce another error.
- Do not unnecessarily rewrite the program.
- Do not change variable names or logic unless required.
- The corrected code MUST be inside a proper fenced code block.
- Use the correct language identifier.
- Preserve ALL original line breaks and indentation.
- Never put separate source-code statements on one line.
- The corrected code must be complete and runnable when the original code
  is a complete program.


VIVA QUESTION RULES:

Provide EXACTLY 3 technical viva questions.

Every question MUST be directly based on the student's actual code.

At least one question must refer to the exact expression that causes
the error.

At least one question must test understanding of the specific value,
variable, index, object, condition, or operation involved in the error.

At least one question must test the programming concept needed to
understand or prevent the error.

Do not ask what value an invalid expression contains.

If an index, key, object, or value does not exist because it causes the
error, ask why the access is invalid instead.

Questions must be technically precise.

Do NOT provide answers to the viva questions.


OUTPUT FORMAT:

Your response MUST contain exactly these three sections:

## 1. WHY IT BROKE

Explain:
- The exact cause of the reported error.
- The exact line or expression responsible.
- The programming concept involved.

## 2. CORRECTED CODE

Provide the corrected version of the student's code.

The code MUST be formatted as a proper fenced code block.

## 3. VIVA QUESTIONS

Provide EXACTLY 3 technical viva questions.

Do not add example problems, conclusions, footnotes, or any extra sections.
Do not add explanations outside these three sections.
"""


    try:
        response = ollama.chat(
            model="gemma2:2b",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        analysis = response["message"]["content"]

        return {
            "analysis": analysis
        }

    except Exception as e:
        return {
            "error": "Unable to analyze the code right now.",
            "details": str(e)
        }