import os
import getpass
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from langchain.chat_models import init_chat_model
from langchain.embeddings import HuggingFaceBgeEmbeddings
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import WebBaseLoader
import bs4
from langgraph.graph import START, StateGraph
from typing import List, TypedDict
from langchain import hub
import uvicorn
from langchain_huggingface import HuggingFaceEmbeddings 
from mangum import Mangum
# Initialize FastAPI app
app = FastAPI()
handler = Mangum(app, lifespan="off")
# Enable CORS (Cross-Origin Resource Sharing)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

# Define a Pydantic model for the request body
class QuestionRequest(BaseModel):
    question: str

# Set up Groq API key
if not os.environ.get("GROQ_API_KEY"):
    os.environ["GROQ_API_KEY"] = getpass.getpass("Enter API key for Groq: ")
os.environ["LANGCHAIN_API_KEY"] = getpass.getpass("Enter your LangSmith API key: ")
# Initialize the LLM
llm = init_chat_model("llama3-8b-8192", model_provider="groq")

# Load and chunk contents of the blog
loader = WebBaseLoader(
    web_paths=("https://lilianweng.github.io/posts/2023-06-23-agent/",),
    bs_kwargs=dict(
        parse_only=bs4.SoupStrainer(
            class_=("post-content", "post-title", "post-header")
        )
    ),
)
docs = loader.load()

# Split documents into chunks
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
all_splits = text_splitter.split_documents(docs)

# Initialize the HuggingFaceBgeEmbeddings object
model_name = "BAAI/bge-small-en-v1.5"
model_kwargs = {"device": "cpu"}
encode_kwargs = {"normalize_embeddings": True}
hf = HuggingFaceEmbeddings(
    model_name=model_name,
    model_kwargs=model_kwargs,
    encode_kwargs=encode_kwargs
)

# Create a list to store the documents with their embeddings
embedded_docs = []
for text in all_splits:
    embedding = hf.embed_query(text.page_content)  # Embed the document content
    text.metadata['embedding'] = embedding  # Store embedding in metadata
    embedded_docs.append(text)

# Initialize the InMemoryVectorStore with the embedded documents
vector_store = InMemoryVectorStore.from_documents(embedded_docs, hf)

# Define prompt for question-answering
prompt = hub.pull("rlm/rag-prompt")

# Define state for application
class State(TypedDict):
    question: str
    context: List[str]
    answer: str

# Define application steps
def retrieve(state: State):
    retrieved_docs = vector_store.similarity_search(state["question"])
    return {"context": retrieved_docs}

def generate(state: State):
    docs_content = "\n\n".join(doc.page_content for doc in state["context"])
    messages = prompt.invoke({"question": state["question"], "context": docs_content})
    response = llm.invoke(messages)
    return {"answer": response.content}

# Compile application
graph_builder = StateGraph(State).add_sequence([retrieve, generate])
graph_builder.add_edge(START, "retrieve")
graph = graph_builder.compile()

# FastAPI route to handle questions
@app.post("/ask")
async def ask(request: QuestionRequest):
    print("hi")
    question = request.question
    if not question:
        raise HTTPException(status_code=400, detail="No question provided")

    # Run the RAG pipeline
    response = graph.invoke({"question": question})
    return {"answer": response["answer"]}

# Run the FastAPI app
if __name__ == "__main__":
   uvicorn.run('Rag:app', host="127.0.0.1", port=8000, reload=True)