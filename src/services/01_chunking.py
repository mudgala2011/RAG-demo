from docling.chunking import HybridChunker
from docling.document_converter import DocumentConverter
from dotenv import load_dotenv
from openai import OpenAI

from utils.tokenizer import OpenAITokenizerWrapper
import os

load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

tokenizer = OpenAITokenizerWrapper()  # Load custom tokenizer for OpenAI embedding model
MAX_TOKENS = 8191  # text-embedding-3-large's maximum context length

####################################################################################
# Data Extraction
####################################################################################
file_path = "F:/Policy_docs/Spice_Digital_HR_policy.pdf"
converter = DocumentConverter()

result = converter.convert(source=file_path)

####################################################################################
# Applying Hybrid chunking
####################################################################################

chunker = HybridChunker(
    tokenizer=tokenizer,
    max_tokens=MAX_TOKENS,
    merge_peers=True,
)

chunk_iter = chunker.chunk(dl_doc=result.document)
chunks = list(chunk_iter)
len(chunks)