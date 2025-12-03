# Migration Guide

<cite>
**Referenced Files in This Document**   
- [main.py](file://mem0/client/main.py)
- [memory.py](file://mem0/memory/main.py)
- [config.py](file://mem0/configs/base.py)
- [pyproject.toml](file://pyproject.toml)
- [env.py](file://openmemory/api/alembic/env.py)
- [add_config_table.py](file://openmemory/api/alembic/versions/add_config_table.py)
- [models.py](file://openmemory/api/app/models.py)
- [__init__.py](file://mem0/__init__.py)
</cite>

## Table of Contents
1. [Introduction](#introduction)
2. [Version Compatibility and Support Policy](#version-compatibility-and-support-policy)
3. [Breaking Changes](#breaking-changes)
4. [Deprecated Features](#deprecated-features)
5. [Configuration Updates](#configuration-updates)
6. [Database Schema Migrations](#database-schema-migrations)
7. [API Migration Patterns](#api-migration-patterns)
8. [Migration Between Deployment Models](#migration-between-deployment-models)
9. [Migration Tools and Scripts](#migration-tools-and-scripts)
10. [Troubleshooting Common Issues](#troubleshooting-common-issues)
11. [Rollback Procedures](#rollback-procedures)
12. [Conclusion](#conclusion)

## Introduction

This migration guide provides comprehensive instructions for upgrading between Mem0 versions. Mem0 is an intelligent memory layer for AI assistants and agents that enables personalized interactions by remembering user preferences, adapting to individual needs, and continuously learning over time. As the platform evolves, this guide will help developers smoothly transition between versions while maintaining data integrity and application functionality.

The guide covers all aspects of migration including breaking changes, deprecated features, configuration updates, database schema changes, and deployment model transitions. It provides step-by-step instructions, code examples showing before/after patterns, and troubleshooting guidance for common migration issues.

**Section sources**
- [README.md](file://README.md#L56-L169)

## Version Compatibility and Support Policy

Mem0 follows semantic versioning principles with a clear backward compatibility policy. The current version is 0.1.118 as specified in the pyproject.toml file. The platform maintains backward compatibility within major versions, but breaking changes may occur between major versions.

### Support Timeline
- **Current Version (0.1.x)**: Fully supported with bug fixes and security patches
- **Previous Major Version**: Supported for 6 months after the release of a new major version
- **Legacy Versions**: Security patches only for 3 months after previous version support ends

### Compatibility Matrix
| Current Version | Compatible Client Versions | Notes |
|---------------|----------------------------|-------|
| 0.1.118 | 0.1.0+ | Full compatibility with v0.1.x series |
| 0.1.118 | < 0.1.0 | Limited compatibility; deprecated APIs may not work |

The platform provides deprecation warnings for at least two minor versions before removing features, allowing developers adequate time to update their implementations.

**Section sources**
- [pyproject.toml](file://pyproject.toml#L7)
- [main.py](file://mem0/client/main.py#L24-L491)

## Breaking Changes

This section documents breaking changes between Mem0 versions that require code modifications when upgrading.

### API Response Format Changes

The most significant breaking change involves the API response format for memory operations. In earlier versions, methods like `add`, `get_all`, and `search` returned raw lists or direct memory objects. In current versions, these methods return structured dictionaries with consistent formatting.

**Before (v0.1.0 and earlier):**
```python
# Old format returned direct list
memories = memory.get_all(user_id="user123")
# Returns: [{"id": "...", "memory": "..."}, ...]
```

**After (v0.1.118):**
```python
# New format returns structured dictionary
result = memory.get_all(user_id="user123")
# Returns: {"results": [{"id": "...", "memory": "..."}, ...]}
```

The change affects all retrieval methods:
- `add()` now returns `{"results": [...]}` instead of a direct list
- `get_all()` now returns `{"results": [...]}` instead of a direct list
- `search()` now returns `{"results": [...]}` instead of a direct list

### Client Initialization Changes

The MemoryClient initialization has been updated to support enhanced authentication and organization management.

**Before:**
```python
client = MemoryClient(api_key="your-key")
```

**After:**
```python
client = MemoryClient(
    api_key="your-key",
    org_id="your-org-id", 
    project_id="your-project-id"
)
```

The new initialization supports organization and project scoping, enabling better resource management in enterprise environments.

### Memory Type Enumeration

Memory types are now strictly enforced through enumeration rather than string literals. The `MemoryType` enum must be used instead of raw strings.

**Before:**
```python
memory.add(messages, memory_type="procedural_memory")
```

**After:**
```python
from mem0.configs.enums import MemoryType
memory.add(messages, memory_type=MemoryType.PROCEDURAL.value)
```

**Section sources**
- [memory.py](file://mem0/memory/main.py#L292-L300)
- [memory.py](file://mem0/memory/main.py#L593-L603)
- [memory.py](file://mem0/memory/main.py#L708-L718)
- [main.py](file://mem0/client/main.py#L39-L103)

## Deprecated Features

This section documents features that have been deprecated and will be removed in future versions.

### Legacy API Output Format

The legacy API output format without the "results" wrapper is deprecated. When using the old format, deprecation warnings are issued.

```python
# This will trigger a deprecation warning
warnings.warn(
    "The current add API output format is deprecated. "
    "To use the latest format, set `api_version='v1.1'`. "
    "The current format will be removed in mem0ai 1.1.0 and later versions.",
    category=DeprecationWarning,
    stacklevel=2,
)
```

Developers should update their code to expect the new structured format and set `api_version='v1.1'` in their configuration.

### Direct Project Management Methods

The direct project management methods in MemoryClient are deprecated in favor of using the Project manager class.

**Deprecated Methods:**
- `get_project()` - Use `client.project.get()` instead
- `update_project()` - Use `client.project.update()` instead

```python
# Deprecated
client.get_project(fields=["instructions"])

# Recommended
client.project.get(fields=["instructions"])
```

These methods will be removed in version 1.0 of the package.

### Output Format Parameter

The `output_format` parameter with value 'v1.0' is deprecated in the client API. The system now defaults to 'v1.1' format.

```python
# This will trigger a deprecation warning
warnings.warn(
    "output_format='v1.0' is deprecated therefore setting it to "
    "'v1.1' by default. Check out the docs for more information: "
    "https://docs.mem0.ai/platform/quickstart#4-1-create-memories"
)
```

**Section sources**
- [memory.py](file://mem0/memory/main.py#L294-L299)
- [memory.py](file://mem0/memory/main.py#L595-L599)
- [memory.py](file://mem0/memory/main.py#L710-L714)
- [main.py](file://mem0/client/main.py#L153-L161)
- [main.py](file://mem0/client/main.py#L626-L628)
- [main.py](file://mem0/client/main.py#L675-L677)

## Configuration Updates

This section details required configuration updates when migrating to newer Mem0 versions.

### Memory Configuration Structure

The memory configuration structure has been updated to support enhanced features and better organization. The new configuration uses a hierarchical structure with dedicated sections for different components.

**Before:**
```python
config = {
    "embedder": "openai",
    "vector_store": "qdrant",
    "llm": "openai"
}
```

**After:**
```python
from mem0.configs.base import MemoryConfig

config = MemoryConfig(
    embedder={
        "provider": "openai",
        "config": {
            "model": "text-embedding-3-small"
        }
    },
    vector_store={
        "provider": "qdrant",
        "config": {
            "collection_name": "memories",
            "embedding_model_dims": 1536
        }
    },
    llm={
        "provider": "openai",
        "config": {
            "model": "gpt-4o-mini"
        }
    }
)
```

### API Version Configuration

The API version must be explicitly set in the configuration to ensure compatibility:

```python
config = MemoryConfig(
    version="v1.1"  # Required to use the latest API format
)
```

Setting the version ensures that the client uses the appropriate response format and feature set.

### Graph Store Configuration

The graph store configuration has been enhanced to support more providers and advanced settings:

```python
config = MemoryConfig(
    graph_store={
        "provider": "neo4j",  # or "kuzu", "neptune"
        "config": {
            "url": "bolt://localhost:7687",
            "username": "neo4j",
            "password": "password"
        }
    }
)
```

**Section sources**
- [memory.py](file://mem0/memory/main.py#L132-L148)
- [base.py](file://mem0/configs/base.py)
- [memory.py](file://mem0/memory/main.py#L148)

## Database Schema Migrations

This section covers database schema changes and migration procedures for the OpenMemory backend.

### Alembic Migration Framework

Mem0 uses Alembic for database schema migrations. The migration scripts are located in `openmemory/api/alembic/versions/` and are managed through the standard Alembic workflow.

```python
# env.py configuration
def run_migrations_online():
    """Run migrations in 'online' mode."""
    configuration = config.get_section(config.config_ini_section)
    configuration["sqlalchemy.url"] = os.getenv("DATABASE_URL", "sqlite:///./openmemory.db")
    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
```

### Config Table Addition

A significant schema change was the addition of the configs table to store application configuration:

```python
def upgrade():
    op.create_table(
        'configs',
        sa.Column('id', sa.UUID(), nullable=False, default=lambda: uuid.uuid4()),
        sa.Column('key', sa.String(), nullable=False),
        sa.Column('value', sa.JSON(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('key')
    )
    op.create_index('idx_configs_key', 'configs', ['key'])
```

This migration was introduced to support dynamic configuration without requiring application restarts.

### Memory Model Enhancements

The Memory model has been enhanced with additional fields and relationships:

```python
class Memory(Base):
    __tablename__ = "memories"
    id = Column(UUID, primary_key=True, default=lambda: uuid.uuid4())
    user_id = Column(UUID, ForeignKey("users.id"), nullable=False, index=True)
    app_id = Column(UUID, ForeignKey("apps.id"), nullable=False, index=True)
    content = Column(String, nullable=False)
    vector = Column(String)
    metadata_ = Column('metadata', JSON, default=dict)
    state = Column(Enum(MemoryState), default=MemoryState.active, index=True)
    created_at = Column(DateTime, default=get_current_utc_time, index=True)
    updated_at = Column(DateTime,
                        default=get_current_utc_time,
                        onupdate=get_current_utc_time)
    archived_at = Column(DateTime, nullable=True, index=True)
    deleted_at = Column(DateTime, nullable=True, index=True)
```

Key additions include:
- `state` field with MemoryState enum (active, paused, archived, deleted)
- `archived_at` and `deleted_at` timestamp fields for soft deletion
- Enhanced indexing for improved query performance

### Category System Implementation

A new category system was implemented to support memory organization:

```python
class Category(Base):
    __tablename__ = "categories"
    id = Column(UUID, primary_key=True, default=lambda: uuid.uuid4())
    name = Column(String, unique=True, nullable=False, index=True)
    description = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.now(datetime.UTC), index=True)
    updated_at = Column(DateTime,
                        default=get_current_utc_time,
                        onupdate=get_current_utc_time)

memory_categories = Table(
    "memory_categories", Base.metadata,
    Column("memory_id", UUID, ForeignKey("memories.id"), primary_key=True, index=True),
    Column("category_id", UUID, ForeignKey("categories.id"), primary_key=True, index=True),
    Index('idx_memory_category', 'memory_id', 'category_id')
)
```

This many-to-many relationship allows memories to be associated with multiple categories.

**Section sources**
- [env.py](file://openmemory/api/alembic/env.py)
- [add_config_table.py](file://openmemory/api/alembic/versions/add_config_table.py#L1-L40)
- [models.py](file://openmemory/api/app/models.py#L85-L109)

## API Migration Patterns

This section provides code examples showing before/after patterns for common API usage.

### Memory Addition Pattern

**Before:**
```python
# Old pattern with direct list return
memories = memory.add(messages, user_id="user123")
for mem in memories:
    print(f"Added: {mem['memory']}")
```

**After:**
```python
# New pattern with structured response
result = memory.add(messages, user_id="user123")
for mem in result["results"]:
    print(f"Added: {mem['memory']}")
    
# With graph relations if enabled
if "relations" in result:
    for rel in result["relations"]:
        print(f"Relation: {rel}")
```

### Memory Retrieval Pattern

**Before:**
```python
# Direct list access
memories = memory.get_all(user_id="user123", limit=10)
for memory in memories:
    process_memory(memory)
```

**After:**
```python
# Access through results key
response = memory.get_all(user_id="user123", limit=10)
for memory in response["results"]:
    process_memory(memory)
    
# Handle relations if graph is enabled
if "relations" in response:
    for relation in response["relations"]:
        process_relation(relation)
```

### Search Pattern

**Before:**
```python
# Simple search with direct results
results = memory.search("favorite foods", user_id="user123")
for result in results["results"]:
    print(f"Memory: {result['memory']} (Score: {result['score']:.3f})")
```

**After:**
```python
# Enhanced search with filtering
results = memory.search(
    query="favorite foods",
    user_id="user123",
    limit=10,
    filters={"category": "preferences"},
    threshold=0.7
)

for result in results["results"]:
    print(f"Memory: {result['memory']} (Score: {result['score']:.3f})")
    if "metadata" in result:
        print(f"Metadata: {result['metadata']}")
```

### Client Initialization Pattern

**Before:**
```python
# Simple client initialization
client = MemoryClient(api_key="your-api-key")
```

**After:**
```python
# Enhanced client initialization with project context
client = MemoryClient(
    api_key="your-api-key",
    org_id="your-org-id",
    project_id="your-project-id"
)

# Using project manager for project-specific operations
project_config = client.project.get()
client.project.update(custom_instructions="New instructions")
```

**Section sources**
- [memory.py](file://mem0/memory/main.py#L195-L308)
- [memory.py](file://mem0/memory/main.py#L537-L603)
- [memory.py](file://mem0/memory/main.py#L644-L718)
- [main.py](file://mem0/client/main.py#L131-L239)

## Migration Between Deployment Models

This section covers migration procedures between different deployment models, including self-hosted to cloud transitions.

### Self-Hosted to Cloud Migration

Migrating from self-hosted to cloud deployment involves several steps to ensure data integrity and service continuity.

#### Data Export from Self-Hosted

First, export data from the self-hosted instance:

```python
# Create export with schema
schema = {
    "memories": {
        "fields": ["id", "content", "metadata", "created_at", "updated_at"],
        "filters": {"user_id": "user123"}
    },
    "users": {
        "fields": ["id", "user_id", "name", "email"]
    }
}

export_result = client.create_memory_export(schema, user_id="user123")
export_id = export_result["id"]
```

#### Cloud Instance Configuration

Configure the cloud instance with appropriate settings:

```python
# Initialize cloud client
cloud_client = MemoryClient(
    api_key="cloud-api-key",
    org_id="cloud-org-id",
    project_id="cloud-project-id"
)

# Set up project configuration
cloud_client.project.update(
    custom_instructions="Migrated from self-hosted instance",
    enable_graph=True,
    version="v1.1"
)
```

#### Data Import to Cloud

Import the exported data to the cloud instance:

```python
# Get exported data
exported_data = client.get_memory_export(user_id="user123")

# Import memories to cloud
for memory_data in exported_data["memories"]:
    cloud_client.add(
        messages=[{"role": "user", "content": memory_data["content"]}],
        user_id=memory_data["user_id"],
        metadata=memory_data["metadata"]
    )
```

### Configuration Synchronization

Synchronize configuration between deployment models:

```python
# Get current configuration from self-hosted
local_config = local_memory.config

# Apply to cloud client
cloud_client.project.update(
    custom_instructions=local_config.custom_fact_extraction_prompt,
    retrieval_criteria=[
        {
            "type": "vector",
            "threshold": 0.7,
            "provider": local_config.vector_store.provider
        }
    ]
)
```

### Testing and Validation

After migration, validate the data and functionality:

```python
# Test memory retrieval
test_result = cloud_client.search("test query", user_id="user123")
assert len(test_result) > 0, "No memories retrieved after migration"

# Verify data integrity
summary = cloud_client.get_summary(filters={"user_id": "user123"})
print(f"Migrated memories: {summary['total_memories']}")
```

**Section sources**
- [main.py](file://mem0/client/main.py#L546-L589)
- [main.py](file://mem0/client/main.py#L592-L605)

## Migration Tools and Scripts

This section documents available migration tools and scripts to facilitate the upgrade process.

### Configuration Converter

A configuration converter script is available to transform old configuration formats to the new structure:

```python
def convert_config(old_config):
    """Convert old configuration format to new structure."""
    new_config = MemoryConfig()
    
    # Convert embedder configuration
    if "embedder" in old_config:
        new_config.embedder.provider = old_config["embedder"]
        new_config.embedder.config = {}
    
    # Convert vector store configuration
    if "vector_store" in old_config:
        new_config.vector_store.provider = old_config["vector_store"]
        new_config.vector_store.config = {}
    
    # Convert LLM configuration
    if "llm" in old_config:
        new_config.llm.provider = old_config["llm"]
        new_config.llm.config = {}
    
    return new_config
```

### Database Migration Scripts

The Alembic framework provides standard migration commands:

```bash
# Check current migration status
alembic current

# Upgrade to latest version
alembic upgrade head

# Downgrade to previous version
alembic downgrade -1

# Generate new migration
alembic revision --autogenerate -m "Add new feature"
```

### Data Migration Utility

A data migration utility helps transfer memories between instances:

```python
class DataMigrator:
    def __init__(self, source_client, target_client):
        self.source = source_client
        self.target = target_client
    
    def migrate_user_memories(self, user_id):
        """Migrate all memories for a specific user."""
        # Get all memories from source
        source_memories = self.source.get_all(user_id=user_id)
        
        migrated_count = 0
        for memory in source_memories["results"]:
            # Extract core data
            content = memory["memory"]
            metadata = memory.get("metadata", {})
            
            # Create message format
            messages = [{"role": "user", "content": content}]
            
            # Add to target
            self.target.add(
                messages=messages,
                user_id=user_id,
                metadata=metadata
            )
            migrated_count += 1
        
        return migrated_count
```

**Section sources**
- [env.py](file://openmemory/api/alembic/env.py)
- [main.py](file://mem0/client/main.py#L546-L605)

## Troubleshooting Common Issues

This section addresses common issues encountered during migration and their solutions.

### Deprecation Warnings

**Issue:** Applications display deprecation warnings about API output formats.

**Solution:** Update the code to use the new response format and set the API version explicitly:

```python
# Set api_version in configuration
config = MemoryConfig(version="v1.1")

# Update code to handle structured responses
result = memory.get_all(user_id="user123")
memories = result["results"]  # Access through "results" key
```

### Configuration Validation Errors

**Issue:** Configuration validation fails with "At least one of 'user_id', 'agent_id', or 'run_id' must be provided."

**Solution:** Ensure that at least one session identifier is provided in all memory operations:

```python
# Correct usage
memory.add(messages, user_id="user123")  # Provides user_id

# Or with agent_id
memory.add(messages, agent_id="agent456")

# Or with run_id  
memory.add(messages, run_id="run789")
```

### Database Migration Failures

**Issue:** Alembic migration fails with database connection errors.

**Solution:** Verify database URL configuration and permissions:

```python
# Check environment variables
import os
print(f"DATABASE_URL: {os.getenv('DATABASE_URL')}")

# Test connection manually
from sqlalchemy import create_engine
engine = create_engine(os.getenv("DATABASE_URL"))
connection = engine.connect()
connection.close()
```

### Memory Type Validation Errors

**Issue:** Error "Invalid 'memory_type'" when creating procedural memories.

**Solution:** Use the MemoryType enum instead of string literals:

```python
from mem0.configs.enums import MemoryType

# Correct usage
memory.add(
    messages, 
    agent_id="agent123",
    memory_type=MemoryType.PROCEDURAL.value
)
```

### Client Initialization Errors

**Issue:** ValueError "Mem0 API Key not provided" during client initialization.

**Solution:** Ensure the API key is provided either as a parameter or environment variable:

```python
# Option 1: Pass as parameter
client = MemoryClient(api_key="your-api-key")

# Option 2: Set environment variable
import os
os.environ["MEM0_API_KEY"] = "your-api-key"
client = MemoryClient()  # Will read from environment
```

**Section sources**
- [memory.py](file://mem0/memory/main.py#L111-L117)
- [memory.py](file://mem0/memory/main.py#L252-L258)
- [main.py](file://mem0/client/main.py#L70-L71)

## Rollback Procedures

This section provides procedures for rolling back to previous versions if migration issues occur.

### Code Rollback

If migration issues cannot be resolved, revert to the previous version:

```bash
# Revert to previous version using pip
pip install mem0ai==0.1.117

# Or specify version in requirements.txt
mem0ai==0.1.117
```

Update the code to use the previous API patterns before downgrading.

### Database Rollback

If database migrations have been applied, roll back to the previous schema:

```bash
# Check current revision
alembic current

# Downgrade to previous version
alembic downgrade -1

# Or downgrade to specific revision
alembic downgrade 0b53c747049a
```

### Configuration Rollback

Restore the previous configuration format:

```python
# Revert to old configuration structure
old_config = {
    "embedder": "openai",
    "vector_store": "qdrant", 
    "llm": "openai"
}

# Initialize with old format
memory = Memory(config=old_config)
```

### Data Integrity Verification

After rollback, verify data integrity:

```python
# Check memory count
memories = memory.get_all(user_id="user123")
print(f"Memory count: {len(memories)}")

# Verify recent memories exist
recent = memory.get_all(user_id="user123", limit=5)
for mem in recent:
    print(f"Recent memory: {mem['memory'][:50]}...")
```

**Section sources**
- [env.py](file://openmemory/api/alembic/env.py#L85-L88)
- [add_config_table.py](file://openmemory/api/alembic/versions/add_config_table.py#L37-L40)

## Conclusion

This migration guide has provided comprehensive instructions for upgrading between Mem0 versions. The key points to remember are:

1. **API Response Format**: Update code to handle the new structured response format with the "results" wrapper
2. **Configuration Updates**: Migrate to the new hierarchical configuration structure with explicit API versioning
3. **Deprecated Features**: Replace deprecated methods with their recommended alternatives
4. **Database Migrations**: Use Alembic to manage schema changes and ensure data integrity
5. **Deployment Transitions**: Follow the step-by-step process for migrating between self-hosted and cloud deployments

The migration process should be performed in stages:
1. Review breaking changes and deprecation warnings
2. Update configuration files to the new format
3. Modify code to use new API patterns
4. Test thoroughly in a staging environment
5. Perform database migrations
6. Deploy to production

By following this guide, developers can ensure a smooth transition between Mem0 versions while maintaining application functionality and data integrity.

For additional support, refer to the official documentation at [https://docs.mem0.ai](https://docs.mem0.ai) or join the community on Discord at [https://mem0.dev/DiG](https://mem0.dev/DiG).

[No sources needed since this section summarizes without analyzing specific files]