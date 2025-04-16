import os
from dotenv import load_dotenv

# Load from .env file. Store your HF token in the .env file.
load_dotenv()


BASE_MODEL = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
# BASE_MODEL = "meta-llama/Llama-3-8b-chat-hf"
# Other options:
# MODEL = "meta-llama/Llama-2-7b-chat-hf"
# MODEL = "openlm-research/open_llama_3b"

# If you finetune the model or change it in any way, save it to huggingface hub, then set MY_MODEL to your model ID. The model ID is in the format "your-username/your-model-name".
MY_MODEL = None

HF_TOKEN = os.getenv("HF_TOKEN")
