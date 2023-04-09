import os
import requests
from knowledgegpt.extractors.pdf_extractor import PDFExtractor

import openai
from local_example_config import SECRET_KEY
openai.api_key = SECRET_KEY

def main():
    source = input("Enter the path to the PDF file or arXiv ID/URL (or 'quit' to exit): ")
    if source.lower() in ["quit", "exit"]:
        return
    
    index_path = input("Enter the path to the index file: ")
    
    index_path = index_path if index_path else None
    load_index = False
    if index_path and os.path.exists(index_path):
        load_index = index_path if index_path else False
    initial_load = True
    
    if source.endswith(".pdf"):
        pdf_file_path = source
    else:
        # Source is an arXiv ID or URL
        arxiv_id = source
        pdf_file_path = f"{arxiv_id}.pdf"
        if not os.path.exists(pdf_file_path):
            # Download the PDF from the arXiv URL
            arxiv_url = f"https://arxiv.org/pdf/{arxiv_id}.pdf"
            response = requests.get(arxiv_url)
            if response.status_code == 200:
                with open(pdf_file_path, "wb") as f:
                    f.write(response.content)
            else:
                print(f"Failed to download PDF for {arxiv_id}: HTTP status code {response.status_code}")
                return
            
    max_tokens = input("Enter the maximum number of tokens in the generated prompt (default: 1500): ")
    try:
        max_tokens = int(max_tokens) if max_tokens else 1500
    except ValueError:
        print("Invalid input. Please enter a valid integer.")
        
    pdf_extractor = PDFExtractor(pdf_file_path=pdf_file_path, extraction_type="paragraph", embedding_extractor="hf", model_lang="en", index_path=index_path, is_turbo=True)
    while True:
        query = input("Enter your query (or 'quit' to exit): ")
        if query.lower() in ["quit", "exit"]:
            return

        # context_restarter = source.lower() in ["restart_context", "reset_context"]
        context_restarter = "restart_context" in query.lower()

        # Extract information from the PDF
        if initial_load:
            print("Firing up the engines...")
            answer, prompt, messages = pdf_extractor.extract(query, max_tokens=max_tokens, load_index=load_index)
        else:
            print("Continuing the conversation...")
            answer, prompt, messages = pdf_extractor.extract(query, max_tokens=max_tokens, context_restarter=context_restarter)
            print(context_restarter)
        initial_load = False

        print(f"Answer: {answer}")

if __name__ == "__main__":
    main()
