---
title: Glossary
description: Definitions of terms and concepts used in Vector Bot and related technologies
audience: all
level: reference
keywords: [glossary, definitions, terms, concepts, vocabulary, ai, rag, vector, embedding]
related_docs: [faq.md, ../user/getting-started.md, configuration-vars.md]
---

# Glossary

Comprehensive definitions of terms and concepts used in Vector Bot and related technologies.

## A

### AI Model
A machine learning system trained to perform specific tasks, such as generating text or understanding language. Vector Bot uses AI models from Ollama to generate answers based on your documents.

### API (Application Programming Interface)
A set of protocols and tools for building software applications. Vector Bot communicates with Ollama through its REST API.

### Auto-Detection
Vector Bot's ability to automatically discover and use available AI models without explicit configuration. Used as the default for `OLLAMA_CHAT_MODEL`.

## B

### Batch Processing
Processing multiple items together as a group rather than individually. Vector Bot processes document chunks in batches during embedding generation for efficiency.

### Base URL
The root URL for an API service. For Vector Bot, `OLLAMA_BASE_URL` specifies where to find the Ollama server (default: `http://localhost:11434`).

## C

### Chat Model
An AI model specifically designed for conversational interactions and text generation. Examples include `llama3.1`, `mistral`, and `qwen2.5`.

### Chunk
A small segment of text extracted from a larger document. Vector Bot splits documents into chunks to create searchable pieces that can be efficiently processed and retrieved.

### Chunk Overlap
The number of characters that consecutive chunks share to maintain context continuity. Default is 200 characters.

### Chunk Size
The maximum number of characters in each document chunk. Default is 1000 characters.

### CLI (Command Line Interface)
A text-based interface for interacting with software. Vector Bot provides a CLI with commands like `doctor`, `ingest`, and `query`.

### Configuration File
A file containing settings and parameters for an application. Vector Bot uses `.env` files and environment profiles in the `configs/` directory.

### Configuration Variable
A setting that controls how Vector Bot behaves. Examples include `DOCS_DIR`, `OLLAMA_CHAT_MODEL`, and `SIMILARITY_TOP_K`.

### Cosine Similarity
A mathematical measure of similarity between vectors, commonly used in vector databases to find relevant content. Vector Bot uses cosine similarity to match queries with document chunks.

## D

### Docker
A platform for developing, shipping, and running applications in containers. Vector Bot supports Docker deployment with specialized configuration.

### Document Index
See [Vector Index](#vector-index).

### Document Ingestion
The process of loading, processing, and indexing documents to make them searchable. Performed by the `vector-bot ingest` command.

## E

### Embedding
A numerical representation (vector) of text that captures semantic meaning. Vector Bot creates embeddings for both document chunks and queries to enable semantic search.

### Embedding Model
An AI model that converts text into numerical vectors (embeddings). Vector Bot's default is `nomic-embed-text`.

### Environment Profile
A predefined set of configuration settings for specific deployment scenarios (development, production, docker). Stored in `configs/{profile}.env` files.

### Environment Variable
A system-level setting that programs can read to modify their behavior. Vector Bot reads environment variables like `DOCS_DIR` and `OLLAMA_CHAT_MODEL`.

## F

### FAQ (Frequently Asked Questions)
A collection of common questions and their answers. Vector Bot's FAQ covers installation, usage, and troubleshooting topics.

## G

### GPU (Graphics Processing Unit)
Specialized hardware that can accelerate AI model processing. Ollama can use GPUs to run models faster than CPU-only processing.

### Glob Pattern
A pattern-matching syntax for specifying groups of files. Examples: `*.pdf` (all PDF files), `docs/**/*.md` (all Markdown files in docs and subdirectories).

## H

### Health Check
A diagnostic test to verify that all system components are working correctly. Vector Bot's `doctor` command performs comprehensive health checks.

### HTTP (Hypertext Transfer Protocol)
The protocol used for web communication. Vector Bot communicates with Ollama over HTTP/HTTPS.

### Hybrid Search
A search approach that combines multiple techniques, such as keyword matching and semantic similarity. Vector Bot primarily uses semantic search via embeddings.

## I

### Index
See [Vector Index](#vector-index).

### Index Directory
The location where Vector Bot stores the vector index files. Controlled by the `INDEX_DIR` configuration variable (default: `./index_storage`).

### Ingestion
See [Document Ingestion](#document-ingestion).

## J

### JSON (JavaScript Object Notation)
A lightweight data format commonly used for configuration files and data exchange. Vector Bot can process JSON documents and uses JSON for some configuration.

### JWT (JSON Web Token)
A security standard for transmitting information securely between parties. Can be used for Vector Bot authentication in enterprise deployments.

## K

### k-NN (k-Nearest Neighbors)
An algorithm for finding the most similar items in a dataset. Vector Bot uses k-NN to find the most relevant document chunks for a query.

### Kubernetes
A container orchestration platform. Vector Bot can be deployed in Kubernetes clusters with appropriate configuration.

## L

### Large Language Model (LLM)
A type of AI model trained on vast amounts of text data to understand and generate human language. Examples include the Llama family of models.

### LlamaIndex
The framework Vector Bot uses for document processing, indexing, and retrieval. LlamaIndex provides the core RAG functionality.

### Local Processing
Performing computation on the user's own hardware rather than sending data to external services. Vector Bot operates entirely locally for privacy and security.

## M

### Metadata
Additional information about data, such as file creation date, author, or document type. Vector Bot extracts and uses metadata during document processing.

### Model
See [AI Model](#ai-model).

### Multi-Environment
The ability to use different configurations for different deployment scenarios (development, staging, production). Vector Bot supports multi-environment configurations.

## N

### Natural Language Processing (NLP)
The field of AI focused on enabling computers to understand and work with human language. Vector Bot uses NLP techniques for document understanding and query processing.

### Neural Network
A machine learning architecture inspired by biological neural networks. Modern AI models, including those used by Vector Bot, are based on neural networks.

### npm (Node Package Manager)
A package manager for JavaScript/Node.js applications. One of Vector Bot's distribution methods is through npm packages.

## O

### Offline Processing
Performing tasks without requiring an internet connection. Vector Bot works entirely offline after initial setup.

### Ollama
An open-source platform for running large language models locally. Vector Bot requires Ollama for both chat and embedding models.

### On-Premises
Software deployed and run on the user's own hardware rather than in the cloud. Vector Bot is designed for on-premises deployment.

## P

### Path Resolution
The process of converting relative paths to absolute paths. Vector Bot resolves relative paths based on the executable's location.

### PDF (Portable Document Format)
A file format commonly used for documents. Vector Bot can extract text from PDF files for indexing.

### Persistent Storage
Data storage that survives between application runs. Vector Bot uses persistent storage for the vector index.

### pip
The package installer for Python. One of Vector Bot's distribution methods is through pip packages.

### Prompt
The input text or question provided to an AI model. Vector Bot combines your query with relevant document content to create effective prompts.

## Q

### Query
A question or request for information submitted to Vector Bot. Processed by the `vector-bot query` command.

### Query Engine
The component responsible for finding relevant content and generating answers. Vector Bot uses LlamaIndex's query engine.

## R

### RAG (Retrieval-Augmented Generation)
An AI technique that combines information retrieval with text generation. Vector Bot is a RAG system that retrieves relevant document content and uses it to generate informed answers.

### Retrieval
The process of finding and extracting relevant information from a dataset. The "R" in RAG refers to retrieving relevant document chunks.

### REST API
A type of web API that follows REST architectural principles. Ollama provides a REST API that Vector Bot uses for communication.

## S

### Semantic Search
Search based on meaning rather than exact keyword matches. Vector Bot uses semantic search to find contextually relevant content even when exact words don't match.

### Similarity Score
A numerical measure of how closely related two pieces of content are. Vector Bot uses similarity scores to rank document chunks by relevance to queries.

### Similarity Top K
The number of most similar document chunks to retrieve for each query. Controlled by the `SIMILARITY_TOP_K` configuration variable.

### Source Document
The original document from which information was retrieved. Vector Bot can show source documents using the `--show-sources` flag.

## T

### Token
A unit of text processing in AI models (roughly equivalent to words or word parts). Also refers to authentication tokens in security contexts.

### Top K
See [Similarity Top K](#similarity-top-k).

### Transformer
A neural network architecture that revolutionized natural language processing. Most modern language models, including those used by Vector Bot, are based on transformers.

## U

### URL (Uniform Resource Locator)
A web address that specifies the location of a resource. Vector Bot uses URLs to connect to Ollama servers.

### User Journey
The path a user takes when learning and using a system. Vector Bot's documentation is organized around common user journeys.

## V

### Vector
A numerical representation of data, typically as a list of numbers. In Vector Bot, text is converted to vectors (embeddings) for similarity comparison.

### Vector Database
A specialized database for storing and searching vector embeddings. Vector Bot uses LlamaIndex's vector storage capabilities.

### Vector Index
A data structure containing document embeddings organized for efficient similarity search. Vector Bot stores this in the index directory.

### Vector Space
A mathematical space where vectors exist and can be compared. Vector Bot performs searches in embedding vector space.

### Verbose Output
Detailed information about processing steps and system behavior. Enabled with `--verbose` flags or `ENABLE_VERBOSE_OUTPUT=true`.

## W

### Workflow
A sequence of steps or processes to accomplish a task. Vector Bot supports various workflows for different use cases.

## Y

### YAML (YAML Ain't Markup Language)
A human-readable data serialization format. Vector Bot documentation uses YAML frontmatter for metadata.

---

## Acronyms and Abbreviations

| Acronym | Full Form | Description |
|---------|-----------|-------------|
| AI | Artificial Intelligence | Computer systems that can perform tasks typically requiring human intelligence |
| API | Application Programming Interface | Set of protocols for building software applications |
| CLI | Command Line Interface | Text-based user interface |
| CPU | Central Processing Unit | The main processor in a computer |
| CSV | Comma-Separated Values | A simple file format for tabular data |
| FAQ | Frequently Asked Questions | Collection of common questions and answers |
| GPU | Graphics Processing Unit | Specialized processor for graphics and parallel computing |
| HTTP | Hypertext Transfer Protocol | Protocol for web communication |
| JSON | JavaScript Object Notation | Lightweight data interchange format |
| JWT | JSON Web Token | Security standard for information transmission |
| LLM | Large Language Model | AI model trained on large amounts of text |
| NLP | Natural Language Processing | AI field focused on human language understanding |
| PDF | Portable Document Format | File format for documents |
| RAG | Retrieval-Augmented Generation | AI technique combining retrieval and generation |
| REST | Representational State Transfer | Architectural style for web services |
| TLS | Transport Layer Security | Cryptographic protocol for secure communication |
| URL | Uniform Resource Locator | Web address format |
| YAML | YAML Ain't Markup Language | Human-readable data serialization format |

---

## Related Concepts by Category

### AI and Machine Learning
- [AI Model](#ai-model), [Chat Model](#chat-model), [Embedding Model](#embedding-model)
- [Large Language Model (LLM)](#large-language-model-llm), [Neural Network](#neural-network), [Transformer](#transformer)
- [Natural Language Processing (NLP)](#natural-language-processing-nlp)

### Vector Bot Architecture
- [RAG (Retrieval-Augmented Generation)](#rag-retrieval-augmented-generation), [LlamaIndex](#llamaindex), [Ollama](#ollama)
- [Vector Index](#vector-index), [Embedding](#embedding), [Chunk](#chunk)
- [Query Engine](#query-engine), [Retrieval](#retrieval)

### Configuration and Deployment
- [Environment Variable](#environment-variable), [Configuration File](#configuration-file), [Environment Profile](#environment-profile)
- [Multi-Environment](#multi-environment), [Path Resolution](#path-resolution)
- [Docker](#docker), [On-Premises](#on-premises)

### Document Processing
- [Document Ingestion](#document-ingestion), [Chunk](#chunk), [Chunk Size](#chunk-size)
- [Metadata](#metadata), [PDF](#pdf), [Semantic Search](#semantic-search)

### Performance and Optimization
- [Batch Processing](#batch-processing), [Similarity Top K](#similarity-top-k), [GPU](#gpu)
- [Persistent Storage](#persistent-storage), [Index Directory](#index-directory)

---

**Need more specific information?** Check the [FAQ](faq.md) or [Configuration Variables Reference](configuration-vars.md) for detailed explanations.