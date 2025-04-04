class SchoolChatbot:
    """
    This class is extra scaffolding around a model. Modify this class to specify how the model recieves prompts and generates responses.

    Example usage:
        model, tokenizer = load_model()
        chatbot = SchoolChatbot(model, tokenizer)
        response = chatbot.get_response("What schools offer Spanish programs?")
    """

    def __init__(self, model, tokenizer):
        """
        Initialize the chatbot with a model and tokenizer.
        You don't need to modify this method.
        """
        self.model = model
        self.tokenizer = tokenizer
        
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
        pass
        
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
        pass