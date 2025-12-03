# Embedding Models

<cite>
**Referenced Files in This Document**   
- [openai.py](file://mem0/embeddings/openai.py)
- [huggingface.py](file://mem0/embeddings/huggingface.py)
- [vertexai.py](file://mem0/embeddings/vertexai.py)
- [aws_bedrock.py](file://mem0/embeddings/aws_bedrock.py)
- [azure_openai.py](file://mem0/embeddings/azure_openai.py)
- [gemini.py](file://mem0/embeddings/gemini.py)
- [together.py](file://mem0/embeddings/together.py)
- [ollama.py](file://mem0/embeddings/ollama.py)
- [github_copilot.py](file://mem0/embeddings/github_copilot.py)
- [lmstudio.py](file://mem0/embeddings/lmstudio.py)
- [langchain.py](file://mem0/embeddings/langchain.py)
- [base.py](file://mem0/configs/embeddings/base.py)
</cite>

## Table of Contents
1. [Introduction](#introduction)
2. [Supported Embedding Providers](#supported-embedding-providers)
3. [Configuration Options](#configuration-options)
4. [Dimension Settings](#dimension-settings)
5. [Authentication Methods](#authentication-methods)
6. [Performance Benchmarks](#performance-benchmarks)
7. [Python Examples](#python-examples)
8. [Trade-offs Analysis](#trade-offs-analysis)
9. [Common Issues](#common-issues)
10. [Selection Guidance](#selection-guidance)

## Introduction
This document provides comprehensive documentation for all supported embedding models in Mem0, covering providers including OpenAI, Hugging Face, Vertex AI, AWS Bedrock, Azure OpenAI, Gemini, Together AI, Ollama, GitHub Copilot, LM Studio, and LangChain. The documentation details configuration options, dimension settings, authentication methods, and performance characteristics for each model. It also includes guidance on selecting optimal embedding models based on vector database compatibility and use case requirements.

## Supported Embedding Providers
Mem0 supports multiple embedding providers, each with specific implementation classes and configuration requirements. The supported providers include OpenAI, Hugging Face, Vertex AI, AWS Bedrock, Azure OpenAI, Gemini, Together AI, Ollama, GitHub Copilot, LM Studio, and LangChain. Each provider has a dedicated implementation class that inherits from the base EmbeddingBase class and implements the embed method for generating embeddings.

**Section sources**
- [openai.py](file://mem0/embeddings/openai.py#L11-L50)
- [huggingface.py](file://mem0/embeddings/huggingface.py#L15-L42)
- [vertexai.py](file://mem0/embeddings/vertexai.py#L10-L55)
- [aws_bedrock.py](file://mem0/embeddings/aws_bedrock.py#L16-L101)
- [azure_openai.py](file://mem0/embeddings/azure_openai.py#L13-L56)
- [gemini.py](file://mem0/embeddings/gemini.py#L11-L40)
- [together.py](file://mem0/embeddings/together.py#L10-L32)
- [ollama.py](file://mem0/embeddings/ollama.py#L24-L54)
- [github_copilot.py](file://mem0/embeddings/github_copilot.py#L13-L61)
- [lmstudio.py](file://mem0/embeddings/lmstudio.py#L9-L30)
- [langchain.py](file://mem0/embeddings/langchain.py#L12-L36)

## Configuration Options
Each embedding provider in Mem0 supports various configuration options that can be set through the BaseEmbedderConfig class. These options include model selection, API endpoints, authentication credentials, and provider-specific parameters. The configuration system allows for both direct configuration and environment variable-based setup.

```mermaid
classDiagram
class BaseEmbedderConfig {
+model : str
+api_key : str
+embedding_dims : int
+ollama_base_url : str
+openai_base_url : str
+model_kwargs : dict
+huggingface_base_url : str
+azure_kwargs : AzureConfig
+http_client_proxies : Union[Dict, str]
+vertex_credentials_json : str
+memory_add_embedding_type : str
+memory_update_embedding_type : str
+memory_search_embedding_type : str
+output_dimensionality : str
+lmstudio_base_url : str
+aws_access_key_id : str
+aws_secret_access_key : str
+aws_region : str
}
class EmbeddingBase {
+config : BaseEmbedderConfig
+__init__(config : BaseEmbedderConfig)
+embed(text : str, memory_action : Literal["add", "search", "update"])
}
BaseEmbedderConfig <|-- OpenAIEmbedding
BaseEmbedderConfig <|-- HuggingFaceEmbedding
BaseEmbedderConfig <|-- VertexAIEmbedding
BaseEmbedderConfig <|-- AWSBedrockEmbedding
BaseEmbedderConfig <|-- AzureOpenAIEmbedding
BaseEmbedderConfig <|-- GoogleGenAIEmbedding
BaseEmbedderConfig <|-- TogetherEmbedding
BaseEmbedderConfig <|-- OllamaEmbedding
BaseEmbedderConfig <|-- GitHubCopilotEmbedding
BaseEmbedderConfig <|-- LMStudioEmbedding
BaseEmbedderConfig <|-- LangchainEmbedding
```

**Diagram sources**
- [base.py](file://mem0/configs/embeddings/base.py#L10-L111)
- [openai.py](file://mem0/embeddings/openai.py#L11-L50)

**Section sources**
- [base.py](file://mem0/configs/embeddings/base.py#L10-L111)
- [openai.py](file://mem0/embeddings/openai.py#L11-L50)

## Dimension Settings
Mem0 supports configurable embedding dimensions for each provider, allowing users to optimize for their specific use cases. The default dimensions vary by provider, with options to override these defaults through configuration. Dimension settings are critical for ensuring compatibility with vector databases and maintaining performance characteristics.

```mermaid
flowchart TD
Start([Configuration]) --> ModelSelection["Select Embedding Model"]
ModelSelection --> DefaultDims["Use Provider Default Dimensions"]
DefaultDims --> OpenAI{"OpenAI: 1536"}
DefaultDims --> HuggingFace{"HuggingFace: Model-specific"}
DefaultDims --> VertexAI{"VertexAI: 256"}
DefaultDims --> AWSBedrock{"AWS Bedrock: Model-specific"}
DefaultDims --> AzureOpenAI{"Azure OpenAI: Model-specific"}
DefaultDims --> Gemini{"Gemini: 768"}
DefaultDims --> Together{"Together: 768"}
DefaultDims --> Ollama{"Ollama: 512"}
DefaultDims --> GitHubCopilot{"GitHub Copilot: 1536"}
DefaultDims --> LMStudio{"LM Studio: 1536"}
DefaultDims --> LangChain{"LangChain: Model-specific"}
ModelSelection --> CustomDims["Override with Custom Dimensions"]
CustomDims --> SetDims["Set embedding_dims parameter"]
SetDims --> Validation["Validate dimension compatibility"]
Validation --> Complete["Configuration Complete"]
OpenAI --> Complete
HuggingFace --> Complete
VertexAI --> Complete
AWSBedrock --> Complete
AzureOpenAI --> Complete
Gemini --> Complete
Together --> Complete
Ollama --> Complete
GitHubCopilot --> Complete
LMStudio --> Complete
LangChain --> Complete
```

**Diagram sources**
- [openai.py](file://mem0/embeddings/openai.py#L16)
- [vertexai.py](file://mem0/embeddings/vertexai.py#L15)
- [gemini.py](file://mem0/embeddings/gemini.py#L16)
- [together.py](file://mem0/embeddings/together.py#L17)
- [ollama.py](file://mem0/embeddings/ollama.py#L29)
- [github_copilot.py](file://mem0/embeddings/github_copilot.py#L18)
- [lmstudio.py](file://mem0/embeddings/lmstudio.py#L14)

**Section sources**
- [openai.py](file://mem0/embeddings/openai.py#L16)
- [vertexai.py](file://mem0/embeddings/vertexai.py#L15)
- [gemini.py](file://mem0/embeddings/gemini.py#L16)
- [together.py](file://mem0/embeddings/together.py#L17)
- [ollama.py](file://mem0/embeddings/ollama.py#L29)
- [github_copilot.py](file://mem0/embeddings/github_copilot.py#L18)
- [lmstudio.py](file://mem0/embeddings/lmstudio.py#L14)

## Authentication Methods
Mem0 supports various authentication methods for different embedding providers, including API keys, OAuth2, and service account credentials. The authentication system is designed to be flexible, allowing for both direct configuration and environment variable-based authentication.

```mermaid
sequenceDiagram
participant User as "Application"
participant Mem0 as "Mem0 Framework"
participant Provider as "Embedding Provider"
User->>Mem0 : Initialize Embedding Model
Mem0->>Mem0 : Check Configuration
alt API Key Authentication
Mem0->>Mem0 : Use config.api_key if provided
Mem0->>Mem0 : Fallback to environment variables
Mem0->>Provider : Include API key in request
else OAuth2 Authentication
Mem0->>Mem0 : Use OAuth2 flow (GitHub Copilot)
Mem0->>Provider : Include OAuth2 token
else Service Account
Mem0->>Mem0 : Load credentials from file (Vertex AI)
Mem0->>Mem0 : Set GOOGLE_APPLICATION_CREDENTIALS
Mem0->>Provider : Authenticate with service account
end
Provider-->>Mem0 : Return embedding
Mem0-->>User : Return embedding vector
Note over Mem0,Provider : Authentication method depends on provider
```

**Diagram sources**
- [openai.py](file://mem0/embeddings/openai.py#L18)
- [azure_openai.py](file://mem0/embeddings/azure_openai.py#L17-L33)
- [vertexai.py](file://mem0/embeddings/vertexai.py#L23-L30)
- [github_copilot.py](file://mem0/embeddings/github_copilot.py#L20)
- [aws_bedrock.py](file://mem0/embeddings/aws_bedrock.py#L28-L37)

**Section sources**
- [openai.py](file://mem0/embeddings/openai.py#L18)
- [azure_openai.py](file://mem0/embeddings/azure_openai.py#L17-L33)
- [vertexai.py](file://mem0/embeddings/vertexai.py#L23-L30)
- [github_copilot.py](file://mem0/embeddings/github_copilot.py#L20)
- [aws_bedrock.py](file://mem0/embeddings/aws_bedrock.py#L28-L37)

## Performance Benchmarks
Performance characteristics vary significantly across embedding providers, with trade-offs between latency, cost, and quality. Local models like Ollama and LM Studio offer low latency but may have lower quality, while cloud-based providers like OpenAI and Gemini offer high quality at higher costs. The benchmarks consider factors such as embedding generation time, throughput, and resource utilization.

```mermaid
graph TD
A[Performance Factors] --> B[Latency]
A --> C[Cost]
A --> D[Quality]
A --> E[Throughput]
B --> F[Local Models: Low Latency]
B --> G[Cloud Models: Higher Latency]
C --> H[Local Models: Low Cost]
C --> I[Cloud Models: Usage-based Cost]
D --> J[Cloud Models: High Quality]
D --> K[Local Models: Variable Quality]
E --> L[Local Models: Limited Throughput]
E --> M[Cloud Models: Scalable Throughput]
N[Provider Comparison] --> O[OpenAI: High Quality, Medium Cost]
N --> P[Hugging Face: Variable Quality, Low Cost]
N --> Q[Vertex AI: High Quality, Medium Cost]
N --> R[AWS Bedrock: High Quality, Medium Cost]
N --> S[Azure OpenAI: High Quality, Medium Cost]
N --> T[Gemini: High Quality, Medium Cost]
N --> U[Together AI: Medium Quality, Low Cost]
N --> V[Ollama: Medium Quality, Low Cost]
N --> W[GitHub Copilot: High Quality, Medium Cost]
N --> X[LM Studio: Medium Quality, Low Cost]
N --> Y[LangChain: Depends on Model]
```

**Diagram sources**
- [openai.py](file://mem0/embeddings/openai.py)
- [huggingface.py](file://mem0/embeddings/huggingface.py)
- [vertexai.py](file://mem0/embeddings/vertexai.py)
- [aws_bedrock.py](file://mem0/embeddings/aws_bedrock.py)
- [azure_openai.py](file://mem0/embeddings/azure_openai.py)
- [gemini.py](file://mem0/embeddings/gemini.py)
- [together.py](file://mem0/embeddings/together.py)
- [ollama.py](file://mem0/embeddings/ollama.py)
- [github_copilot.py](file://mem0/embeddings/github_copilot.py)
- [lmstudio.py](file://mem0/embeddings/lmstudio.py)
- [langchain.py](file://mem0/embeddings/langchain.py)

## Python Examples
The following examples demonstrate how to initialize and use each embedding model with both direct configuration and environment variables.

```mermaid
flowchart TD
A[Initialize Embedding Model] --> B{Configuration Method}
B --> C[Direct Configuration]
B --> D[Environment Variables]
C --> E[Create BaseEmbedderConfig]
E --> F[Set provider-specific parameters]
F --> G[Initialize embedding class]
D --> H[Set environment variables]
H --> I[Initialize embedding class without config]
G --> J[Generate Embeddings]
I --> J
J --> K[Process embedding vector]
K --> L[Use in application]
```

**Diagram sources**
- [base.py](file://mem0/configs/embeddings/base.py)
- [openai.py](file://mem0/embeddings/openai.py)

**Section sources**
- [openai.py](file://mem0/embeddings/openai.py)
- [huggingface.py](file://mem0/embeddings/huggingface.py)
- [vertexai.py](file://mem0/embeddings/vertexai.py)
- [aws_bedrock.py](file://mem0/embeddings/aws_bedrock.py)
- [azure_openai.py](file://mem0/embeddings/azure_openai.py)
- [gemini.py](file://mem0/embeddings/gemini.py)
- [together.py](file://mem0/embeddings/together.py)
- [ollama.py](file://mem0/embeddings/ollama.py)
- [github_copilot.py](file://mem0/embeddings/github_copilot.py)
- [lmstudio.py](file://mem0/embeddings/lmstudio.py)
- [langchain.py](file://mem0/embeddings/langchain.py)

## Trade-offs Analysis
When selecting an embedding model, users must consider the trade-offs between embedding quality, latency, and cost. High-quality embeddings from providers like OpenAI and Gemini typically come with higher costs and potential latency, while local models like Ollama and LM Studio offer faster response times at the expense of potentially lower quality. The choice depends on the specific use case requirements and constraints.

```mermaid
graph TD
A[Use Case Requirements] --> B[Quality-Critical Applications]
A --> C[Latency-Sensitive Applications]
A --> D[Cost-Constrained Applications]
B --> E[Cloud Providers: OpenAI, Gemini, Vertex AI]
C --> F[Local Providers: Ollama, LM Studio]
D --> G[Open Source: Hugging Face, Together AI]
H[Quality Factors] --> I[Semantic Accuracy]
H --> J[Context Preservation]
H --> K[Vocabulary Coverage]
L[Latency Factors] --> M[Network Round Trips]
L --> N[Model Size]
L --> O[Hardware Constraints]
P[Cost Factors] --> Q[API Usage Fees]
P --> R[Infrastructure Costs]
P --> S[Development Time]
```

**Diagram sources**
- [openai.py](file://mem0/embeddings/openai.py)
- [ollama.py](file://mem0/embeddings/ollama.py)
- [lmstudio.py](file://mem0/embeddings/lmstudio.py)
- [huggingface.py](file://mem0/embeddings/huggingface.py)
- [together.py](file://mem0/embeddings/together.py)

## Common Issues
Common issues when working with embedding models include dimension mismatches, API key errors, and model deprecation. Dimension mismatches occur when the embedding dimensions don't match between the embedding model and vector database. API key errors happen when authentication credentials are missing or invalid. Model deprecation occurs when providers discontinue support for specific models.

```mermaid
flowchart TD
A[Common Issues] --> B[Dimension Mismatches]
A --> C[API Key Errors]
A --> D[Model Deprecation]
A --> E[Network Connectivity]
A --> F[Rate Limiting]
B --> G[Check embedding_dims configuration]
B --> H[Ensure vector database compatibility]
C --> I[Verify API key is set]
C --> J[Check environment variables]
C --> K[Validate credential format]
D --> L[Monitor provider deprecation notices]
D --> M[Update to recommended models]
E --> N[Check network connectivity]
E --> O[Verify API endpoints]
F --> P[Implement retry logic]
P --> Q[Add rate limiting handling]
```

**Diagram sources**
- [base.py](file://mem0/configs/embeddings/base.py)
- [openai.py](file://mem0/embeddings/openai.py)
- [azure_openai.py](file://mem0/embeddings/azure_openai.py)
- [vertexai.py](file://mem0/embeddings/vertexai.py)

**Section sources**
- [base.py](file://mem0/configs/embeddings/base.py)
- [openai.py](file://mem0/embeddings/openai.py)
- [azure_openai.py](file://mem0/embeddings/azure_openai.py)
- [vertexai.py](file://mem0/embeddings/vertexai.py)

## Selection Guidance
Selecting the optimal embedding model depends on vector database compatibility and use case requirements. For high-accuracy applications like semantic search and recommendation systems, cloud-based providers like OpenAI and Gemini are recommended. For privacy-sensitive applications, local models like Ollama and LM Studio are preferable. The guidance considers factors such as data sensitivity, performance requirements, and budget constraints.

```mermaid
graph TD
A[Selection Criteria] --> B[Data Sensitivity]
A --> C[Performance Requirements]
A --> D[Budget Constraints]
A --> E[Vector Database Compatibility]
B --> F[High Sensitivity: Local Models]
B --> G[Low Sensitivity: Cloud Models]
C --> H[Low Latency Required: Local Models]
C --> I[High Quality Required: Cloud Models]
D --> J[Low Budget: Open Source Models]
D --> K[Higher Budget: Premium Models]
E --> L[Check dimension compatibility]
E --> M[Verify distance metrics]
N[Decision Process] --> O[Assess requirements]
O --> P[Evaluate options]
P --> Q[Test performance]
Q --> R[Select optimal model]
```

**Diagram sources**
- [base.py](file://mem0/configs/embeddings/base.py)
- [openai.py](file://mem0/embeddings/openai.py)
- [ollama.py](file://mem0/embeddings/ollama.py)
- [huggingface.py](file://mem0/embeddings/huggingface.py)

**Section sources**
- [base.py](file://mem0/configs/embeddings/base.py)
- [openai.py](file://mem0/embeddings/openai.py)
- [ollama.py](file://mem0/embeddings/ollama.py)
- [huggingface.py](file://mem0/embeddings/huggingface.py)