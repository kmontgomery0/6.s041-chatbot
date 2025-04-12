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
        # Get response from chatbot
        response = chatbot.get_response(message)
        return response

    
    
    # Create Gradio interface. Customize the interface however you'd like!
    demo = gr.ChatInterface(
        fn=chat,
        title="Boston Public School Recommender",
        description=(
            "Looking for a Boston public school for your child? <br><br>"
            "I'm here to help you explore school options based on your needs.<br><br>"
            "<b>Tell me things like:</b><br> "
            "• Your neighborhood (e.g., Roxbury, Jamaica Plain)<br>"
            "• Grade level (e.g., kindergarten, 6th grade)<br>"
            "• Program preferences (e.g., Spanish immersion, advanced work, STEM focus)<br>"
            "• Special requirements (e.g., before-school care, bus eligibility)<br><br>"
            "I'll recommend schools, explain programs, and answer your questions."
        ),
        examples=[
            "I live in Dorchester and my daughter is going into 1st grade. Any schools you recommend?",
            "We want a school with Spanish immersion for kindergarten near Jamaica Plain.",
            "My son is in 6th grade and loves science. Are there STEM-focused schools in Boston?",
            "Do any Boston public schools offer advanced work classes in 4th grade?",
            "We need before-school care and bus service. Which schools provide those?",
        ]
    )

    
    return demo

if __name__ == "__main__":
    demo = create_chatbot()
    demo.launch()