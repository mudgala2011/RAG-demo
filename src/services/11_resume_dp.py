from docling.chunking import HybridChunker
from docling.document_converter import DocumentConverter

from dotenv import load_dotenv
from openai import OpenAI
import os
import tiktoken
from docling_core.transforms.chunker.tokenizer.openai import OpenAITokenizer
import lancedb
from lancedb.embeddings import get_registry
from lancedb.pydantic import LanceModel, Vector
from pathlib import Path

load_dotenv()

# Initialize OpenAI client for embedding model
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

tokenizer = OpenAITokenizer(
    tokenizer=tiktoken.encoding_for_model("text-embedding-3-large"), max_tokens=8191
)

MAX_TOKENS = 8191  # text-embedding-3-large's maximum context length

####################################################################################
# Data Extraction (PreProcessing step) & gen docling
####################################################################################
file_path = "F:/resume_src/cv_dump/Candidate ID 1003"

file_paths = [
    os.path.join(folder_path, fname)
    for fname in os.listdir(folder_path)
    if os.path.isfile(os.path.join(folder_path, fname))
]

converter = DocumentConverter()

result = converter.convert_all(source=file_path)


####################################################################################
# Applying Docling Hybrid chunking
####################################################################################

chunker = HybridChunker(
    tokenizer=tokenizer,
    max_tokens=MAX_TOKENS,
    merge_peers=True,
)

chunk_iter = chunker.chunk(dl_doc=result.document)
chunks = list(chunk_iter)
len(chunks)
# chunks[0].model_dump()

####################################################################################
# Create a Lance Db
####################################################################################
# Create a LanceDB database

db = lancedb.connect("data/lancedb")
# db = lancedb.connect(
#   uri="db://dnv-demo-qmbv2y",
#   api_key=os.getenv("LANCEDB_API_KEY"),
#   region="us-east-1"
# )


# Get the OpenAI embedding function
func = get_registry().get("openai").create(name="text-embedding-3-large")


# Define a simplified metadata schema
class ChunkMetadata(LanceModel):
    """
    You must order the fields in alphabetical order.
    This is a requirement of the Pydantic implementation.
    """

    filename: str | None
    page_numbers: list[int] | None
    title: str | None


# Define the main Schema
class Chunks(LanceModel):
    text: str = func.SourceField()
    vector: Vector(func.ndims()) = func.VectorField()  # type: ignore
    metadata: ChunkMetadata


table = db.create_table("resume_db", schema=Chunks, mode="overwrite")

#############################################################################
# Loop over all the 335 chunks and prepare for the upsert
#############################################################################

processed_chunks = [
    {
        "text": chunk.text,
        "metadata": {
            "filename": chunk.meta.origin.filename,
            "page_numbers": [
                page_no
                for page_no in sorted(
                    set(
                        prov.page_no
                        for item in chunk.meta.doc_items
                        for prov in item.prov
                    )
                )
            ]
            or None,
            "title": chunk.meta.headings[0] if chunk.meta.headings else None,
        },
    }
    for chunk in chunks
]

#############################################################################
# Add the chunks to the table
#############################################################################

table.add(processed_chunks)
table.to_pandas()
table.count_rows()

# tbl = db.open_table("HR_kb")
# tbl.create_index(metric="cosine", vector_column_name="vector")

### Temporary  to check if the search function is working
# table_1 = db.open_table("HR_kb")

# search_result = table_1.search(query="Whats the gratuity policy", query_type="vector").limit(3)
