# Memory Orchestrator

<cite>
**Referenced Files in This Document**
- [mem0/memory/main.py](file://mem0/memory/main.py)
- [mem0/client/main.py](file://mem0/client/main.py)
- [mem0/utils/factory.py](file://mem0/utils/factory.py)
- [mem0/configs/base.py](file://mem0/configs/base.py)
- [mem0/memory/base.py](file://mem0/memory/base.py)
- [mem0/memory/storage.py](file://mem0/memory/storage.py)
- [mem0/exceptions.py](file://mem0/exceptions.py)
</cite>

## Table of Contents
1. [Introduction](#introduction)
2. [Architecture Overview](#architecture-overview)
3. [Core Components](#core-components)
4. [Configuration System](#configuration-system)
5. [Memory Operations Lifecycle](#memory-operations-lifecycle)
6. [Async/Sync Execution Paths](#async-sync-execution-paths)
7. [Error Handling and Fallback Strategies](#error-handling-and-fallback-strategies)
8. [Integration Patterns](#integration-patterns)
9. [Performance Considerations](#performance-considerations)
10. [Troubleshooting Guide](#troubleshooting-guide)
11. [Conclusion](#conclusion)

## Introduction

The Memory orchestrator in `main.py` serves as the central coordination hub for all memory operations within the Mem0 system. It acts as the primary interface between users and the underlying memory infrastructure, seamlessly integrating LLMs for fact extraction and inference, embedders for vectorization, vector stores for semantic search, graph stores for relationship mapping, and storage backends for history tracking.

This orchestrator implements both synchronous and asynchronous execution patterns, providing flexibility for different use cases while maintaining consistency in the memory management lifecycle. The system is designed with modularity and extensibility in mind, allowing for easy integration of new components and providers.

## Architecture Overview

The Memory orchestrator follows a layered architecture pattern with clear separation of concerns:

```mermaid
graph TB
subgraph "Client Layer"
Client[Memory Client]
AsyncClient[Async Memory Client]
end
subgraph "Orchestrator Layer"
SyncMem[Memory]
AsyncMem[AsyncMemory]
end
subgraph "Component Layer"
LLM[LLM Factory]
Embedder[Embedder Factory]
VectorStore[Vector Store Factory]
GraphStore[Graph Store Factory]
Storage[SQLite Manager]
end
subgraph "Storage Layer"
VectorDB[(Vector Database)]
GraphDB[(Graph Database)]
HistoryDB[(History Database)]
end
Client --> SyncMem
AsyncClient --> AsyncMem
SyncMem --> LLM
SyncMem --> Embedder
SyncMem --> VectorStore
SyncMem --> GraphStore
SyncMem --> Storage
AsyncMem --> LLM
AsyncMem --> Embedder
AsyncMem --> VectorStore
AsyncMem --> GraphStore
AsyncMem --> Storage
VectorStore --> VectorDB
GraphStore --> GraphDB
Storage --> HistoryDB
```

**Diagram sources**
- [mem0/memory/main.py](file://mem0/memory/main.py#L131-L170)
- [mem0/client/main.py](file://mem0/client/main.py#L24-L106)
- [mem0/utils/factory.py](file://mem0/utils/factory.py#L23-L224)

**Section sources**
- [mem0/memory/main.py](file://mem0/memory/main.py#L131-L170)
- [mem0/client/main.py](file://mem0/client/main.py#L24-L106)

## Core Components

### Memory Class (Synchronous)

The `Memory` class serves as the primary synchronous orchestrator, implementing the core memory operations with thread-based parallelism for optimal performance:

```mermaid
classDiagram
class Memory {
+MemoryConfig config
+Embedder embedding_model
+VectorStore vector_store
+LLM llm
+SQLiteManager db
+GraphStore graph
+bool enable_graph
+string api_version
+add(messages, user_id, agent_id, run_id, metadata, infer, memory_type, prompt) dict
+get(memory_id) dict
+get_all(user_id, agent_id, run_id, filters, limit) dict
+search(query, user_id, agent_id, run_id, limit, filters, threshold) dict
+update(memory_id, data) dict
+delete(memory_id) dict
+delete_all(user_id, agent_id, run_id) dict
+history(memory_id) list
+reset() void
-_create_memory(data, existing_embeddings, metadata) string
-_update_memory(memory_id, data, existing_embeddings, metadata) string
-_delete_memory(memory_id) string
-_create_procedural_memory(messages, metadata, prompt) dict
-_add_to_vector_store(messages, metadata, filters, infer) list
-_add_to_graph(messages, filters) list
-_get_all_from_vector_store(filters, limit) list
-_search_vector_store(query, filters, limit, threshold) list
}
class MemoryConfig {
+VectorStoreConfig vector_store
+LlmConfig llm
+EmbedderConfig embedder
+GraphStoreConfig graph_store
+string history_db_path
+string version
+string custom_fact_extraction_prompt
+string custom_update_memory_prompt
}
Memory --> MemoryConfig : uses
```

**Diagram sources**
- [mem0/memory/main.py](file://mem0/memory/main.py#L131-L170)
- [mem0/configs/base.py](file://mem0/configs/base.py#L29-L61)

### AsyncMemory Class (Asynchronous)

The `AsyncMemory` class provides fully asynchronous operations using asyncio for non-blocking execution:

```mermaid
classDiagram
class AsyncMemory {
+MemoryConfig config
+Embedder embedding_model
+VectorStore vector_store
+LLM llm
+SQLiteManager db
+GraphStore graph
+bool enable_graph
+string api_version
+add(messages, user_id, agent_id, run_id, metadata, infer, memory_type, prompt, llm) dict
+get(memory_id) dict
+get_all(user_id, agent_id, run_id, filters, limit) dict
+search(query, user_id, agent_id, run_id, limit, filters, threshold) dict
+update(memory_id, data) dict
+delete(memory_id) dict
+delete_all(user_id, agent_id, run_id) dict
+history(memory_id) list
+reset() void
-_create_memory(data, existing_embeddings, metadata) string
-_update_memory(memory_id, data, existing_embeddings, metadata) string
-_delete_memory(memory_id) string
-_create_procedural_memory(messages, metadata, llm, prompt) dict
-_add_to_vector_store(messages, metadata, filters, infer) list
-_add_to_graph(messages, filters) list
-_get_all_from_vector_store(filters, limit) list
-_search_vector_store(query, filters, limit, threshold) list
}
AsyncMemory --> MemoryConfig : uses
```

**Diagram sources**
- [mem0/memory/main.py](file://mem0/memory/main.py#L1009-L1911)

**Section sources**
- [mem0/memory/main.py](file://mem0/memory/main.py#L131-L170)
- [mem0/memory/main.py](file://mem0/memory/main.py#L1009-L1911)

## Configuration System

The configuration system provides flexible and extensible setup for all memory components through the `MemoryConfig` class:

### Configuration Injection Pattern

The orchestrator uses a factory-based approach for component instantiation:

```mermaid
sequenceDiagram
participant Client as Client Application
participant Memory as Memory/AsyncMemory
participant Factory as Component Factories
participant Component as Component Instances
Client->>Memory : __init__(config)
Memory->>Factory : EmbedderFactory.create(provider, config, vector_config)
Factory->>Component : Instantiate Embedder
Component-->>Factory : Embedder Instance
Factory-->>Memory : Embedder
Memory->>Factory : VectorStoreFactory.create(provider, config)
Factory->>Component : Instantiate VectorStore
Component-->>Factory : VectorStore Instance
Factory-->>Memory : VectorStore
Memory->>Factory : LlmFactory.create(provider, config)
Factory->>Component : Instantiate LLM
Component-->>Factory : LLM Instance
Factory-->>Memory : LLM
Memory->>Factory : GraphStoreFactory.create(provider, config)
Factory->>Component : Instantiate GraphStore
Component-->>Factory : GraphStore Instance
Factory-->>Memory : GraphStore (optional)
Memory-->>Client : Initialized Memory Orchestrator
```

**Diagram sources**
- [mem0/utils/factory.py](file://mem0/utils/factory.py#L23-L224)
- [mem0/memory/main.py](file://mem0/memory/main.py#L137-L157)

### Component Factory Implementation

Each factory implements a standardized interface for component creation:

| Factory | Purpose | Key Features |
|---------|---------|--------------|
| `EmbedderFactory` | Creates embedding models | Supports multiple providers, dimension handling |
| `VectorStoreFactory` | Creates vector databases | Handles various vector DB types, reset functionality |
| `LlmFactory` | Creates language models | Provider-specific configs, vision support |
| `GraphStoreFactory` | Creates graph databases | Flexible graph store selection |

**Section sources**
- [mem0/utils/factory.py](file://mem0/utils/factory.py#L23-L224)
- [mem0/memory/main.py](file://mem0/memory/main.py#L137-L157)

## Memory Operations Lifecycle

### Add Operation Lifecycle

The `add` operation demonstrates the orchestrator's coordination capabilities:

```mermaid
sequenceDiagram
participant Client as Client
participant Memory as Memory Orchestrator
participant Embedder as Embedding Model
participant VectorStore as Vector Database
participant GraphStore as Graph Database
participant Storage as History Storage
Client->>Memory : add(messages, user_id, agent_id, ...)
Memory->>Memory : _build_filters_and_metadata()
Memory->>Memory : validate_input_parameters()
alt Procedural Memory
Memory->>Memory : _create_procedural_memory()
Memory-->>Client : Procedural Memory Result
else Standard Memory
par Parallel Processing
Memory->>Embedder : embed(messages, "add")
Embedder-->>Memory : Embeddings
and
Memory->>GraphStore : add(data, filters)
GraphStore-->>Memory : Entities Added
end
Memory->>VectorStore : insert(vectors, ids, payloads)
Memory->>Storage : add_history(memory_id, old_data, new_data, "ADD")
Memory-->>Client : Memory Addition Results
end
```

**Diagram sources**
- [mem0/memory/main.py](file://mem0/memory/main.py#L195-L308)
- [mem0/memory/main.py](file://mem0/memory/main.py#L1135-L1158)

### Search Operation Lifecycle

The search operation showcases the orchestrator's ability to coordinate multiple data sources:

```mermaid
sequenceDiagram
participant Client as Client
participant Memory as Memory Orchestrator
participant Embedder as Embedding Model
participant VectorStore as Vector Database
participant GraphStore as Graph Database
Client->>Memory : search(query, user_id, agent_id, ...)
Memory->>Memory : _build_filters_and_metadata()
Memory->>Embedder : embed(query, "search")
Embedder-->>Memory : Query Embeddings
par Parallel Search
Memory->>VectorStore : search(query, vectors, limit, filters)
VectorStore-->>Memory : Vector Results
and
Memory->>GraphStore : search(query, filters, limit)
GraphStore-->>Memory : Graph Results
end
Memory->>Memory : format_results()
Memory-->>Client : Combined Search Results
```

**Diagram sources**
- [mem0/memory/main.py](file://mem0/memory/main.py#L644-L718)
- [mem0/memory/main.py](file://mem0/memory/main.py#L1514-L1591)

**Section sources**
- [mem0/memory/main.py](file://mem0/memory/main.py#L195-L308)
- [mem0/memory/main.py](file://mem0/memory/main.py#L644-L718)

## Async/Sync Execution Paths

### Synchronous Path Implementation

The synchronous path uses ThreadPoolExecutor for CPU-intensive operations:

```mermaid
flowchart TD
Start([Sync Operation Start]) --> ValidateInput["Validate Input Parameters"]
ValidateInput --> BuildFilters["Build Filters & Metadata"]
BuildFilters --> ThreadExecutor["ThreadPoolExecutor"]
ThreadExecutor --> Task1["Task 1: Vector Store Operation"]
ThreadExecutor --> Task2["Task 2: Graph Store Operation"]
Task1 --> WaitTasks["Wait for All Tasks"]
Task2 --> WaitTasks
WaitTasks --> CombineResults["Combine Results"]
CombineResults --> FormatOutput["Format Output"]
FormatOutput --> End([Operation Complete])
```

**Diagram sources**
- [mem0/memory/main.py](file://mem0/memory/main.py#L283-L290)

### Asynchronous Path Implementation

The asynchronous path uses asyncio for non-blocking execution:

```mermaid
flowchart TD
Start([Async Operation Start]) --> ValidateInput["Validate Input Parameters"]
ValidateInput --> BuildFilters["Build Filters & Metadata"]
BuildFilters --> AsyncTasks["Create Async Tasks"]
AsyncTasks --> Task1["Task 1: Vector Store Operation"]
AsyncTasks --> Task2["Task 2: Graph Store Operation"]
Task1 --> AwaitTasks["Await All Tasks"]
Task2 --> AwaitTasks
AwaitTasks --> CombineResults["Combine Results"]
CombineResults --> FormatOutput["Format Output"]
FormatOutput --> End([Operation Complete])
```

**Diagram sources**
- [mem0/memory/main.py](file://mem0/memory/main.py#L1135-L1140)
- [mem0/memory/main.py](file://mem0/memory/main.py#L1339-L1346)

### Execution Strategy Comparison

| Aspect | Synchronous | Asynchronous |
|--------|-------------|--------------|
| **Concurrency Model** | ThreadPoolExecutor | asyncio |
| **CPU-bound Tasks** | Offloaded to threads | Blocked on I/O |
| **Network-bound Tasks** | Thread blocking | Non-blocking |
| **Resource Usage** | Higher thread overhead | Lower resource usage |
| **Scalability** | Limited by thread pool | Better scalability |
| **Error Handling** | Thread-local exceptions | Coroutine-based |

**Section sources**
- [mem0/memory/main.py](file://mem0/memory/main.py#L283-L290)
- [mem0/memory/main.py](file://mem0/memory/main.py#L1135-L1140)

## Error Handling and Fallback Strategies

### Exception Hierarchy

The orchestrator implements a comprehensive exception hierarchy for robust error handling:

```mermaid
classDiagram
class MemoryError {
+string message
+string error_code
+dict details
+string suggestion
+dict debug_info
}
class ValidationError {
+validation_error_details()
}
class AuthenticationError {
+auth_error_details()
}
class NetworkError {
+network_error_details()
}
class MemoryNotFoundError {
+memory_not_found_details()
}
class VectorSearchError {
+vector_search_error_details()
}
class CacheError {
+cache_error_details()
}
MemoryError <|-- ValidationError
MemoryError <|-- AuthenticationError
MemoryError <|-- NetworkError
MemoryError <|-- MemoryNotFoundError
MemoryError <|-- VectorSearchError
MemoryError <|-- CacheError
```

**Diagram sources**
- [mem0/exceptions.py](file://mem0/exceptions.py#L34-L466)

### Fallback Strategies

The orchestrator implements several fallback mechanisms:

1. **Component Failure Fallback**: Continue operation with disabled components
2. **Provider Switching**: Automatic fallback to alternative providers
3. **Degraded Mode**: Reduced functionality when components fail
4. **Circuit Breaker**: Prevent cascading failures

```mermaid
flowchart TD
Operation[Memory Operation] --> TryExecute["Try Execute"]
TryExecute --> Success{Success?}
Success --> |Yes| ReturnResult["Return Result"]
Success --> |No| CatchException["Catch Exception"]
CatchException --> ClassifyError["Classify Error Type"]
ClassifyError --> NetworkError{Network Error?}
ClassifyError --> ComponentError{Component Error?}
ClassifyError --> ValidationError{Validation Error?}
NetworkError --> |Yes| RetryWithBackoff["Retry with Backoff"]
ComponentError --> |Yes| DisableComponent["Disable Component"]
ValidationError --> |Yes| LogError["Log Error & Raise"]
RetryWithBackoff --> RetrySuccess{Retry Success?}
RetrySuccess --> |Yes| ReturnResult
RetrySuccess --> |No| DisableComponent
DisableComponent --> DegradedMode["Operate in Degraded Mode"]
DegradedMode --> ReturnPartialResult["Return Partial Result"]
ReturnResult --> End([Operation Complete])
ReturnPartialResult --> End
LogError --> End
```

**Diagram sources**
- [mem0/exceptions.py](file://mem0/exceptions.py#L442-L466)

**Section sources**
- [mem0/exceptions.py](file://mem0/exceptions.py#L34-L466)

## Integration Patterns

### LLM Integration for Fact Extraction

The orchestrator integrates LLMs for intelligent fact extraction and memory inference:

```mermaid
sequenceDiagram
participant Memory as Memory Orchestrator
participant LLM as LLM Provider
participant Embedder as Embedding Model
participant VectorStore as Vector Database
Memory->>LLM : generate_response(system_prompt, user_prompt)
LLM-->>Memory : Extracted Facts (JSON)
Memory->>Memory : parse_extracted_facts()
loop For Each Fact
Memory->>Embedder : embed(fact, "add")
Embedder-->>Memory : Fact Embeddings
Memory->>VectorStore : search(query=fact, vectors=embeddings, limit=5)
VectorStore-->>Memory : Existing Memories
end
Memory->>LLM : generate_response(update_prompt)
LLM-->>Memory : Memory Actions (ADD/UPDATE/DELETE)
Memory->>Memory : process_memory_actions()
Memory-->>Memory : Updated Memory Store
```

**Diagram sources**
- [mem0/memory/main.py](file://mem0/memory/main.py#L349-L474)

### Graph Store Integration

The orchestrator coordinates with graph stores for relationship mapping:

```mermaid
sequenceDiagram
participant Memory as Memory Orchestrator
participant GraphStore as Graph Store
participant VectorStore as Vector Database
Memory->>GraphStore : add(data, filters)
GraphStore-->>Memory : Entities & Relationships
Memory->>Memory : extract_entities_relations()
Memory->>GraphStore : create_nodes(entities)
Memory->>GraphStore : create_relationships(relations)
GraphStore-->>Memory : Confirmation
Note over Memory,VectorStore : Cross-reference with vector store
Memory->>VectorStore : link_entities_to_memories()
VectorStore-->>Memory : Linked Entities
```

**Diagram sources**
- [mem0/memory/main.py](file://mem0/memory/main.py#L483-L492)

### Storage Backend Integration

The orchestrator manages multiple storage backends through the SQLiteManager:

```mermaid
classDiagram
class SQLiteManager {
+string db_path
+sqlite3.Connection connection
+threading.Lock _lock
+add_history(memory_id, old_memory, new_memory, event) void
+get_history(memory_id) list
+reset() void
+close() void
+_create_history_table() void
+_migrate_history_table() void
}
class HistoryManager {
<<interface>>
+add_history(memory_id, old_memory, new_memory, event) void
+get_history(memory_id) list
+reset() void
+close() void
}
SQLiteManager ..|> HistoryManager : implements
```

**Diagram sources**
- [mem0/memory/storage.py](file://mem0/memory/storage.py#L10-L219)

**Section sources**
- [mem0/memory/main.py](file://mem0/memory/main.py#L349-L474)
- [mem0/memory/main.py](file://mem0/memory/main.py#L483-L492)
- [mem0/memory/storage.py](file://mem0/memory/storage.py#L10-L219)

## Performance Considerations

### Optimization Strategies

The orchestrator implements several performance optimization techniques:

1. **Parallel Processing**: Concurrent execution of independent operations
2. **Connection Pooling**: Reuse database connections
3. **Embedding Caching**: Cache frequently used embeddings
4. **Batch Operations**: Group multiple operations together
5. **Lazy Loading**: Load components only when needed

### Memory Management

```mermaid
flowchart TD
Start([Operation Start]) --> CheckCache["Check Embedding Cache"]
CheckCache --> CacheHit{Cache Hit?}
CacheHit --> |Yes| UseCached["Use Cached Embeddings"]
CacheHit --> |No| GenerateEmbeddings["Generate New Embeddings"]
GenerateEmbeddings --> StoreCache["Store in Cache"]
UseCached --> ProcessOperation["Process Operation"]
StoreCache --> ProcessOperation
ProcessOperation --> CleanupOld["Cleanup Old Entries"]
CleanupOld --> GC["Garbage Collection"]
GC --> End([Operation Complete])
```

### Scalability Patterns

| Pattern | Implementation | Benefits |
|---------|----------------|----------|
| **Connection Pooling** | SQLiteManager with thread-safe connections | Reduced connection overhead |
| **Async Processing** | asyncio for I/O-bound operations | Better resource utilization |
| **Component Lazy Loading** | Factory pattern for component instantiation | Faster startup times |
| **Batch Operations** | Group multiple vector operations | Improved throughput |

## Troubleshooting Guide

### Common Issues and Solutions

#### Configuration Validation Errors

**Problem**: Invalid configuration parameters
**Solution**: Use `MemoryConfig` validation with proper provider configurations

#### Memory Operation Failures

**Problem**: Operations fail due to component unavailability
**Solution**: Implement circuit breaker pattern and fallback strategies

#### Performance Issues

**Problem**: Slow memory operations
**Solution**: Enable async processing and optimize embedding caching

#### Graph Store Integration Issues

**Problem**: Graph operations fail silently
**Solution**: Check component availability and enable graph store conditionally

### Debugging Techniques

1. **Enable Debug Logging**: Set log level to DEBUG for detailed operation traces
2. **Monitor Component Health**: Track component availability and response times
3. **Validate Configuration**: Use configuration validation before initialization
4. **Test Component Isolation**: Test individual components separately

**Section sources**
- [mem0/exceptions.py](file://mem0/exceptions.py#L34-L466)
- [mem0/memory/main.py](file://mem0/memory/main.py#L131-L170)

## Conclusion

The Memory orchestrator in `main.py` represents a sophisticated and well-architected system for managing complex memory operations. Its modular design, comprehensive error handling, and support for both synchronous and asynchronous execution patterns make it suitable for a wide range of applications.

Key strengths of the orchestrator include:

- **Modular Architecture**: Clear separation of concerns with factory-based component creation
- **Flexible Execution**: Support for both sync and async patterns
- **Robust Error Handling**: Comprehensive exception hierarchy and fallback strategies
- **Extensible Design**: Easy integration of new providers and components
- **Performance Optimization**: Parallel processing and caching mechanisms

The orchestrator successfully abstracts the complexity of coordinating multiple memory systems while providing a clean and intuitive interface for developers. Its design patterns and implementation strategies serve as excellent examples for building scalable memory management systems in AI applications.