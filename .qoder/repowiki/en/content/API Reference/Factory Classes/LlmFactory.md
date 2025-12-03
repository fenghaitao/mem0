# LlmFactory

<cite>
**Referenced Files in This Document**   
- [factory.py](file://mem0/utils/factory.py#L23-L129)
- [base.py](file://mem0/configs/llms/base.py#L7-L63)
- [openai.py](file://mem0/configs/llms/openai.py#L6-L80)
- [anthropic.py](file://mem0/configs/llms/anthropic.py#L6-L57)
- [ollama.py](file://mem0/configs/llms/ollama.py#L6-L57)
- [azure.py](file://mem0/configs/llms/azure.py#L7-L58)
- [openai.py](file://mem0/llms/openai.py#L14-L148)
- [anthropic.py](file://mem0/llms/anthropic.py#L14-L88)
- [ollama.py](file://mem0/llms/ollama.py#L13-L115)
</cite>

## Table of Contents
1. [Introduction](#introduction)
2. [Core Components](#core-components)
3. [Architecture Overview](#architecture-overview)
4. [Detailed Component Analysis](#detailed-component-analysis)
5. [Dependency Analysis](#dependency-analysis)
6. [Performance Considerations](#performance-considerations)

## Introduction
The LlmFactory class provides a comprehensive factory pattern implementation for creating and managing LLM (Large Language Model) provider instances. It supports multiple LLM providers with their specific configuration requirements, enabling flexible instantiation through various configuration methods. The factory handles configuration normalization, provider registration, and instance creation with proper error handling for unsupported providers.

## Core Components
The LlmFactory class is the central component for LLM provider management, offering methods to create instances, register new providers, and discover available options. It works in conjunction with provider-specific configuration classes that extend the BaseLlmConfig to handle both common and provider-specific parameters.

**Section sources**
- [factory.py](file://mem0/utils/factory.py#L23-L129)

## Architecture Overview
```mermaid
classDiagram
class LlmFactory {
+provider_to_class : Dict[str, Tuple[str, Type[BaseLlmConfig]]]
+create(provider_name : str, config : Optional[Union[BaseLlmConfig, Dict]], **kwargs) : LLMBase
+register_provider(name : str, class_path : str, config_class : Optional[Type[BaseLlmConfig]])
+get_supported_providers() list[str]
}
class BaseLlmConfig {
+model : Optional[Union[str, Dict]]
+temperature : float
+api_key : Optional[str]
+max_tokens : int
+top_p : float
+top_k : int
+enable_vision : bool
+vision_details : Optional[str]
+http_client : Optional[httpx.Client]
+__init__(model, temperature, api_key, max_tokens, top_p, top_k, enable_vision, vision_details, http_client_proxies)
}
class OpenAIConfig {
+openai_base_url : Optional[str]
+models : Optional[List[str]]
+route : Optional[str]
+openrouter_base_url : Optional[str]
+site_url : Optional[str]
+app_name : Optional[str]
+store : bool
+response_callback : Optional[Callable[[Any, dict, dict], None]]
+__init__(...)
}
class AnthropicConfig {
+anthropic_base_url : Optional[str]
+__init__(...)
}
class OllamaConfig {
+ollama_base_url : Optional[str]
+__init__(...)
}
class AzureOpenAIConfig {
+azure_kwargs : AzureConfig
+__init__(...)
}
LlmFactory --> BaseLlmConfig : "uses"
LlmFactory --> OpenAIConfig : "creates"
LlmFactory --> AnthropicConfig : "creates"
LlmFactory --> OllamaConfig : "creates"
LlmFactory --> AzureOpenAIConfig : "creates"
BaseLlmConfig <|-- OpenAIConfig : "extends"
BaseLlmConfig <|-- AnthropicConfig : "extends"
BaseLlmConfig <|-- OllamaConfig : "extends"
BaseLlmConfig <|-- AzureOpenAIConfig : "extends"
```

**Diagram sources**
- [factory.py](file://mem0/utils/factory.py#L23-L129)
- [base.py](file://mem0/configs/llms/base.py#L7-L63)
- [openai.py](file://mem0/configs/llms/openai.py#L6-L80)
- [anthropic.py](file://mem0/configs/llms/anthropic.py#L6-L57)
- [ollama.py](file://mem0/configs/llms/ollama.py#L6-L57)
- [azure.py](file://mem0/configs/llms/azure.py#L7-L58)

## Detailed Component Analysis

### LlmFactory Class Analysis
The LlmFactory class implements a factory pattern for creating LLM instances with proper configuration handling. It supports multiple configuration types and provides methods for extensibility.

#### create() Method
The create() method handles LLM instance creation with flexible configuration options:

```mermaid
flowchart TD
Start([create method]) --> CheckProvider{"Provider supported?"}
CheckProvider --> |No| RaiseError["Raise ValueError"]
CheckProvider --> |Yes| GetConfigClass["Get config class from provider_to_class"]
GetConfigClass --> HandleConfig{"Handle config type"}
HandleConfig --> ConfigNull{"config is None?"}
ConfigNull --> |Yes| CreateDefault["Create default config with kwargs"]
ConfigNull --> |No| ConfigDict{"config is dict?"}
ConfigDict --> |Yes| MergeAndUpdate["Merge dict with kwargs, create config"]
ConfigDict --> |No| ConfigBase{"config is BaseLlmConfig?"}
ConfigBase --> |Yes| ConvertIfNeeded["Convert to provider-specific config if needed"]
ConfigBase --> |No| UseAsIs["Use config as-is"]
ConvertIfNeeded --> ReturnInstance["Return LLM instance"]
MergeAndUpdate --> ReturnInstance
CreateDefault --> ReturnInstance
UseAsIs --> ReturnInstance
ReturnInstance --> End([Return LLM instance])
```

**Diagram sources**
- [factory.py](file://mem0/utils/factory.py#L51-L105)

**Section sources**
- [factory.py](file://mem0/utils/factory.py#L51-L105)

#### provider_to_class Mapping
The provider_to_class dictionary maps provider names to their corresponding implementation classes and configuration types:

```mermaid
erDiagram
PROVIDER_TO_CLASS {
string provider_name PK
string class_path
string config_class_name
}
PROVIDER_TO_CLASS ||--o{ LLM_PROVIDER : "maps to"
LLM_PROVIDER {
string name PK
string description
}
PROVIDER_TO_CLASS {
"ollama" | "mem0.llms.ollama.OllamaLLM" | "OllamaConfig"
"openai" | "mem0.llms.openai.OpenAILLM" | "OpenAIConfig"
"anthropic" | "mem0.llms.anthropic.AnthropicLLM" | "AnthropicConfig"
"azure_openai" | "mem0.llms.azure_openai.AzureOpenAILLM" | "AzureOpenAIConfig"
"groq" | "mem0.llms.groq.GroqLLM" | "BaseLlmConfig"
"together" | "mem0.llms.together.TogetherLLM" | "BaseLlmConfig"
"aws_bedrock" | "mem0.llms.aws_bedrock.AWSBedrockLLM" | "BaseLlmConfig"
"litellm" | "mem0.llms.litellm.LiteLLM" | "BaseLlmConfig"
"openai_structured" | "mem0.llms.openai_structured.OpenAIStructuredLLM" | "OpenAIConfig"
"azure_openai_structured" | "mem0.llms.azure_openai_structured.AzureOpenAIStructuredLLM" | "AzureOpenAIConfig"
"gemini" | "mem0.llms.gemini.GeminiLLM" | "BaseLlmConfig"
"deepseek" | "mem0.llms.deepseek.DeepSeekLLM" | "DeepSeekConfig"
"xai" | "mem0.llms.xai.XAILLM" | "BaseLlmConfig"
"sarvam" | "mem0.llms.sarvam.SarvamLLM" | "BaseLlmConfig"
"lmstudio" | "mem0.llms.lmstudio.LMStudioLLM" | "LMStudioConfig"
"vllm" | "mem0.llms.vllm.VllmLLM" | "VllmConfig"
"langchain" | "mem0.llms.langchain.LangchainLLM" | "BaseLlmConfig"
}
```

**Diagram sources**
- [factory.py](file://mem0/utils/factory.py#L30-L48)

**Section sources**
- [factory.py](file://mem0/utils/factory.py#L30-L48)

#### Configuration Handling
The factory supports three configuration types with appropriate conversion logic:

```mermaid
stateDiagram-v2
[*] --> NullConfig
[*] --> DictConfig
[*] --> BaseConfig
[*] --> SpecificConfig
NullConfig --> CreateDefault : config is None
DictConfig --> MergeAndCreate : config is dict
BaseConfig --> ConvertAndCreate : config is BaseLlmConfig
SpecificConfig --> UseDirectly : config is provider-specific
CreateDefault --> ReturnInstance : config_class(**kwargs)
MergeAndCreate --> ReturnInstance : config.update(kwargs), config_class(**config)
ConvertAndCreate --> CheckType : config_class != BaseLlmConfig?
CheckType --> |Yes| ConvertToSpecific : Extract common params, create specific config
CheckType --> |No| UseBase : Use BaseLlmConfig as-is
ConvertToSpecific --> ReturnInstance
UseBase --> ReturnInstance
UseDirectly --> ReturnInstance
ReturnInstance --> [*]
```

**Diagram sources**
- [factory.py](file://mem0/utils/factory.py#L73-L102)

**Section sources**
- [factory.py](file://mem0/utils/factory.py#L73-L102)

### Configuration Classes Analysis
The configuration system uses a hierarchy of classes to handle both common and provider-specific parameters.

#### Base Configuration
```mermaid
classDiagram
class BaseLlmConfig {
+model : Optional[Union[str, Dict]]
+temperature : float = 0.1
+api_key : Optional[str]
+max_tokens : int = 2000
+top_p : float = 0.1
+top_k : int = 1
+enable_vision : bool = False
+vision_details : Optional[str] = "auto"
+http_client : Optional[httpx.Client]
+__init__(model, temperature, api_key, max_tokens, top_p, top_k, enable_vision, vision_details, http_client_proxies)
}
```

**Diagram sources**
- [base.py](file://mem0/configs/llms/base.py#L7-L63)

**Section sources**
- [base.py](file://mem0/configs/llms/base.py#L7-L63)

#### Provider-Specific Configuration Examples
```mermaid
classDiagram
class OpenAIConfig {
+openai_base_url : Optional[str]
+models : Optional[List[str]]
+route : Optional[str]
+openrouter_base_url : Optional[str]
+site_url : Optional[str]
+app_name : Optional[str]
+store : bool
+response_callback : Optional[Callable[[Any, dict, dict], None]]
}
class AnthropicConfig {
+anthropic_base_url : Optional[str]
}
class OllamaConfig {
+ollama_base_url : Optional[str]
}
class AzureOpenAIConfig {
+azure_kwargs : AzureConfig
}
BaseLlmConfig <|-- OpenAIConfig
BaseLlmConfig <|-- AnthropicConfig
BaseLlmConfig <|-- OllamaConfig
BaseLlmConfig <|-- AzureOpenAIConfig
```

**Diagram sources**
- [openai.py](file://mem0/configs/llms/openai.py#L6-L80)
- [anthropic.py](file://mem0/configs/llms/anthropic.py#L6-L57)
- [ollama.py](file://mem0/configs/llms/ollama.py#L6-L57)
- [azure.py](file://mem0/configs/llms/azure.py#L7-L58)

**Section sources**
- [openai.py](file://mem0/configs/llms/openai.py#L6-L80)
- [anthropic.py](file://mem0/configs/llms/anthropic.py#L6-L57)
- [ollama.py](file://mem0/configs/llms/ollama.py#L6-L57)
- [azure.py](file://mem0/configs/llms/azure.py#L7-L58)

### Implementation Examples
The LLM implementations follow a consistent pattern across providers:

```mermaid
sequenceDiagram
participant User
participant LlmFactory
participant LLMInstance
participant API
User->>LlmFactory : create(provider_name, config, **kwargs)
LlmFactory->>LlmFactory : Validate provider
LlmFactory->>LlmFactory : Handle configuration
LlmFactory->>LlmFactory : Load LLM class
LlmFactory->>LLMInstance : Initialize with config
LLMInstance->>LLMInstance : Set default model
LLMInstance->>LLMInstance : Initialize API client
LlmFactory-->>User : Return LLM instance
User->>LLMInstance : generate_response(messages, **params)
LLMInstance->>LLMInstance : Prepare parameters
LLMInstance->>API : Call API with parameters
API-->>LLMInstance : Return response
LLMInstance->>LLMInstance : Process response
LLMInstance-->>User : Return processed response
```

**Diagram sources**
- [openai.py](file://mem0/llms/openai.py#L14-L148)
- [anthropic.py](file://mem0/llms/anthropic.py#L14-L88)
- [ollama.py](file://mem0/llms/ollama.py#L13-L115)

**Section sources**
- [openai.py](file://mem0/llms/openai.py#L14-L148)
- [anthropic.py](file://mem0/llms/anthropic.py#L14-L88)
- [ollama.py](file://mem0/llms/ollama.py#L13-L115)

## Dependency Analysis
```mermaid
graph TD
LlmFactory --> load_class : "uses"
LlmFactory --> BaseLlmConfig : "depends on"
LlmFactory --> OpenAIConfig : "depends on"
LlmFactory --> AnthropicConfig : "depends on"
LlmFactory --> OllamaConfig : "depends on"
LlmFactory --> AzureOpenAIConfig : "depends on"
LlmFactory --> DeepSeekConfig : "depends on"
LlmFactory --> LMStudioConfig : "depends on"
LlmFactory --> VllmConfig : "depends on"
BaseLlmConfig --> httpx : "uses"
OpenAIConfig --> OpenAI : "uses"
AnthropicConfig --> anthropic : "uses"
OllamaConfig --> ollama : "uses"
AzureOpenAIConfig --> AzureConfig : "uses"
LlmFactory --> LLMBase : "creates"
OpenAILLM --> OpenAI : "uses"
AnthropicLLM --> anthropic : "uses"
OllamaLLM --> ollama : "uses"
```

**Diagram sources**
- [factory.py](file://mem0/utils/factory.py#L23-L129)
- [base.py](file://mem0/configs/llms/base.py#L7-L63)
- [openai.py](file://mem0/configs/llms/openai.py#L6-L80)
- [anthropic.py](file://mem0/configs/llms/anthropic.py#L6-L57)
- [ollama.py](file://mem0/configs/llms/ollama.py#L6-L57)
- [azure.py](file://mem0/configs/llms/azure.py#L7-L58)
- [openai.py](file://mem0/llms/openai.py#L14-L148)
- [anthropic.py](file://mem0/llms/anthropic.py#L14-L88)
- [ollama.py](file://mem0/llms/ollama.py#L13-L115)

**Section sources**
- [factory.py](file://mem0/utils/factory.py#L23-L129)

## Performance Considerations
The LlmFactory implementation includes several performance considerations:

1. **Instance Reuse**: LLM instances should be reused rather than created repeatedly, as initialization involves API client setup and configuration processing.

2. **Configuration Caching**: For applications with frequent LLM creation, consider caching commonly used configurations to avoid repeated dictionary merging and object creation.

3. **Lazy Initialization**: The factory could be extended with lazy initialization patterns to defer expensive operations until the first method call.

4. **Connection Pooling**: The underlying API clients (OpenAI, Anthropic, etc.) typically handle connection pooling internally, but this should be verified for each provider.

5. **Error Handling**: The factory provides clear error messages for unsupported providers, helping to prevent repeated failed instantiation attempts.

6. **Thread Safety**: The current implementation appears to be thread-safe as it doesn't maintain mutable shared state across method calls.

**Section sources**
- [factory.py](file://mem0/utils/factory.py#L23-L129)