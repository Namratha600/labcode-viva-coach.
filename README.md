# LabCode Fixer & Viva Coach

> **Don't just fix the bug. Learn how to defend the code.**

LabCode Fixer & Viva Coach is a student-focused AI debugging and viva preparation tool.

It helps students understand programming errors instead of simply copying a solution. The application explains why the code failed, provides a corrected version, and generates three technical viva questions based on the student's actual code.

## Problem

Students often use AI tools to fix compiler or runtime errors, but they may still struggle to explain the solution during a laboratory viva.

A professor may ask:

- Why did this error occur?
- Which line caused the error?
- What value caused the problem?
- Why did you use this particular fix?
- What happens if the input changes?
- What programming concept is involved?

LabCode Fixer & Viva Coach is designed to help students prepare for these questions.

## How It Works

The application follows this workflow:

**Debug → Understand → Correct → Defend**

1. Select the programming language.
2. Paste the broken code.
3. Paste the compiler or runtime error.
4. The AI analyzes the problem.
5. The application explains why the code failed.
6. A corrected version of the code is provided.
7. Three technical viva questions are generated.

## Architecture

```text
Student
   |
   v
Streamlit Frontend
   |
   v
FastAPI Backend
   |
   v
Ollama
   |
   v
Gemma 2B
   |
   v
AI Response
   |
   v
Streamlit Frontend
```
