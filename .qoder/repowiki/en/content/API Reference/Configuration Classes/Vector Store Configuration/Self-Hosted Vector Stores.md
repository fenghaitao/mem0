# Self-Hosted Vector Stores

<cite>
**Referenced Files in This Document**   
- [chroma.py](file://mem0/configs/vector_stores/chroma.py)
- [faiss.py](file://mem0/configs/vector_stores/faiss.py)
- [milvus.py](file://mem0/configs/vector_stores/milvus.py)
- [elasticsearch.py](file://mem0/configs/vector_stores/elasticsearch.py)
- [opensearch.py](file://mem0/configs/vector_stores/opensearch.py)
- [pgvector.py](file://mem0/configs/vector_stores/pgvector.py)
- [redis.py](file://mem0/configs/vector_stores/redis.py)
- [mongodb.py](file://mem0/configs/vector_stores/mongodb.py)
- [databricks.py](file://mem0/configs/vector_stores/databricks.py)
- [chroma.yaml](file://embedchain/configs/chroma.yaml)
- [opensearch.yaml](file://embedchain/configs/opensearch.yaml)
- [chroma.yml](file://openmemory/compose/chroma.yml)
- [elasticsearch.yml](file://openmemory/compose/elasticsearch.yml)
- [base.py](file://mem0/vector_stores/base.py)
</cite>

## Table of Contents
1. [Introduction](#introduction)
2. [Chroma Configuration](#chroma-configuration)
3. [FAISS Configuration](#faiss-configuration)
4. [Milvus Configuration](#milvus-configuration)
5. [OpenSearch Configuration](#opensearch-configuration)
6. [Elasticsearch Configuration](#elasticsearch-configuration)
7. [PGVector Configuration](#pgvector-configuration)
8. [Redis Configuration](#redis-configuration)
9. [MongoDB Configuration](#mongodb-configuration)
10. [Databricks Configuration](#databricks-configuration)
11. [Docker and Kubernetes Deployment](#docker-and-kubernetes-deployment)
12. [Common Self-Hosted Challenges](#common-self-hosted-challenges)
13. [Monitoring and Performance Benchmarking](#monitoring-and-performance-benchmarking)

## Introduction
This document provides comprehensive guidance for configuring self-hosted vector stores in the mem0 framework. It covers setup parameters for Chroma, FAISS, Milvus, OpenSearch, Elasticsearch, PGVector, Redis, MongoDB, and Databricks. The documentation details connection URLs, port configurations, authentication methods, TLS/SSL settings, and network security considerations. It also explains local storage paths, memory mapping options, and performance tuning parameters for various vector databases.

**Section sources**
- [base.py](file://mem0/vector_stores/base.py#L1-L59)

## Chroma Configuration

### Connection and Authentication
Chroma supports both local and cloud configurations. For self-hosted deployments, use either a local path or host/port configuration. The configuration includes:
- **collection_name**: Default name for the collection (default: "mem0")
- **path**: Path to the database directory for local storage
- **host**: Remote host for server connection
- **port**: Remote port for server connection
- **api_key**: Required for ChromaDB Cloud authentication
- **tenant**: Tenant ID for ChromaDB Cloud

The configuration enforces mutual exclusivity between cloud and local/server configurations to prevent conflicts.

### Storage and Network Settings
For local deployments, specify the `path` parameter to define where Chroma stores data. When using server mode, configure `host` and `port` to connect to a remote Chroma server. The default configuration validates that either cloud credentials (api_key and tenant) or local/server parameters (path or host/port) are provided, but not both simultaneously.

```mermaid
classDiagram
class ChromaDbConfig {
+string collection_name
+Optional[str] path
+Optional[str] host
+Optional[int] port
+Optional[str] api_key
+Optional[str] tenant
+check_connection_config() bool
+validate_extra_fields() bool
}
```

**Diagram sources**
- [chroma.py](file://mem0/configs/vector_stores/chroma.py#L6-L59)

**Section sources**
- [chroma.py](file://mem0/configs/vector_stores/chroma.py#L6-L59)

## FAISS Configuration

### Core Parameters
FAISS configuration focuses on local file-based storage with the following parameters:
- **collection_name**: Name for the collection (default: "mem0")
- **path**: Directory path to store FAISS index and metadata files
- **distance_strategy**: Distance calculation method ("euclidean", "inner_product", "cosine")
- **normalize_L2**: Whether to normalize L2 vectors (applies only to euclidean distance)
- **embedding_model_dims**: Dimension of the embedding vectors (default: 1536)

### Performance Tuning
The distance strategy significantly impacts search performance and accuracy:
- **euclidean**: Measures straight-line distance between vectors
- **inner_product**: Uses dot product for similarity calculation
- **cosine**: Measures cosine similarity between vectors

The configuration validates that the distance strategy is one of the three supported options and prevents the use of unauthorized fields.

```mermaid
classDiagram
class FAISSConfig {
+string collection_name
+Optional[str] path
+string distance_strategy
+bool normalize_L2
+int embedding_model_dims
+validate_distance_strategy() bool
+validate_extra_fields() bool
}
```

**Diagram sources**
- [faiss.py](file://mem0/configs/vector_stores/faiss.py#L6-L38)

**Section sources**
- [faiss.py](file://mem0/configs/vector_stores/faiss.py#L6-L38)

## Milvus Configuration

### Connection Parameters
Milvus configuration requires the following connection details:
- **url**: Full URL for Milvus/Zilliz server (default: "http://localhost:19530")
- **token**: Authentication token for Zilliz server or secured Milvus instances
- **collection_name**: Name of the collection (default: "mem0")
- **embedding_model_dims**: Dimensions of the embedding model (default: 1536)
- **metric_type**: Similarity metric type ("L2", "IP", "COSINE", "HAMMING", "JACCARD")
- **db_name**: Name of the database

### Index and Search Configuration
Milvus supports multiple metric types for similarity search:
- **L2**: Euclidean distance
- **IP**: Inner product
- **COSINE**: Cosine similarity
- **HAMMING**: Hamming distance for binary vectors
- **JACCARD**: Jaccard distance for binary vectors

The configuration ensures that only valid fields are provided and prevents unauthorized parameters.

```mermaid
classDiagram
class MilvusDBConfig {
+string url
+Optional[str] token
+string collection_name
+int embedding_model_dims
+str metric_type
+str db_name
+validate_extra_fields() bool
}
class MetricType {
+L2
+IP
+COSINE
+HAMMING
+JACCARD
}
MilvusDBConfig --> MetricType : "uses"
```

**Diagram sources**
- [milvus.py](file://mem0/configs/vector_stores/milvus.py#L7-L43)

**Section sources**
- [milvus.py](file://mem0/configs/vector_stores/milvus.py#L7-L43)

## OpenSearch Configuration

### Connection and Authentication
OpenSearch configuration includes:
- **collection_name**: Index name (default: "mem0")
- **host**: OpenSearch host (default: "localhost")
- **port**: OpenSearch port (default: 9200)
- **user**: Username for authentication
- **password**: Password for authentication
- **api_key**: API key for authentication
- **verify_certs**: Whether to verify SSL certificates (default: False)
- **use_ssl**: Whether to use SSL for connection (default: False)
- **http_auth**: HTTP authentication method or AWS SigV4 configuration
- **connection_class**: Connection class for OpenSearch (default: "RequestsHttpConnection")
- **pool_maxsize**: Maximum number of connections in the pool (default: 20)

### Security Settings
OpenSearch has security settings disabled by default:
- **verify_certs**: Set to False by default, allowing connections without certificate verification
- **use_ssl**: Set to False by default, enabling HTTP connections
- **http_auth**: Supports various authentication methods including basic auth and AWS SigV4

The configuration validates that a host is provided and ensures no unauthorized fields are used.

```mermaid
classDiagram
class OpenSearchConfig {
+string collection_name
+str host
+int port
+Optional[str] user
+Optional[str] password
+Optional[str] api_key
+bool verify_certs
+bool use_ssl
+Optional[object] http_auth
+Optional[Union[str, Type]] connection_class
+int pool_maxsize
+validate_auth() bool
+validate_extra_fields() bool
}
```

**Diagram sources**
- [opensearch.py](file://mem0/configs/vector_stores/opensearch.py#L6-L42)

**Section sources**
- [opensearch.py](file://mem0/configs/vector_stores/opensearch.py#L6-L42)

## Elasticsearch Configuration

### Connection Parameters
Elasticsearch configuration includes:
- **collection_name**: Index name (default: "mem0")
- **host**: Elasticsearch host (default: "localhost")
- **port**: Elasticsearch port (default: 9200)
- **user**: Username for authentication
- **password**: Password for authentication
- **cloud_id**: Cloud ID for Elastic Cloud deployments
- **api_key**: API key for authentication
- **embedding_model_dims**: Dimension of the embedding vector (default: 1536)
- **verify_certs**: Verify SSL certificates (default: True)
- **use_ssl**: Use SSL for connection (default: True)
- **auto_create_index**: Automatically create index during initialization (default: True)
- **custom_search_query**: Custom search query function
- **headers**: Custom headers to include in requests

### Authentication Methods
Elasticsearch supports multiple authentication methods:
- **cloud_id**: For Elastic Cloud deployments
- **user/password**: Basic authentication
- **api_key**: API key authentication

The configuration validates that either cloud_id or host is provided, and that authentication credentials (api_key or user/password) are present.

```mermaid
classDiagram
class ElasticsearchConfig {
+string collection_name
+str host
+int port
+Optional[str] user
+Optional[str] password
+Optional[str] cloud_id
+Optional[str] api_key
+int embedding_model_dims
+bool verify_certs
+bool use_ssl
+bool auto_create_index
+Optional[Callable] custom_search_query
+Optional[Dict[str, str]] headers
+validate_auth() bool
+validate_headers() bool
+validate_extra_fields() bool
}
```

**Diagram sources**
- [elasticsearch.py](file://mem0/configs/vector_stores/elasticsearch.py#L7-L66)

**Section sources**
- [elasticsearch.py](file://mem0/configs/vector_stores/elasticsearch.py#L7-L66)

## PGVector Configuration

### Database Connection
PGVector configuration for PostgreSQL with pgvector extension:
- **dbname**: Database name (default: "postgres")
- **collection_name**: Collection name (default: "mem0")
- **embedding_model_dims**: Embedding model dimensions (default: 1536)
- **user**: Database user
- **password**: Database password
- **host**: Database host (default: localhost)
- **port**: Database port
- **diskann**: Use diskann for approximate nearest neighbors search (default: False)
- **hnsw**: Use hnsw for faster search (default: True)
- **minconn**: Minimum connections in pool (default: 1)
- **maxconn**: Maximum connections in pool (default: 5)
- **sslmode**: SSL mode for PostgreSQL connection
- **connection_string**: PostgreSQL connection string (overrides individual parameters)
- **connection_pool**: Psycopg connection pool object (overrides other connection parameters)

### Connection Priority
The configuration follows a specific priority order:
1. If `connection_pool` is provided, use it exclusively
2. If `connection_string` is provided, use it exclusively
3. Otherwise, use individual connection parameters (user, password, host, port)

This prevents configuration conflicts and ensures consistent connection behavior.

```mermaid
classDiagram
class PGVectorConfig {
+str dbname
+str collection_name
+Optional[int] embedding_model_dims
+Optional[str] user
+Optional[str] password
+Optional[str] host
+Optional[int] port
+Optional[bool] diskann
+Optional[bool] hnsw
+Optional[int] minconn
+Optional[int] maxconn
+Optional[str] sslmode
+Optional[str] connection_string
+Optional[Any] connection_pool
+check_auth_and_connection() bool
+validate_extra_fields() bool
}
```

**Diagram sources**
- [pgvector.py](file://mem0/configs/vector_stores/pgvector.py#L6-L53)

**Section sources**
- [pgvector.py](file://mem0/configs/vector_stores/pgvector.py#L6-L53)

## Redis Configuration

### Connection Settings
Redis configuration is minimal and focused on the Redis URL:
- **redis_url**: Complete Redis URL (required)
- **collection_name**: Collection name (default: "mem0")
- **embedding_model_dims**: Embedding model dimensions (default: 1536)

The Redis URL should include authentication if required, following the format: `redis://[:password@]host[:port][/database]`

### Performance Considerations
Since Redis stores data in memory, consider:
- Memory allocation based on vector count and dimension size
- Persistence configuration (RDB snapshots, AOF)
- Replication and high availability setup
- Eviction policies for memory management

The configuration validates that no unauthorized fields are provided.

```mermaid
classDiagram
class RedisDBConfig {
+str redis_url
+str collection_name
+int embedding_model_dims
+validate_extra_fields() bool
}
```

**Diagram sources**
- [redis.py](file://mem0/configs/vector_stores/redis.py#L7-L25)

**Section sources**
- [redis.py](file://mem0/configs/vector_stores/redis.py#L7-L25)

## MongoDB Configuration

### Connection Parameters
MongoDB configuration includes:
- **db_name**: MongoDB database name (default: "mem0_db")
- **collection_name**: MongoDB collection name (default: "mem0")
- **embedding_model_dims**: Embedding vector dimensions (default: 1536)
- **mongo_uri**: MongoDB URI (default: "mongodb://localhost:27017")

### URI Configuration
The mongo_uri parameter supports all MongoDB connection options:
- Authentication: `mongodb://username:password@host:port/database`
- Replica sets: `mongodb://host1:port1,host2:port2/database?replicaSet=rs0`
- SSL/TLS: `mongodb://host:port/database?ssl=true`
- Connection options: Various query parameters for tuning behavior

The configuration validates that only authorized fields are provided.

```mermaid
classDiagram
class MongoDBConfig {
+str db_name
+str collection_name
+Optional[int] embedding_model_dims
+str mongo_uri
+validate_extra_fields() bool
}
```

**Diagram sources**
- [mongodb.py](file://mem0/configs/vector_stores/mongodb.py#L6-L26)

**Section sources**
- [mongodb.py](file://mem0/configs/vector_stores/mongodb.py#L6-L26)

## Databricks Configuration

### Workspace and Authentication
Databricks configuration for Vector Search:
- **workspace_url**: Databricks workspace URL (required)
- **access_token**: Personal access token for authentication
- **client_id**: Databricks Service principal client ID
- **client_secret**: Databricks Service principal client secret
- **azure_client_id**: Azure AD application client ID (for Azure Databricks)
- **azure_client_secret**: Azure AD application client secret (for Azure Databricks)

### Vector Search Configuration
- **endpoint_name**: Vector search endpoint name (required)
- **catalog**: Unity Catalog catalog name (required)
- **schema**: Unity Catalog schema name (required)
- **table_name**: Source Delta table name (required)
- **collection_name**: Vector search index name (default: "mem0")
- **index_type**: Index type ("DELTA_SYNC" or "DIRECT_ACCESS")
- **embedding_model_endpoint_name**: Embedding model endpoint for Databricks-computed embeddings
- **embedding_dimension**: Vector embedding dimensions (default: 1536)
- **endpoint_type**: Endpoint type ("STANDARD" or "STORAGE_OPTIMIZED")
- **pipeline_type**: Sync pipeline type ("TRIGGERED" or "CONTINUOUS")
- **warehouse_name**: Databricks SQL warehouse name
- **query_type**: Query type ("ANN" or "HYBRID")

### Authentication Validation
The configuration validates that either:
- An access_token is provided, or
- Both client_id and client_secret are provided, or
- Both azure_client_id and azure_client_secret are provided

This ensures proper authentication to the Databricks workspace.

```mermaid
classDiagram
class DatabricksConfig {
+str workspace_url
+Optional[str] access_token
+Optional[str] client_id
+Optional[str] client_secret
+Optional[str] azure_client_id
+Optional[str] azure_client_secret
+str endpoint_name
+str catalog
+str schema
+str table_name
+str collection_name
+VectorIndexType index_type
+Optional[str] embedding_model_endpoint_name
+int embedding_dimension
+EndpointType endpoint_type
+PipelineType pipeline_type
+Optional[str] warehouse_name
+str query_type
+validate_extra_fields() bool
+validate_authentication() bool
}
```

**Diagram sources**
- [databricks.py](file://mem0/configs/vector_stores/databricks.py#L8-L62)

**Section sources**
- [databricks.py](file://mem0/configs/vector_stores/databricks.py#L8-L62)

## Docker and Kubernetes Deployment

### Docker Compose Examples
The repository includes Docker compose examples for various vector stores:

#### Chroma Deployment
```yaml
services:
  mem0_store:
    image: ghcr.io/chroma-core/chroma:latest
    restart: unless-stopped
    environment:
      - CHROMA_SERVER_HOST=0.0.0.0
      - CHROMA_SERVER_HTTP_PORT=8000
    ports:
      - "8000:8000"
    volumes:
      - mem0_storage:/data
```

#### Elasticsearch Deployment
```yaml
services:
  mem0_store:
    image: docker.elastic.co/elasticsearch/elasticsearch:8.13.4
    restart: unless-stopped
    environment:
      - discovery.type=single-node
      - xpack.security.enabled=false
      - ES_JAVA_OPTS=-Xms512m -Xmx512m
    ulimits:
      memlock: { soft: -1, hard: -1 }
      nofile:  { soft: 65536, hard: 65536 }
    ports:
      - "9200:9200"
    volumes:
      - mem0_storage:/usr/share/elasticsearch/data
```

### Kubernetes Considerations
When deploying to Kubernetes, consider:
- **Resource allocation**: Set appropriate CPU and memory limits based on expected load
- **Persistent storage**: Use PersistentVolumeClaims for data persistence
- **Service exposure**: Configure Services to expose vector stores to applications
- **Configuration management**: Use ConfigMaps and Secrets for configuration and credentials
- **Scaling**: Implement HorizontalPodAutoscalers based on CPU/memory usage

### Resource Allocation Guidelines
- **Chroma**: 1-2 GB RAM per 1M vectors (1536 dimensions)
- **FAISS**: Memory usage depends on index type; HNSW uses ~2x vector storage
- **Milvus**: 4+ GB RAM recommended, scales with vector count and index complexity
- **Elasticsearch/OpenSearch**: 4+ GB RAM, significant disk I/O requirements
- **PGVector**: Depends on PostgreSQL configuration; consider indexing strategy
- **Redis**: Entire dataset must fit in memory; plan accordingly
- **MongoDB**: Memory for working set; consider indexing and sharding
- **Databricks**: Managed service; resource allocation handled by Databricks

```mermaid
graph TD
A[Docker/Kubernetes Deployment] --> B[Chroma]
A --> C[Elasticsearch]
A --> D[Resource Allocation]
A --> E[Persistent Storage]
A --> F[Service Configuration]
B --> B1["Image: ghcr.io/chroma-core/chroma:latest"]
B --> B2["Port: 8000"]
B --> B3["Volume: /data"]
C --> C1["Image: docker.elastic.co/elasticsearch:8.13.4"]
C --> C2["Port: 9200"]
C --> C3["Volume: /usr/share/elasticsearch/data"]
C --> C4["Memory: 512m-1g"]
D --> D1["RAM per 1M vectors"]
D --> D2["CPU requirements"]
E --> E1["Persistent Volumes"]
E --> E2["Backup strategy"]
F --> F1["Service exposure"]
F --> F2["Ingress configuration"]
```

**Diagram sources**
- [chroma.yml](file://openmemory/compose/chroma.yml#L1-L11)
- [elasticsearch.yml](file://openmemory/compose/elasticsearch.yml#L1-L15)

**Section sources**
- [chroma.yml](file://openmemory/compose/chroma.yml#L1-L11)
- [elasticsearch.yml](file://openmemory/compose/elasticsearch.yml#L1-L15)

## Common Self-Hosted Challenges

### Resource Allocation
Self-hosted vector stores require careful resource planning:
- **Memory**: Ensure sufficient RAM for vector storage and indexing
- **CPU**: Index building and search operations are CPU-intensive
- **Disk**: Plan for storage capacity and I/O performance
- **Network**: Consider bandwidth for distributed deployments

### Backup Strategies
Implement regular backup procedures:
- **Chroma**: Backup the data directory specified in `path`
- **FAISS**: Backup index files and metadata
- **Milvus**: Use Milvus backup tools or snapshot storage
- **Elasticsearch/OpenSearch**: Use snapshot and restore functionality
- **PGVector**: PostgreSQL backup tools (pg_dump, WAL archiving)
- **Redis**: RDB snapshots and AOF persistence
- **MongoDB**: mongodump or filesystem snapshots
- **Databricks**: Managed backups through Databricks platform

### Index Persistence
Ensure index persistence across restarts:
- Configure proper storage volumes in container deployments
- Validate that indexes are correctly loaded on startup
- Monitor disk space to prevent out-of-space errors
- Implement health checks to verify index availability

### Version Compatibility
Maintain compatibility between components:
- Vector store client library versions
- Server and client version alignment
- Embedding model dimension consistency
- Protocol compatibility for remote connections

**Section sources**
- [chroma.py](file://mem0/configs/vector_stores/chroma.py#L6-L59)
- [faiss.py](file://mem0/configs/vector_stores/faiss.py#L6-L38)
- [milvus.py](file://mem0/configs/vector_stores/milvus.py#L7-L43)
- [elasticsearch.py](file://mem0/configs/vector_stores/elasticsearch.py#L7-L66)
- [opensearch.py](file://mem0/configs/vector_stores/opensearch.py#L6-L42)
- [pgvector.py](file://mem0/configs/vector_stores/pgvector.py#L6-L53)
- [redis.py](file://mem0/configs/vector_stores/redis.py#L7-L25)
- [mongodb.py](file://mem0/configs/vector_stores/mongodb.py#L6-L26)
- [databricks.py](file://mem0/configs/vector_stores/databricks.py#L8-L62)

## Monitoring and Performance Benchmarking

### Monitoring Setup
Implement monitoring for self-hosted vector stores:
- **Metrics collection**: Track query latency, throughput, resource usage
- **Logging**: Enable detailed logging for troubleshooting
- **Alerting**: Set up alerts for high latency, errors, or resource exhaustion
- **Health checks**: Implement readiness and liveness probes

### Performance Benchmarking
Conduct regular performance testing:
- **Index building time**: Measure time to create indexes on sample data
- **Search latency**: Test query response times under various conditions
- **Throughput**: Measure queries per second at different concurrency levels
- **Memory usage**: Monitor memory consumption during operations
- **Scalability**: Test performance as data volume increases

### Configuration Tuning
Optimize configurations based on benchmark results:
- Adjust index parameters for better performance
- Tune resource allocation based on observed usage
- Optimize query patterns and filters
- Implement caching strategies where appropriate

**Section sources**
- [chroma.py](file://mem0/configs/vector_stores/chroma.py#L6-L59)
- [faiss.py](file://mem0/configs/vector_stores/faiss.py#L6-L38)
- [milvus.py](file://mem0/configs/vector_stores/milvus.py#L7-L43)
- [elasticsearch.py](file://mem0/configs/vector_stores/elasticsearch.py#L7-L66)
- [opensearch.py](file://mem0/configs/vector_stores/opensearch.py#L6-L42)
- [pgvector.py](file://mem0/configs/vector_stores/pgvector.py#L6-L53)
- [redis.py](file://mem0/configs/vector_stores/redis.py#L7-L25)
- [mongodb.py](file://mem0/configs/vector_stores/mongodb.py#L6-L26)
- [databricks.py](file://mem0/configs/vector_stores/databricks.py#L8-L62)