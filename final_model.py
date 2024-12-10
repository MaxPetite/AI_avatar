import os 
import openai 
from openai import OpenAI
from embedding_handler import get_relevant_context
from data_processor import get_convo
from datetime import datetime

openai.api_key = os.getenv('OPENAI_API_KEY')
openai.proxy = None

system_prompt = (
    "You are Max Petite, a 19-year-old college student from St. Louis, Missouri, studying at Colby College. "
    "Respond to the user from your perspective using your understanding of the world"
)

synthetic_conversation_final = get_convo()

# Initialize conversation messages with system prompt and synthetic conversation
messages = [
    {"role": "system", "content": system_prompt},
    *synthetic_conversation_final,
]

# Get fine-tuned model name from the fine-tuning job
fine_tune_job_id = "ftjob-bD0stuZBrl9FEOSIoJSiTevy" #'ftjob-0FUCOlMYyut3QkL8ADYaSKK5'version2 w/o interview #'ftjob-t7PTo6MxpFsvcAuYjCUCwUqX' version 1
client = OpenAI()
fine_tune_job = client.fine_tuning.jobs.retrieve(fine_tune_job_id)
fine_tuned_model_name = fine_tune_job.fine_tuned_model

# Function to get a response from the fine-tuned model
"""
def get_response(user_input):
    messages.append({"role": "user", "content": user_input})
    print("Model requested...")
    try:
        response = client.chat.completions.create(
            model=fine_tuned_model_name,
            messages=messages
        )
        assistant_message = response.choices[0].message.content
        messages.append({"role": "assistant", "content": assistant_message})
        print("Response return")
        return assistant_message
    except Exception as e:
        return f"An error occurred: {e}"

    
    
def get_response(user_input):
    # Get the most relevant context from embeddings
    relevant_context = get_relevant_context(user_input, k=3)

    # Prepare the prompt
    context_str = " ".join(relevant_context)
    final_prompt = f"{context_str}\nUser: {user_input}\nMax:"

    # Query the fine-tuned model
    response = client.chat.completions.create(
        model=fine_tuned_model_name,
        prompt=final_prompt
    )

    return response.choices[0].text.strip()
"""


# Global messages to track conversation (initialized with context)
messages = [
    {
        "role": "system",
        "content": (
            system_prompt
        )
    }
]

def simplify_conversation(conversation):
    """
    Simplifies a conversation structure to just the user questions and AI responses.
    
    Parameters:
        conversation (list of dict): The convoluted conversation format where each dictionary 
                                     contains "role" (either "user" or "assistant") and 
                                     "content" (the text).
    
    Returns:
        list of tuples: A list of tuples where each tuple is (user_question, ai_response).
    """
    simplified_convo = []
    user_question = ""
    
    for entry in conversation:
        if entry['role'] == 'user':
            user_question = entry['content']  # Save the user question
        elif entry['role'] == 'assistant' and user_question:
            ai_response = entry['content']  # Save the AI response
            simplified_convo.append((f"User: {user_question}", f"Max: {ai_response}"))  # Store the pair
    
    return simplified_convo


def save_convo():
    simplified_convo = simplify_conversation(messages)
    
    # Create a filename with the current date and time
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"conversation_{timestamp}.txt"
    
    # Write the conversation to the file
    with open(filename, 'w') as file:
        for user_question, ai_response in simplified_convo:
            file.write(f"{user_question}\n")
            file.write(f"{ai_response}\n")
            file.write("\n")  # Add a newline for better readability
    
    print(f"Conversation saved to {filename}")

def get_response(user_input):
    # Retrieve relevant context from embeddings
    relevant_context = get_relevant_context(user_input, k=5)
    #print(f"\n{relevant_context}\n")

    # Add relevant context to messages (as a user message for continuity)
    """
    if relevant_context:
        for context in relevant_context:
            messages.append({"role": "user", "content": context})
    """       
    if relevant_context:
        context_text = "\n".join(relevant_context)
        messages.append({
            "role": "system",
            "content": f"Relevant context for the current conversation:\n{context_text}"
        })

    # Append the new user input to messages
    messages.append({"role": "user", "content": user_input})

    print("Model requested...")

    try:
        # Query the fine-tuned model with updated messages
        response = client.chat.completions.create(
            model=fine_tuned_model_name,
            messages=messages
        )

        # Extract assistant's response and append to conversation history
        assistant_message = response.choices[0].message.content
        messages.append({"role": "assistant", "content": assistant_message})
        
        print("Response returned")
        return assistant_message
    except Exception as e:
        # Handle exceptions, like connectivity or API issues
        return f"An error occurred: {e}"