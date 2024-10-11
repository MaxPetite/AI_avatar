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
    {'filenam