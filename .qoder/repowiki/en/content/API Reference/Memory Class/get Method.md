# get Method API Documentation

<cite>
**Referenced Files in This Document**
- [mem0/memory/main.py](file://mem0/memory/main.py)
- [mem0/memory/base.py](file://mem0/memory/base.py)
- [mem0-ts/src/oss/src/memory/index.ts](file://mem0-ts/src/oss/src/memory/index.ts)
- [mem0/configs/base.py](file://mem0/configs/base.py)
- [mem0-ts/src/oss/src/vector_stores/base.ts](file://mem0-ts/src/oss/src/vector_stores/base.ts)
- [mem0/vector_stores/chroma.py](file://mem0/vector_stores/chroma.py)
- [tests/test_main.py](file://tests/test_main.py)
</cite>

## Table of Contents
1. [Introduction](#introduction)
2. [Method Signature and Purpose](#method-signature-and-purpose)
3. [Parameter Details](#parameter-details)
4. [Return Structure](#return-structure)
5. [Internal Processing Workflow](#internal-processing-workflow)
6. [Promoted Payload Keys](#promoted-payload-keys)
7. [Vector Store Integration](#vector-store-integration)
8. [Error Handling and Edge Cases](#error-handling-and-edge-cases)
9. [Performance Considerations](#performance-considerations)
10. [Usage Examples](#usage-examples)
11. [Common Issues and Troubleshooting](#common-issues-and-troubleshooting)
12. [Best Practices](#best-practices)

## Introduction

The `get()` method is a core API endpoint in the Mem0 memory system that retrieves a specific memory record by its unique identifier. This method serves as the primary mechanism for accessing individual memory entries within the vector store, enabling precise retrieval of stored information while maintaining the hierarchical structure of memory metadata.

The method operates as part of the Memory class, which provides a unified interface for memory operations across different vector store implementations. It follows a consistent pattern of vector store lookup, payload parsing, and structured response formatting to ensure reliable and predictable behavior.

## Method Signature and Purpose

The `get()` method is defined in the Memory class and inherits from the MemoryBase abstract class. Its primary purpose is to retrieve a specific memory record by its ID, providing access to stored information with appropriate metadata promotion and structured formatting.

### Python Implementation

```python
def get(self, memory_id):
    """
    Retrieve a memory by ID.

    Args:
        memory_id (str): ID of the memory to retrieve.

    Returns:
        dict: Retrieved memory.
    """
```

### TypeScript Implementation

```typescript
async get(memoryId: string): Promise<MemoryItem | null>
```

**Section sources**
- [mem0/memory/main.py](file://mem0/memory/main.py#L494-L535)
- [mem0-ts/src/oss/src/memory/index.ts](file://mem0-ts/src/oss/src/memory/index.ts#L377-L412)

## Parameter Details

### memory_id (Required)

The `memory_id` parameter is the unique identifier of the memory record to be retrieved. This parameter accepts string values representing UUID-formatted identifiers.

#### Valid UUID Formats

The method expects UUID-formatted strings in the standard hexadecimal format. Valid examples include:

- **Standard UUID format**: `"550e8400-e29b-41d4-a716-446655440000"`
- **Shortened UUID format**: `"12345678-abcd-ef01-2345-6789abcdef01"`
- **Minimal UUID format**: `"00000000-0000-0000-0000-000000000000"`

#### Parameter Validation

While the method does not perform explicit UUID validation internally, it relies on the underlying vector store implementation to handle ID format validation. Invalid or malformed UUIDs will typically result in a "not found" condition.

**Section sources**
- [mem0/memory/main.py](file://mem0/memory/main.py#L498-L499)
- [tests/test_main.py](file://tests/test_main.py#L98-L121)

## Return Structure

The `get()` method returns a structured dictionary containing the memory record with core fields, promoted payload keys, and additional metadata. The return structure varies slightly between Python and TypeScript implementations but maintains consistent semantics.

### Core Fields

The returned object contains fundamental memory properties:

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique identifier of the memory record |
| `memory` | string | The deduced memory content extracted from the text data |
| `hash` | string \| null | MD5 hash of the memory content for integrity verification |
| `created_at` | string \| null | ISO 8601 timestamp of memory creation |
| `updated_at` | string \| null | ISO 8601 timestamp of last modification |

### Promoted Payload Keys

Certain payload fields are elevated to top-level properties for convenient access:

| Field | Type | Description |
|-------|------|-------------|
| `user_id` | string \| null | Identifier of the user associated with the memory |
| `agent_id` | string \| null | Identifier of the agent associated with the memory |
| `run_id` | string \| null | Identifier of the run/session associated with the memory |
| `actor_id` | string \| null | Identifier of the actor/entity involved |
| `role` | string \| null | Role of the entity in the memory context |

### Additional Metadata

All remaining payload fields are organized under the `metadata` property as a dictionary:

```python
{
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "memory": "User mentioned liking coffee in the morning",
    "hash": "abc123def456...",
    "created_at": "2023-01-01T00:00:00Z",
    "updated_at": "2023-01-02T00:00:00Z",
    "user_id": "user_123",
    "agent_id": "agent_456",
    "metadata": {
        "confidence_score": 0.95,
        "source": "conversation",
        "tags": ["morning", "coffee"],
        "priority": "high"
    }
}
```

### Return Types

- **Python**: Returns a dictionary or `None` if the memory is not found
- **TypeScript**: Returns a `MemoryItem` object or `null` if not found

**Section sources**
- [mem0/configs/base.py](file://mem0/configs/base.py#L15-L25)
- [mem0-ts/src/oss/src/types/index.ts](file://mem0-ts/src/oss/src/types/index.ts#L83-L91)

## Internal Processing Workflow

The `get()` method follows a structured workflow that ensures reliable memory retrieval across different vector store implementations.

```mermaid
flowchart TD
Start([get() Called]) --> ValidateInput["Validate memory_id Parameter"]
ValidateInput --> CallVectorStore["Call vector_store.get(vector_id)"]
CallVectorStore --> CheckResult{"Memory Found?"}
CheckResult --> |No| ReturnNone["Return None"]
CheckResult --> |Yes| ExtractCore["Extract Core Fields<br/>(id, memory, hash, timestamps)"]
ExtractCore --> PromoteKeys["Promote Payload Keys<br/>(user_id, agent_id, etc.)"]
PromoteKeys --> FilterMetadata["Filter Additional Metadata"]
FilterMetadata --> BuildResponse["Build Structured Response"]
BuildResponse --> ReturnResult["Return MemoryItem"]
ReturnNone --> End([End])
ReturnResult --> End
```

**Diagram sources**
- [mem0/memory/main.py](file://mem0/memory/main.py#L494-L535)
- [mem0-ts/src/oss/src/memory/index.ts](file://mem0-ts/src/oss/src/memory/index.ts#L377-L412)

### Step-by-Step Process

1. **Parameter Validation**: The method receives the `memory_id` parameter and passes it to the vector store
2. **Vector Store Lookup**: The underlying vector store performs the actual memory retrieval
3. **Result Processing**: The method extracts core fields from the vector store response
4. **Payload Parsing**: Promoted keys are extracted from the payload and elevated to top-level properties
5. **Metadata Filtering**: Remaining payload fields are filtered and organized under the `metadata` property
6. **Response Formatting**: The method constructs a standardized response object
7. **Return Value**: The formatted memory object is returned to the caller

**Section sources**
- [mem0/memory/main.py](file://mem0/memory/main.py#L504-L535)
- [mem0-ts/src/oss/src/memory/index.ts](file://mem0-ts/src/oss/src/memory/index.ts#L377-L412)

## Promoted Payload Keys

The `get()` method automatically promotes specific payload fields to top-level properties for improved accessibility and convenience. These promoted keys represent commonly accessed metadata that benefits from direct property access.

### Standard Promoted Keys

The following payload fields are consistently promoted across all vector store implementations:

| Payload Key | Top-Level Property | Description |
|-------------|-------------------|-------------|
| `user_id` | `user_id` | User identifier for session scoping |
| `agent_id` | `agent_id` | Agent identifier for agent-specific memories |
| `run_id` | `run_id` | Run/session identifier for temporal scoping |
| `actor_id` | `actor_id` | Actor/entity identifier for role-based filtering |
| `role` | `role` | Role of the entity in the memory context |

### Automatic Promotion Process

The promotion process involves identifying payload keys that match the predefined set and elevating them to the top-level object structure. This process occurs after core field extraction and before metadata filtering.

```python
# Example promotion logic
promoted_payload_keys = ["user_id", "agent_id", "run_id", "actor_id", "role"]

# During processing:
for key in promoted_payload_keys:
    if key in memory.payload:
        result_item[key] = memory.payload[key]
```

### Benefits of Promotion

- **Convenience**: Direct property access eliminates the need for nested dictionary lookups
- **Performance**: Reduces memory allocation for frequently accessed metadata
- **Consistency**: Provides uniform access patterns across different vector store implementations
- **Readability**: Improves code readability by avoiding deeply nested property access

**Section sources**
- [mem0/memory/main.py](file://mem0/memory/main.py#L508-L515)
- [mem0-ts/src/oss/src/memory/index.ts](file://mem0-ts/src/oss/src/memory/index.ts#L381-L385)

## Vector Store Integration

The `get()` method delegates the actual memory retrieval to the underlying vector store implementation, ensuring compatibility with various storage backends while maintaining a consistent interface.

### Supported Vector Stores

The method works seamlessly with all supported vector store implementations:

- **ChromaDB**: Local and server-based vector database
- **Redis**: In-memory and persistent Redis instances
- **Pinecone**: Cloud-native vector search platform
- **Qdrant**: Open-source vector database
- **Weaviate**: GraphQL-based vector search engine
- **Supabase**: PostgreSQL-based vector search
- **Elasticsearch**: Distributed search and analytics engine
- **Milvus**: Cloud-native vector database
- **FAISS**: Facebook AI Similarity Search library

### Vector Store Abstraction

Each vector store implementation provides a consistent `get()` method signature while handling backend-specific details:

```typescript
// TypeScript interface definition
async get(vectorId: string): Promise<VectorStoreResult | null>
```

### Implementation Variations

Different vector stores handle the `get()` operation with varying approaches:

- **Direct ID Lookup**: Some stores perform direct ID-based retrieval
- **Filtered Search**: Others use filtered search with the ID as a constraint
- **Hybrid Approaches**: Some combine multiple strategies for optimal performance

**Section sources**
- [mem0/vector_stores/chroma.py](file://mem0/vector_stores/chroma.py#L188-L200)
- [mem0-ts/src/oss/src/vector_stores/base.ts](file://mem0-ts/src/oss/src/vector_stores/base.ts#L14)

## Error Handling and Edge Cases

The `get()` method implements robust error handling to manage various failure scenarios gracefully.

### Memory Not Found

When the specified memory ID does not exist in the vector store, the method returns `None` (Python) or `null` (TypeScript):

```python
# Python example
result = memory.get("nonexistent_id")
assert result is None  # Memory not found
```

### Vector Store Connectivity Issues

Network or configuration issues with the vector store may result in exceptions:

```python
try:
    memory = memory_instance.get("valid_id")
except VectorStoreError as e:
    print(f"Vector store connection failed: {e}")
```

### Invalid Memory IDs

While the method does not validate UUID format internally, malformed IDs typically result in "not found" behavior:

```python
# Invalid UUID format
result = memory.get("invalid-format")  # Returns None
```

### Performance Degradation

In cases of vector store performance issues, the method may experience increased latency:

```python
# Monitor retrieval time
import time
start_time = time.time()
memory = memory.get("slow_id")
retrieval_time = time.time() - start_time
print(f"Retrieved in {retrieval_time:.2f} seconds")
```

**Section sources**
- [mem0/memory/main.py](file://mem0/memory/main.py#L505-L506)
- [tests/test_main.py](file://tests/test_main.py#L98-L121)

## Performance Considerations

The `get()` method is optimized for single-item lookups, but several factors influence retrieval performance.

### Single-Item Optimization

The method is specifically designed for efficient single-memory retrieval:

- **Direct ID Access**: Most vector stores support direct ID-based lookups
- **Minimal Processing**: Only essential fields are extracted and promoted
- **Efficient Serialization**: Minimal data transformation reduces overhead

### Caching Strategies

While the method itself does not implement caching, several caching approaches can improve performance:

#### Application-Level Caching

```python
from functools import lru_cache

class CachedMemory:
    def __init__(self, memory_instance):
        self.memory = memory_instance
        self._get_cached = lru_cache(maxsize=1000)(self._get_uncached)
    
    def get(self, memory_id):
        return self._get_cached(memory_id)
    
    def _get_uncached(self, memory_id):
        return self.memory.get(memory_id)
```

#### Vector Store Caching

Some vector stores provide built-in caching mechanisms:

- **Redis**: Built-in caching for frequently accessed keys
- **Pinecone**: Automatic caching for recent queries
- **ChromaDB**: In-memory caching for local deployments

### Performance Monitoring

Monitor retrieval performance using telemetry:

```python
# Enable telemetry
memory_instance.config.enable_telemetry = True

# Track retrieval metrics
result = memory_instance.get("memory_id")
# Telemetry captures retrieval time and success rate
```

### Optimization Guidelines

1. **Batch Operations**: Use `get_all()` for multiple retrievals
2. **Connection Pooling**: Maintain persistent vector store connections
3. **Index Optimization**: Ensure proper indexing on memory IDs
4. **Resource Management**: Close connections when appropriate

**Section sources**
- [mem0/memory/main.py](file://mem0/memory/main.py#L503-L503)

## Usage Examples

### Basic Memory Retrieval

```python
# Python example
memory_id = "550e8400-e29b-41d4-a716-446655440000"
memory = memory_instance.get(memory_id)

if memory:
    print(f"Memory: {memory['memory']}")
    print(f"Created: {memory['created_at']}")
    print(f"User: {memory['user_id']}")
else:
    print("Memory not found")
```

### TypeScript Usage

```typescript
// TypeScript example
const memoryId = "550e8400-e29b-41d4-a716-446655440000";
const memory = await memoryInstance.get(memoryId);

if (memory) {
    console.log(`Memory: ${memory.memory}`);
    console.log(`Created: ${memory.createdAt}`);
    console.log(`User: ${memory.user_id}`);
} else {
    console.log("Memory not found");
}
```

### Error Handling Example

```python
# Robust error handling
def get_memory_safely(memory_instance, memory_id):
    try:
        memory = memory_instance.get(memory_id)
        if memory:
            return memory
        else:
            print(f"Memory {memory_id} not found")
            return None
    except Exception as e:
        print(f"Error retrieving memory: {e}")
        return None
```

### Metadata Access Example

```python
# Accessing promoted and additional metadata
memory = memory_instance.get("memory_id")

# Promoted keys (direct access)
print(f"User ID: {memory['user_id']}")
print(f"Agent ID: {memory['agent_id']}")

# Additional metadata (nested access)
print(f"Confidence: {memory['metadata'].get('confidence_score')}")
print(f"Tags: {memory['metadata'].get('tags')}")
```

**Section sources**
- [tests/test_main.py](file://tests/test_main.py#L98-L121)
- [mem0-ts/src/oss/src/memory/index.ts](file://mem0-ts/src/oss/src/memory/index.ts#L377-L412)

## Common Issues and Troubleshooting

### Invalid Memory ID Format

**Problem**: Providing an improperly formatted UUID string.

**Solution**: Ensure the memory ID follows standard UUID format:
```python
# Correct UUID format
correct_id = "550e8400-e29b-41d4-a716-446655440000"

# Incorrect UUID formats
incorrect_ids = [
    "550e8400e29b41d4a716446655440000",  # Missing hyphens
    "550e8400-e29b-41d4-a716-44665544000",  # Wrong length
    "invalid-uuid-format"  # Non-hexadecimal characters
]
```

### Vector Store Connection Failures

**Problem**: Network or configuration issues preventing vector store access.

**Diagnostic Steps**:
1. Verify vector store connectivity
2. Check authentication credentials
3. Validate network configuration
4. Review vector store logs

**Solution**:
```python
# Connection health check
def check_vector_store_health(memory_instance):
    try:
        # Test with a known memory ID
        test_id = "test_id_that_exists"
        result = memory_instance.get(test_id)
        return True
    except Exception as e:
        print(f"Vector store health check failed: {e}")
        return False
```

### Memory Retrieval Performance Issues

**Problem**: Slow memory retrieval affecting application performance.

**Optimization Strategies**:
1. **Enable Caching**: Implement application-level caching
2. **Index Optimization**: Ensure proper indexing on memory IDs
3. **Connection Pooling**: Use persistent connections
4. **Monitor Metrics**: Track retrieval performance

### Data Integrity Concerns

**Problem**: Inconsistent or corrupted memory data.

**Verification Approach**:
```python
# Hash verification
def verify_memory_integrity(memory):
    import hashlib
    
    if not memory.get('hash'):
        return False
    
    calculated_hash = hashlib.md5(memory['memory'].encode()).hexdigest()
    return calculated_hash == memory['hash']
```

**Section sources**
- [tests/test_main.py](file://tests/test_main.py#L98-L121)

## Best Practices

### Memory ID Management

1. **Use UUIDs**: Always use properly formatted UUIDs for memory IDs
2. **Consistent Format**: Maintain consistent UUID format across the application
3. **Validation**: Validate UUID format before calling `get()`
4. **Persistence**: Store memory IDs securely for future retrieval

### Error Handling Patterns

1. **Graceful Degradation**: Handle missing memories without crashing
2. **Logging**: Log retrieval failures for debugging
3. **Retry Logic**: Implement retry mechanisms for transient failures
4. **Fallback Data**: Provide fallback data when memory retrieval fails

### Performance Optimization

1. **Caching Strategy**: Implement appropriate caching for frequently accessed memories
2. **Connection Management**: Use connection pooling for vector store access
3. **Monitoring**: Track retrieval performance and errors
4. **Resource Cleanup**: Properly close connections and release resources

### Security Considerations

1. **Access Control**: Implement proper authorization for memory access
2. **Data Validation**: Validate all input parameters
3. **Audit Logging**: Log memory access for security auditing
4. **Encryption**: Consider encrypting sensitive memory content

### Code Organization

1. **Wrapper Functions**: Create wrapper functions for common retrieval patterns
2. **Error Handling**: Centralize error handling logic
3. **Documentation**: Document memory retrieval patterns and expectations
4. **Testing**: Implement comprehensive tests for memory retrieval

**Section sources**
- [mem0/memory/main.py](file://mem0/memory/main.py#L494-L535)
- [mem0-ts/src/oss/src/memory/index.ts](file://mem0-ts/src/oss/src/memory/index.ts#L377-L412)