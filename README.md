---
title: Staff School Choice Chatbot
emoji: 🚀
colorFrom: blue
colorTo: red
sdk: gradio
sdk_version: 5.23.3
python_version: "3.10"
app_file: app.py
pinned: false
---

# Boston Public School Selection Chatbot

This is a skeleton repo you can use to design a school choice chatbot. Feel free to change it however you'd like! This repo is compatible with CPU (using your own computer). Loading the model and running inference might be a little slow, but it should be manageable. If you have access to your own GPUs you can use them as well, but we don't require it whatsoever.

The end goal: make the chatbot and upload it to a huggingface space. We have included instructions for interacting with huggingface below. Here's an example of the final output we made as an example:. Your chatbot should be much better!

Note: We encourage you to use AI tools (like Cursor or LLMs) to help you on this assignment. Learn how to leverage these tools.

## Setup

1. Make a virtual environment and install the required dependencies:
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

2. Make a HuggingFace account and make an access token:
   - Visit [Hugging Face](https://huggingface.co)
   - Make an account if you don't already have one
   - Click on your profile, then "Access Tokens" and make a new token
   - Make a .env file and save the token as HF_TOKEN
   - Now, log in to Hugging Face in the terminal as well:
   ```bash
   huggingface-cli login
   ```

3. Choose a base model:
   - In config.py, set the BASE_MODEL variable to your base model of choice from HuggingFace.
   - Keep in mind it's better to have a small, lightweight model if you plan on finetuning.

3. Run the chatbot:
```bash
python app.py
```

## Deploying to Hugging Face

To deploy your chatbot as a free web interface using Hugging Face Spaces:

1. Create a Hugging Face Space:
   - Go to [Hugging Face Spaces](https://huggingface.co/spaces)
   - Click "New Space"
   - Choose a name for your space (e.g., "boston-school-chatbot")
   - Select "Gradio" as the SDK
   - Choose "CPU" as the hardware (free tier)
   - Make it "Public" so others can use your chatbot

2. Prepare your files:
   Your repository should already have all needed files:
   ```
   6.so41-midterm/
   ├── README.md           # Description of your chatbot
   ├── app.py             # Your Gradio interface
   ├── requirements.txt   # Already set up with needed dependencies
   └── src/              # Your implementation files
   ```

3. Push your code to the Space:
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://huggingface.co/spaces/YOUR_USERNAME/YOUR_SPACE_NAME
   git push -u origin main
   ```

4. Important Free Tier Considerations:
   - Use free tier model (already configured in model.py)
   - Free CPU spaces have 2GB RAM limit
   - Responses might be slower than local testing
   - The interface might queue requests when multiple users access it

5. After Deployment:
   - Your chatbot will be available at: `https://huggingface.co/spaces/YOUR_USERNAME/YOUR_SPACE_NAME`
   - Anyone can use it through their web browser
   - You can update the deployment anytime by pushing changes:
     ```bash
     git add .
     git commit -m "Update chatbot"
     git push
     ```

6. Troubleshooting:
   - Check the Space's logs if the chatbot isn't working
   - Make sure you're using TinyLlama model
   - Verify the chatbot works locally before deploying
   - Remember free tier has limited resources

Your chatbot should now be accessible to anyone through their web browser!

## Repository Organization

```
boston-school-chatbot/
├── app.py              # Gradio web interface - implement the chat function
├── requirements.txt    # Python dependencies
├── chatbot_development.ipynb     # Notebook for developing and testing your chatbot
├── chatbot_conversation_example.txt     # Example conversation we might want to have with this chatbot
└── src/
    ├── model.py       # Model loading/saving (already implemented)
    └── chat.py        # SchoolChatbot class (implement this)
```

### Key Files:

- **app.py**: Creates the web interface using Gradio. You only need to implement the `chat` function that generates responses.

- **chat.py**: Contains the `SchoolChatbot` class where you'll implement:
  - `format_prompt`: Format user input into proper prompts
  - `get_response`: Generate responses using the model

- **config.py**: Contains the `BASE_MODEL` and `MY_MODEL` variables, which are names of models on HuggingFace. Update the `MY_MODEL` variable if you create a new model and upload it to the HuggingFace Hub.

- **chatbot_development.ipynb**: Jupyter notebook for:
  - Experimenting with the chatbot
  - Trying different approaches
  - Testing responses before deployment

### What You Need to Implement:

1. In `chat.py`:
   - Complete the `SchoolChatbot` class methods
   - Design how the chatbot formats prompts
   - Implement response generation

2. In `app.py`:
   - Implement the `chat` function to work with Gradio
   - The rest of the file is already set up

3. Use `chatbot_development.ipynb` to:
   - Develop and test your implementation
   - Try different approaches
   - Verify everything works before deployment

