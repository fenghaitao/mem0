# Supported Providers

<cite>
**Referenced Files in This Document**   
- [chroma.py](file://mem0/vector_stores/chroma.py)
- [pinecone.py](file://mem0/configs/vector_stores/pinecone.py)
- [qdrant.py](file://mem0/configs/vector_stores/qdrant.py)
- [weaviate.py](file://mem0/configs/vector_stores/weaviate.py)
- [faiss.py](file://mem0/configs/vector_stores/faiss.py)
- [openai.py](file://mem0/llms/openai.py)
- [anthropic.py](file://mem0/llms/anthropic.py)
- [azure_openai.py](file://mem0/llms/azure_openai.py)
- [gemini.py](file://mem0/embeddings/gemini.py)
- [huggingface.py](file://mem0/embeddings/huggingface.py)
- [vertexai.py](file://mem0/embeddings/vertexai.py)
- [ollama.py](file://mem0/embeddings/ollama.py)
- [neptunedb.py](file://mem0/graphs/neptune/neptunedb.py)
- [neptunegraph.py](file://mem0/graphs/neptune/neptunegraph.py)
- [base.py](file://mem0/configs/embeddings/base.py)
- [base.py](file://mem0/configs/base.py)
</cite>

## Table of Contents
1. [Introduction](#introduction)
2. [Vector Database Providers](#vector-database-providers)
   - [Qdrant](#qdrant)
   - [Chroma](#chroma)
   - [Pinecone](#pinecone)
   - [Weaviate](#weaviate)
   - [FAISS](#faiss)
3. [LLM Providers](#llm-providers)
   - [OpenAI](#openai)
   - [Anthropic](#anthropic)
   - [Azure OpenAI](#azure-openai)
   - [Gemini](#gemini)
   - [Ollama](#ollama)
4. [Embedding Model Providers](#embedding-model-providers)
   - [OpenAI](#openai-1)
   - [HuggingFace](#huggingface)
   - [VertexAI](#vertexai)
   - [AWS Bedrock](#aws-bedrock)
   - [LM Studio](#lm-studio)
5. [Graph Store Providers](#graph-store-providers)
   - [Memgraph](#memgraph)
   - [Neptune](#neptune)
   - [Kuzu](#kuzu)
6. [Configuration and Integration Patterns](#configuration-and-integration-patterns)
7. [Troubleshooting Guide](#troubleshooting-guide)
8. [Conclusion](#conclusion)

## Introduction

The Mem0 ecosystem supports a wide range of providers across vector databases, LLMs, embedding models, and graph stores. This documentation provides comprehensive details on each supported provider, including configuration requirements, authentication methods, connection parameters, and status. For each provider, we include code examples showing how to configure them using both Python and environment variables, explain integration patterns and performance characteristics, and address common setup issues and troubleshooting steps.

The Mem0 platform is designed to be provider-agnostic, allowing developers to choose the best tools for their specific use cases. The configuration system is built around Pydantic models that validate provider-specific parameters and ensure proper setup. Providers are categorized into four main types: vector databases for storing and retrieving embeddings, LLMs for generating responses, embedding models for creating vector representations of text, and graph stores for managing complex relationships between entities.

**Section sources**
- [base.py](file://mem0/configs/base.py#L1-L86)
- [base.py](file://mem0/configs/embeddings/base.py#L1-L111)

## Vector Database Providers

### Qdrant

Qdrant is a vector similarity search engine with extended filtering support. It's designed for storing and searching high-dimensional vectors efficiently.

**Status**: Stable

**Configuration Requirements**:
- `collection_name`: Name of the collection (default: "mem0")
- `embedding_model_dims`: Dimensions of the embedding model (default: 1536)
- Connection method (one of):
  - `host` and `port` for server connection
  - `path` for local storage (default: "/tmp/qdrant")
  - `url` and `api_key` for cloud connection

**Authentication**:
- API key required for cloud instances
- No authentication needed for local/server instances

**Connection Parameters**:
```python
from mem0.configs.vector_stores.qdrant import QdrantConfig

config = QdrantConfig(
    collection_name="my_collection",
    host="localhost",
    port=6333,
    api_key="your-api-key"  # Only for cloud
)
```

Environment variables:
```
QDRANT_HOST=localhost
QDRANT_PORT=6333
QDRANT_API_KEY=your-api-key
```

**Performance Characteristics**:
- Optimized for high-speed similarity search
- Supports on-disk storage for persistence
- Efficient memory usage with configurable caching

**Common Issues and Troubleshooting**:
- **Connection refused**: Verify host and port are correct and Qdrant server is running
- **API key errors**: Ensure API key is provided for cloud instances
- **Collection not found**: Check that the collection name matches exactly

**Official Documentation**: [Qdrant Documentation](https://qdrant.tech/documentation/)

**Section sources**
- [qdrant.py](file://mem0/configs/vector_stores/qdrant.py#L1-L48)

### Chroma

Chroma is a lightweight, open-source vector database designed for AI applications. It provides both in-memory and persistent storage options.

**Status**: Stable

**Configuration Requirements**:
- `collection_name`: Name of the collection (default: "mem0")
- Connection method (one of):
  - `path` for local persistent storage
  - `host` and `port` for server connection
  - `api_key` and `tenant` for ChromaDB Cloud

**Authentication**:
- API key and tenant ID required for ChromaDB Cloud
- No authentication needed for local/server instances

**Connection Parameters**:
```python
from mem0.configs.vector_stores.chroma import ChromaDbConfig

config = ChromaDbConfig(
    collection_name="my_collection",
    path="./chroma_db",  # Local persistent storage
    # OR for cloud:
    # api_key="your-api-key",
    # tenant="your-tenant-id"
)
```

Environment variables:
```
CHROMA_PATH=./chroma_db
# OR for cloud:
# CHROMA_API_KEY=your-api-key
# CHROMA_TENANT=your-tenant-id
```

**Performance Characteristics**:
- Lightweight with minimal dependencies
- Supports both in-memory and persistent storage
- Good performance for small to medium datasets
- Cloud version offers scalability

**Common Issues and Troubleshooting**:
- **Mixed configuration**: Cannot specify both cloud and local configuration simultaneously
- **Missing required fields**: When using cloud, both api_key and tenant are required
- **Permission errors**: Ensure write permissions for the specified path

**Official Documentation**: [Chroma Documentation](https://docs.trychroma.com/)

**Section sources**
- [chroma.py](file://mem0/configs/vector_stores/chroma.py#L1-L59)
- [chroma.py](file://mem0/vector_stores/chroma.py#L1-L268)

### Pinecone

Pinecone is a managed vector database service that handles infrastructure complexity while providing high-performance similarity search.

**Status**: Stable

**Configuration Requirements**:
- `collection_name`: Name of the index/collection (default: "mem0")
- `embedding_model_dims`: Dimensions of the embedding model (default: 1536)
- `api_key`: API key for Pinecone (required unless in environment)
- Deployment configuration (one of):
  - `serverless_config` for serverless deployment
  - `pod_config` for pod-based deployment

**Authentication**:
- API key required (can be provided directly or via PINECONE_API_KEY environment variable)

**Connection Parameters**:
```python
from mem0.configs.vector_stores.pinecone import PineconeConfig

config = PineconeConfig(
    collection_name="my_index",
    api_key="your-api-key",
    serverless_config={
        "cloud": "aws",
        "region": "us-west-2"
    },
    metric="cosine"
)
```

Environment variables:
```
PINECONE_API_KEY=your-api-key
PINECONE_ENVIRONMENT=us-west1-gcp
```

**Performance Characteristics**:
- Managed service with automatic scaling
- High availability and durability
- Optimized for low-latency queries
- Supports hybrid search (metadata + vector)

**Common Issues and Troubleshooting**:
- **API key missing**: Ensure API key is provided or PINECONE_API_KEY environment variable is set
- **Deployment conflict**: Cannot specify both pod_config and serverless_config
- **Index limits**: Be aware of free tier limitations on number of indexes and vectors

**Official Documentation**: [Pinecone Documentation](https://docs.pinecone.io/)

**Section sources**
- [pinecone.py](file://mem0/configs/vector_stores/pinecone.py#L1-L56)

### Weaviate

Weaviate is an open-source vector database with built-in ML model inference, enabling end-to-end AI applications.

**Status**: Stable

**Configuration Requirements**:
- `collection_name`: Name of the collection (default: "mem0")
- `embedding_model_dims`: Dimensions of the embedding model (default: 1536)
- `cluster_url`: URL for Weaviate server (required)
- `auth_client_secret`: API key for authentication (optional)

**Authentication**:
- API key via auth_client_secret
- Additional headers can be provided for custom authentication

**Connection Parameters**:
```python
from mem0.configs.vector_stores.weaviate import WeaviateConfig

config = WeaviateConfig(
    collection_name="my_collection",
    cluster_url="https://your-cluster.weaviate.cloud",
    auth_client_secret="your-api-key"
)
```

Environment variables:
```
WEAVIATE_CLUSTER_URL=https://your-cluster.weaviate.cloud
WEAVIATE_API_KEY=your-api-key
```

**Performance Characteristics**:
- Combines vector search with GraphQL interface
- Supports hybrid search (keyword + vector)
- Built-in schema validation
- Horizontal scalability

**Common Issues and Troubleshooting**:
- **Missing cluster_url**: This parameter is required and cannot be omitted
- **Authentication failures**: Verify API key and ensure it has proper permissions
- **Schema mismatches**: Ensure your data structure matches the defined schema

**Official Documentation**: [Weaviate Documentation](https://weaviate.io/developers/weaviate)

**Section sources**
- [weaviate.py](file://mem0/configs/vector_stores/weaviate.py#L1-L42)

### FAISS

FAISS (Facebook AI Similarity Search) is a library for efficient similarity search and clustering of dense vectors.

**Status**: Stable

**Configuration Requirements**:
- `collection_name`: Name of the collection (default: "mem0")
- `path`: Path to store FAISS index and metadata (optional)
- `distance_strategy`: Distance strategy to use (default: "euclidean")
- `embedding_model_dims`: Dimension of the embedding vector (default: 1536)

**Authentication**:
- No authentication required (local library)

**Connection Parameters**:
```python
from mem0.configs.vector_stores.faiss import FAISSConfig

config = FAISSConfig(
    collection_name="my_index",
    path="./faiss_index",
    distance_strategy="cosine",
    embedding_model_dims=1536
)
```

Environment variables:
```
FAISS_PATH=./faiss_index
FAISS_DISTANCE_STRATEGY=cosine
```

**Performance Characteristics**:
- Extremely fast search performance
- Low memory footprint
- Ideal for offline applications
- Supports GPU acceleration

**Common Issues and Troubleshooting**:
- **Invalid distance strategy**: Must be one of: 'euclidean', 'inner_product', 'cosine'
- **File permission errors**: Ensure write permissions for the specified path
- **Memory issues**: For very large datasets, consider using approximate search methods

**Official Documentation**: [FAISS Documentation](https://github.com/facebookresearch/faiss)

**Section sources**
- [faiss.py](file://mem0/configs/vector_stores/faiss.py#L1-L38)

## LLM Providers

### OpenAI

OpenAI provides state-of-the-art language models including GPT-4, GPT-3.5, and specialized models.

**Status**: Stable

**Configuration Requirements**:
- `model`: OpenAI model to use (default: "gpt-4o-mini")
- `api_key`: OpenAI API key (required)
- `temperature`: Controls randomness (default: 0.1)
- `max_tokens`: Maximum tokens to generate (default: 2000)

**Authentication**:
- API key via api_key parameter or OPENAI_API_KEY environment variable

**Connection Parameters**:
```python
from mem0.configs.llms.openai import OpenAIConfig

config = OpenAIConfig(
    model="gpt-4o",
    api_key="your-api-key",
    temperature=0.7,
    max_tokens=4000,
    top_p=0.9
)
```

Environment variables:
```
OPENAI_API_KEY=your-api-key
OPENAI_MODEL=gpt-4o
OPENAI_TEMPERATURE=0.7
```

**Performance Characteristics**:
- High-quality responses with strong reasoning capabilities
- Fast response times
- Context window up to 128K tokens (for latest models)
- Supports vision capabilities

**Common Issues and Troubleshooting**:
- **Authentication errors**: Verify API key format and ensure it hasn't been revoked
- **Rate limits**: Implement retry logic for 429 errors
- **Model not available**: Check that your API key has access to the requested model
- **Timeouts**: Increase timeout settings for complex queries

**Official Documentation**: [OpenAI API Documentation](https://platform.openai.com/docs/)

**Section sources**
- [openai.py](file://mem0/configs/llms/openai.py#L1-L80)
- [openai.py](file://mem0/llms/openai.py#L1-L148)

### Anthropic

Anthropic provides AI models like Claude with strong reasoning and safety features.

**Status**: Stable

**Configuration Requirements**:
- `model`: Anthropic model to use (e.g., "claude-3-opus-20240229")
- `api_key`: Anthropic API key (required)
- `temperature`: Controls randomness (default: 0.1)
- `max_tokens`: Maximum tokens to generate (default: 2000)

**Authentication**:
- API key via api_key parameter or ANTHROPIC_API_KEY environment variable

**Connection Parameters**:
```python
from mem0.configs.llms.anthropic import AnthropicConfig

config = AnthropicConfig(
    model="claude-3-sonnet-20240229",
    api_key="your-api-key",
    temperature=0.5,
    max_tokens=4000
)
```

Environment variables:
```
ANTHROPIC_API_KEY=your-api-key
ANTHROPIC_MODEL=claude-3-sonnet-20240229
```

**Performance Characteristics**:
- Strong reasoning and coding capabilities
- Large context window (up to 200K tokens)
- Focus on AI safety and alignment
- Good performance on complex tasks

**Common Issues and Troubleshooting**:
- **API key errors**: Ensure the key starts with "sk-ant-"
- **Model access**: Some models may require special access
- **Content filtering**: Responses may be filtered based on safety policies
- **Rate limiting**: Monitor usage to avoid hitting limits

**Official Documentation**: [Anthropic API Documentation](https://docs.anthropic.com/claude/docs)

**Section sources**
- [anthropic.py](file://mem0/configs/llms/anthropic.py#L1-L50)

### Azure OpenAI

Azure OpenAI provides OpenAI models through Microsoft Azure with enterprise-grade security and compliance.

**Status**: Stable

**Configuration Requirements**:
- `model`: Model deployment name in Azure
- `api_key`: Azure OpenAI API key
- `azure_endpoint`: Endpoint URL for Azure OpenAI service
- `api_version`: API version to use

**Authentication**:
- API key and endpoint credentials

**Connection Parameters**:
```python
from mem0.configs.llms.azure import AzureConfig
from mem0.configs.llms.azure_openai import AzureOpenAIConfig

config = AzureOpenAIConfig(
    model="gpt-4o-deployment",
    api_key="your-api-key",
    azure_endpoint="https://your-resource.openai.azure.com/",
    api_version="2024-02-15-preview"
)
```

Environment variables:
```
AZURE_OPENAI_API_KEY=your-api-key
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_API_VERSION=2024-02-15-preview
```

**Performance Characteristics**:
- Enterprise-grade security and compliance
- Integration with Azure services
- Data residency options
- SLA-backed availability

**Common Issues and Troubleshooting**:
- **Resource not found**: Verify endpoint URL and deployment name
- **Region mismatch**: Ensure your application and Azure resource are in compatible regions
- **Permission errors**: Check that your API key has appropriate permissions
- **Version compatibility**: Ensure API version matches your service configuration

**Official Documentation**: [Azure OpenAI Documentation](https://learn.microsoft.com/en-us/azure/ai-services/openai/)

**Section sources**
- [azure.py](file://mem0/configs/llms/azure.py#L1-L40)

### Gemini

Gemini (formerly Bard) is Google's AI model with strong multimodal capabilities.

**Status**: Stable

**Configuration Requirements**:
- `model`: Gemini model to use (e.g., "gemini-pro")
- `api_key`: Google API key (required)
- `temperature`: Controls randomness (default: 0.1)

**Authentication**:
- API key via api_key parameter or GOOGLE_API_KEY environment variable

**Connection Parameters**:
```python
from mem0.embeddings.gemini import GeminiEmbedding

config = GeminiEmbedding(
    model="gemini-pro",
    api_key="your-api-key",
    temperature=0.7
)
```

Environment variables:
```
GOOGLE_API_KEY=your-api-key
GEMINI_MODEL=gemini-pro
```

**Performance Characteristics**:
- Strong multimodal capabilities (text, images, etc.)
- Integration with Google services
- Real-time information access
- Good performance on factual queries

**Common Issues and Troubleshooting**:
- **API key errors**: Ensure the key has Gemini API enabled
- **Quota exceeded**: Check your usage against quota limits
- **Region restrictions**: Some features may be limited by region
- **Content policies**: Responses may be filtered based on Google's policies

**Official Documentation**: [Gemini API Documentation](https://ai.google.dev/)

**Section sources**
- [gemini.py](file://mem0/embeddings/gemini.py#L1-L50)

### Ollama

Ollama allows running large language models locally with a simple API.

**Status**: Stable

**Configuration Requirements**:
- `model`: Model to use (e.g., "llama2", "mistral")
- `ollama_base_url`: Base URL for Ollama API (default: "http://localhost:11434")

**Authentication**:
- No authentication required for local instances

**Connection Parameters**:
```python
from mem0.configs.llms.ollama import OllamaConfig

config = OllamaConfig(
    model="llama2",
    ollama_base_url="http://localhost:11434"
)
```

Environment variables:
```
OLLAMA_HOST=http://localhost:11434
OLLAMA_MODEL=llama2
```

**Performance Characteristics**:
- Runs locally with no data leaving your machine
- Supports many open-source models
- Good for privacy-sensitive applications
- Performance depends on local hardware

**Common Issues and Troubleshooting**:
- **Connection refused**: Ensure Ollama server is running
- **Model not found**: Pull the model first using `ollama pull model-name`
- **Memory issues**: Large models may require significant RAM/VRAM
- **Slow responses**: Performance depends on local hardware capabilities

**Official Documentation**: [Ollama Documentation](https://github.com/jmorganca/ollama)

**Section sources**
- [ollama.py](file://mem0/configs/llms/ollama.py#L1-L35)

## Embedding Model Providers

### OpenAI

OpenAI provides high-quality text embedding models like text-embedding-ada-002.

**Status**: Stable

**Configuration Requirements**:
- `model`: Embedding model to use (default: "text-embedding-ada-002")
- `api_key`: OpenAI API key (required)
- `embedding_dims`: Number of dimensions (default: 1536)

**Authentication**:
- API key via api_key parameter or OPENAI_API_KEY environment variable

**Connection Parameters**:
```python
from mem0.embeddings.openai import OpenAIEmbedding

config = OpenAIEmbedding(
    model="text-embedding-3-small",
    api_key="your-api-key",
    embedding_dims=1536
)
```

Environment variables:
```
OPENAI_API_KEY=your-api-key
OPENAI_EMBEDDING_MODEL=text-embedding-3-small
```

**Performance Characteristics**:
- High-quality embeddings with strong semantic understanding
- Consistent performance across domains
- Well-documented and widely used
- Reliable API with SLA

**Common Issues and Troubleshooting**:
- **Authentication errors**: Verify API key format and permissions
- **Rate limits**: Implement exponential backoff for retries
- **Model deprecation**: Check for deprecated models in favor of newer versions
- **Cost management**: Monitor usage as embeddings are billed per token

**Official Documentation**: [OpenAI Embeddings Documentation](https://platform.openai.com/docs/guides/embeddings)

**Section sources**
- [openai.py](file://mem0/embeddings/openai.py#L1-L50)

### HuggingFace

HuggingFace provides access to thousands of open-source embedding models.

**Status**: Stable

**Configuration Requirements**:
- `model`: HuggingFace model to use (e.g., "sentence-transformers/all-MiniLM-L6-v2")
- `api_key`: HuggingFace API key (required for Inference API)
- `model_kwargs`: Additional model parameters

**Authentication**:
- API key for Inference API, or local execution without authentication

**Connection Parameters**:
```python
from mem0.embeddings.huggingface import HuggingFaceEmbedding

config = HuggingFaceEmbedding(
    model="sentence-transformers/all-MiniLM-L6-v2",
    api_key="your-api-key",  # For Inference API
    model_kwargs={"device": "cuda"}  # For local execution
)
```

Environment variables:
```
HUGGINGFACE_API_KEY=your-api-key
HF_MODEL=sentence-transformers/all-MiniLM-L6-v2
```

**Performance Characteristics**:
- Access to diverse range of models
- Open-source with transparent development
- Can run locally for privacy
- Community-driven with rapid innovation

**Common Issues and Troubleshooting**:
- **Model loading errors**: Ensure model name is correct and accessible
- **Memory issues**: Large models may require significant RAM/VRAM
- **Inference API limits**: Free tier has rate limits
- **Device compatibility**: Ensure CUDA drivers are installed for GPU acceleration

**Official Documentation**: [HuggingFace Documentation](https://huggingface.co/docs)

**Section sources**
- [huggingface.py](file://mem0/embeddings/huggingface.py#L1-L50)

### VertexAI

Vertex AI is Google's unified ML platform that includes embedding models.

**Status**: Stable

**Configuration Requirements**:
- `model`: Vertex AI model to use
- `vertex_credentials_json`: Path to service account JSON file
- `project_id`: Google Cloud project ID

**Authentication**:
- Service account credentials via JSON file

**Connection Parameters**:
```python
from mem0.embeddings.vertexai import VertexAIEmbedding

config = VertexAIEmbedding(
    model="textembedding-gecko@001",
    vertex_credentials_json="/path/to/credentials.json",
    project_id="your-project-id"
)
```

Environment variables:
```
GOOGLE_APPLICATION_CREDENTIALS=/path/to/credentials.json
VERTEXAI_PROJECT_ID=your-project-id
VERTEXAI_MODEL=textembedding-gecko@001
```

**Performance Characteristics**:
- Enterprise-grade reliability
- Integration with Google Cloud services
- Scalable infrastructure
- Data residency options

**Common Issues and Troubleshooting**:
- **Authentication errors**: Verify service account permissions and JSON file
- **API not enabled**: Ensure Vertex AI API is enabled in your project
- **Billing issues**: Confirm billing is set up for your Google Cloud project
- **Region availability**: Some models may not be available in all regions

**Official Documentation**: [Vertex AI Documentation](https://cloud.google.com/vertex-ai)

**Section sources**
- [vertexai.py](file://mem0/embeddings/vertexai.py#L1-L50)

### AWS Bedrock

AWS Bedrock provides access to foundation models from AWS and third parties.

**Status**: Stable

**Configuration Requirements**:
- `model`: Bedrock model to use (e.g., "amazon.titan-embed-text-v1")
- AWS credentials (access key, secret key, region)

**Authentication**:
- AWS IAM credentials

**Connection Parameters**:
```python
from mem0.embeddings.aws_bedrock import AWSBedrockEmbedding

config = AWSBedrockEmbedding(
    model="amazon.titan-embed-text-v1",
    aws_access_key_id="your-access-key",
    aws_secret_access_key="your-secret-key",
    aws_region="us-west-2"
)
```

Environment variables:
```
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key
AWS_DEFAULT_REGION=us-west-2
BEDROCK_MODEL=amazon.titan-embed-text-v1
```

**Performance Characteristics**:
- Access to multiple foundation models
- AWS security and compliance
- Integration with AWS ecosystem
- Pay-per-use pricing

**Common Issues and Troubleshooting**:
- **Access denied**: Verify IAM permissions for Bedrock
- **Region not supported**: Confirm Bedrock is available in your region
- **Model access**: Some models require additional approval
- **VPC configuration**: Ensure proper network configuration if using VPC

**Official Documentation**: [AWS Bedrock Documentation](https://docs.aws.amazon.com/bedrock/)

**Section sources**
- [aws_bedrock.py](file://mem0/embeddings/aws_bedrock.py#L1-L50)

### LM Studio

LM Studio allows running local LLMs with a user-friendly interface.

**Status**: Stable

**Configuration Requirements**:
- `model`: Model to use
- `lmstudio_base_url`: Base URL for LM Studio API (default: "http://localhost:1234/v1")

**Authentication**:
- No authentication required for local instances

**Connection Parameters**:
```python
from mem0.embeddings.lmstudio import LMStudioEmbedding

config = LMStudioEmbedding(
    model="nomic-ai/nomic-embed-text-v1.5",
    lmstudio_base_url="http://localhost:1234/v1"
)
```

Environment variables:
```
LM_STUDIO_URL=http://localhost:1234/v1
LM_STUDIO_MODEL=nomic-ai/nomic-embed-text-v1.5
```

**Performance Characteristics**:
- Runs entirely on local machine
- No data leaves your device
- Easy to use with GUI
- Good for development and testing

**Common Issues and Troubleshooting**:
- **Connection errors**: Ensure LM Studio is running and API is enabled
- **Model loading**: Large models may take time to load into memory
- **Memory constraints**: Monitor RAM usage, especially with large models
- **Port conflicts**: Change port if 1234 is already in use

**Official Documentation**: [LM Studio Documentation](https://lmstudio.ai/)

**Section sources**
- [lmstudio.py](file://mem0/embeddings/lmstudio.py#L1-L50)

## Graph Store Providers

### Memgraph

Memgraph is a high-performance graph database optimized for real-time analytics.

**Status**: Experimental

**Configuration Requirements**:
- Connection details (host, port, username, password)
- Database name

**Authentication**:
- Username and password

**Connection Parameters**:
```python
# Configuration through environment variables
MEMGRAPH_HOST=localhost
MEMGRAPH_PORT=7687
MEMGRAPH_USERNAME=memgraph
MEMGRAPH_PASSWORD=memgraph
```

**Performance Characteristics**:
- Real-time query performance
- Cypher query language support
- Stream processing capabilities
- In-memory computing

**Common Issues and Troubleshooting**:
- **Connection failures**: Verify host and port are correct
- **Authentication errors**: Check username and password
- **Cypher syntax errors**: Validate query syntax
- **Memory usage**: Monitor for high memory consumption with large datasets

**Official Documentation**: [Memgraph Documentation](https://memgraph.com/docs)

**Section sources**
- [memgraph_memory.py](file://mem0/memory/memgraph_memory.py#L1-L50)

### Neptune

Amazon Neptune is a fully managed graph database service.

**Status**: Stable

**Configuration Requirements**:
- `endpoint`: Neptune DB or Analytics endpoint
- AWS credentials for authentication
- For Neptune Analytics: `app_id`

**Authentication**:
- IAM credentials or username/password depending on configuration

**Connection Parameters**:
```python
from mem0.graphs.neptune.neptunedb import MemoryGraph

config = {
    "graph_store": {
        "config": {
            "endpoint": "neptune-db://your-instance.cluster-xxx.us-east-1.neptune.amazonaws.com",
            "base_label": True
        }
    },
    "vector_store": {
        "provider": "opensearch",
        "config": {
            "collection_name": "mem0_neptune_vector_store"
        }
    }
}
```

Environment variables:
```
NEPTUNE_ENDPOINT=neptune-db://your-instance.cluster-xxx.us-east-1.neptune.amazonaws.com
NEPTUNE_REGION=us-east-1
```

**Performance Characteristics**:
- Fully managed service with automatic backups
- High availability and durability
- Supports both property graph and RDF models
- Integration with AWS ecosystem

**Common Issues and Troubleshooting**:
- **Connection timeouts**: Ensure security groups allow connections
- **IAM permissions**: Verify IAM roles have neptune-db permissions
- **VPC configuration**: Neptune instances are typically in VPC
- **Query performance**: Use indexes for frequently queried properties

**Official Documentation**: [Neptune Documentation](https://docs.aws.amazon.com/neptune/)

**Section sources**
- [neptunedb.py](file://mem0/graphs/neptune/neptunedb.py#L1-L512)
- [neptunegraph.py](file://mem0/graphs/neptune/neptunegraph.py#L1-L475)

### Kuzu

Kuzu is a high-performance, open-source graph database management system.

**Status**: Experimental

**Configuration Requirements**:
- `db_path`: Path to store the database
- Schema definitions for nodes and relationships

**Authentication**:
- No authentication required (local database)

**Connection Parameters**:
```python
from mem0.memory.kuzu_memory import KuzuMemory

config = KuzuMemory(
    db_path="./kuzu_db",
    # Schema is automatically created based on usage
)
```

Environment variables:
```
KUZU_DB_PATH=./kuzu_db
```

**Performance Characteristics**:
- High-speed query execution
- Lightweight with small footprint
- ACID-compliant transactions
- SQL-like query language

**Common Issues and Troubleshooting**:
- **File permissions**: Ensure write access to the database path
- **Disk space**: Monitor for growing database files
- **Schema evolution**: Plan for schema changes in production
- **Concurrency**: Test under expected load conditions

**Official Documentation**: [Kuzu Documentation](https://kuzudb.com/)

**Section sources**
- [kuzu_memory.py](file://mem0/memory/kuzu_memory.py#L1-L50)

## Configuration and Integration Patterns

The Mem0 ecosystem uses a consistent configuration pattern across all providers, leveraging Pydantic models for validation and type safety. The configuration system is hierarchical, with a main MemoryConfig that contains configurations for vector store, LLM, embedder, and graph store components.

```python
from mem0.configs.base import MemoryConfig
from mem0.configs.vector_stores.chroma import ChromaDbConfig
from mem0.configs.llms.openai import OpenAIConfig
from mem0.configs.embeddings.base import BaseEmbedderConfig
from mem0.configs.graphs.configs import GraphStoreConfig

config = MemoryConfig(
    vector_store=ChromaDbConfig(
        collection_name="my_memories",
        path="./chroma_data"
    ),
    llm=OpenAIConfig(
        model="gpt-4o",
        api_key="your-api-key"
    ),
    embedder=BaseEmbedderConfig(
        model="text-embedding-3-small",
        api_key="your-api-key"
    ),
    graph_store=GraphStoreConfig(
        provider="neptune",
        config={
            "endpoint": "neptune-db://your-instance.cluster-xxx.us-east-1.neptune.amazonaws.com"
        }
    )
)
```

Key integration patterns include:

1. **Provider Chaining**: Using different providers for different components (e.g., OpenAI for LLM, Chroma for vector storage)
2. **Fallback Strategies**: Configuring multiple providers for high availability
3. **Hybrid Storage**: Combining vector databases with graph stores for rich memory representation
4. **Environment-based Configuration**: Using different providers for development, staging, and production

The configuration system supports both programmatic configuration and environment variable-based configuration, making it easy to manage secrets and adapt to different deployment environments.

**Section sources**
- [base.py](file://mem0/configs/base.py#L1-L86)
- [base.py](file://mem0/configs/embeddings/base.py#L1-L111)

## Troubleshooting Guide

### General Troubleshooting Steps

1. **Verify Provider Status**: Check if the provider is marked as stable, experimental, or deprecated
2. **Check Authentication**: Ensure all required credentials are provided and valid
3. **Validate Configuration**: Confirm all required parameters are set correctly
4. **Test Connectivity**: Verify network connectivity to the provider
5. **Review Error Messages**: Examine detailed error messages for specific issues

### Common Issues and Solutions

**Authentication Failures**:
- Double-check API keys and ensure they haven't expired
- Verify that environment variables are properly set
- Check that IAM roles have the necessary permissions (for cloud providers)

**Connection Issues**:
- Test network connectivity to the provider endpoint
- Verify hostnames, ports, and URLs are correct
- Check firewall and security group settings

**Performance Problems**:
- Monitor resource usage (CPU, memory, network)
- Consider upgrading to a higher-tier plan for managed services
- Optimize queries and reduce payload sizes

**Configuration Errors**:
- Validate configuration against the provider's documentation
- Use configuration validation tools when available
- Start with minimal configuration and add options incrementally

### Debugging Tips

1. **Enable Logging**: Set appropriate log levels to capture detailed information
2. **Use Test Endpoints**: Many providers offer test endpoints for validation
3. **Check Provider Status**: Verify the provider's status page for outages
4. **Review Rate Limits**: Ensure you're not exceeding rate limits
5. **Validate Data Formats**: Confirm data formats match provider requirements

**Section sources**
- [errors.py](file://mem0/exceptions.py#L1-L50)
- [base.py](file://mem0/configs/base.py#L1-L86)

## Conclusion

The Mem0 ecosystem provides comprehensive support for a wide range of providers across vector databases, LLMs, embedding models, and graph stores. This flexibility allows developers to choose the best tools for their specific use cases while maintaining a consistent interface and configuration pattern.

Key takeaways:
- The configuration system is robust and validated using Pydantic models
- Providers are categorized by stability (stable, experimental, deprecated)
- Both programmatic and environment-based configuration are supported
- Comprehensive error handling and validation are built into the system
- Integration patterns support complex, production-grade applications

When selecting providers, consider factors such as:
- Data privacy requirements (local vs. cloud)
- Performance and scalability needs
- Cost considerations
- Existing infrastructure and expertise
- Specific feature requirements

The modular design of Mem0 makes it easy to switch providers or combine multiple providers to create sophisticated AI applications with persistent memory capabilities.

**Section sources**
- [base.py](file://mem0/configs/base.py#L1-L86)
- [base.py](file://mem0/configs/embeddings/base.py#L1-L111)