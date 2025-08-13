# RAG Implementation Example


## Use Case
There is a large document of the Human Resource policies in an enterprise. The HR team is pressed against the time to answer all queries coming from the employees. Hence an AI solution is implemented in form of 
a HR Policy chatbot

## Solution Steps 
- Chunk the HR policy document/s using Docling
- Generate embeddings using the popular embedding models
- Upsert the embeddings to a reliable vector store like lanceDB
- Instance of lancedb is hosted locally
- Develop the web applicaton capable connected to the local vector db (embedded policy document)
- Use OpenAI (or any other text generation LLM) to generate natural language responses against the employee queries
- Suitable prompts to OpenAI LLM (gpt-4o-mini in this case) to prevent hallucinations and inappropriate responses from LLM
- Deploy the web applicaton for end user

## Important Code files 
- 02_chat.py is the streamlit app
- End user required to provide their OpenAI, Lancedb API keys in order for application to work 
