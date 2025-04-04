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
from src.chat import SchoolChatbot

def create_chatbot():
    """
    Creates and configures the chatbot interface.
    """
    chatbot = SchoolChatbot()
    
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
        try:
            # Generate response using our chatbot
            response = chatbot.get_response(message)
            return response
            
        except Exception as e:
            return f"I apologize, but I encountered an error. Please try again. Error: {str(e)}"
    
    
    # Create Gradio interface. Customize the interface as you'd like!
    demo = gr.ChatInterface(
        chat,
        title="Boston Public School Selection Assistant",
        description="Ask me anything about Boston public schools! Since I am a free tier chatbot, I may give a 503 error when I'm busy. If that happens, please try again in a few minutes.",
        examples=[
            "I live in Jamaica Plain and want to send my child to kindergarten. What schools are available?"
        ]
    )
    
    return demo

if __name__ == "__main__":
    demo = create_chatbot()
    demo.launch()