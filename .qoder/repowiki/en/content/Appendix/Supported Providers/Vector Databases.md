# Vector Databases

<cite>
**Referenced Files in This Document**   
- [chroma.py](file://mem0/configs/vector_stores/chroma.py)
- [pinecone.py](file://mem0/configs/vector_stores/pinecone.py)
- [qdrant.py](file://mem0/configs/vector_stores/qdrant.py)
- [weaviate.py](file://mem0/configs/vector_stores/weaviate.py)
- [faiss.py](file://mem0/configs/vector_stores/faiss.py)
- [elasticsearch.py](file://mem0/configs/vector_stores/elasticsearch.py)
- [opensearch.py](file://mem0/configs/vector_stores/opensearch.py)
- [pgvector.py](file://mem0/configs/vector_stores/pgvector.py)
- [supabase.py](file://mem0/configs/vector_stores/supabase.py)
- [mongodb.py](file://mem0/configs/vector_stores/mongodb.py)
- [redis.py](file://mem0/configs/vector_stores/redis.py)
- [milvus.py](file://mem0/configs/vector_stores/milvus.py)
- [upstash_vector.py](file://mem0/configs/vector_stores/upstash_vector.py)
- [vertex_ai_vector_search.py](file://mem0/configs/vector_stores/vertex_ai_vector_search.py)
- [azure_ai_search.py](file://mem0/configs/vector_stores/azure_ai_search.py)
- [databricks.py](file://mem0/configs/vector_stores/databricks.py)
- [baidu.py](file://mem0/configs/vector_stores/baidu.py)
- [azure_mysql.py](file://mem0/configs/vector_stores/azure_mysql.py)
- [langchain.py](file://mem0/configs/vector_stores/langchain.py)
- [s3_vectors.py](file://mem0/configs/vector_stores/s3_vectors.py)
- [valkey.py](file://mem0/configs/vector_stores/valkey.py)
</cite>

## Table of Contents
1. [Introduction](#introduction)
2. [Qdrant](#qdrant)
3. [Chroma](#chroma)
4. [Pinecone](#pinecone)
5. [Weaviate](#weaviate)
6. [FAISS](#faiss)
7. [Elasticsearch](#elasticsearch)
8. [OpenSearch](#opensearch)
9. [PGVector](#pgvector)
10. [Supabase](#supabase)
11. [MongoDB](#mongodb)
12. [Redis](#redis)
13. [Milvus](#milvus)
14. [Upstash](#upstash)
15. [Vertex AI Vector Search](#vertex-ai-vector-search)
16. [Azure AI Search](#azure-ai-search)
17. [Databricks](#databricks)
18. [Baidu](#baidu)
19. [Azure MySQL](#azure-mysql)
20. [LangChain](#langchain)
21. [S3 Vectors](#s3-vectors)
22. [Valkey](#valkey)

## Introduction
This document provides comprehensive documentation for all vector database providers supported by Mem0. Each section details the configuration parameters, authentication methods, connection setup, and performance characteristics for the respective vector database. The documentation includes Python code examples for configuration via config objects and environment variables, outlines use cases where each database excels, discusses scalability considerations, and highlights known limitations. Additionally, it addresses common connection issues, troubleshooting steps, and differences between cloud-hosted and self-managed deployments.

## Qdrant
Qdrant is a vector similarity search engine with extended filtering support. It is designed for efficient similarity search and storage of embedding vectors.

**Configuration Parameters**
- `collection_name`: Name of the collection (default: "mem0")
- `embedding_model_dims`: Dimensions of the embedding model (default: 1536)
- `client`: Existing Qdrant client instance
- `host`: Host address for Qdrant server
- `port`: Port for Qdrant server
- `path`: Path for local Qdrant database (default: "/tmp/qdrant")
- `url`: Full URL for Qdrant server
- `api_key`: API key for Qdrant server
- `on_disk`: Enables persistent storage (default: False)

**Authentication Methods**
Qdrant supports authentication via API key when connecting to a remote server. For local deployments, no authentication is required.

**Connection Setup**
Connection can be established using either:
- Host and port for local or self-managed instances
- URL and API key for cloud-hosted instances
- Path for local file-based storage

```python
from mem0.configs.vector_stores.qdrant import QdrantConfig

# Configuration via config object
config = QdrantConfig(
    collection_name="my_collection",
    host="localhost",
    port=6333,
    api_key="your-api-key"
)

# Configuration via environment variables
import os
os.environ["QDRANT_HOST"] = "localhost"
os.environ["QDRANT_PORT"] = "6333"
os.environ["QDRANT_API_KEY"] = "your-api-key"
```

**Performance Characteristics**
Qdrant offers high-performance vector search with support for approximate nearest neighbor search algorithms. It performs well with large datasets and supports efficient filtering operations.

**Use Cases**
- Large-scale similarity search applications
- Recommendation systems requiring complex filtering
- Applications needing persistent vector storage

**Scalability Considerations**
Qdrant scales horizontally and can handle large vector datasets efficiently. It supports distributed deployments for high availability and load balancing.

**Known Limitations**
- Requires careful tuning of HNSW parameters for optimal performance
- Memory usage can be high for very large datasets

**Common Connection Issues and Troubleshooting**
- Ensure the Qdrant server is running when using host/port configuration
- Verify API key validity for cloud instances
- Check network connectivity between client and server

**Cloud vs Self-Managed Differences**
Cloud-hosted Qdrant provides managed infrastructure with automatic scaling, while self-managed deployments offer more control over configuration and data locality.

**Section sources**
- [qdrant.py](file://mem0/configs/vector_stores/qdrant.py#L6-L48)

## Chroma
Chroma is a lightweight, open-source vector database designed for AI applications with a focus on developer experience.

**Configuration Parameters**
- `collection_name`: Default name for the collection/database (default: "mem0")
- `client`: Existing ChromaDB client instance
- `path`: Path to the database directory
- `host`: Database connection remote host
- `port`: Database connection remote port
- `api_key`: ChromaDB Cloud API key
- `tenant`: ChromaDB Cloud tenant ID

**Authentication Methods**
For cloud deployments, authentication is handled via API key and tenant ID. Local deployments do not require authentication.

**Connection Setup**
Chroma supports three connection modes:
- Local: Using a file system path
- Server: Using host and port
- Cloud: Using API key and tenant ID

```python
from mem0.configs.vector_stores.chroma import ChromaDbConfig

# Configuration via config object
config = ChromaDbConfig(
    collection_name="my_collection",
    path="/path/to/chroma/db",
    api_key="your-api-key",
    tenant="your-tenant-id"
)

# Configuration via environment variables
import os
os.environ["CHROMA_PATH"] = "/path/to/chroma/db"
os.environ["CHROMA_API_KEY"] = "your-api-key"
os.environ["CHROMA_TENANT"] = "your-tenant-id"
```

**Performance Characteristics**
Chroma provides fast in-memory search capabilities with persistence options. It is optimized for small to medium-sized datasets and prototyping.

**Use Cases**
- Rapid prototyping of AI applications
- Small to medium-scale vector search needs
- Development and testing environments

**Scalability Considerations**
Chroma is best suited for single-node deployments. For larger scale requirements, consider distributed vector databases.

**Known Limitations**
- Limited scalability for very large datasets
- Fewer enterprise features compared to commercial offerings

**Common Connection Issues and Troubleshooting**
- Ensure only one connection method is specified (local, server, or cloud)
- Verify cloud credentials are correct
- Check file permissions when using local path storage

**Cloud vs Self-Managed Differences**
Chroma Cloud provides managed infrastructure with automatic backups, while self-managed instances offer complete data control and on-premises deployment options.

**Section sources**
- [chroma.py](file://mem0/configs/vector_stores/chroma.py#L6-L59)

## Pinecone
Pinecone is a fully managed vector database service designed for production AI applications with automatic scaling.

**Configuration Parameters**
- `collection_name`: Name of the index/collection (default: "mem0")
- `embedding_model_dims`: Dimensions of the embedding model (default: 1536)
- `client`: Existing Pinecone client instance
- `api_key`: API key for Pinecone
- `environment`: Pinecone environment
- `serverless_config`: Configuration for serverless deployment
- `pod_config`: Configuration for pod-based deployment
- `hybrid_search`: Enable hybrid search (default: False)
- `metric`: Distance metric for vector similarity (default: "cosine")
- `batch_size`: Batch size for operations (default: 100)
- `extra_params`: Additional parameters for Pinecone client
- `namespace`: Namespace for the collection

**Authentication Methods**
Authentication is performed using an API key, which can be provided directly or via the PINECONE_API_KEY environment variable.

**Connection Setup**
Pinecone supports both serverless and pod-based deployments. Configuration requires either an API key or an existing client instance.

```python
from mem0.configs.vector_stores.pinecone import PineconeConfig

# Configuration via config object
config = PineconeConfig(
    collection_name="my_index",
    api_key="your-api-key",
    environment="us-west1-gcp",
    serverless_config={"cloud": "aws", "region": "us-west-2"}
)

# Configuration via environment variables
import os
os.environ["PINECONE_API_KEY"] = "your-api-key"
os.environ["PINECONE_ENVIRONMENT"] = "us-west1-gcp"
```

**Performance Characteristics**
Pinecone offers low-latency search with automatic indexing and scaling. It handles high query volumes efficiently and provides consistent performance.

**Use Cases**
- Production AI applications requiring high availability
- Applications with variable query loads
- Enterprise-scale vector search needs

**Scalability Considerations**
Pinecone automatically scales to handle varying workloads. Serverless deployments scale automatically, while pod-based deployments allow for capacity planning.

**Known Limitations**
- Cost can increase significantly with high usage
- Limited control over underlying infrastructure

**Common Connection Issues and Troubleshooting**
- Ensure API key has appropriate permissions
- Verify environment name matches the deployment region
- Check network connectivity to Pinecone endpoints

**Cloud vs Self-Managed Differences**
Pinecone is exclusively a cloud-hosted service with no self-managed option, providing a fully managed experience with automatic updates and maintenance.

**Section sources**
- [pinecone.py](file://mem0/configs/vector_stores/pinecone.py#L7-L56)

## Weaviate
Weaviate is an open-source vector database with built-in semantic search capabilities and a GraphQL interface.

**Configuration Parameters**
- `collection_name`: Name of the collection (default: "mem0")
- `embedding_model_dims`: Dimensions of the embedding model (default: 1536)
- `cluster_url`: URL for Weaviate server
- `auth_client_secret`: API key for Weaviate authentication
- `additional_headers`: Additional headers for requests

**Authentication Methods**
Weaviate supports API key authentication through the auth_client_secret parameter.

**Connection Setup**
Connection requires the cluster URL and authentication credentials.

```python
from mem0.configs.vector_stores.weaviate import WeaviateConfig

# Configuration via config object
config = WeaviateConfig(
    collection_name="my_collection",
    cluster_url="https://your-cluster.weaviate.cloud",
    auth_client_secret="your-api-key"
)

# Configuration via environment variables
import os
os.environ["WEAVIATE_CLUSTER_URL"] = "https://your-cluster.weaviate.cloud"
os.environ["WEAVIATE_API_KEY"] = "your-api-key"
```

**Performance Characteristics**
Weaviate provides fast vector search with additional semantic search capabilities. It supports hybrid search combining vector and keyword-based approaches.

**Use Cases**
- Applications requiring hybrid search capabilities
- Knowledge graphs with vector search
- Semantic search applications

**Scalability Considerations**
Weaviate scales horizontally and supports distributed deployments. It can handle large datasets with proper resource allocation.

**Known Limitations**
- Resource requirements can be high for large deployments
- Complex queries may require optimization

**Common Connection Issues and Troubleshooting**
- Ensure cluster URL is accessible
- Verify API key has appropriate permissions
- Check SSL/TLS configuration for secure connections

**Cloud vs Self-Managed Differences**
Weaviate offers both cloud-hosted and self-managed deployment options, with the cloud version providing managed infrastructure and the self-managed version offering complete control.

**Section sources**
- [weaviate.py](file://mem0/configs/vector_stores/weaviate.py#L6-L42)

## FAISS
FAISS (Facebook AI Similarity Search) is a library for efficient similarity search and clustering of dense vectors.

**Configuration Parameters**
- `collection_name`: Default name for the collection (default: "mem0")
- `path`: Path to store FAISS index and metadata
- `distance_strategy`: Distance strategy to use ("euclidean", "inner_product", "cosine") (default: "euclidean")
- `normalize_L2`: Whether to normalize L2 vectors (default: False)
- `embedding_model_dims`: Dimension of the embedding vector (default: 1536)

**Authentication Methods**
FAISS is a local library with no authentication requirements.

**Connection Setup**
FAISS operates on local files and does not require network connections.

```python
from mem0.configs.vector_stores.faiss import FAISSConfig

# Configuration via config object
config = FAISSConfig(
    collection_name="my_index",
    path="/path/to/faiss/index",
    distance_strategy="cosine",
    normalize_L2=True
)

# Configuration via environment variables
import os
os.environ["FAISS_PATH"] = "/path/to/faiss/index"
```

**Performance Characteristics**
FAISS provides extremely fast search performance, especially for exact nearest neighbor search. It is optimized for memory efficiency and speed.

**Use Cases**
- High-performance similarity search
- Offline applications without network connectivity
- Applications requiring maximum search speed

**Scalability Considerations**
FAISS is best suited for single-machine deployments. For distributed search, consider other vector databases.

**Known Limitations**
- Limited to single-machine deployments
- No built-in persistence or replication
- Requires manual index management

**Common Connection Issues and Troubleshooting**
- Ensure sufficient disk space for index storage
- Verify file permissions for index files
- Check memory availability for large indexes

**Cloud vs Self-Managed Differences**
FAISS is exclusively self-managed as it is a library rather than a service, requiring local deployment and management.

**Section sources**
- [faiss.py](file://mem0/configs/vector_stores/faiss.py#L6-L38)

## Elasticsearch
Elasticsearch is a distributed search and analytics engine that supports vector search capabilities.

**Configuration Parameters**
- `collection_name`: Name of the index (default: "mem0")
- `host`: Elasticsearch host (default: "localhost")
- `port`: Elasticsearch port (default: 9200)
- `user`: Username for authentication
- `password`: Password for authentication
- `cloud_id`: Cloud ID for Elastic Cloud
- `api_key`: API key for authentication
- `embedding_model_dims`: Dimension of the embedding vector (default: 1536)
- `verify_certs`: Verify SSL certificates (default: True)
- `use_ssl`: Use SSL for connection (default: True)
- `auto_create_index`: Automatically create index during initialization (default: True)
- `custom_search_query`: Custom search query function
- `headers`: Custom headers to include in requests

**Authentication Methods**
Elasticsearch supports multiple authentication methods including basic auth (user/password), API keys, and cloud ID for Elastic Cloud.

**Connection Setup**
Configuration requires either host/port for self-managed instances or cloud_id for Elastic Cloud.

```python
from mem0.configs.vector_stores.elasticsearch import ElasticsearchConfig

# Configuration via config object
config = ElasticsearchConfig(
    collection_name="my_index",
    host="localhost",
    port=9200,
    user="elastic",
    password="your-password",
    use_ssl=True,
    verify_certs=True
)

# Configuration via environment variables
import os
os.environ["ELASTICSEARCH_HOST"] = "localhost"
os.environ["ELASTICSEARCH_PORT"] = "9200"
os.environ["ELASTICSEARCH_USER"] = "elastic"
os.environ["ELASTICSEARCH_PASSWORD"] = "your-password"
```

**Performance Characteristics**
Elasticsearch provides robust search capabilities with good performance for vector search. It excels at hybrid search combining vector and full-text search.

**Use Cases**
- Applications requiring hybrid search capabilities
- Existing Elasticsearch users adding vector search
- Enterprise search applications

**Scalability Considerations**
Elasticsearch scales horizontally and can handle large datasets across multiple nodes. Proper cluster sizing is essential for performance.

**Known Limitations**
- Resource intensive compared to specialized vector databases
- Complex configuration for optimal vector search performance

**Common Connection Issues and Troubleshooting**
- Ensure authentication credentials are correct
- Verify network connectivity to Elasticsearch nodes
- Check SSL/TLS configuration for secure connections

**Cloud vs Self-Managed Differences**
Elastic Cloud provides managed infrastructure with automated operations, while self-managed deployments offer complete control over configuration and infrastructure.

**Section sources**
- [elasticsearch.py](file://mem0/configs/vector_stores/elasticsearch.py#L7-L66)

## OpenSearch
OpenSearch is an open-source fork of Elasticsearch that supports vector search capabilities.

**Configuration Parameters**
- `collection_name`: Name of the index (default: "mem0")
- `host`: OpenSearch host (default: "localhost")
- `port`: OpenSearch port (default: 9200)
- `user`: Username for authentication
- `password`: Password for authentication
- `api_key`: API key for authentication
- `embedding_model_dims`: Dimension of the embedding vector (default: 1536)
- `verify_certs`: Verify SSL certificates (default: False)
- `use_ssl`: Use SSL for connection (default: False)
- `http_auth`: HTTP authentication method / AWS SigV4
- `connection_class`: Connection class for OpenSearch (default: "RequestsHttpConnection")
- `pool_maxsize`: Maximum number of connections in the pool (default: 20)

**Authentication Methods**
OpenSearch supports basic authentication (user/password), API keys, and AWS SigV4 for AWS deployments.

**Connection Setup**
Configuration requires host and port for connection to the OpenSearch cluster.

```python
from mem0.configs.vector_stores.opensearch import OpenSearchConfig

# Configuration via config object
config = OpenSearchConfig(
    collection_name="my_index",
    host="localhost",
    port=9200,
    user="admin",
    password="your-password",
    use_ssl=True,
    verify_certs=False
)

# Configuration via environment variables
import os
os.environ["OPENSEARCH_HOST"] = "localhost"
os.environ["OPENSEARCH_PORT"] = "9200"
os.environ["OPENSEARCH_USER"] = "admin"
os.environ["OPENSEARCH_PASSWORD"] = "your-password"
```

**Performance Characteristics**
OpenSearch provides solid vector search performance with good scalability. It supports approximate k-nearest neighbor search for large datasets.

**Use Cases**
- Open-source alternative to Elasticsearch
- Applications requiring vector and full-text search
- AWS deployments using OpenSearch Service

**Scalability Considerations**
OpenSearch scales horizontally across multiple nodes. Performance depends on proper cluster configuration and resource allocation.

**Known Limitations**
- SSL verification is disabled by default
- Fewer managed service options compared to Elasticsearch

**Common Connection Issues and Troubleshooting**
- Ensure authentication credentials are correct
- Verify network connectivity to OpenSearch nodes
- Check firewall rules for required ports

**Cloud vs Self-Managed Differences**
OpenSearch Service on AWS provides managed infrastructure, while self-managed deployments offer complete control over the environment.

**Section sources**
- [opensearch.py](file://mem0/configs/vector_stores/opensearch.py#L6-L42)

## PGVector
PGVector is an extension for PostgreSQL that adds vector similarity search capabilities.

**Configuration Parameters**
- `dbname`: Name for the database (default: "postgres")
- `collection_name`: Name for the collection (default: "mem0")
- `embedding_model_dims`: Dimensions of the embedding model (default: 1536)
- `user`: Database user
- `password`: Database password
- `host`: Database host (default: localhost)
- `port`: Database port (default: 1536)
- `diskann`: Use diskann for approximate nearest neighbors search (default: False)
- `hnsw`: Use hnsw for faster search (default: True)
- `minconn`: Minimum number of connections in the pool (default: 1)
- `maxconn`: Maximum number of connections in the pool (default: 5)
- `sslmode`: SSL mode for PostgreSQL connection
- `connection_string`: PostgreSQL connection string
- `connection_pool`: psycopg connection pool object

**Authentication Methods**
Authentication uses standard PostgreSQL authentication with username and password.

**Connection Setup**
Connection can be established using individual parameters or a connection string.

```python
from mem0.configs.vector_stores.pgvector import PGVectorConfig

# Configuration via config object
config = PGVectorConfig(
    dbname="mydb",
    collection_name="my_collection",
    user="postgres",
    password="your-password",
    host="localhost",
    port=5432,
    hnsw=True
)

# Configuration via connection string
config = PGVectorConfig(
    connection_string="postgresql://user:password@localhost:5432/mydb",
    collection_name="my_collection"
)

# Configuration via environment variables
import os
os.environ["POSTGRES_USER"] = "postgres"
os.environ["POSTGRES_PASSWORD"] = "your-password"
os.environ["POSTGRES_HOST"] = "localhost"
os.environ["POSTGRES_PORT"] = "5432"
os.environ["POSTGRES_DB"] = "mydb"
```

**Performance Characteristics**
PGVector leverages PostgreSQL's robust infrastructure for reliable vector search. Performance depends on proper indexing and hardware resources.

**Use Cases**
- Applications already using PostgreSQL
- Organizations preferring a single database for structured and vector data
- Applications requiring ACID transactions with vector search

**Scalability Considerations**
Scalability follows PostgreSQL's capabilities, including replication and partitioning. Performance scales with hardware and proper indexing.

**Known Limitations**
- Requires PostgreSQL installation and PGVector extension
- Performance may not match specialized vector databases for large-scale search

**Common Connection Issues and Troubleshooting**
- Ensure PGVector extension is installed in the database
- Verify PostgreSQL credentials and permissions
- Check network connectivity to the database server

**Cloud vs Self-Managed Differences**
Available as a self-managed extension or through cloud providers offering PostgreSQL with PGVector support.

**Section sources**
- [pgvector.py](file://mem0/configs/vector_stores/pgvector.py#L6-L53)

## Supabase
Supabase is an open-source Firebase alternative that includes vector search capabilities through its PostgreSQL backend.

**Configuration Parameters**
- `connection_string`: PostgreSQL connection string
- `collection_name`: Name for the vector collection (default: "mem0")
- `embedding_model_dims`: Dimensions of the embedding model (default: 1536)
- `index_method`: Index method to use (AUTO, HNSW, IVFFLAT) (default: AUTO)
- `index_measure`: Distance measure to use (cosine_distance, l2_distance, l1_distance, max_inner_product) (default: cosine_distance)

**Authentication Methods**
Authentication is handled through the PostgreSQL connection string with username and password.

**Connection Setup**
Requires a valid PostgreSQL connection string pointing to a Supabase project.

```python
from mem0.configs.vector_stores.supabase import SupabaseConfig

# Configuration via config object
config = SupabaseConfig(
    connection_string="postgresql://user:password@db.supabase.com:5432/postgres",
    collection_name="my_collection",
    index_method="HNSW",
    index_measure="cosine_distance"
)

# Configuration via environment variables
import os
os.environ["SUPABASE_CONNECTION_STRING"] = "postgresql://user:password@db.supabase.com:5432/postgres"
```

**Performance Characteristics**
Supabase vector search performance depends on the underlying PostgreSQL instance size and configuration. It provides reliable performance for most use cases.

**Use Cases**
- Applications already using Supabase
- Developers preferring a full-stack open-source solution
- Projects requiring both structured and vector data storage

**Scalability Considerations**
Scalability follows Supabase's infrastructure, with different pricing tiers offering varying performance levels.

**Known Limitations**
- Performance tied to Supabase plan limitations
- Less control over underlying infrastructure compared to self-managed PostgreSQL

**Common Connection Issues and Troubleshooting**
- Ensure connection string format is correct
- Verify database credentials and permissions
- Check network connectivity to Supabase endpoints

**Cloud vs Self-Managed Differences**
Supabase is exclusively a cloud-hosted service with no self-managed option, providing a fully managed database experience.

**Section sources**
- [supabase.py](file://mem0/configs/vector_stores/supabase.py#L20-L45)

## MongoDB
MongoDB is a NoSQL document database that supports vector search capabilities.

**Configuration Parameters**
- `db_name`: Name of the MongoDB database (default: "mem0_db")
- `collection_name`: Name of the MongoDB collection (default: "mem0")
- `embedding_model_dims`: Dimensions of the embedding vectors (default: 1536)
- `mongo_uri`: MongoDB URI (default: "mongodb://localhost:27017")

**Authentication Methods**
Authentication is handled through the MongoDB URI, which can include username and password.

**Connection Setup**
Requires a MongoDB URI for connection to the database instance.

```python
from mem0.configs.vector_stores.mongodb import MongoDBConfig

# Configuration via config object
config = MongoDBConfig(
    db_name="mydb",
    collection_name="my_collection",
    mongo_uri="mongodb://user:password@localhost:27017/mydb"
)

# Configuration via environment variables
import os
os.environ["MONGODB_URI"] = "mongodb://user:password@localhost:27017/mydb"
```

**Performance Characteristics**
MongoDB provides solid vector search performance with good scalability. Performance depends on proper indexing and sharding configuration.

**Use Cases**
- Applications already using MongoDB
- Projects requiring flexible schema with vector search
- Document-based applications needing similarity search

**Scalability Considerations**
MongoDB scales horizontally through sharding and replication. Vector search performance scales with proper index configuration.

**Known Limitations**
- Vector search capabilities are relatively new in MongoDB
- May require additional configuration for optimal performance

**Common Connection Issues and Troubleshooting**
- Ensure MongoDB URI format is correct
- Verify database credentials and permissions
- Check network connectivity to MongoDB instances

**Cloud vs Self-Managed Differences**
Available through MongoDB Atlas (cloud) or self-managed deployments, with Atlas providing managed infrastructure and automated operations.

**Section sources**
- [mongodb.py](file://mem0/configs/vector_stores/mongodb.py#L6-L26)

## Redis
Redis is an in-memory data structure store that supports vector search through its Redis Stack extension.

**Configuration Parameters**
- `redis_url`: Redis URL
- `collection_name`: Collection name (default: "mem0")
- `embedding_model_dims`: Embedding model dimensions (default: 1536)

**Authentication Methods**
Authentication is handled through the Redis URL, which can include username and password.

**Connection Setup**
Requires a Redis URL for connection to the Redis instance.

```python
from mem0.configs.vector_stores.redis import RedisDBConfig

# Configuration via config object
config = RedisDBConfig(
    redis_url="redis://user:password@localhost:6379",
    collection_name="my_collection"
)

# Configuration via environment variables
import os
os.environ["REDIS_URL"] = "redis://user:password@localhost:6379"
```

**Performance Characteristics**
Redis provides extremely fast vector search due to its in-memory nature. It offers sub-millisecond latency for queries.

**Use Cases**
- Applications requiring ultra-low latency search
- Caching layers with vector search capabilities
- Real-time recommendation systems

**Scalability Considerations**
Redis scales through clustering and can handle high query volumes. Memory capacity limits the dataset size.

**Known Limitations**
- Dataset size limited by available memory
- Persistence options may impact performance
- Requires careful memory management

**Common Connection Issues and Troubleshooting**
- Ensure Redis Stack is installed with vector search capabilities
- Verify Redis URL format and credentials
- Check memory availability for large datasets

**Cloud vs Self-Managed Differences**
Available through various cloud providers (AWS ElastiCache, Google Memorystore, Azure Cache) or self-managed deployments.

**Section sources**
- [redis.py](file://mem0/configs/vector_stores/redis.py#L7-L25)

## Milvus
Milvus is an open-source vector database built for scalable similarity search.

**Configuration Parameters**
- `url`: Full URL for Milvus/Zilliz server (default: "http://localhost:19530")
- `token`: Token for Zilliz server (default: None)
- `collection_name`: Name of the collection (default: "mem0")
- `embedding_model_dims`: Dimensions of the embedding model (default: 1536)
- `metric_type`: Metric type for similarity search (default: "L2")
- `db_name`: Name of the database (default: "")

**Authentication Methods**
Authentication is handled through tokens for Zilliz cloud instances.

**Connection Setup**
Requires URL and optional token for connection to Milvus or Zilliz instances.

```python
from mem0.configs.vector_stores.milvus import MilvusDBConfig

# Configuration via config object
config = MilvusDBConfig(
    url="http://localhost:19530",
    token="your-token",
    collection_name="my_collection",
    metric_type="COSINE"
)

# Configuration via environment variables
import os
os.environ["MILVUS_URL"] = "http://localhost:19530"
os.environ["MILVUS_TOKEN"] = "your-token"
```

**Performance Characteristics**
Milvus provides high-performance vector search with support for large-scale datasets. It is optimized for distributed environments.

**Use Cases**
- Large-scale similarity search applications
- Enterprise AI applications
- Applications requiring high query throughput

**Scalability Considerations**
Milvus is designed for horizontal scalability and can handle massive datasets across distributed clusters.

**Known Limitations**
- Complex deployment and management
- Resource intensive for large deployments

**Common Connection Issues and Troubleshooting**
- Ensure Milvus server is running and accessible
- Verify token validity for Zilliz cloud
- Check network connectivity and firewall rules

**Cloud vs Self-Managed Differences**
Available as Zilliz Cloud (managed) or self-managed Milvus, with Zilliz providing automated operations and Milvus offering complete control.

**Section sources**
- [milvus.py](file://mem0/configs/vector_stores/milvus.py#L22-L43)

## Upstash
Upstash is a serverless data platform that includes a vector database service.

**Configuration Parameters**
- `url`: URL for Upstash Vector index
- `token`: Token for Upstash Vector index
- `client`: Existing upstash_vector.Index client instance
- `collection_name`: Namespace to use for the index (default: "mem0")
- `enable_embeddings`: Whether to use built-in upstash embeddings (default: False)

**Authentication Methods**
Authentication is handled through URL and token, or via environment variables UPSTASH_VECTOR_REST_URL and UPSTASH_VECTOR_REST_TOKEN.

**Connection Setup**
Requires either a client instance or URL and token for authentication.

```python
from mem0.configs.vector_stores.upstash_vector import UpstashVectorConfig

# Configuration via config object
config = UpstashVectorConfig(
    url="https://your-upstash-url.upstash.io",
    token="your-token",
    collection_name="my_namespace"
)

# Configuration via environment variables
import os
os.environ["UPSTASH_VECTOR_REST_URL"] = "https://your-upstash-url.upstash.io"
os.environ["UPSTASH_VECTOR_REST_TOKEN"] = "your-token"
```

**Performance Characteristics**
Upstash provides low-latency vector search with serverless scaling. Performance is consistent across different load levels.

**Use Cases**
- Serverless applications
- Applications with variable query patterns
- Projects requiring minimal infrastructure management

**Scalability Considerations**
Upstash automatically scales to handle varying workloads without manual intervention.

**Known Limitations**
- Limited control over underlying infrastructure
- Pricing based on usage which can vary

**Common Connection Issues and Troubleshooting**
- Ensure URL and token are correct
- Verify environment variables are set properly
- Check network connectivity to Upstash endpoints

**Cloud vs Self-Managed Differences**
Upstash is exclusively a cloud-hosted service with no self-managed option, providing a fully serverless experience.

**Section sources**
- [upstash_vector.py](file://mem0/configs/vector_stores/upstash_vector.py#L12-L35)

## Vertex AI Vector Search
Vertex AI Vector Search is Google Cloud's managed vector database service.

**Configuration Parameters**
- `project_id`: Google Cloud project ID
- `project_number`: Google Cloud project number
- `region`: Google Cloud region
- `endpoint_id`: Vertex AI Vector Search endpoint ID
- `index_id`: Vertex AI Vector Search index ID
- `deployment_index_id`: Deployment-specific index ID
- `collection_name`: Collection name (defaults to index_id)
- `credentials_path`: Path to service account credentials file
- `vector_search_api_endpoint`: Vector search API endpoint

**Authentication Methods**
Authentication is handled through Google Cloud service account credentials, either via credentials file or default application credentials.

**Connection Setup**
Requires Google Cloud project information and authentication credentials.

```python
from mem0.configs.vector_stores.vertex_ai_vector_search import GoogleMatchingEngineConfig

# Configuration via config object
config = GoogleMatchingEngineConfig(
    project_id="my-project",
    project_number="123456789",
    region="us-central1",
    endpoint_id="my-endpoint",
    index_id="my-index",
    deployment_index_id="my-deployment-index"
)

# Configuration via environment variables
import os
os.environ["GOOGLE_PROJECT_ID"] = "my-project"
os.environ["GOOGLE_PROJECT_NUMBER"] = "123456789"
os.environ["GOOGLE_REGION"] = "us-central1"
```

**Performance Characteristics**
Vertex AI Vector Search provides high-performance, scalable vector search with Google Cloud's infrastructure reliability.

**Use Cases**
- Applications within the Google Cloud ecosystem
- Enterprise applications requiring high availability
- Projects already using Google Cloud services

**Scalability Considerations**
Fully managed service that automatically scales to handle varying workloads.

**Known Limitations**
- Vendor lock-in to Google Cloud
- Limited to Google Cloud regions

**Common Connection Issues and Troubleshooting**
- Ensure service account has appropriate permissions
- Verify project IDs and region are correct
- Check authentication credentials are properly configured

**Cloud vs Self-Managed Differences**
Exclusively a cloud-hosted service as part of Google Cloud Platform, with no self-managed option.

**Section sources**
- [vertex_ai_vector_search.py](file://mem0/configs/vector_stores/vertex_ai_vector_search.py#L6-L28)

## Azure AI Search
Azure AI Search is Microsoft's cloud search service with vector search capabilities.

**Configuration Parameters**
- `collection_name`: Name of the collection (default: "mem0")
- `service_name`: Azure AI Search service name
- `api_key`: API key for the Azure AI Search service
- `embedding_model_dims`: Dimension of the embedding vector (default: 1536)
- `compression_type`: Type of vector compression to use ("scalar", "binary", or None)
- `use_float16`: Store vectors in half precision (default: False)
- `hybrid_search`: Use hybrid search (default: False)
- `vector_filter_mode`: Mode for vector filtering ("preFilter", "postFilter")

**Authentication Methods**
Authentication is handled through API keys.

**Connection Setup**
Requires service name and API key for authentication.

```python
from mem0.configs.vector_stores.azure_ai_search import AzureAISearchConfig

# Configuration via config object
config = AzureAISearchConfig(
    service_name="my-search-service",
    api_key="your-api-key",
    collection_name="my-collection",
    hybrid_search=True,
    compression_type="scalar"
)

# Configuration via environment variables
import os
os.environ["AZURE_SEARCH_SERVICE_NAME"] = "my-search-service"
os.environ["AZURE_SEARCH_API_KEY"] = "your-api-key"
```

**Performance Characteristics**
Azure AI Search provides reliable vector search performance with enterprise-grade reliability and scalability.

**Use Cases**
- Applications within the Microsoft Azure ecosystem
- Enterprise applications requiring compliance and security
- Hybrid search applications combining vector and full-text search

**Scalability Considerations**
Scales automatically within Azure's infrastructure, with different pricing tiers for varying performance needs.

**Known Limitations**
- Vendor lock-in to Azure
- Complex pricing structure

**Common Connection Issues and Troubleshooting**
- Ensure API key has appropriate permissions
- Verify service name and region
- Check network connectivity to Azure endpoints

**Cloud vs Self-Managed Differences**
Exclusively a cloud-hosted service as part of Microsoft Azure, with no self-managed option.

**Section sources**
- [azure_ai_search.py](file://mem0/configs/vector_stores/azure_ai_search.py#L6-L58)

## Databricks
Databricks provides vector search capabilities within its data intelligence platform.

**Configuration Parameters**
- Standard Databricks connection parameters including host, token, and catalog information
- Vector search-specific configurations for index creation and management

**Authentication Methods**
Authentication through Databricks personal access tokens or OAuth.

**Connection Setup**
Requires Databricks workspace URL and authentication token.

```python
# Databricks configuration follows standard Databricks connection patterns
# with additional vector search index configuration
```

**Performance Characteristics**
Leverages Databricks' optimized data processing engine for vector search, with performance tied to cluster configuration.

**Use Cases**
- Applications already using Databricks for data processing
- Data science workflows requiring vector search
- Lakehouse architecture implementations

**Scalability Considerations**
Scales with Databricks cluster configuration and autoscaling capabilities.

**Known Limitations**
- Tied to Databricks ecosystem
- Cost can be high for large-scale deployments

**Common Connection Issues and Troubleshooting**
- Ensure Databricks token has appropriate permissions
- Verify workspace URL is correct
- Check network connectivity to Databricks workspace

**Cloud vs Self-Managed Differences**
Databricks is a cloud-native platform with no self-managed option, hosted on major cloud providers.

**Section sources**
- [databricks.py](file://mem0/configs/vector_stores/databricks.py)

## Baidu
Baidu offers vector database services as part of its cloud platform.

**Configuration Parameters**
- Baidu Cloud-specific parameters including AK/SK authentication
- Service endpoint and region information
- Vector index configuration parameters

**Authentication Methods**
Authentication through Baidu Cloud Access Key and Secret Key.

**Connection Setup**
Requires Baidu Cloud credentials and service endpoint information.

```python
# Baidu vector database configuration uses Baidu Cloud authentication
# and service-specific parameters
```

**Performance Characteristics**
Provides high-performance vector search with Baidu Cloud's infrastructure.

**Use Cases**
- Applications targeting Chinese market
- Projects requiring compliance with Chinese data regulations
- Multi-cloud strategies including Baidu Cloud

**Scalability Considerations**
Scales within Baidu Cloud's infrastructure with regional limitations.

**Known Limitations**
- Limited outside China
- Language and documentation primarily in Chinese

**Common Connection Issues and Troubleshooting**
- Ensure AK/SK credentials are correct
- Verify service endpoint and region
- Check network connectivity to Baidu Cloud

**Cloud vs Self-Managed Differences**
Exclusively a cloud-hosted service as part of Baidu Cloud, with no self-managed option.

**Section sources**
- [baidu.py](file://mem0/configs/vector_stores/baidu.py)

## Azure MySQL
Azure MySQL with vector search extensions.

**Configuration Parameters**
- Standard MySQL connection parameters (host, port, user, password)
- Database and table configuration for vector storage
- Indexing parameters for vector columns

**Authentication Methods**
Standard MySQL authentication with username and password.

**Connection Setup**
Requires MySQL connection string with Azure-specific endpoint.

```python
# Azure MySQL vector configuration follows standard MySQL patterns
# with Azure-specific connection details
```

**Performance Characteristics**
Performance depends on MySQL configuration and indexing strategy.

**Use Cases**
- Applications using MySQL with need for vector search
- Azure ecosystem integrations
- Hybrid transactional/analytical workloads

**Scalability Considerations**
Follows Azure MySQL scaling options including read replicas and flexible servers.

**Known Limitations**
- Vector search capabilities depend on extensions
- Performance may not match specialized vector databases

**Common Connection Issues and Troubleshooting**
- Ensure MySQL server has vector search extensions
- Verify connection parameters and firewall rules
- Check database permissions

**Cloud vs Self-Managed Differences**
Azure MySQL is a managed service with automated backups and updates.

**Section sources**
- [azure_mysql.py](file://mem0/configs/vector_stores/azure_mysql.py)

## LangChain
LangChain provides vector store integrations as part of its framework.

**Configuration Parameters**
- LangChain-specific vector store configuration
- Underlying vector database parameters
- Embedding model configuration

**Authentication Methods**
Depends on the underlying vector database being used.

**Connection Setup**
Configured through LangChain's vector store interface with specific parameters for the chosen backend.

```python
# LangChain vector store configuration uses LangChain's
# standardized interface for various vector databases
```

**Performance Characteristics**
Performance depends on the underlying vector database implementation.

**Use Cases**
- Applications using LangChain framework
- Prototyping and development
- Multi-vector database strategies

**Scalability Considerations**
Follows the scalability characteristics of the underlying vector database.

**Known Limitations**
- Additional abstraction layer may impact performance
- Limited to LangChain-supported vector databases

**Common Connection Issues and Troubleshooting**
- Ensure underlying vector database is properly configured
- Verify LangChain dependencies are installed
- Check compatibility between LangChain and vector database versions

**Cloud vs Self-Managed Differences**
Depends on the underlying vector database being used.

**Section sources**
- [langchain.py](file://mem0/configs/vector_stores/langchain.py)

## S3 Vectors
Amazon S3 for vector storage with external indexing.

**Configuration Parameters**
- AWS credentials (access key, secret key)
- S3 bucket and object configuration
- Region information
- External indexing service parameters

**Authentication Methods**
AWS IAM authentication through access keys or IAM roles.

**Connection Setup**
Requires AWS credentials and S3 bucket information.

```python
# S3 vector configuration uses AWS SDK patterns
# with additional parameters for vector indexing
```

**Performance Characteristics**
Storage performance follows S3 characteristics with indexing performance depending on external services.

**Use Cases**
- Cost-effective vector storage
- Archival of vector data
- Hybrid storage/indexing architectures

**Scalability Considerations**
S3 provides virtually unlimited storage scalability.

**Known Limitations**
- Retrieval latency higher than database solutions
- Requires external indexing service

**Common Connection Issues and Troubleshooting**
- Ensure AWS credentials have appropriate S3 permissions
- Verify bucket exists and is accessible
- Check network connectivity to AWS

**Cloud vs Self-Managed Differences**
S3 is exclusively a cloud-hosted service as part of AWS.

**Section sources**
- [s3_vectors.py](file://mem0/configs/vector_stores/s3_vectors.py)

## Valkey
Valkey is a community-driven fork of Redis with vector search capabilities.

**Configuration Parameters**
- Valkey URL
- Authentication credentials
- Vector index configuration
- Connection pool settings

**Authentication Methods**
Similar to Redis, through URL-based authentication.

**Connection Setup**
Uses connection patterns similar to Redis with Valkey-specific endpoints.

```python
# Valkey configuration follows Redis patterns
# with Valkey-specific connection details
```

**Performance Characteristics**
Similar to Redis with in-memory performance characteristics.

**Use Cases**
- Open-source Redis alternative
- Applications requiring Redis-compatible API
- Community-driven open-source projects

**Scalability Considerations**
Follows Redis-like scaling patterns through clustering.

**Known Limitations**
- Newer project with potentially less ecosystem support
- Compatibility with existing Redis tools

**Common Connection Issues and Troubleshooting**
- Ensure Valkey server is accessible
- Verify authentication credentials
- Check network connectivity

**Cloud vs Self-Managed Differences**
Primarily self-managed with potential cloud offerings emerging.

**Section sources**
- [valkey.py](file://mem0/configs/vector_stores/valkey.py)