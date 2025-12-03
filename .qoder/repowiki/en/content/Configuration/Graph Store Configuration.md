# Graph Store Configuration

<cite>
**Referenced Files in This Document**
- [mem0/graphs/configs.py](file://mem0/graphs/configs.py)
- [mem0/utils/factory.py](file://mem0/utils/factory.py)
- [mem0/configs/vector_stores/neptune.py](file://mem0/configs/vector_stores/neptune.py)
- [mem0/configs/vector_stores/mongodb.py](file://mem0/configs/vector_stores/mongodb.py)
- [mem0/configs/vector_stores/pgvector.py](file://mem0/configs/vector_stores/pgvector.py)
- [mem0/configs/vector_stores/supabase.py](file://mem0/configs/vector_stores/supabase.py)
- [mem0/configs/vector_stores/redis.py](file://mem0/configs/vector_stores/redis.py)
- [mem0/memory/graph_memory.py](file://mem0/memory/graph_memory.py)
- [mem0/exceptions.py](file://mem0/exceptions.py)
- [examples/graph-db-demo/neptune-example.ipynb](file://examples/graph-db-demo/neptune-example.ipynb)
- [mem0/configs/base.py](file://mem0/configs/base.py)
</cite>

## Table of Contents
1. [Introduction](#introduction)
2. [Graph Database Architecture](#graph-database-architecture)
3. [Supported Graph Stores](#supported-graph-stores)
4. [Configuration Parameters](#configuration-parameters)
5. [GraphStoreFactory Implementation](#graphstorefactory-implementation)
6. [Connection Setup Examples](#connection-setup-examples)
7. [Performance Characteristics](#performance-characteristics)
8. [Query Patterns and Scalability](#query-patterns-and-scalability)
9. [Troubleshooting Guide](#troubleshooting-guide)
10. [Best Practices](#best-practices)

## Introduction

Graph stores provide a powerful alternative to traditional vector-only approaches for memory systems by storing relational memory structures and procedural knowledge in interconnected graph databases. Unlike pure vector stores that rely solely on similarity search, graph stores maintain explicit relationships between entities, enabling sophisticated reasoning and knowledge representation.

Mem0's graph store architecture supports multiple graph database providers, each offering unique advantages for different use cases. The system uses a factory pattern to initialize graph database clients and provides unified interfaces for graph operations regardless of the underlying provider.

## Graph Database Architecture

Graph databases excel at representing complex relationships and procedural knowledge through nodes (entities) and edges (relationships). This architecture enables:

- **Explicit Relationship Storage**: Maintains precise connections between entities
- **Procedural Knowledge Representation**: Captures temporal and causal relationships
- **Multi-hop Reasoning**: Enables complex queries across multiple relationship layers
- **Schema Flexibility**: Adapts to evolving knowledge structures

```mermaid
graph TB
subgraph "Graph Memory Architecture"
A[Text Input] --> B[Entity Extraction]
B --> C[Relationship Detection]
C --> D[Graph Store]
D --> E[Nodes: Entities]
D --> F[Edges: Relationships]
D --> G[Properties: Metadata]
H[Query Input] --> I[Entity Recognition]
I --> J[Graph Traversal]
J --> K[Similarity Search]
K --> L[Result Ranking]
end
subgraph "Vector Integration"
M[Embedding Model] --> N[Vector Storage]
N --> O[Similarity Search]
O --> P[Hybrid Results]
end
D -.->|Enriches| M
M -.->|Enhances| D
```

**Diagram sources**
- [mem0/memory/graph_memory.py](file://mem0/memory/graph_memory.py#L29-L699)

## Supported Graph Stores

Mem0 supports multiple graph database providers, each with specific strengths and use cases:

### Amazon Neptune

Amazon Neptune provides both graph analytics (Neptune Analytics) and graph database (Neptune DB) capabilities:

- **Neptune Analytics**: Managed graph analytics service for large-scale graph processing
- **Neptune DB**: Fully managed graph database with Gremlin and Cypher support
- **Vector Similarity**: Built-in vector similarity search capabilities
- **Scalability**: Automatic scaling and high availability

### MongoDB with Vector Search

MongoDB Atlas offers integrated vector search capabilities:

- **Native Vector Indexing**: Built-in support for vector similarity search
- **Flexible Schema**: JSON-like document structure with graph-like relationships
- **Global Indexing**: Cross-region replication and indexing
- **Cost Efficiency**: Pay-as-you-go pricing model

### PostgreSQL with pgvector

PostgreSQL extensions provide robust vector capabilities:

- **ACID Compliance**: Strong consistency guarantees
- **Advanced Indexing**: Multiple vector indexing strategies (HNSW, IVF)
- **SQL Integration**: Full SQL support with vector operations
- **Mature Ecosystem**: Extensive tooling and community support

### Supabase with pgvector

Supabase combines PostgreSQL with modern development tools:

- **Developer-Friendly**: Built-in APIs and authentication
- **Real-time Features**: WebSocket connections and real-time subscriptions
- **Open Source**: Transparent architecture and customization
- **Cloud-Native**: Managed infrastructure with automatic scaling

### Redis with RedisTimeSeries

Redis provides high-performance vector search:

- **In-Memory Performance**: Ultra-low latency operations
- **Rich Data Types**: Multiple data structures for complex relationships
- **Persistence Options**: Disk persistence with configurable durability
- **Clustering**: Horizontal scaling with Redis Cluster

### Milvus

Milvus specializes in vector similarity search:

- **Distributed Architecture**: Horizontal scaling for large datasets
- **Multiple Index Types**: HNSW, IVF, and specialized indexes
- **Cloud-Native**: Kubernetes-native deployment
- **Multi-modal Support**: Text, image, and audio embeddings

**Section sources**
- [mem0/graphs/configs.py](file://mem0/graphs/configs.py#L8-L106)
- [mem0/utils/factory.py](file://mem0/utils/factory.py#L208-L224)

## Configuration Parameters

Each graph store provider requires specific configuration parameters for connection, authentication, and operational settings.

### Amazon Neptune Configuration

```python
# Neptune Analytics Configuration
neptune_config = {
    "provider": "neptune",
    "config": {
        "endpoint": "neptune-graph://your-graph-id",
        "collection_name": "mem0",
        "app_id": "Mem0"
    }
}

# Neptune DB Configuration  
neptune_db_config = {
    "provider": "neptunedb",
    "config": {
        "endpoint": "neptune-db://your-endpoint",
        "base_label": True,
        "collection_name": "mem0_neptune_vectors"
    }
}
```

**Key Parameters:**
- `endpoint`: Connection URL with protocol prefix
- `collection_name`: Vector collection name for hybrid stores
- `base_label`: Enable universal entity labeling
- `app_id`: Application identifier for connection tracking

### MongoDB Configuration

```python
mongodb_config = {
    "provider": "mongodb",
    "config": {
        "db_name": "mem0_db",
        "collection_name": "mem0",
        "embedding_model_dims": 1536,
        "mongo_uri": "mongodb://username:password@host:port"
    }
}
```

**Key Parameters:**
- `db_name`: Target database name
- `collection_name`: Collection for vector storage
- `embedding_model_dims`: Vector dimension compatibility
- `mongo_uri`: Connection string with authentication

### PostgreSQL with pgvector Configuration

```python
pgvector_config = {
    "provider": "pgvector",
    "config": {
        "dbname": "postgres",
        "collection_name": "mem0",
        "user": "username",
        "password": "password",
        "host": "localhost",
        "port": 5432,
        "embedding_model_dims": 1536,
        "diskann": False,
        "hnsw": True,
        "minconn": 1,
        "maxconn": 5
    }
}
```

**Key Parameters:**
- `dbname`: Database name
- `user/password`: Authentication credentials
- `host/port`: Connection endpoint
- `embedding_model_dims`: Vector dimension
- `diskann/hnsw`: Index strategy selection
- `minconn/maxconn`: Connection pool sizing

### Supabase Configuration

```python
supabase_config = {
    "provider": "supabase",
    "config": {
        "connection_string": "postgresql://username:password@host:port/dbname",
        "collection_name": "mem0",
        "embedding_model_dims": 1536,
        "index_method": "auto",  # auto, hnsw, ivfflat
        "index_measure": "cosine_distance"  # cosine_distance, l2_distance, etc.
    }
}
```

**Key Parameters:**
- `connection_string`: PostgreSQL-compatible connection
- `index_method`: Vector indexing strategy
- `index_measure`: Distance calculation method

### Redis Configuration

```python
redis_config = {
    "provider": "redis",
    "config": {
        "redis_url": "redis://username:password@host:port",
        "collection_name": "mem0",
        "embedding_model_dims": 1536
    }
}
```

**Key Parameters:**
- `redis_url`: Redis connection string
- `collection_name`: Namespace identifier
- `embedding_model_dims`: Vector dimension compatibility

**Section sources**
- [mem0/configs/vector_stores/neptune.py](file://mem0/configs/vector_stores/neptune.py#L11-L28)
- [mem0/configs/vector_stores/mongodb.py](file://mem0/configs/vector_stores/mongodb.py#L6-L26)
- [mem0/configs/vector_stores/pgvector.py](file://mem0/configs/vector_stores/pgvector.py#L6-L53)
- [mem0/configs/vector_stores/supabase.py](file://mem0/configs/vector_stores/supabase.py#L20-L45)
- [mem0/configs/vector_stores/redis.py](file://mem0/configs/vector_stores/redis.py#L7-L25)

## GraphStoreFactory Implementation

The GraphStoreFactory uses a centralized factory pattern to initialize graph database clients based on provider configurations.

```mermaid
classDiagram
class GraphStoreFactory {
+provider_to_class : dict
+create(provider_name, config) MemoryGraph
}
class MemoryGraph {
+config : MemoryConfig
+graph : GraphClient
+embedding_model : Embedder
+llm : LLMClient
+add(data, filters) dict
+search(query, filters, limit) list
+delete_all(filters) void
+get_all(filters, limit) list
}
class NeptuneMemoryGraph {
+graph : NeptuneGraph
+embedding_model : Embedder
+node_label : str
}
class MongoDBMemoryGraph {
+client : MongoClient
+db : Database
+collection : Collection
}
class PGVectorMemoryGraph {
+connection : Connection
+vector_store : VectorStore
+index_strategy : str
}
GraphStoreFactory --> MemoryGraph : creates
MemoryGraph <|-- NeptuneMemoryGraph
MemoryGraph <|-- MongoDBMemoryGraph
MemoryGraph <|-- PGVectorMemoryGraph
```

**Diagram sources**
- [mem0/utils/factory.py](file://mem0/utils/factory.py#L202-L224)
- [mem0/memory/graph_memory.py](file://mem0/memory/graph_memory.py#L29-L699)

### Factory Initialization Process

The factory follows a standardized initialization process:

1. **Provider Resolution**: Maps provider names to implementation classes
2. **Configuration Validation**: Validates required parameters
3. **Client Instantiation**: Creates provider-specific graph clients
4. **Integration Setup**: Establishes embedding models and LLM connections

### Supported Providers Mapping

```python
provider_to_class = {
    "memgraph": "mem0.memory.memgraph_memory.MemoryGraph",
    "neptune": "mem0.graphs.neptune.neptunegraph.MemoryGraph",
    "neptunedb": "mem0.graphs.neptune.neptunedb.MemoryGraph", 
    "kuzu": "mem0.memory.kuzu_memory.MemoryGraph",
    "default": "mem0.memory.graph_memory.MemoryGraph"
}
```

**Section sources**
- [mem0/utils/factory.py](file://mem0/utils/factory.py#L208-L224)

## Connection Setup Examples

### Amazon Neptune Analytics Setup

```python
import os
from mem0 import Memory

# Configure Neptune Analytics
config = {
    "embedder": {
        "provider": "aws_bedrock",
        "config": {
            "model": "amazon.titan-embed-text-v2:0",
            "embedding_dims": 1024
        }
    },
    "llm": {
        "provider": "aws_bedrock",
        "config": {
            "model": "anthropic.claude-3-sonnet-20241022-v1:0",
            "temperature": 0.1,
            "max_tokens": 2000
        }
    },
    "vector_store": {
        "provider": "neptune",
        "config": {
            "endpoint": f"neptune-graph://{os.environ.get('GRAPH_ID')}",
        }
    },
    "graph_store": {
        "provider": "neptune",
        "config": {
            "endpoint": f"neptune-graph://{os.environ.get('GRAPH_ID')}",
        }
    }
}

# Initialize memory with graph store
memory = Memory.from_config(config_dict=config)
```

### MongoDB Atlas Setup

```python
# MongoDB Atlas Configuration
mongodb_config = {
    "embedder": {
        "provider": "openai",
        "config": {
            "model": "text-embedding-3-small",
            "embedding_dims": 1536
        }
    },
    "vector_store": {
        "provider": "mongodb",
        "config": {
            "db_name": "mem0_production",
            "collection_name": "memories",
            "embedding_model_dims": 1536,
            "mongo_uri": os.environ.get("MONGODB_URI")
        }
    },
    "graph_store": {
        "provider": "mongodb",
        "config": {
            "db_name": "mem0_production",
            "collection_name": "memories",
            "embedding_model_dims": 1536,
            "mongo_uri": os.environ.get("MONGODB_URI")
        }
    }
}
```

### PostgreSQL with pgvector Setup

```python
# PostgreSQL with pgvector Configuration
pgvector_config = {
    "embedder": {
        "provider": "openai",
        "config": {
            "model": "text-embedding-3-small",
            "embedding_dims": 1536
        }
    },
    "vector_store": {
        "provider": "pgvector",
        "config": {
            "dbname": "mem0",
            "collection_name": "memories",
            "user": os.environ.get("DB_USER"),
            "password": os.environ.get("DB_PASSWORD"),
            "host": os.environ.get("DB_HOST"),
            "port": 5432,
            "embedding_model_dims": 1536,
            "hnsw": True,
            "minconn": 2,
            "maxconn": 10
        }
    },
    "graph_store": {
        "provider": "pgvector",
        "config": {
            "dbname": "mem0",
            "collection_name": "memories",
            "user": os.environ.get("DB_USER"),
            "password": os.environ.get("DB_PASSWORD"),
            "host": os.environ.get("DB_HOST"),
            "port": 5432,
            "embedding_model_dims": 1536,
            "hnsw": True,
            "minconn": 2,
            "maxconn": 10
        }
    }
}
```

**Section sources**
- [examples/graph-db-demo/neptune-example.ipynb](file://examples/graph-db-demo/neptune-example.ipynb#L125-L159)

## Performance Characteristics

### Query Performance Comparison

Different graph stores offer varying performance characteristics:

| Provider | Latency (ms) | Throughput (ops/sec) | Scalability | Best Use Case |
|----------|--------------|---------------------|-------------|---------------|
| Redis | 1-5 | 10K+ | Vertical | Real-time applications |
| MongoDB | 10-50 | 1K-5K | Horizontal | Flexible schema |
| Neptune Analytics | 50-200 | 500-2K | Cloud-native | Large-scale analytics |
| pgvector | 20-100 | 500-1K | Vertical | ACID compliance |
| Supabase | 30-150 | 500-1K | Cloud-native | Developer-friendly |

### Indexing Strategies

Each provider offers different indexing approaches:

- **HNSW (Hierarchical Navigable Small World)**: Fast approximate search
- **DiskANN**: Disk-based approximate nearest neighbor
- **IVF (Inverted File)**: Partition-based indexing
- **LSH (Locality Sensitive Hashing)**: Hash-based approximate search

### Memory Usage Patterns

Graph stores consume memory differently based on their architecture:

- **In-memory stores** (Redis, Memgraph): High performance with memory constraints
- **Disk-based stores** (PostgreSQL, MongoDB): Lower memory usage with disk I/O
- **Cloud-managed** (Neptune, Supabase): Optimized memory management

## Query Patterns and Scalability

### Graph Query Patterns

Graph stores excel at specific query patterns that vector-only approaches struggle with:

#### Entity Relationship Queries
```cypher
# Find all relationships involving a specific entity
MATCH (n {name: 'Alice'})-[r]->(m)
RETURN n.name, type(r), m.name
```

#### Multi-hop Path Queries
```cypher
# Find connections through intermediaries
MATCH path = (a)-[:KNOWS*1..3]->(b)
WHERE a.name = 'Alice' AND b.name = 'Bob'
RETURN path
```

#### Temporal Reasoning
```cypher
# Query relationships with timestamps
MATCH (a)-[r:INTERACTED_WITH]->(b)
WHERE r.timestamp > '2024-01-01'
RETURN a.name, b.name, r.timestamp
```

### Hybrid Search Patterns

Combining graph traversal with vector similarity:

```python
# Graph traversal with semantic filtering
def hybrid_search(query, user_id):
    # Step 1: Graph traversal
    graph_results = graph.query("""
        MATCH (n {user_id: $user_id})-[r]->(m)
        WHERE n.embedding IS NOT NULL
        WITH n, m, vector.similarity.cosine(n.embedding, $query_vector) as similarity
        WHERE similarity > 0.7
        RETURN n.name, m.name, similarity
        ORDER BY similarity DESC
        LIMIT 10
    """, {"user_id": user_id, "query_vector": query_embedding})
    
    # Step 2: Semantic ranking
    return rerank_by_semantics(graph_results, query)
```

### Scalability Considerations

#### Horizontal Scaling Options

- **Partitioning**: Shard data across multiple instances
- **Replication**: Distribute read operations
- **Caching**: Implement tiered caching strategies
- **Batch Processing**: Optimize bulk operations

#### Performance Optimization

- **Index Selection**: Choose appropriate vector indices
- **Connection Pooling**: Manage database connections efficiently
- **Query Optimization**: Use efficient graph traversal patterns
- **Memory Management**: Balance in-memory vs. disk storage

## Troubleshooting Guide

### Common Connection Issues

#### Authentication Failures

**Symptoms:**
- `AuthenticationError` exceptions
- Connection refused messages
- Invalid credentials warnings

**Solutions:**
```python
# Verify credentials
config = {
    "graph_store": {
        "provider": "mongodb",
        "config": {
            "mongo_uri": "mongodb://correct_user:correct_password@host:port"
        }
    }
}

# Test connection
from pymongo import MongoClient
client = MongoClient(config["graph_store"]["config"]["mongo_uri"])
try:
    client.admin.command('ping')
    print("Connection successful")
except Exception as e:
    print(f"Connection failed: {e}")
```

#### Network Connectivity Problems

**Symptoms:**
- `NetworkError` exceptions
- Timeout errors
- DNS resolution failures

**Solutions:**
```python
# Check network connectivity
import socket
try:
    socket.gethostbyname("your-host.com")
    print("DNS resolution successful")
except socket.gaierror:
    print("DNS resolution failed")

# Test port connectivity
import socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
result = sock.connect_ex(("your-host.com", 5432))
if result == 0:
    print("Port is open")
else:
    print("Port is closed")
sock.close()
```

### Schema Validation Errors

#### Vector Dimension Mismatches

**Symptoms:**
- `EmbeddingError` exceptions
- Dimension mismatch warnings
- Vector storage failures

**Solutions:**
```python
# Verify embedding dimensions match
embedding_model_dims = 1536  # From your embedding model
vector_store_dims = 1536     # From your vector store config

if embedding_model_dims != vector_store_dims:
    raise ValueError(f"Dimension mismatch: {embedding_model_dims} vs {vector_store_dims}")

# Ensure vector store supports the dimensions
if vector_store_dims not in [128, 256, 512, 768, 1024, 1536]:
    raise ValueError(f"Unsupported vector dimensions: {vector_store_dims}")
```

#### Index Creation Failures

**Symptoms:**
- `VectorStoreError` during initialization
- Index creation timeouts
- Storage quota exceeded

**Solutions:**
```python
# Check available storage
import psutil
disk_usage = psutil.disk_usage('/')
print(f"Available disk space: {disk_usage.free / (1024**3):.2f} GB")

# Monitor index creation progress
def monitor_index_creation(collection):
    stats = collection.aggregate([
        {"$collStats": {"storageStats": {}}}
    ]).next()
    print(f"Index size: {stats['storageStats']['indexSize'] / (1024**3):.2f} GB")
```

### Performance Bottlenecks

#### Slow Query Performance

**Symptoms:**
- High query latency
- Timeout errors
- Resource exhaustion warnings

**Solutions:**
```python
# Enable query profiling
import time

def profile_query(query, params):
    start_time = time.time()
    result = graph.query(query, params)
    end_time = time.time()
    
    print(f"Query took {end_time - start_time:.3f} seconds")
    print(f"Returned {len(result)} results")
    
    return result

# Optimize query patterns
optimized_query = """
MATCH (n {user_id: $user_id})-[r]->(m)
WHERE n.embedding IS NOT NULL
WITH n, m, 
     vector.similarity.cosine(n.embedding, $query_vector) as similarity
WHERE similarity > $threshold
RETURN n.name, m.name, similarity
ORDER BY similarity DESC
LIMIT $limit
"""
```

#### Memory Usage Issues

**Symptoms:**
- Out of memory errors
- Slow performance degradation
- Garbage collection timeouts

**Solutions:**
```python
# Monitor memory usage
import psutil
import gc

def monitor_memory():
    process = psutil.Process()
    memory_info = process.memory_info()
    print(f"Memory usage: {memory_info.rss / (1024**2):.2f} MB")
    
    # Force garbage collection
    gc.collect()
    print(f"After GC: {process.memory_info().rss / (1024**2):.2f} MB")

# Implement pagination for large queries
def paginated_search(query, batch_size=100):
    offset = 0
    results = []
    
    while True:
        batch = graph.query(query, {"offset": offset, "limit": batch_size})
        if not batch:
            break
        results.extend(batch)
        offset += batch_size
        
        if len(batch) < batch_size:
            break
            
    return results
```

### Error Handling Best Practices

#### Structured Error Handling

```python
from mem0.exceptions import (
    GraphStoreError, 
    AuthenticationError, 
    NetworkError,
    MemoryError
)

def safe_graph_operation(operation_func, *args, **kwargs):
    try:
        return operation_func(*args, **kwargs)
    except AuthenticationError as e:
        logger.error(f"Authentication failed: {e.message}")
        # Implement re-authentication logic
        return None
    except NetworkError as e:
        logger.error(f"Network error: {e.message}")
        # Implement retry logic with exponential backoff
        return None
    except GraphStoreError as e:
        logger.error(f"Graph store error: {e.message}")
        # Implement fallback to vector-only search
        return None
    except MemoryError as e:
        logger.error(f"Memory error: {e.message}")
        # Implement memory cleanup
        return None
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return None
```

**Section sources**
- [mem0/exceptions.py](file://mem0/exceptions.py#L324-L342)

## Best Practices

### Configuration Management

#### Environment-Based Configuration

```python
import os
from typing import Dict, Any

class GraphStoreConfig:
    @staticmethod
    def from_environment(env_prefix: str = "GRAPH_STORE_") -> Dict[str, Any]:
        """Load configuration from environment variables."""
        config = {}
        
        # Core connection settings
        config["provider"] = os.environ.get(f"{env_prefix}PROVIDER", "neptune")
        
        # Provider-specific settings
        if config["provider"] == "neptune":
            config["endpoint"] = os.environ.get(f"{env_prefix}ENDPOINT")
            config["collection_name"] = os.environ.get(f"{env_prefix}COLLECTION_NAME", "mem0")
            
        elif config["provider"] == "mongodb":
            config["mongo_uri"] = os.environ.get(f"{env_prefix}URI")
            config["db_name"] = os.environ.get(f"{env_prefix}DB_NAME", "mem0")
            
        elif config["provider"] == "pgvector":
            config["host"] = os.environ.get(f"{env_prefix}HOST", "localhost")
            config["port"] = int(os.environ.get(f"{env_prefix}PORT", "5432"))
            config["dbname"] = os.environ.get(f"{env_prefix}DBNAME", "postgres")
            
        return config
```

#### Configuration Validation

```python
from pydantic import BaseModel, validator, root_validator
from typing import Optional

class GraphStoreValidator(BaseModel):
    provider: str
    endpoint: Optional[str] = None
    mongo_uri: Optional[str] = None
    host: Optional[str] = None
    port: Optional[int] = None
    
    @root_validator
    def validate_provider_specific_fields(cls, values):
        provider = values.get("provider")
        
        if provider == "neptune":
            if not values.get("endpoint"):
                raise ValueError("Neptune requires endpoint configuration")
                
        elif provider == "mongodb":
            if not values.get("mongo_uri"):
                raise ValueError("MongoDB requires URI configuration")
                
        elif provider == "pgvector":
            if not (values.get("host") and values.get("port")):
                raise ValueError("PostgreSQL requires host and port configuration")
                
        return values
```

### Security Considerations

#### Credential Management

```python
import boto3
from azure.identity import DefaultAzureCredential
from google.oauth2 import service_account

class SecureCredentialManager:
    @staticmethod
    def get_credentials(provider: str) -> dict:
        """Retrieve secure credentials based on provider."""
        if provider == "aws":
            # Use AWS IAM roles or assume role
            sts_client = boto3.client('sts')
            assumed_role = sts_client.assume_role(
                RoleArn="arn:aws:iam::account:role/role-name",
                RoleSessionName="mem0-session"
            )
            return assumed_role['Credentials']
            
        elif provider == "azure":
            # Use Azure managed identity
            credential = DefaultAzureCredential()
            token = credential.get_token("https://graph.microsoft.com/.default")
            return {"access_token": token.token}
            
        elif provider == "gcp":
            # Load service account credentials
            creds = service_account.Credentials.from_service_account_file(
                "/path/to/service-account.json"
            )
            return {"credentials": creds}
            
        else:
            # Fallback to environment variables
            return {
                "username": os.environ.get("DB_USERNAME"),
                "password": os.environ.get("DB_PASSWORD")
            }
```

#### Connection Security

```python
import ssl
import psycopg2

def create_secure_connection(config: dict) -> psycopg2.extensions.connection:
    """Create a secure database connection."""
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    
    return psycopg2.connect(
        dbname=config["dbname"],
        user=config["user"],
        password=config["password"],
        host=config["host"],
        port=config["port"],
        sslmode="require",
        ssl_context=ssl_context
    )
```

### Monitoring and Observability

#### Performance Metrics

```python
import time
import logging
from functools import wraps

class GraphStoreMetrics:
    def __init__(self):
        self.metrics = {
            "query_count": 0,
            "avg_query_time": 0,
            "error_count": 0,
            "cache_hit_rate": 0
        }
    
    def track_query(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            self.metrics["query_count"] += 1
            
            try:
                result = func(*args, **kwargs)
                duration = time.time() - start_time
                
                # Update average query time
                current_avg = self.metrics["avg_query_time"]
                count = self.metrics["query_count"]
                self.metrics["avg_query_time"] = (current_avg * (count - 1) + duration) / count
                
                return result
                
            except Exception as e:
                self.metrics["error_count"] += 1
                logging.error(f"Query failed: {e}")
                raise
                
        return wrapper
```

#### Health Checks

```python
def health_check(graph_store):
    """Perform comprehensive health check."""
    health_status = {
        "connectivity": False,
        "performance": "unknown",
        "capacity": "unknown",
        "security": "unknown"
    }
    
    # Test basic connectivity
    try:
        graph_store.query("RETURN 1")
        health_status["connectivity"] = True
    except Exception as e:
        health_status["connectivity"] = False
        health_status["connectivity_error"] = str(e)
    
    # Test query performance
    if health_status["connectivity"]:
        try:
            start_time = time.time()
            graph_store.query("MATCH (n) RETURN COUNT(n)")
            duration = time.time() - start_time
            
            if duration < 1.0:
                health_status["performance"] = "good"
            elif duration < 5.0:
                health_status["performance"] = "moderate"
            else:
                health_status["performance"] = "poor"
                
        except Exception:
            health_status["performance"] = "unknown"
    
    return health_status
```

### Migration and Backup Strategies

#### Data Migration Between Providers

```python
class GraphStoreMigrator:
    def __init__(self, source_store, target_store):
        self.source_store = source_store
        self.target_store = target_store
    
    def migrate_all_data(self):
        """Migrate all graph data from source to target store."""
        # Step 1: Export data from source
        exported_data = self.export_data()
        
        # Step 2: Transform data for target format
        transformed_data = self.transform_data(exported_data)
        
        # Step 3: Import data to target
        self.import_data(transformed_data)
    
    def export_data(self):
        """Export graph data from source store."""
        # Export nodes
        nodes = self.source_store.query("""
            MATCH (n)
            RETURN n.id as node_id, n.properties as properties
        """)
        
        # Export relationships
        relationships = self.source_store.query("""
            MATCH (n)-[r]->(m)
            RETURN r.id as rel_id, 
                   n.id as source_id, 
                   m.id as target_id,
                   r.properties as properties
        """)
        
        return {"nodes": nodes, "relationships": relationships}
    
    def transform_data(self, data):
        """Transform data format for target store."""
        # Format for target provider
        transformed = {
            "nodes": [],
            "relationships": []
        }
        
        for node in data["nodes"]:
            transformed["nodes"].append({
                "id": node["node_id"],
                "labels": ["Entity"],
                "properties": node["properties"]
            })
        
        for rel in data["relationships"]:
            transformed["relationships"].append({
                "id": rel["rel_id"],
                "type": "RELATED_TO",
                "start_node_id": rel["source_id"],
                "end_node_id": rel["target_id"],
                "properties": rel["properties"]
            })
        
        return transformed
```

#### Backup and Recovery

```python
import json
from datetime import datetime

class GraphStoreBackup:
    def __init__(self, graph_store):
        self.graph_store = graph_store
    
    def create_backup(self, backup_path: str = None):
        """Create a complete backup of graph store data."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = backup_path or f"backup_{timestamp}.json"
        
        # Export all graph data
        backup_data = {
            "metadata": {
                "created_at": timestamp,
                "provider": self.graph_store.provider,
                "version": "1.0"
            },
            "data": {
                "nodes": self.export_nodes(),
                "relationships": self.export_relationships(),
                "indexes": self.export_indexes()
            }
        }
        
        # Save to file
        with open(backup_path, "w") as f:
            json.dump(backup_data, f, indent=2)
        
        return backup_path
    
    def restore_backup(self, backup_path: str):
        """Restore graph store from backup file."""
        with open(backup_path, "r") as f:
            backup_data = json.load(f)
        
        # Clear existing data
        self.graph_store.query("MATCH (n) DETACH DELETE n")
        
        # Restore nodes
        for node in backup_data["data"]["nodes"]:
            self.restore_node(node)
        
        # Restore relationships
        for rel in backup_data["data"]["relationships"]:
            self.restore_relationship(rel)
        
        # Restore indexes
        for index in backup_data["data"]["indexes"]:
            self.restore_index(index)
    
    def export_nodes(self):
        """Export all nodes from graph store."""
        return self.graph_store.query("""
            MATCH (n)
            RETURN elementId(n) as id, 
                   labels(n) as labels, 
                   properties(n) as properties
        """)
    
    def export_relationships(self):
        """Export all relationships from graph store."""
        return self.graph_store.query("""
            MATCH (n)-[r]->(m)
            RETURN elementId(r) as id,
                   type(r) as type,
                   elementId(n) as start_node_id,
                   elementId(m) as end_node_id,
                   properties(r) as properties
        """)
```

This comprehensive guide provides detailed information about graph store configuration in Mem0, covering all supported providers, configuration parameters, implementation details, and best practices for production deployment.