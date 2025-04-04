"""
This module handles loading and saving of LLaMA models with efficient quantization.
This is already implemented and ready to use -- you don't need to modify this file.

Key Features:
- Loads LLaMA models from Hugging Face or local storage
- Implements 4-bit quantization for memory efficiency
- Provides save/load functionality for model persistence
- Handles model loading errors gracefully

Example Usage:
    from model import load_model, save_model
    
    # Load a model (will download if not found locally)
    model, tokenizer = load_model("meta-llama/Llama-2-7b-chat-hf")
    
    # Save model after making changes
    save_model(model, tokenizer)
"""

import os
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
import torch
import gc

# Choose a model
MODEL_NAME = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"  # Change this to your preferred model
# Other options:
# MODEL_NAME = "meta-llama/Llama-2-7b-chat-hf"
# MODEL_NAME = "openlm-research/open_llama_3b"

# Path to save and load models
MODEL_SAVE_PATH = "models/school_chatbot"


def save_model(model, tokenizer, save_directory="models/school_chatbot"):
    """
    Save the model and tokenizer to a local directory with CPU memory optimization
    """
    # Create directory if it doesn't exist
    os.makedirs(save_directory, exist_ok=True)
    
    # Move model to CPU if it's on GPU
    model = model.cpu()
    
    # Save in half precision to reduce file size
    model.half()  # Convert to float16
    
    try:
        # Save in smaller chunks
        model.save_pretrained(
            save_directory,
            safe_serialization=True,  # More memory efficient serialization
            max_shard_size="500MB"    # Split into smaller files
        )
        
        # Save tokenizer (relatively small, no special handling needed)
        tokenizer.save_pretrained(save_directory)
        
        print(f"Model and tokenizer saved to {save_directory}")
    finally:
        # Clean up memory
        gc.collect()
        
        # Convert back to float32 for continued use if needed
        model.float()


def load_model():
    """
    Load the model for CPU usage
    """
    try:
        if os.path.exists(MODEL_SAVE_PATH):
            print("Loading model from local storage...")
            tokenizer = AutoTokenizer.from_pretrained(MODEL_SAVE_PATH)
            model = AutoModelForCausalLM.from_pretrained(
                MODEL_SAVE_PATH,
                low_cpu_mem_usage=True,
                torch_dtype=torch.float32
            )
        else:
            print("Downloading model from Hugging Face... Should take 2-3 minutes.")
            tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
            model = AutoModelForCausalLM.from_pretrained(
                MODEL_NAME,
                low_cpu_mem_usage=True,
                torch_dtype=torch.float32
            )
            # Save for future use
            save_model(model, tokenizer)
            
        # Move model to CPU
        model = model.to("cpu")
        return model, tokenizer
        
    except Exception as e:
        print(f"Error loading model: {e}")
        return None, None

if __name__ == "__main__":
    model, tokenizer = load_model()
    print(model)
    print(tokenizer)
