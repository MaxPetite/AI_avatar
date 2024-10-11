import docx
import os
import json
import tiktoken
import glob
from docx import Document
import PyPDF2
from pdfminer.high_level import extract_text
import pypandoc

def docx_to_text(docx_path):
    doc = Document(docx_path)
    full_text = [para.text for para in doc.paragraphs]
    return '\n'.join(full_text)

def pdf_to_text(pdf_path):
    text = ''
    with open(pdf_path, 'rb') as f:
        reader = PyPDF2.PdfReader(f)
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            text += page.extract_text()
    return text

def pdfminer_to_text(pdf_path):
    text = extract_text(pdf_path)
    return text

def txt_to_text(txt_path):
    with open(txt_path, 'r', encoding='utf-8') as f:
        text = f.read()
    return text

def rtf_to_text(rtf_path):
    text = pypandoc.convert_file(rtf_path, 'plain')
    return text


def convert_files_in_directory(input_dir, output_dir):
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Define file patterns for different formats
    file_patterns = ['*.docx', '*.pdf', '*.txt', '*.rtf']

    for pattern in file_patterns:
        for file_path in glob.glob(os.path.join(input_dir, pattern)):
            filename = os.path.basename(file_path)
            name, ext = os.path.splitext(filename)
            print(f"Processing {filename}...")

            # Determine the conversion function based on file extension
            if ext.lower() == '.docx':
                text = docx_to_text(file_path)
            elif ext.lower() == '.pdf':
                # You can choose between pdf_to_text and pdfminer_to_text
                text = pdfminer_to_text(file_path)
            elif ext.lower() == '.txt':
                text = txt_to_text(file_path)
            elif ext.lower() == '.rtf':
                text = rtf_to_text(file_path)
            else:
                print(f"Unsupported file format: {ext}")
                continue

            # Save the text to a file
            output_file = os.path.join(output_dir, f"{name}.txt")
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(text)
            print(f"Saved text to {output_file}")


input_directory = r"/Users/maxpetite/Desktop/Colby 154/AI_avatar/my writing/formal"

output_directory = 'writings_as_text'

#convert_files_in_directory(input_directory, output_directory)


# Define your system prompt
system_prompt = "You are a 19 year old male college student name Max Petite at colby college from St.Louis Missouri and your goal is to respond as if you are him."

# List of your writings with associated topics
writings = [
    {'filename': r'Abortion Paper.txt', 'topic': 'an opion and perspective on abortion'},
    {'filename': r'Catcher in the rye personal essay.txt', 'topic': ' an interpretation of the Catcher in the Rye in respect to your own life and ideas of purpose'},
    {'filename': r'Chillingworth Analytical.txt', 'topic': 'the character Chillingsworth from the Scarlet Letter and what he represent'},
    {'filename': r'CNF final.txt', 'topic': 'how you have been influenced by your brother and a meaningful experience with authenticity you have had'},
    {'filename': r'College Essay- English.txt', 'topic': 'how you view yourself and how that has changed over time'},
    {'filename': r'Copy of Essay #3(1).txt', 'topic': 'your thoughts on determinism and free will'},
    {'filename': r'Copy of final paper.txt', 'topic': 'how you view beauty and how you came to that understanding of it'},
    {'filename': r'Copy of much ado- in class.txt', 'topic': 'your thoughts and analysis of a scene from Much Ado About Nothing'},
    {'filename': r'Copy of paper #2.txt', 'topic': 'your thoughts on community and your experiences with it'},
    {'filename': r'Copy of PLAM essay.txt', 'topic': 'your thoughts on appreciation in respect to the book Please Look After Mom'},
    {'filename': r'Copy of Slaughterhouse five essay.txt', 'topic': 'your thoughts on what Slaughterhouse five is about and represents'},
    {'filename': r'Crucible essay.txt', 'topic': 'your thoughts on mob mentality and critical thinking in respect to the play the Crucible'},
    {'filename': r'Favorite story 2.txt', 'topic': 'one of your favorite childhood stories to tell'},
    {'filename': r'Favorite story.txt', 'topic': 'a story you love to tell and says a lot about who you are'},
    {'filename': r'Final Term Paper (1).txt', 'topic': 'your thoughts on How the New Deal Affected African Americans and Segregation in the form of a research paper'},
    {'filename': r'full term paper.txt', 'topic': 'your thoughts on socrates and why he was killed in the form of a research paper'},
    {'filename': r'Journaling.txt', 'topic': 'your ideas and thoughts about some journaling topics that interest you'},
    {'filename': r'petite-A1.txt', 'topic': 'a technology that was important to you and how it shapped you'},
    {'filename': r'poem analysis final.txt', 'topic': 'your thoughts and analysis about the poem Colonial Girls School'},
    {'filename': r'primary source analysis.txt', 'topic': 'your thoughts and though process about a primary source that interests you'},
    {'filename': r'Salvage the bones essay.txt', 'topic': 'your thoughts on women and motherhood in respect to the book Salvage the Bones'},
    {'filename': r'Summer page.txt', 'topic': 'a experience you have had that was meaningful'},
    {'filename': r'thanksgiving speech rearange.txt', 'topic': 'by giving an example of how you would write a speech about your thoughts on thanksgiving and life'},
    {'filename': r'U.B.I. term paper (1).txt', 'topic': 'your thoughts on a U.B.I. in the form of a research paper'},
]


training_data = []
"""
for writing in writings:
    # Read the content of each file
    with open(os.path.join(r"/Users/maxpetite/Desktop/Colby 154/AI_avatar/writings_as_text/", writing['filename']), 'r', encoding='utf-8') as file:
        content = file.read()

    # Create a training example
    example = {
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Could you explain {writing['topic']}?"},
            {"role": "assistant", "content": content.strip()}
        ]
    }
    training_data.append(example)

# Save training data to a JSONL file
with open('training_data.jsonl', 'w', encoding='utf-8') as outfile:
    for entry in training_data:
        json.dump(entry, outfile)
        outfile.write('\n')

"""
def validate_jsonl(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        for i, line in enumerate(file, 1):
            try:
                json.loads(line)
            except json.JSONDecodeError as e:
                print(f"Error in line {i}: {e}")
                return False
    print("All lines are valid JSON.")
    return True

validate_jsonl('training_data.jsonl')


encoding = tiktoken.encoding_for_model('gpt-3.5-turbo-0613')
max_tokens = 4096
valid_training_data = []

for entry in training_data:
    total_tokens = 0
    for message in entry['messages']:
        total_tokens += len(encoding.encode(message['content']))
    if total_tokens <= max_tokens:
        valid_training_data.append(entry)
    else:
        print(f"Entry exceeds token limit and will be excluded: {entry['messages'][1]['content']}")
