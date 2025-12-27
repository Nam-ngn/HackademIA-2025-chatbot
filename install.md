# Simple RAG Pipeline

This project is a beginner-friendly tutorial project for building a Retrieval Augmented Generation (RAG) system. It demonstrates how to index documents, retrieve relevant content, generate AI-powered responses, and evaluate results—all through a command line interface (CLI).

![rag-image](./rag-design-basic.png)

## Overview

The RAG Framework lets you:

- **Index Documents:** Process and break documents (e.g., PDFs) into smaller, manageable chunks.
- **Store & Retrieve Information:** Save document embeddings in a vector database (using LanceDB) and search using similarity.
- **Generate Responses:** Use an AI model (via the OpenAI API) to provide concise answers based on the retrieved context.
- **Evaluate Responses:** Compare the generated response against expected answers and view the reasoning behind the evaluation.

## Architecture

- **Pipeline (src/rag_pipeline.py):**  
  Orchestrates the process using:

  - **Datastore:** Manages embeddings and vector storage.
  - **Indexer:** Processes documents and creates data chunks. Two versions are available—a basic PDF indexer and one using the Docling package.
  - **ResponseGenerator:** Generates answers by calling the AI service.
  - **Evaluator:** Compares the AI responses to expected answers and explains the outcome.

- **Interfaces (interface/):**  
  Abstract base classes define contracts for all components (e.g., BaseDatastore, BaseIndexer, BaseResponseGenerator, and BaseEvaluator), making it easy to extend or swap implementations.

## Installation

### Prerequisites

- **Python 3.12 or 3.13** (recommended)
- Python 3.14 is **not supported** due to missing pre-built wheels for `pyclipper` (required by `docling`)

### Set Up a Virtual Environment (Recommended)

**On Windows with PowerShell:**

```powershell
# Create virtual environment with Python 3.13
py -3.13 -m venv .venv

# Activate the environment
.venv\Scripts\Activate.ps1
```

**On macOS/Linux:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Install Dependencies

```powershell
# Upgrade pip first
python -m pip install --upgrade pip

# Install all dependencies
pip install -r requirements.txt
```

**Note:** If you encounter C++ build errors with `lxml` or `pyclipper`, ensure you're using Python 3.12 or 3.13. Python 3.14 requires Microsoft C++ Build Tools which can be avoided by using an older Python version.

### Configure Environment Variables

We use OpenAI for the LLM (you can modify/replace it in `src/util/invoke_ai.py`). Make sure to set your OpenAI API key.

**On Windows (PowerShell):**

```powershell
# Temporary (current session only)
$env:OPENAI_API_KEY='your_openai_api_key'

# Permanent (for your user account)
[System.Environment]::SetEnvironmentVariable('OPENAI_API_KEY', 'your_openai_api_key', 'User')
```

**On macOS/Linux:**

```bash
export OPENAI_API_KEY='your_openai_api_key'
```

### Initialize the Database

Before using the chatbot, you need to index your documents:

```powershell
# Reset/create the database
python main.py reset

# Add documents from CSV
python main.py add -p "sample_data/tabac/associations.csv"
```

This will index all 132 associations from the CSV file into the vector database.

## Usage

The CLI provides several commands to interact with the RAG pipeline. By default, they will use the source/eval paths specified in `main.py`, but there are flags to override them.

```python
DEFAULT_SOURCE_PATH = "sample_data/tabac/"
DEFAULT_EVAL_PATH = "sample_data/eval/sample_questions.json"
```

#### Run the Full Pipeline

This command resets the datastore, indexes documents, and evaluates the model.

```bash
python main.py run
```

#### Reset the Database

Clears the vector database.

```bash
python main.py reset
```

#### Add Documents

Index and embed documents. You can specify a file or directory path.

```bash
python main.py add -p "sample_data/tabac/"
```

To load the association catalogue specifically, point directly to the CSV file:

```bash
python main.py add -p "sample_data/tabac/associations.csv"
```

You can also ingest directly from your Prisma HTTP endpoint by passing a URL. Set the optional
`PRISMA_API_TOKEN` environment variable if your service requires bearer authentication:

```bash
set PRISMA_API_TOKEN=your_token_here
python main.py add -p "https://your-service.local/api/associations"
```
The endpoint must return either a JSON array of association objects or an object with a `data`
array property.

#### Query the Database

Search for information using a query string.

```bash
python main.py query "What is the opening year of The Lagoon Breeze Hotel?"
```

#### Evaluate the Model

Use a JSON file (with question/answer pairs) to evaluate the response quality.

```bash
python main.py evaluate -f "sample_data/eval/sample_questions.json"
```

## Deploy as an API

For real-time usage on the web, start the FastAPI server which keeps the pipeline warm and reuses the same model clients across requests:

```bash
uvicorn src.server:app --host 0.0.0.0 --port 8000 --reload
```

### Scheduled Refresh

To refresh LanceDB embeddings on a schedule, configure the Prisma endpoint via environment variables
then run the helper script (ideal for cron or Windows Task Scheduler):

```bash
set PRISMA_API_URL=https://your-service.local/api/associations
python scripts/refresh_embeddings.py
```

### Example Request

```bash
curl -X POST "http://localhost:8000/query" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "How's the life in Swan Lagoon?"}'
```

The response includes both the generated answer and the time spent servicing the request. Add this endpoint behind your web front-end to keep latency low.




rappel : 


 set the two env vars, test with python [main.py](http://_vscodecontentref_/6) add -p https://…, then automate python scripts/refresh_embeddings.py. Natural follow-ups: configure Windows Task Scheduler for your bi-weekly refresh, tighten CORS/rate limits before production, and plan secret storage (env vars today, vault later).

 