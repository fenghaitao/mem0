# API Reference

<cite>
**Referenced Files in This Document**   
- [main.py](file://mem0/client/main.py)
- [main.py](file://mem0/memory/main.py)
- [project.py](file://mem0/client/project.py)
- [factory.py](file://mem0/utils/factory.py)
- [base.py](file://mem0/configs/base.py)
- [memories.py](file://openmemory/api/app/routers/memories.py)
</cite>

## Table of Contents
1. [Introduction](#introduction)
2. [Memory Class API](#memory-class-api)
3. [Configuration Classes](#configuration-classes)
4. [Factory Classes](#factory-classes)
5. [REST API Endpoints](#rest-api-endpoints)
6. [Client Implementation Guidelines](#client-implementation-guidelines)
7. [Versioning and Backwards Compatibility](#versioning-and-backwards-compatibility)
8. [Rate Limiting](#rate-limiting)

## Introduction
The Mem0 API provides a comprehensive interface for managing memories in AI applications. This documentation covers all public interfaces including the Memory class, configuration options, factory patterns, and REST API endpoints. The system enables developers to create, retrieve, search, update, and delete memories with support for various LLM providers, vector databases, and embedding models. The API is designed to be intuitive and flexible, supporting both synchronous and asynchronous operations.

## Memory Class API

The Memory class provides the core functionality for managing memories in the Mem0 system. It supports creating, retrieving, searching, updating, and deleting memories with various filtering options.

### MemoryClient Methods

The MemoryClient class provides a high-level interface for interacting with the Mem0 API.

**Section sources**
- [main.py](file://mem0/client/main.py#L24-L800)

#### add()
Adds a new memory to the system.

**Parameters:**
- `messages`: List of message dictionaries containing role and content
- `user_id`: Optional user identifier for scoping memories
- `agent_id`: Optional agent identifier for scoping memories
- `app_id`: Optional application identifier for scoping memories
- `metadata`: Optional metadata dictionary to attach to the memory
- `filters`: Optional filtering criteria for memory operations

**Returns:** Dictionary containing the API response with memory details.

**Exceptions:**
- `ValidationError`: Invalid input data
- `AuthenticationError`: Authentication failure
- `RateLimitError`: Rate limit exceeded
- `MemoryQuotaExceededError`: Memory quota exceeded
- `NetworkError`: Network connectivity issues
- `MemoryNotFoundError`: Memory not found

**Example:**
```python
client.add(messages=[{"role": "user", "content": "I enjoy hiking on weekends"}], user_id="user_123")
```

#### get()
Retrieves a specific memory by ID.

**Parameters:**
- `memory_id`: The unique identifier of the memory to retrieve

**Returns:** Dictionary containing the memory data.

**Exceptions:**
- `ValidationError`: Invalid input data
- `AuthenticationError`: Authentication failure
- `RateLimitError`: Rate limit exceeded
- `MemoryQuotaExceededError`: Memory quota exceeded
- `NetworkError`: Network connectivity issues
- `MemoryNotFoundError`: Memory not found

#### get_all()
Retrieves all memories with optional filtering.

**Parameters:**
- `version`: API version to use (v1 or v2)
- `user_id`: Filter by user ID
- `agent_id`: Filter by agent ID
- `app_id`: Filter by application ID
- `top_k`: Maximum number of results to return

**Returns:** List of dictionaries containing memory objects.

#### search()
Searches memories based on a query string.

**Parameters:**
- `query`: Search query string
- `version`: API version to use
- `user_id`: Filter by user ID
- `agent_id`: Filter by agent ID
- `app_id`: Filter by application ID
- `top_k`: Maximum number of results to return
- `filters`: Additional filtering criteria

**Returns:** List of dictionaries containing search results.

#### update()
Updates an existing memory by ID.

**Parameters:**
- `memory_id`: ID of the memory to update
- `text`: New content for the memory
- `metadata`: New metadata for the memory

**Returns:** Dictionary containing the server response.

#### delete()
Deletes a specific memory by ID.

**Parameters:**
- `memory_id`: ID of the memory to delete

**Returns:** Dictionary containing the API response.

#### delete_all()
Deletes all memories with optional filtering.

**Parameters:**
- `user_id`: Delete memories for specific user
- `agent_id`: Delete memories for specific agent
- `app_id`: Delete memories for specific application

**Returns:** Dictionary containing the API response.

#### history()
Retrieves the change history of a specific memory.

**Parameters:**
- `memory_id`: ID of the memory to retrieve history for

**Returns:** List of dictionaries containing memory history entries.

#### users()
Retrieves all users, agents, and sessions for which memories exist.

**Returns:** Dictionary containing entity information.

#### delete_users()
Deletes specific entities or all entities if no filters provided.

**Parameters:**
- `user_id`: Delete specific user
- `agent_id`: Delete specific agent
- `app_id`: Delete specific application
- `run_id`: Delete specific run

**Returns:** Dictionary with success message.

#### reset()
Resets the client by deleting all users and memories.

**Returns:** Dictionary with reset confirmation message.

#### batch_update()
Performs batch update of multiple memories.

**Parameters:**
- `memories`: List of memory dictionaries to update, each containing memory_id, text, and/or metadata

**Returns:** Dictionary containing the server response.

#### batch_delete()
Performs batch deletion of multiple memories.

**Parameters:**
- `memories`: List of memory dictionaries to delete, each containing memory_id

**Returns:** Dictionary containing the server response.

#### create_memory_export()
Creates a memory export with the provided schema.

**Parameters:**
- `schema`: JSON schema defining the export structure
- `user_id`: Filter for specific user
- `run_id`: Filter for specific run

**Returns:** Dictionary containing export request ID and status.

#### get_memory_export()
Retrieves a memory export.

**Parameters:**
- `user_id`: Filter for specific user

**Returns:** Dictionary containing the exported data.

#### get_summary()
Retrieves the summary of a memory export.

**Parameters:**
- `filters`: Optional filters to apply to the summary request

**Returns:** Dictionary containing the export status and summary data.

#### get_project()
Retrieves project details (deprecated, use client.project.get() instead).

**Parameters:**
- `fields`: List of fields to retrieve

**Returns:** Dictionary containing the requested fields.

#### update_project()
Updates project settings (deprecated, use client.project.update() instead).

**Parameters:**
- `custom_instructions`: New instructions for the project
- `custom_categories`: New categories for the project
- `retrieval_criteria`: New retrieval criteria for the project
- `enable_graph`: Enable or disable graph functionality
- `version`: Project version

**Returns:** Dictionary containing the API response.

#### get_webhooks()
Retrieves webhook configuration for the project.

**Parameters:**
- `project_id`: ID of the project to get webhooks for

**Returns:** Dictionary containing webhook details.

#### create_webhook()
Creates a new webhook for the project.

**Parameters:**
- `url`: URL to send the webhook to
- `name`: Name of the webhook
- `project_id`: ID of the project
- `event_types`: List of event types to trigger the webhook

**Returns:** Dictionary containing the created webhook details.

#### update_webhook()
Updates an existing webhook configuration.

**Parameters:**
- `webhook_id`: ID of the webhook to update
- `name`: New name for the webhook
- `url`: New URL for the webhook
- `event_types`: List of event types to trigger the webhook

**Returns:** Dictionary containing the updated webhook details.

#### delete_webhook()
Deletes a webhook.

**Parameters:**
- `webhook_id`: ID of the webhook to delete

**Returns:** Dictionary containing the deletion confirmation.

## Configuration Classes

The Mem0 system uses configuration classes to define settings for various components including vector stores, LLMs, embedders, and graph stores.

### MemoryConfig

The MemoryConfig class defines the overall configuration for the memory system.

**Section sources**
- [base.py](file://mem0/configs/base.py#L29-L63)

**Attributes:**
- `vector_store`: Configuration for the vector store (VectorStoreConfig)
- `llm`: Configuration for the language model (LlmConfig)
- `embedder`: Configuration for the embedding model (EmbedderConfig)
- `history_db_path`: Path to the history database (string, default: ~/.mem0/history.db)
- `graph_store`: Configuration for the graph store (GraphStoreConfig)
- `version`: API version (string, default: "v1.1")
- `custom_fact_extraction_prompt`: Custom prompt for fact extraction (string, optional)
- `custom_update_memory_prompt`: Custom prompt for updating memories (string, optional)

### VectorStoreConfig

Configuration for vector database providers.

**Available Providers:**
- qdrant
- chroma
- pgvector
- milvus
- upstash_vector
- azure_ai_search
- azure_mysql
- pinecone
- mongodb
- redis
- valkey
- databricks
- elasticsearch
- vertex_ai_vector_search
- opensearch
- supabase
- weaviate
- faiss
- langchain
- s3_vectors
- baidu
- neptune

### LlmConfig

Configuration for language model providers.

**Available Providers:**
- ollama
- openai
- groq
- together
- aws_bedrock
- litellm
- azure_openai
- openai_structured
- anthropic
- azure_openai_structured
- gemini
- deepseek
- xai
- sarvam
- lmstudio
- vllm
- langchain

### EmbedderConfig

Configuration for embedding model providers.

**Available Providers:**
- openai
- ollama
- huggingface
- azure_openai
- gemini
- vertexai
- together
- lmstudio
- langchain
- aws_bedrock
- github_copilot

### GraphStoreConfig

Configuration for graph database providers.

**Available Providers:**
- neptune
- kuzu
- memgraph
- neo4j

## Factory Classes

The Mem0 system uses factory classes to create instances of various components based on configuration.

### LlmFactory

Creates LLM instances with appropriate configurations.

**Section sources**
- [factory.py](file://mem0/utils/factory.py#L23-L129)

**Methods:**
- `create(provider_name, config, **kwargs)`: Creates an LLM instance
- `register_provider(name, class_path, config_class)`: Registers a new provider
- `get_supported_providers()`: Returns list of supported providers

**Usage:**
```python
from mem0.utils.factory import LlmFactory
llm = LlmFactory.create("openai", {"model": "gpt-4"})
```

### EmbedderFactory

Creates embedder instances with appropriate configurations.

**Methods:**
- `create(provider_name, config, vector_config)`: Creates an embedder instance

**Usage:**
```python
from mem0.utils.factory import EmbedderFactory
embedder = EmbedderFactory.create("openai", {"model": "text-embedding-ada-002"})
```

### VectorStoreFactory

Creates vector store instances with appropriate configurations.

**Methods:**
- `create(provider_name, config)`: Creates a vector store instance
- `reset(instance)`: Resets a vector store instance

**Usage:**
```python
from mem0.utils.factory import VectorStoreFactory
vector_store = VectorStoreFactory.create("qdrant", {"host": "localhost", "port": 6333})
```

### GraphStoreFactory

Creates graph store instances with appropriate configurations.

**Methods:**
- `create(provider_name, config)`: Creates a graph store instance

**Usage:**
```python
from mem0.utils.factory import GraphStoreFactory
graph_store = GraphStoreFactory.create("neptune", {"host": "localhost", "port": 8182})
```

## REST API Endpoints

The Mem0 system provides a REST API for interacting with memories and related resources.

### Authentication

All API requests require authentication via API key in the Authorization header:

```
Authorization: Token <your_api_key>
```

Additionally, include the Mem0-User-ID header:

```
Mem0-User-ID: <user_id_hash>
```

### Base URL

The base URL for the API is: `https://api.mem0.ai`

### Memories Endpoints

#### List Memories
```
GET /v1/memories/
```

**Parameters:**
- `user_id`: Filter by user ID
- `agent_id`: Filter by agent ID
- `app_id`: Filter by application ID
- `page`: Page number for pagination
- `page_size`: Number of items per page

**Response:**
```json
{
  "results": [
    {
      "id": "string",
      "memory": "string",
      "hash": "string",
      "created_at": "string",
      "updated_at": "string",
      "user_id": "string",
      "agent_id": "string",
      "app_id": "string",
      "metadata": {}
    }
  ]
}
```

#### Create Memory
```
POST /v1/memories/
```

**Request Body:**
```json
{
  "messages": [
    {
      "role": "user",
      "content": "string"
    }
  ],
  "user_id": "string",
  "agent_id": "string",
  "app_id": "string",
  "metadata": {},
  "output_format": "v1.1",
  "version": "v2"
}
```

**Response:**
```json
{
  "results": [
    {
      "id": "string",
      "memory": "string",
      "event": "ADD"
    }
  ]
}
```

#### Get Memory
```
GET /v1/memories/{memory_id}/
```

**Response:**
```json
{
  "id": "string",
  "memory": "string",
  "hash": "string",
  "created_at": "string",
  "updated_at": "string",
  "user_id": "string",
  "agent_id": "string",
  "app_id": "string",
  "metadata": {}
}
```

#### Update Memory
```
PUT /v1/memories/{memory_id}/
```

**Request Body:**
```json
{
  "text": "string",
  "metadata": {}
}
```

**Response:**
```json
{
  "id": "string",
  "memory": "string",
  "event": "UPDATE",
  "previous_memory": "string"
}
```

#### Delete Memory
```
DELETE /v1/memories/{memory_id}/
```

**Response:**
```json
{
  "message": "Memory deleted successfully!"
}
```

#### Search Memories
```
POST /v1/memories/search/
```

**Request Body:**
```json
{
  "query": "string",
  "user_id": "string",
  "agent_id": "string",
  "app_id": "string",
  "top_k": 100
}
```

**Response:**
```json
{
  "results": [
    {
      "id": "string",
      "memory": "string",
      "score": 0.95,
      "created_at": "string",
      "updated_at": "string"
    }
  ]
}
```

#### Get Memory History
```
GET /v1/memories/{memory_id}/history/
```

**Response:**
```json
[
  {
    "id": "string",
    "memory": "string",
    "created_at": "string",
    "event": "ADD"
  }
]
```

### Entities Endpoints

#### List Entities
```
GET /v1/entities/
```

**Response:**
```json
{
  "results": [
    {
      "type": "user",
      "name": "string"
    }
  ]
}
```

#### Delete Entities
```
DELETE /v2/entities/{type}/{name}/
```

**Response:**
```json
{
  "message": "Entity deleted successfully."
}
```

### Project Endpoints

#### Get Project Details
```
GET /api/v1/orgs/organizations/{org_id}/projects/{project_id}/
```

**Response:**
```json
{
  "id": "string",
  "name": "string",
  "custom_instructions": "string",
  "custom_categories": ["string"],
  "retrieval_criteria": [],
  "enable_graph": false
}
```

#### Update Project
```
PATCH /api/v1/orgs/organizations/{org_id}/projects/{project_id}/
```

**Request Body:**
```json
{
  "custom_instructions": "string",
  "custom_categories": ["string"],
  "retrieval_criteria": [],
  "enable_graph": true
}
```

**Response:**
```json
{
  "message": "Project updated successfully!"
}
```

### Webhooks Endpoints

#### List Webhooks
```
GET /api/v1/webhooks/projects/{project_id}/
```

**Response:**
```json
{
  "webhooks": [
    {
      "id": 1,
      "url": "string",
      "name": "string",
      "event_types": ["string"],
      "created_at": "string"
    }
  ]
}
```

#### Create Webhook
```
POST /api/v1/webhooks/projects/{project_id}/
```

**Request Body:**
```json
{
  "url": "string",
  "name": "string",
  "event_types": ["string"]
}
```

**Response:**
```json
{
  "id": 1,
  "url": "string",
  "name": "string",
  "event_types": ["string"],
  "created_at": "string"
}
```

#### Update Webhook
```
PUT /api/v1/webhooks/{webhook_id}/
```

**Request Body:**
```json
{
  "url": "string",
  "name": "string",
  "event_types": ["string"]
}
```

**Response:**
```json
{
  "id": 1,
  "url": "string",
  "name": "string",
  "event_types": ["string"],
  "created_at": "string"
}
```

#### Delete Webhook
```
DELETE /api/v1/webhooks/{webhook_id}/
```

**Response:**
```json
{
  "message": "Webhook deleted successfully!"
}
```

### Error Codes

The API returns standard HTTP status codes with additional error details in the response body.

**Common Status Codes:**
- `200 OK`: Successful request
- `201 Created`: Resource created successfully
- `400 Bad Request`: Invalid request parameters
- `401 Unauthorized`: Authentication failed
- `403 Forbidden`: Insufficient permissions
- `404 Not Found`: Resource not found
- `429 Too Many Requests`: Rate limit exceeded
- `500 Internal Server Error`: Server error

**Error Response Format:**
```json
{
  "detail": "Error description"
}
```

## Client Implementation Guidelines

### Python Client

The Python client provides a convenient interface for interacting with the Mem0 API.

**Installation:**
```bash
pip install mem0ai
```

**Initialization:**
```python
from mem0 import MemoryClient

client = MemoryClient(api_key="your_api_key")
# or use environment variable MEM0_API_KEY
```

**Configuration Options:**
- `api_key`: API key for authentication
- `host`: API base URL (default: https://api.mem0.ai)
- `org_id`: Organization ID
- `project_id`: Project ID
- `client`: Custom httpx.Client instance

**Example Usage:**
```python
# Add a memory
response = client.add(
    messages=[{"role": "user", "content": "I enjoy hiking on weekends"}],
    user_id="user_123"
)

# Search memories
results = client.search("hiking", user_id="user_123")

# Update a memory
client.update(memory_id="mem_456", text="I enjoy hiking in the mountains on weekends")

# Delete a memory
client.delete(memory_id="mem_456")
```

### JavaScript/TypeScript Client

The JavaScript/TypeScript client is available for browser and Node.js environments.

**Installation:**
```bash
npm install @mem0/client
```

**Initialization:**
```javascript
import { MemoryClient } from '@mem0/client';

const client = new MemoryClient({
  apiKey: 'your_api_key',
  host: 'https://api.mem0.ai'
});
```

**Example Usage:**
```javascript
// Add a memory
const response = await client.add({
  messages: [{ role: 'user', content: 'I enjoy hiking on weekends' }],
  userId: 'user_123'
});

// Search memories
const results = await client.search('hiking', { userId: 'user_123' });
```

### REST API Direct Calls

For languages without a dedicated client library, you can make direct HTTP requests to the API.

**Example (curl):**
```bash
curl -X POST https://api.mem0.ai/v1/memories/ \
  -H "Authorization: Token your_api_key" \
  -H "Mem0-User-ID: user_hash" \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [{"role": "user", "content": "I enjoy hiking on weekends"}],
    "user_id": "user_123"
  }'
```

## Versioning and Backwards Compatibility

The Mem0 API follows semantic versioning principles to ensure backwards compatibility.

### API Versions

The API supports multiple versions to allow for gradual migration:

- `v1`: Original API version
- `v1.1`: Updated response format with "results" wrapper
- `v2`: Enhanced features and improved performance

**Version Specification:**
- Include version in endpoint URL: `/v1/memories/`
- Use version parameter in requests when supported

### Deprecation Policy

Deprecated features are maintained for a minimum of 6 months before removal. During this period:

1. Deprecated methods emit deprecation warnings
2. Documentation clearly marks deprecated features
3. Alternative approaches are provided

**Current Deprecations:**
- `get_project()` method - use `client.project.get()` instead
- `update_project()` method - use `client.project.update()` instead
- `output_format='v1.0'` - use 'v1.1' instead

### Migration Guide

When upgrading between major versions:

1. Review the changelog for breaking changes
2. Update client library to the latest version
3. Test all API calls in a staging environment
4. Update version parameters in requests
5. Monitor for deprecation warnings

## Rate Limiting

The Mem0 API implements rate limiting to ensure fair usage and system stability.

### Rate Limits

Rate limits are applied per API key and vary by plan:

**Free Tier:**
- 100 requests per minute
- 10,000 requests per day

**Pro Tier:**
- 1,000 requests per minute
- 1,000,000 requests per day

**Enterprise Tier:**
- Custom rate limits based on agreement

### Rate Limit Headers

Rate limit information is included in response headers:

- `X-RateLimit-Limit`: Maximum number of requests in the current window
- `X-RateLimit-Remaining`: Number of requests remaining in the current window
- `X-RateLimit-Reset`: Time when the rate limit window resets (Unix timestamp)

### Handling Rate Limits

When rate limits are exceeded, the API returns a 429 status code. Implement retry logic with exponential backoff:

```python
import time
import random

def make_api_call_with_retry(client, *args, max_retries=3):
    for i in range(max_retries):
        try:
            return client.add(*args)
        except RateLimitError:
            if i == max_retries - 1:
                raise
            # Exponential backoff with jitter
            sleep_time = (2 ** i) + random.uniform(0, 1)
            time.sleep(sleep_time)
    return None
```

### Burst Limits

In addition to sustained rate limits, burst limits apply:

- Maximum of 10 requests per second
- Bursts larger than 10 requests will be rate limited

Monitor your usage through the dashboard to optimize request patterns and avoid hitting limits.