# OpenAI Integration in Mem0

<cite>
**Referenced Files in This Document**
- [mem0/configs/llms/openai.py](file://mem0/configs/llms/openai.py)
- [mem0/llms/openai.py](file://mem0/llms/openai.py)
- [mem0/memory/telemetry.py](file://mem0/memory/telemetry.py)
- [mem0/exceptions.py](file://mem0/exceptions.py)
- [embedchain/notebooks/openai.ipynb](file://embedchain/notebooks/openai.ipynb)
- [embedchain/embedchain/llm/openai.py](file://embedchain/embedchain/llm/openai.py)
- [embedchain/embedchain/config/model_prices_and_context_window.json](file://embedchain/embedchain/config/model_prices_and_context_window.json)
- [embedchain/examples/rest-api/default.yaml](file://embedchain/examples/rest-api/default.yaml)
- [openmemory/api/config.json](file://openmemory/api/config.json)
- [openmemory/api/default_config.json](file://openmemory/api/default_config.json)
</cite>

## Table of Contents
1. [Introduction](#introduction)
2. [API Key Configuration](#api-key-configuration)
3. [Supported Models](#supported-models)
4. [Configuration Parameters](#configuration-parameters)
5. [Code Examples](#code-examples)
6. [Rate Limiting and Telemetry](#rate-limiting-and-telemetry)
7. [Error Handling](#error-handling)
8. [Performance Considerations](#performance-considerations)
9. [Cost Optimization](#cost-optimization)
10. [Official Documentation Links](#official-documentation-links)

## Introduction

Mem0 provides comprehensive OpenAI integration support through multiple pathways, enabling seamless interaction with OpenAI's language models and embedding services. The integration supports various OpenAI models including GPT-4, GPT-3.5 Turbo, and specialized models like GPT-4o and GPT-4o-mini, along with OpenAI's embedding models for vector operations.

The OpenAI integration in Mem0 is built around two primary components:
- **Language Model (LLM) Integration**: Handles text generation, chat completion, and structured output
- **Embedding Model Integration**: Manages text embedding creation for semantic search and similarity operations

## API Key Configuration

### Environment Variable Configuration

The simplest way to configure OpenAI API access is through environment variables:

```bash
# Primary environment variable
export OPENAI_API_KEY="your-api-key-here"

# Alternative environment variable (deprecated)
export OPENAI_API_BASE="https://api.openai.com/v1"  # Deprecated, use OPENAI_BASE_URL instead

# Current preferred environment variable
export OPENAI_BASE_URL="https://api.openai.com/v1"
```

### Direct Initialization

OpenAI API keys can also be configured directly during initialization:

```python
from mem0 import Memory

# Direct API key configuration
memory = Memory(
    config={
        "llm": {
            "provider": "openai",
            "config": {
                "api_key": "direct-api-key",
                "model": "gpt-4o-mini",
                "temperature": 0.1
            }
        }
    }
)
```

### Configuration Priority

The OpenAI integration follows this priority order for API key resolution:
1. **Direct configuration** in the LLM config
2. **Environment variable** `OPENAI_API_KEY`
3. **Fallback** to empty string (will cause authentication errors)

**Section sources**
- [mem0/llms/openai.py](file://mem0/llms/openai.py#L48-L49)
- [embedchain/embedchain/llm/openai.py](file://embedchain/embedchain/llm/openai.py#L61-L62)

## Supported Models

### GPT Language Models

Mem0 supports the full spectrum of OpenAI's GPT models:

| Model | Context Window | Input Cost/Token | Output Cost/Token | Max Tokens |
|-------|----------------|------------------|-------------------|------------|
| `gpt-4o-mini` | 128K | $0.00000015 | $0.00000060 | 4096 |
| `gpt-4o` | 128K | $0.000005 | $0.000015 | 4096 |
| `gpt-4-turbo` | 128K | $0.00001 | $0.00003 | 4096 |
| `gpt-4` | 8K | $0.00003 | $0.00006 | 4096 |
| `gpt-3.5-turbo` | 16K | $0.0000005 | $0.0000015 | 4096 |

### Embedding Models

| Model | Dimensions | Input Cost/Token | Output Cost/Token |
|-------|------------|------------------|-------------------|
| `text-embedding-3-small` | 1536 | $0.00000002 | $0.000000 |
| `text-embedding-3-large` | 3072 | $0.00000013 | $0.000000 |
| `text-embedding-ada-002` | 1536 | $0.0000001 | $0.000000 |

### Specialized Models

- **Reasoning Models**: `o1`, `o1-preview`, `o3-mini`, `o3`
- **Vision Models**: `gpt-4o`, `gpt-4-vision`
- **Legacy Models**: `gpt-4-0314`, `gpt-3.5-turbo-0301`

**Section sources**
- [embedchain/embedchain/config/model_prices_and_context_window.json](file://embedchain/embedchain/config/model_prices_and_context_window.json#L1-L824)

## Configuration Parameters

### Core Configuration Class

The `OpenAIConfig` class provides comprehensive configuration options:

```python
from mem0.configs.llms.openai import OpenAIConfig

config = OpenAIConfig(
    model="gpt-4o-mini",           # Model selection
    temperature=0.1,               # Creativity control (0.0-2.0)
    max_tokens=2000,               # Maximum response length
    top_p=0.1,                     # Nucleus sampling parameter
    top_k=1,                       # Top-k sampling parameter
    enable_vision=False,           # Vision capabilities
    vision_details="auto",         # Vision detail level
    api_key="your-key",            # API key (optional)
    openai_base_url=None,          # Custom base URL
    models=None,                   # OpenRouter model list
    route="fallback",              # OpenRouter routing
    store=False                    # Store conversation history
)
```

### Advanced Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| `temperature` | float | Controls randomness (0.0-2.0) | 0.1 |
| `max_tokens` | int | Maximum tokens to generate | 2000 |
| `top_p` | float | Nucleus sampling parameter (0.0-1.0) | 0.1 |
| `top_k` | int | Top-k sampling parameter | 1 |
| `enable_vision` | bool | Enable vision capabilities | False |
| `vision_details` | str | Vision detail level ("auto", "low", "high") | "auto" |
| `openai_base_url` | str | Custom OpenAI API endpoint | None |
| `models` | list | OpenRouter model selection | None |
| `route` | str | OpenRouter routing strategy | "fallback" |
| `store` | bool | Store conversation history | False |

**Section sources**
- [mem0/configs/llms/openai.py](file://mem0/configs/llms/openai.py#L12-L80)

## Code Examples

### Basic OpenAI LLM Initialization

```python
from mem0 import Memory

# Simple initialization with default settings
memory = Memory()

# Custom configuration
memory = Memory(
    config={
        "llm": {
            "provider": "openai",
            "config": {
                "model": "gpt-4o-mini",
                "temperature": 0.5,
                "max_tokens": 1000,
                "top_p": 0.9
            }
        }
    }
)
```

### Advanced Configuration with Custom Parameters

```python
from mem0.configs.llms.openai import OpenAIConfig

# Create advanced configuration
config = OpenAIConfig(
    model="gpt-4o",
    temperature=0.3,
    max_tokens=1500,
    top_p=0.8,
    top_k=5,
    enable_vision=True,
    vision_details="high",
    store=True,
    response_callback=lambda llm, response, params: print("Response received")
)

# Initialize with custom config
memory = Memory(config={"llm": {"provider": "openai", "config": config}})
```

### YAML Configuration Examples

#### REST API Configuration
```yaml
llm:
  provider: openai
  config:
    model: 'gpt-4o-mini'
    temperature: 0.1
    max_tokens: 2000
    top_p: 0.9
    stream: false
```

#### OpenMemory Configuration
```json
{
    "mem0": {
        "llm": {
            "provider": "openai",
            "config": {
                "model": "gpt-4o-mini",
                "temperature": 0.1,
                "max_tokens": 2000,
                "api_key": "env:OPENAI_API_KEY"
            }
        }
    }
}
```

### Notebook Example

The embedchain notebook demonstrates practical usage:

```python
from embedchain import App

# Complete configuration example
app = App.from_config(config={
    "llm": {
        "provider": "openai",
        "config": {
            "model": "gpt-4o-mini",
            "temperature": 0.5,
            "max_tokens": 1000,
            "top_p": 1,
            "stream": False
        }
    },
    "embedder": {
        "provider": "openai",
        "config": {
            "model": "text-embedding-ada-002"
        }
    }
})
```

**Section sources**
- [embedchain/notebooks/openai.ipynb](file://embedchain/notebooks/openai.ipynb#L79-L96)
- [openmemory/api/config.json](file://openmemory/api/config.json#L1-L20)

## Rate Limiting and Telemetry

### Token Usage Tracking

Mem0 automatically tracks token usage and costs for OpenAI models:

```python
# Token usage is automatically tracked and included in responses
response, token_info = memory.add("Your query here")

print(f"Prompt tokens: {token_info['prompt_tokens']}")
print(f"Completion tokens: {token_info['completion_tokens']}")
print(f"Total tokens: {token_info['total_tokens']}")
print(f"Total cost: ${token_info['total_cost']}")
print(f"Cost currency: {token_info['cost_currency']}")
```

### Telemetry Implementation

The telemetry system captures anonymous usage data:

```python
# Telemetry is enabled by default
# To disable telemetry:
import os
os.environ["MEM0_TELEMETRY"] = "False"

# Telemetry captures:
# - Model usage statistics
# - Request patterns
# - Performance metrics
# - Error rates
```

### Rate Limit Handling

OpenAI's rate limiting is handled transparently:

```python
try:
    response = memory.query("Your question here")
except Exception as e:
    if "rate limit" in str(e).lower():
        # Handle rate limit exceeded
        print("Rate limit exceeded, please wait before retrying")
    elif "authentication" in str(e).lower():
        # Handle authentication failure
        print("Invalid API key or authentication failed")
    else:
        # Handle other errors
        print(f"Error: {e}")
```

**Section sources**
- [embedchain/embedchain/llm/openai.py](file://embedchain/embedchain/llm/openai.py#L34-L46)
- [mem0/memory/telemetry.py](file://mem0/memory/telemetry.py#L1-L91)

## Error Handling

### Common Error Types

Mem0 provides comprehensive error handling for OpenAI integration:

#### Authentication Errors
```python
from mem0.exceptions import AuthenticationError

try:
    memory = Memory(config={"llm": {"provider": "openai"}})
except AuthenticationError as e:
    print(f"Authentication failed: {e.message}")
    print(f"Suggested action: {e.suggestion}")
```

#### Rate Limit Exceeded
```python
from mem0.exceptions import RateLimitError

try:
    response = memory.query("Your question here")
except RateLimitError as e:
    print(f"Rate limit exceeded: {e.message}")
    print(f"Retry after: {e.debug_info.get('retry_after')} seconds")
```

#### Model Not Found
```python
from mem0.exceptions import ModelNotFoundError

try:
    memory = Memory(
        config={
            "llm": {
                "provider": "openai",
                "config": {"model": "non-existent-model"}
            }
        }
    )
except ModelNotFoundError as e:
    print(f"Model not found: {e.message}")
    print(f"Available models: {e.details.get('available_models')}")
```

### Error Recovery Strategies

```python
import time
from mem0.exceptions import RateLimitError, AuthenticationError

def safe_query(memory, query, max_retries=3):
    for attempt in range(max_retries):
        try:
            return memory.query(query)
        except RateLimitError as e:
            if attempt == max_retries - 1:
                raise
            wait_time = 2 ** attempt  # Exponential backoff
            print(f"Rate limited, waiting {wait_time} seconds...")
            time.sleep(wait_time)
        except AuthenticationError:
            raise  # Cannot recover from auth errors
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            if attempt == max_retries - 1:
                raise
            time.sleep(1)
```

### Error Response Monitoring

OpenAI integration supports response callbacks for monitoring:

```python
def monitor_response(llm, response, params):
    print(f"Generated {len(response.choices)} choices")
    print(f"Model: {params.get('model')}")
    print(f"Temperature: {params.get('temperature')}")
    print(f"Max tokens: {params.get('max_tokens')}")

config = OpenAIConfig(
    model="gpt-4o-mini",
    response_callback=monitor_response
)
```

**Section sources**
- [mem0/exceptions.py](file://mem0/exceptions.py#L64-L503)
- [mem0/llms/openai.py](file://mem0/llms/openai.py#L140-L146)

## Performance Considerations

### Model Selection Guidelines

#### For Fast Responses
- **Use**: `gpt-4o-mini` or `gpt-3.5-turbo`
- **Characteristics**: Lower latency, cost-effective
- **Best for**: Simple queries, real-time applications

#### For High Quality
- **Use**: `gpt-4o` or `gpt-4-turbo`
- **Characteristics**: Better reasoning, higher quality
- **Best for**: Complex tasks, critical decisions

#### For Vision Tasks
- **Use**: `gpt-4o` with `enable_vision=True`
- **Characteristics**: Image understanding capabilities
- **Best for**: Image analysis, visual content processing

### Temperature Settings

| Temperature Range | Use Case | Characteristics |
|------------------|----------|-----------------|
| 0.0 - 0.3 | Factual, deterministic | Consistent, predictable |
| 0.4 - 0.7 | Balanced creativity | Good mix of creativity and accuracy |
| 0.8 - 1.0 | Creative, exploratory | More varied, creative responses |

### Token Management

```python
# Optimize token usage
memory = Memory(
    config={
        "llm": {
            "provider": "openai",
            "config": {
                "max_tokens": 500,  # Limit response length
                "temperature": 0.1,  # Reduce randomness
                "top_p": 0.9  # Focus on likely tokens
            }
        }
    }
)
```

### Streaming vs Non-Streaming

```python
# Streaming for real-time feedback
memory_streaming = Memory(
    config={
        "llm": {
            "provider": "openai",
            "config": {
                "stream": True,
                "max_tokens": 1000
            }
        }
    }
)

# Non-streaming for batch processing
memory_batch = Memory(
    config={
        "llm": {
            "provider": "openai",
            "config": {
                "stream": False,
                "max_tokens": 2000
            }
        }
    }
)
```

**Section sources**
- [mem0/llms/base.py](file://mem0/llms/base.py#L39-L79)

## Cost Optimization

### Pricing Comparison

Based on current OpenAI pricing:

| Model | Input ($/1M tokens) | Output ($/1M tokens) | Best For |
|-------|-------------------|-------------------|----------|
| `gpt-4o-mini` | $0.00000015 | $0.00000060 | General tasks |
| `gpt-3.5-turbo` | $0.0000005 | $0.0000015 | Budget-friendly |
| `gpt-4o` | $0.000005 | $0.000015 | High-quality tasks |
| `text-embedding-3-small` | $0.00000002 | $0.000000 | Embeddings |

### Cost Optimization Strategies

#### 1. Model Selection Based on Task Complexity
```python
# Simple tasks - use cheaper models
simple_tasks = [
    "gpt-3.5-turbo",  # Cheapest option
    "gpt-4o-mini"     # Good balance
]

# Complex tasks - use higher quality models
complex_tasks = [
    "gpt-4o",         # Best quality
    "gpt-4-turbo"     # High quality
]
```

#### 2. Token Optimization
```python
# Use smaller context windows when possible
memory_optimized = Memory(
    config={
        "llm": {
            "provider": "openai",
            "config": {
                "max_tokens": 500,  # Reduce response length
                "temperature": 0.2, # Reduce randomness
                "top_p": 0.8        # Focus on likely tokens
            }
        }
    }
)
```

#### 3. Caching Strategies
```python
# Implement caching for repeated queries
from functools import lru_cache

@lru_cache(maxsize=100)
def cached_query(memory, query_hash):
    return memory.query(query_hash)

# Calculate hash for caching
import hashlib
def get_query_hash(query):
    return hashlib.md5(query.encode()).hexdigest()
```

#### 4. Batch Processing
```python
# Process multiple queries efficiently
def process_queries_efficiently(memory, queries):
    results = []
    for query in queries:
        # Use smaller max_tokens for batch processing
        result = memory.query(query, max_tokens=200)
        results.append(result)
    return results
```

### Cost Monitoring

```python
# Track costs programmatically
def track_costs(memory, queries):
    total_input_tokens = 0
    total_output_tokens = 0
    total_cost = 0
    
    for query in queries:
        response = memory.query(query)
        
        # Extract token information
        if hasattr(response, 'token_info'):
            token_info = response.token_info
            total_input_tokens += token_info.get('prompt_tokens', 0)
            total_output_tokens += token_info.get('completion_tokens', 0)
            total_cost += token_info.get('total_cost', 0)
    
    print(f"Total input tokens: {total_input_tokens}")
    print(f"Total output tokens: {total_output_tokens}")
    print(f"Estimated total cost: ${total_cost:.6f}")
```

**Section sources**
- [embedchain/embedchain/config/model_prices_and_context_window.json](file://embedchain/embedchain/config/model_prices_and_context_window.json#L1-L824)

## Official Documentation Links

### OpenAI Official Resources

- **API Documentation**: [https://platform.openai.com/docs/api-reference](https://platform.openai.com/docs/api-reference)
- **Pricing Information**: [https://openai.com/pricing](https://openai.com/pricing)
- **Model Specifications**: [https://platform.openai.com/docs/models](https://platform.openai.com/docs/models)
- **Authentication Guide**: [https://platform.openai.com/docs/api-reference/authentication](https://platform.openai.com/docs/api-reference/authentication)

### Mem0 Documentation

- **Mem0 GitHub Repository**: [https://github.com/mem0ai/mem0](https://github.com/mem0ai/mem0)
- **Embedchain Documentation**: [https://docs.embedchain.ai](https://docs.embedchain.ai)
- **OpenAI Integration Examples**: [https://github.com/mem0ai/mem0/tree/main/embedchain/notebooks](https://github.com/mem0ai/mem0/tree/main/embedchain/notebooks)

### Related Tools and Libraries

- **OpenAI Python Library**: [https://github.com/openai/openai-python](https://github.com/openai/openai-python)
- **LangChain Integration**: [https://python.langchain.com](https://python.langchain.com)
- **Hugging Face Transformers**: [https://huggingface.co/docs/transformers](https://huggingface.co/docs/transformers)