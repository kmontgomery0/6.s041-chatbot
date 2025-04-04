"""
Gradio Web Interface for Boston School Chatbot

This script creates a web interface for your chatbot using Gradio.
You only need to implement the chat function.

Key Features:
- Creates a web UI for your chatbot
- Handles conversation history
- Provides example questions
- Can be deployed to Hugging Face Spaces

Example Usage:
    # Run locally:
    python app.py
    
    # Access in browser:
    # http://localhost:7860
"""

import gradio as gr
from src.model import load_model, generate_response
from src.chat import SchoolChatbot

def create_chatbot():
    """
    Creates and configures the chatbot interface.
    """
    model, tokenizer = load_model()
    chatbot = SchoolChatbot(model, tokenizer)
    
    def chat(message, history):
        """
        TODO:Generate a response for the current message in a Gradio chat interface.
        
        This function is called by Gradio's ChatInterface every time a user sends a message.
        You only need to generate and return the assistant's response - Gradio handles the
        chat display and history management automatically.

        Args:
            message (str): The current message from the user
            history (list): List of previous message pairs, where each pair is
                           [user_message, assistant_message]
                           Example:
                           [
                               ["What schools offer Spanish?", "The Hernandez School..."],
                               ["Where is it located?", "The Hernandez School is in Roxbury..."]
                           ]

        Returns:
            str: The assistant's response to the current message.


        Note:
            - Gradio automatically:
                - Displays the user's message
                - Displays your returned response
                - Updates the chat history
                - Maintains the chat interface
            - You only need to:
                - Generate an appropriate response to the current message
                - Return that response as a string
        """
        # TODO: Generate and return response
        pass
    
    # Create Gradio interface
    demo = gr.ChatInterface(
        chat,
        title="Boston Public School Selection Assistant",
        description="Ask me anything about Boston public schools!",
        examples=[
            "What schools in Jamaica Plain offer Spanish programs?",
            "How do I schedule a tour of the Hernandez School?"
        ]
    )
    
    return demo

if __name__ == "__main__":
    demo = create_chatbot()
    demo.launch()