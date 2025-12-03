import sys
sys.path.append('src/components/ai')
from llm import rag_answer
import os

# Test the RAG pipeline
if __name__ == "__main__":
    # API key
    api_key = "AIzaSyCQZZSP3RlmP97XYIwt9JCcNTezM3GSuNc"

    sql_file = "src/data/data_fixed.sql"

    # Test question
    question = "What are the top 5 highest rated menu items?"

    print(f"\n{'='*60}")
    print(f"Testing RAG Pipeline")
    print(f"{'='*60}")
    print(f"\nQuestion: {question}")
    print(f"\nProcessing...\n")

    try:
        answer = rag_answer(question, sql_file, api_key)
        print(f"\n{'='*60}")
        print(f"FINAL ANSWER")
        print(f"{'='*60}")
        print(answer)
        print(f"\n{'='*60}")
        print("Test completed successfully!")
        print(f"{'='*60}\n")
    except Exception as e:
        print(f"\nError occurred: {e}")
        import traceback
        traceback.print_exc()
