# Vertex AI Embeddings

<cite>
**Referenced Files in This Document**   
- [vertexai.py](file://mem0/embeddings/vertexai.py)
- [base.py](file://mem0/configs/embeddings/base.py)
- [vertex_ai_vector_search.py](file://mem0/configs/vector_stores/vertex_ai_vector_search.py)
- [test_vertexai_embeddings.py](file://tests/embeddings/test_vertexai_embeddings.py)
- [vertex_ai.ipynb](file://embedchain/notebooks/vertex_ai.ipynb)
</cite>

## Table of Contents
1. [Introduction](#introduction)
2. [Authentication Methods](#authentication-methods)
3. [Configuration Parameters](#configuration-parameters)
4. [Initialization and Usage](#initialization-and-usage)
5. [Regional Availability and Model Options](#regional-availability-and-model-options)
6. [Performance and Pricing](#performance-and-pricing)
7. [Error Handling and Troubleshooting](#error-handling-and-troubleshooting)
8. [Best Practices](#best-practices)

## Introduction
This document provides comprehensive guidance on integrating Google Vertex AI embeddings into applications. The Vertex AI embedding system enables developers to generate high-quality text embeddings using Google's advanced machine learning models. The integration supports both synchronous and asynchronous operations, with configurable parameters for model selection, dimensionality, and task-specific embedding types. This documentation covers authentication, configuration, initialization, performance characteristics, and best practices for implementing Vertex AI embeddings effectively.

## Authentication Methods
Vertex AI embeddings support two primary authentication methods: service account keys and application default credentials. The authentication mechanism is implemented through the `VertexAIEmbedding` class, which checks for credentials in a specific order of precedence.

When initializing the `VertexAIEmbedding` class, the system first checks if a service account key path is provided via the `vertex_credentials_json` configuration parameter. If present, this path is set as the `GOOGLE_APPLICATION_CREDENTIALS` environment variable, which Vertex AI uses for authentication. This approach allows explicit specification of credentials for specific service accounts.

If no explicit credentials path is provided, the system falls back to application default credentials by checking if the `GOOGLE_APPLICATION_CREDENTIALS` environment variable is already set. This enables developers to use pre-configured credentials in their development or production environments without hardcoding paths in their applications.

The authentication process includes validation to ensure credentials are available before attempting to initialize the embedding model. If neither method provides valid credentials, the system raises a `ValueError` with a descriptive message indicating that Google application credentials must be provided either through a JSON file path or environment variable.

**Section sources**
- [vertexai.py](file://mem0/embeddings/vertexai.py#L23-L30)
- [base.py](file://mem0/configs/embeddings/base.py#L30-L31)

## Configuration Parameters
The Vertex AI embedding system provides several configurable parameters to customize the embedding generation process. These parameters are defined in the `BaseEmbedderConfig` class and can be set during initialization of the `VertexAIEmbedding` instance.

The primary configuration parameters include:
- **model**: Specifies the embedding model to use, with a default value of "text-embedding-004". This parameter allows selection of different Vertex AI embedding models based on requirements.
- **embedding_dims**: Sets the dimensionality of the generated embeddings, defaulting to 256 dimensions. This parameter controls the size of the output embedding vector.
- **vertex_credentials_json**: Path to the service account credentials JSON file for authentication.
- **memory_add_embedding_type**: Specifies the embedding type for memory add operations, defaulting to "RETRIEVAL_DOCUMENT".
- **memory_update_embedding_type**: Specifies the embedding type for memory update operations, defaulting to "RETRIEVAL_DOCUMENT".
- **memory_search_embedding_type**: Specifies the embedding type for memory search operations, defaulting to "RETRIEVAL_QUERY".

Additional parameters related to Vertex AI Vector Search integration include project ID, region, endpoint ID, and index ID, which are used when integrating with Vertex AI's vector database capabilities.

The configuration system follows a hierarchy where provided values take precedence over defaults, allowing flexible customization while ensuring sensible defaults for required parameters.

**Section sources**
- [base.py](file://mem0/configs/embeddings/base.py#L15-L111)
- [vertex_ai_vector_search.py](file://mem0/configs/vector_stores/vertex_ai_vector_search.py#L6-L15)

## Initialization and Usage
The Vertex AI embedding system can be initialized and used in both synchronous and asynchronous modes, providing flexibility for different application requirements.

### Synchronous Usage
To initialize the Vertex AI embedding system synchronously, create an instance of the `VertexAIEmbedding` class with the desired configuration:

```python
from mem0.embeddings.vertexai import VertexAIEmbedding
from mem0.configs.embeddings.base import BaseEmbedderConfig

config = BaseEmbedderConfig(
    model="text-embedding-004",
    embedding_dims=256,
    vertex_credentials_json="/path/to/credentials.json"
)
embedder = VertexAIEmbedding(config)
```

Once initialized, generate embeddings by calling the `embed` method with the text to be embedded:

```python
embedding = embedder.embed("This is a sample text to embed")
```

The `embed` method also supports a `memory_action` parameter that specifies the purpose of the embedding (add, search, or update), which influences the embedding type used:

```python
# For adding content to memory
embedding = embedder.embed("New content", memory_action="add")

# For searching memory
search_embedding = embedder.embed("Search query", memory_action="search")
```

### Asynchronous Usage
For applications requiring asynchronous operations, the system can be integrated with async frameworks. While the core embedding functionality is synchronous, it can be wrapped in async functions for non-blocking execution in async applications.

The embedding process uses the `TextEmbeddingModel.from_pretrained()` method to load the specified model and the `get_embeddings()` method to generate embeddings with the configured dimensionality. The system handles the conversion of the model's output to a standard list format for easy integration with downstream applications.

**Section sources**
- [vertexai.py](file://mem0/embeddings/vertexai.py#L10-L54)
- [test_vertexai_embeddings.py](file://tests/embeddings/test_vertexai_embeddings.py#L49-L161)

## Regional Availability and Model Options
Vertex AI embeddings are available in multiple Google Cloud regions, allowing developers to select the optimal location based on their infrastructure and latency requirements. The region is specified through the configuration parameters when integrating with Vertex AI Vector Search.

The primary embedding model available is "text-embedding-004", which is optimized for semantic similarity tasks. This model supports various embedding types through the task_type parameter, including:
- SEMANTIC_SIMILARITY: For general semantic similarity tasks
- RETRIEVAL_DOCUMENT: For document retrieval scenarios
- RETRIEVAL_QUERY: For query retrieval scenarios
- CLASSIFICATION: For classification tasks
- CLUSTERING: For clustering operations
- QUESTION_ANSWERING: For question answering applications
- FACT_VERIFICATION: For fact verification use cases
- CODE_RETRIEVAL_QUERY: For code retrieval queries

The "textembedding-gecko" model mentioned in the configuration example is another available option, particularly suitable for retrieval tasks. Different models may have varying performance characteristics, latency, and cost structures, so selection should be based on the specific use case requirements.

When configuring the embedding system, developers should consider the regional availability of models and select regions that provide the best performance and compliance with data residency requirements.

**Section sources**
- [vertexai.py](file://mem0/embeddings/vertexai.py#L14-L15)
- [vertex_ai.ipynb](file://embedchain/notebooks/vertex_ai.ipynb#L94-L97)

## Performance and Pricing
The Vertex AI embedding system offers competitive performance characteristics with configurable dimensionality options. The default embedding dimension is 256, but this can be adjusted based on application requirements, with higher dimensions potentially providing more nuanced representations at the cost of increased storage and computational requirements.

Performance benchmarks indicate that the system can efficiently process text inputs of varying lengths, with response times typically in the range of hundreds of milliseconds for single embeddings. The actual performance may vary based on the selected model, input text length, and network conditions between the client and Vertex AI services.

Pricing for Vertex AI embeddings follows Google Cloud's pay-per-use model, with costs based on the number of characters processed. The exact pricing details are not available in the codebase, but developers should consult the official Google Cloud pricing documentation for current rates. The system is designed to be cost-effective for both small-scale applications and high-volume production use cases.

For applications requiring high throughput, the system supports batching of embedding requests, which can significantly improve efficiency and reduce costs compared to individual requests. Developers should consider implementing request batching for applications that need to process multiple texts simultaneously.

**Section sources**
- [vertexai.py](file://mem0/embeddings/vertexai.py#L15-L16)
- [vertex_ai.ipynb](file://embedchain/notebooks/vertex_ai.ipynb#L87-L90)

## Error Handling and Troubleshooting
The Vertex AI embedding system includes comprehensive error handling to address common issues that may arise during integration and usage.

### Common Issues and Solutions
**Permission Errors**: These typically occur when authentication credentials are not properly configured. Ensure that either the `vertex_credentials_json` parameter is set with a valid service account key path or the `GOOGLE_APPLICATION_CREDENTIALS` environment variable is set. Verify that the service account has the necessary permissions for Vertex AI services.

**Quota Limits**: Google Cloud projects have default quotas for API usage. If you encounter quota-related errors, check your Google Cloud Console to monitor usage and request quota increases if needed. Implement retry logic with exponential backoff for handling temporary quota exhaustion.

**Network Connectivity Problems**: These may occur due to firewall restrictions or network configuration issues. Ensure that your environment can connect to Google Cloud APIs and that any required proxy settings are configured in your application.

### Specific Error Conditions
The system explicitly handles several error conditions:
- Missing credentials: Raises a `ValueError` if no credentials are provided through either method
- Invalid memory actions: Raises a `ValueError` if an unsupported memory action is specified
- Model initialization failures: Propagates errors from the underlying Vertex AI client library

The error messages are designed to be descriptive, helping developers quickly identify and resolve issues. For example, the credential validation provides clear guidance on how to properly configure authentication.

**Section sources**
- [vertexai.py](file://mem0/embeddings/vertexai.py#L28-L30)
- [vertexai.py](file://mem0/embeddings/vertexai.py#L46-L48)
- [test_vertexai_embeddings.py](file://tests/embeddings/test_vertexai_embeddings.py#L126-L135)

## Best Practices
Implementing Vertex AI embeddings effectively requires following several best practices to ensure security, performance, and maintainability.

### Securing Credentials
- Never hardcode service account keys in source code
- Use environment variables or secure secret management systems to store credentials
- Apply the principle of least privilege when creating service accounts
- Regularly rotate service account keys and monitor their usage
- Use application default credentials in production environments when possible

### Optimizing Request Batching
- Batch multiple embedding requests when processing large datasets
- Configure appropriate batch sizes based on your application's memory and performance requirements
- Implement connection pooling to reduce overhead for repeated requests
- Consider using asynchronous processing for high-volume applications
- Monitor API usage patterns and adjust batching strategies accordingly

### General Recommendations
- Cache frequently used embeddings to reduce API calls and improve response times
- Implement proper error handling and retry mechanisms for transient failures
- Monitor usage and costs through Google Cloud's monitoring tools
- Test with different models and configurations to find the optimal setup for your use case
- Document your configuration and deployment process for reproducibility

Following these best practices will help ensure a secure, efficient, and maintainable integration of Vertex AI embeddings in your applications.

**Section sources**
- [vertexai.py](file://mem0/embeddings/vertexai.py#L25-L27)
- [base.py](file://mem0/configs/embeddings/base.py#L30-L31)