from huggingface_hub import InferenceClient
from config import BASE_MODEL, MY_MODEL, HF_TOKEN

class SchoolChatbot:
    """
    This class is extra scaffolding around a model. Modify this class to specify how the model recieves prompts and generates responses.

    Example usage:
        chatbot = SchoolChatbot()
        response = chatbot.get_response("What schools offer Spanish programs?")
    """

    def __init__(self):
        """
        Initialize the chatbot with a HF model ID
        """
        model_id = MY_MODEL if MY_MODEL else BASE_MODEL # define MY_MODEL in config.py if you create a new model in the HuggingFace Hub
        self.client = InferenceClient(model=model_id, token=HF_TOKEN)
        
    def format_prompt(self, user_input):
        """
        TODO: Implement this method to format the user's input into a proper prompt.
        
        This method should:
        1. Add any necessary system context or instructions
        2. Format the user's input appropriately
        3. Add any special tokens or formatting the model expects

        Args:
            user_input (str): The user's question about Boston schools

        Returns:
            str: A formatted prompt ready for the model
        
        Example prompt format:
            "You are a helpful assistant that specializes in Boston schools...
             User: {user_input}
             Assistant:"
        """
        system_prompt = """You are a helpful assistant that specializes in helping parents choose Boston public schools.
        You provide accurate information about school programs, locations, enrollment processes, and other important details.
        Always be professional, clear, and focused on helping parents make informed decisions about schools.
        """
        
        # Combine system prompt with user input
        formatted_prompt = f"""
        {system_prompt}

        User: {user_input}
        Assistant:"""
        
        return formatted_prompt
        
    def get_response(self, user_input):
        """
        TODO: Implement this method to generate responses to user questions.
        
        This method should:
        1. Use format_prompt() to prepare the input
        2. Generate a response using the model
        3. Clean up and return the response

        Args:
            user_input (str): The user's question about Boston schools

        Returns:
            str: The chatbot's response

        Implementation tips:
        - Use self.tokenizer to convert text to tokens
        - Use self.model.generate() for text generation
        - Consider parameters like temperature and max_length
        - Clean up the response before returning it
        """
        prompt = self.format_prompt(user_input)
        
        try:
            print("Generating response...")
            response = self.client.text_generation(
                prompt,
                max_new_tokens=300,
                temperature=0.7,
                top_p=0.95,
                do_sample=True,
                return_full_text=False
            )
            return response.strip().split("Assistant:")[-1].strip()
            
        except Exception as e:
            print(f"API error: {e}")
            return f"I apologize, but I encountered an error: {str(e)}"