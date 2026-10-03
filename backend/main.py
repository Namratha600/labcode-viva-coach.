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

Analyze the code according to the rules, syntax, runtime behavior,
and error behavior of the specified programming language.

Do not apply rules from another programming language.


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
- Never describe a variable as "unassigned" or "not assigned" if the code
  explicitly assigns it the value null.
- In Java, remember that null is a valid reference value, but calling an
  instance method through a null reference can cause NullPointerException.
- Explain what happens at the exact expression that causes the error.
- Make sure the explanation is technically correct for the specified language.
- Use simple student-friendly English.


CORRECTED CODE RULES:

- Preserve the student's original purpose and structure.
- Make the minimum necessary change to fix the reported error.
- Verify that the corrected code actually removes the reported error.
- Do not introduce the same error again.
- Mentally check the corrected code before providing it.
- Do not unnecessarily rewrite the program.
- Do not change variable names or logic unless required.
- The corrected code MUST be inside a proper fenced code block.
- Use the correct language identifier for the code block, such as
  ```java, ```python, ```c, or ```cpp.
- Preserve normal line breaks and indentation.
- Include a short comment only if it helps the student understand the fix.


VIVA QUESTION RULES:

Provide EXACTLY 3 technical viva questions.

Every question MUST be directly based on the student's actual code.

At least one question must refer to the exact expression that causes
the error.

At least one question must test understanding of the specific value,
variable, index, object, condition, or operation involved in the error.

At least one question must test the programming concept needed to
understand or prevent the error.

Questions should be specific enough that a professor could ask them
while looking at this exact code.

For example, if the code contains:
    String name = null;
    System.out.println(name.length());

Good questions include:
- What value is stored in name when name.length() is executed?
- Why does calling length() on name cause a NullPointerException?
- How could you modify this code so that name.length() can execute safely?

Bad questions include:
- What is a class?
- What is the main method?
- What is Java?
- What is the syntax of a method?

Do NOT ask generic questions unrelated to the reported error.

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

        return {
            "analysis": response["message"]["content"]
        }

    except Exception as e:
        return {
            "error": "Unable to analyze the code right now.",
            "details": str(e)
        }