import os
import logging
from dataclasses import dataclass, field
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Optional
from transformers import (
    DPRContextEncoder,
    DPRContextEncoderTokenizer,
    RagRetriever,
    RagTokenForGeneration,
    RagTokenizer,
    HfArgumentParser,
)
import torch
import faiss  # Import Faiss for indexing
from PyPDF2 import PdfReader
from datasets import Dataset

#Shor’s algorithm
#Grover’s and Deutsch-Jozsa algorithms
logger = logging.getLogger(__name__)
torch.set_grad_enabled(False)
device = "cuda" if torch.cuda.is_available() else "cpu"

def extract_text_from_pdf(pdf_path):
    pdf_reader = PdfReader(pdf_path)
    text = ""
    for page_num in range((len(pdf_reader.pages))):
        page = pdf_reader.pages[page_num]
        text += page.extract_text()
    return text

def split_text(text, max_words=100):
    chunks = [text[i:i + max_words] for i in range(0, len(text), max_words)]
    return chunks

@dataclass
class RagExampleArguments:
    pdf_folder: str
    output_folder: str
    rag_model_name: str
    dpr_ctx_encoder_model_name: str
    output_dir: Optional[str] = None

def create_faiss_index(embeddings):
    # Concatenate the list of NumPy arrays into a single NumPy array
    concatenated_embeddings = np.concatenate(embeddings, axis=0)
    
    # Create a Faiss index using the shape of the concatenated embeddings
    index = faiss.IndexFlatIP(concatenated_embeddings.shape[1])
    
    # Add the concatenated embeddings to the index
    index.add(concatenated_embeddings)
    
    return index

def save_faiss_index(index, index_path):
    # Save the Faiss index to disk
    faiss.write_index(index, index_path)

def load_faiss_index(index_path):
    # Load a Faiss index from disk
    index = faiss.read_index(index_path)
    return index

def main(args):
    # Step 1: Convert PDFs to Text Data
    text_data = {}
    pdf_files = [f for f in os.listdir(args.pdf_folder) if f.endswith(".pdf")]
    for pdf_file in pdf_files:
        pdf_path = os.path.join(args.pdf_folder, pdf_file)
        text = extract_text_from_pdf(pdf_path)
        text_data[pdf_file] = text

    # Step 2: Preprocess and Embed PDF Text Data
    ctx_encoder = DPRContextEncoder.from_pretrained(args.dpr_ctx_encoder_model_name)
    ctx_tokenizer = DPRContextEncoderTokenizer.from_pretrained(args.dpr_ctx_encoder_model_name)

    dataset = {"title": [], "text": [], "embeddings": []}

    for pdf_file, text in text_data.items():
        title = pdf_file  # Use the PDF file name as the title
        chunks = split_text(text)  # Split text into 100-word chunks

        for chunk in chunks:
            input_data = ctx_tokenizer(title, chunk, return_tensors="pt", padding="longest", truncation=True)
            with torch.no_grad():
                outputs = ctx_encoder(**input_data)
            embeddings = outputs.pooler_output.cpu()

            dataset["title"].append(title)
            dataset["text"].append(chunk)
            dataset["embeddings"].append(embeddings)

    # Create a dataset
    dataset = {k: torch.cat(v) if k == "embeddings" else v for k, v in dataset.items()}
    dataset = Dataset.from_dict(dataset)

    # Step 3: Create and Use a Faiss Index
    embeddings = dataset["embeddings"]
    faiss_index = create_faiss_index(embeddings)
    index_path = os.path.join(args.output_folder, "faiss_index.faiss")
    save_faiss_index(faiss_index, index_path)

    # Step 4: Load RAG Model with the Faiss Index
    retriever = RagRetriever.from_pretrained(args.rag_model_name, indexed_dataset=dataset, index_name="custom")
    
    # Load the Faiss index
    retriever.index.load_faiss_index(index_path)

    rag_tokenizer = RagTokenizer.from_pretrained(args.rag_model_name)
    rag_model = RagTokenForGeneration.from_pretrained(args.rag_model_name, retriever=retriever)

    # Step 5: Question Answering
    while True:
        question = input("Ask a question (or type 'exit' to quit): ")
        if question == 'exit':
            break
        input_data = rag_tokenizer(question, return_tensors="pt")
        generated = rag_model.generate(input_data["input_ids"])
        generated_string = rag_tokenizer.batch_decode(generated, skip_special_tokens=True)[0]
        logger.info("Q: " + question)
        logger.info("A: " + generated_string)

if __name__ == "__main__":
    logging.basicConfig(level=logging.WARNING)
    logger.setLevel(logging.INFO)

    pdf_folder = "C:\\expt\\HuggingFace\\hfenv\\src\\pdfData\\"
    output_folder = "C:\\expt\\HuggingFace\\hfenv\\src\\datasetpath\\"
    rag_model_name = "facebook/rag-token-nq"  # Replace with the actual model name
    dpr_ctx_encoder_model_name = "facebook/dpr-ctx_encoder-multiset-base"  # Replace with the actual model name

    rag_example_args = RagExampleArguments(
        pdf_folder=pdf_folder,
        output_folder=output_folder,
        rag_model_name=rag_model_name,
        dpr_ctx_encoder_model_name=dpr_ctx_encoder_model_name,
    )
    main(rag_example_args)
