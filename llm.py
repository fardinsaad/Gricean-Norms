import openai
import os
import backoff
from dotenv import load_dotenv
from openai import OpenAI
from openai import RateLimitError  # Directly import RateLimitError

# Load environment variables from the .env file
load_dotenv()

# Set OpenAI API key from environment variable
key = os.getenv('OPENAI_API_KEY')

# Set OpenAI API key
client = OpenAI(api_key  = key)

@backoff.on_exception(backoff.expo, RateLimitError, max_time=100)  # Use RateLimitError directly
def get_completion_with_backoff(**kwargs):
    """Get completion from OpenAI API with backoff in case of RateLimitError."""
    return client.chat.completions.create(**kwargs)  # Corrected method for chat-based models like GPT-4

def get_response(prompt):
    """Function to interact with GPT-4 and generate a response."""
    
    # Define the messages in a variable called 'msgs'
    msgs = [
        {"role": "system", "content": "You are an intelligent assistant helping a human in a collaborative game to collect a gem the human desires. Your task is to interpret the instruction provided by the human and generate an appropriate response enabling the human retrieve their desired gem."
},
        {"role": "user", "content": prompt}
    ]
    response = client.chat.completions.create(
        model="gpt-4",
        messages=msgs,
        max_tokens=512,
        temperature=0.2,
        #top_p = 0.9
    )
    return response.choices[0].message.content.strip()

# Main function to run the script and test the API connection
if __name__ == '__main__':
    # Check if the API key is correctly loaded
    if key:
        print("API key loaded successfully.")
        # Test with a sample prompt
        test_prompt = "How are you today?"
        result = get_response(test_prompt)
        print("GPT-4 Response:", result)
    else:
        print("API key not found. Please set it in your .env file.")

