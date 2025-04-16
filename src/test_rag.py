"""
Test script for the RAG-based Boston Schools Chatbot

This script provides a simple way to test the RAG functionality
by asking questions and showing both the retrieved documents
and the final model response.
"""

from src.chat import SchoolChatbot
import argparse

def test_rag_chatbot(query):
    """
    Test the RAG-based chatbot with a specific query.
    
    Args:
        query (str): The question to ask the chatbot
    """
    print(f"Initializing chatbot with RAG capability...")
    chatbot = SchoolChatbot()
    
    print("\n" + "="*50)
    print(f"QUERY: {query}")
    print("="*50)
    
    # Get the retrieved documents
    retrieved_docs = chatbot.rag_engine.retrieve(query, top_k=3)
    
    print("\nRetrieved Documents:")
    print("-"*50)
    for i, doc in enumerate(retrieved_docs, 1):
        print(f"{i}. {doc.school_name}")
        print(f"   {doc.content}")
        print(f"   Neighborhood: {doc.metadata.get('neighborhood', 'Unknown')}")
        print(f"   Grades: {doc.metadata.get('grades', 'Unknown')}")
        print(f"   Programs: {', '.join(doc.metadata.get('programs', []))}")
        print()
    
    # Get the chatbot's response
    print("\nChatbot Response:")
    print("-"*50)
    response = chatbot.get_response(query)
    print(response)
    print("="*50)
    

def main():
    parser = argparse.ArgumentParser(description="Test the RAG-based Boston Schools Chatbot")
    parser.add_argument("--query", type=str, 
                        default="My child is starting kindergarten and we live in Jamaica Plain. What are our options?",
                        help="The question to ask the chatbot")
    
    args = parser.parse_args()
    test_rag_chatbot(args.query)

if __name__ == "__main__":
    main() 