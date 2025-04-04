import torch
import gc

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
    
        # Memory-efficient tokenization
        print("Tokenizing...")
        inputs = self.tokenizer(
            prompt,
            return_tensors="pt",
            padding=True,
            truncation=True,
            max_length=256    # Reduced input length for CPU
        )
        
        # Memory-efficient generation
        print("Generating...")
        with torch.inference_mode():
            outputs = self.model.generate(
                inputs['input_ids'],    # Changed to directly use input_ids
                attention_mask=inputs['attention_mask'] if 'attention_mask' in inputs else None,
                max_new_tokens=150,     # Reduced output length for CPU
                temperature=0.7,
                top_p=0.95,
                do_sample=True,
                pad_token_id=self.tokenizer.eos_token_id,
                repetition_penalty=1.2,
                num_return_sequences=1,
                early_stopping=True
            )
        
        # Clean up memory
        del inputs
        gc.collect()     # Force garbage collection
        
        response = self.tokenizer.decode(
            outputs[0],
            skip_special_tokens=True,
            clean_up_tokenization_spaces=True
        )
        
        # Clean up more memory
        del outputs
        gc.collect()
        
        response = response.split("Assistant:")[-1].strip()
        return response