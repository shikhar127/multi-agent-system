import os
from dotenv import load_dotenv

load_dotenv()

def run(question: str) -> str:
    # Pipeline: call_1 -> call_2 -> call_3 -> final answer
    raise NotImplementedError("Pipeline not yet implemented")

if __name__ == "__main__":
    question = input("Ask a question: ")
    answer = run(question)
    print(answer)
