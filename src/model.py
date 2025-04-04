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

# Choose a model
MODEL_NAME = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"  # Change this to your preferred model
# Other options:
# MODEL_NAME = "meta-llama/Llama-2-7b-chat-hf"
# MODEL_NAME = "openlm-research/open_llama_3b"

# Path to save and load models
MODEL_SAVE_PATH = "models/school_chatbot"


def save_model(model, tokenizer, save_directory="models/school_chatbot"):
    """
    Save the model and tokenizer to a local directory
    """
    # Create directory if it doesn't exist
    os.makedirs(save_directory, exist_ok=True)
    
    # Save model and tokenizer
    model.save_pretrained(save_directory)
    tokenizer.save_pretrained(save_directory)
    
    print(f"Model and tokenizer saved to {save_directory}")


def load_model():
    """
    Load the model with 4-bit quantization
    """
    try:
        # Use quantization to reduce memory usage
        quantization_config = BitsAndBytesConfig(
            load_in_4bit=True,              # Enable 4-bit quantization
            bnb_4bit_compute_dtype=torch.float16,  # Compute dtype
            bnb_4bit_quant_type="nf4",     # Normalized float 4 format
            bnb_4bit_use_double_quant=True # Use nested quantization
        )

        if os.path.exists(MODEL_SAVE_PATH):
            print("Loading quantized model from local storage...")
            tokenizer = AutoTokenizer.from_pretrained(MODEL_SAVE_PATH)
            model = AutoModelForCausalLM.from_pretrained(
                MODEL_SAVE_PATH,
                quantization_config=quantization_config,
                device_map="auto"
            )
        else:
            print("Downloading and quantizing model from Hugging Face...")
            tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
            model = AutoModelForCausalLM.from_pretrained(
                MODEL_NAME,
                quantization_config=quantization_config,
                device_map="auto"
            )
            # Save for future use
            save_model(model, tokenizer)
            
        return model, tokenizer
        
    except Exception as e:
        print(f"Error loading model: {e}")
        return None, None

