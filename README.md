<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
     
        
</head>
<body>

<h1>RAG (Retrieval-Augmented Generation) with Groq and LangChain</h1>

<p>This project demonstrates a Retrieval-Augmented Generation (RAG) pipeline using Groq's <code>llama3-8b-8192</code> model, LangChain, and HuggingFace embeddings. It loads a blog post, splits it into chunks, embeds the chunks, and uses a vector store to retrieve relevant information for answering user questions.</p>

<h2>Features</h2>
<ul>
    <li><strong>Web Content Loading</strong>: Loads and processes blog posts using <code>WebBaseLoader</code>.</li>
    <li><strong>Text Splitting</strong>: Splits documents into manageable chunks using <code>RecursiveCharacterTextSplitter</code>.</li>
    <li><strong>Embeddings</strong>: Uses HuggingFace's <code>BAAI/bge-base-en-v1.5</code> model for embedding text.</li>
    <li><strong>Vector Store</strong>: Stores embeddings in an in-memory vector store for similarity search.</li>
    <li><strong>RAG Pipeline</strong>: Combines retrieval and generation to answer user questions.</li>
</ul>

<h2>Prerequisites</h2>
<ul>
    <li>Python 3.8 or higher</li>
    <li>A Groq API key (sign up at <a href="https://groq.com/" target="_blank">Groq</a>)</li>
    <li>Required Python libraries (see <code>requirements.txt</code>)</li>
</ul>

<h2>Setup</h2>

<h3>1. Clone the Repository</h3>
<pre><code>git clone https://github.com/your-username/your-repo.git
cd your-repo</code></pre>

<h3>2. Install Dependencies</h3>
<pre><code>pip install -r requirements.txt</code></pre>

<h3>3. Set Up Environment Variables</h3>
<ul>
    <li>Add your Groq API key to the environment:
        <pre><code>export GROQ_API_KEY="your-api-key-here"</code></pre>
    </li>
    <li>Alternatively, you can enter the API key interactively when running the script.</li>
</ul>



<h2>Usage</h2>
<p>The script will load a blog post, process it, and allow you to ask questions. For example:</p>
<pre><code>response = graph.invoke({"question": "What is Task Decomposition?"})
print(response["answer"])</code></pre>

<h2>Code Overview</h2>

<h3>Key Components</h3>
<ol>
    <li><strong>Loading and Splitting Documents</strong>:
        <ul>
            <li>Uses <code>WebBaseLoader</code> to load a blog post.</li>
            <li>Splits the content into chunks using <code>RecursiveCharacterTextSplitter</code>.</li>
        </ul>
    </li>
    <li><strong>Embeddings</strong>:
        <ul>
            <li>Uses HuggingFace's <code>BAAI/bge-base-en-v1.5</code> model to generate embeddings for the text chunks.</li>
        </ul>
    </li>
    <li><strong>Vector Store</strong>:
        <ul>
            <li>Stores the embedded documents in an in-memory vector store for retrieval.</li>
        </ul>
    </li>
    <li><strong>RAG Pipeline</strong>:
        <ul>
            <li>Retrieves relevant documents based on the user's question.</li>
            <li>Generates an answer using the Groq <code>llama3-8b-8192</code> model.</li>
        </ul>
    </li>
</ol>

<h3>Example Workflow</h3>
<ol>
    <li>Load a blog post.</li>
    <li>Split the post into chunks.</li>
    <li>Generate embeddings for each chunk.</li>
    <li>Store embeddings in a vector store.</li>
    <li>Retrieve relevant chunks for a user question.</li>
    <li>Generate an answer using the RAG pipeline.</li>
</ol>

<h2>Dependencies</h2>
<ul>
    <li><code>langchain</code></li>
    <li><code>langchain-community</code></li>
    <li><code>langchain-core</code></li>
    <li><code>langgraph</code></li>
    <li><code>huggingface-hub</code></li>
    <li><code>bs4</code></li>
</ul>

<h2>License</h2>
<p>This project is licensed under the MIT License. See the <a href="LICENSE">LICENSE</a> file for details.</p>


https://github.com/user-attachments/assets/14c5b9e8-bde1-4646-8ec3-8e15414c497f


</body>
</html>
