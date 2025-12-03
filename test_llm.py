import sys
sys.path.append('src/components/ai')
from llm import rag_answer
import os

# Test the RAG pipeline
if __name__ == "__main__":
    # Check if API key is set
    api_key = os.environ.get("GEMINI_API_KEY")

    if not api_key:
        print("ERROR: Please set GEMINI_API_KEY environment variable")
        print("Example: export GEMINI_API_KEY='your-api-key-here'")
        sys.exit(1)

    sql_file = "Platemate_mock_data_trail.sql"

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
        print("✅ Test completed successfully!")
        print(f"{'='*60}\n")
    except Exception as e:
        print(f"\n❌ Error occurred: {e}")
        import traceback
        traceback.print_exc()
