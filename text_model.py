import os
import openai
from openai import OpenAI

# Set your OpenAI API key
openai.api_key = os.getenv('OPENAI_API_KEY')

client = OpenAI()

# Upload the training data file
training_file = client.files.create(
    file=open("training_data.jsonl", "rb"),
    purpose="fine-tune"
)

# Get the ID of the uploaded file
training_file_id = training_file.id
print(f"Training file uploaded with ID: {training_file_id}")

# Create a fine-tuning job
fine_tune_job = client.fine_tuning.jobs.create(
  training_file= training_file_id,
  model="gpt-4o-mini-2024-07-18"
)

# Get the ID of the fine-tuning job
fine_tune_job_id = fine_tune_job.id
print(f"Fine-tuning job started with ID: {fine_tune_job_id}")
