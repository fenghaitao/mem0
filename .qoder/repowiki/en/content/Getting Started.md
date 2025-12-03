# Getting Started

<cite>
**Referenced Files in This Document**   
- [README.md](file://README.md)
- [mem0/__init__.py](file://mem0/__init__.py)
- [mem0/client/main.py](file://mem0/client/main.py)
- [mem0/memory/main.py](file://mem0/memory/main.py)
- [mem0-ts/package.json](file://mem0-ts/package.json)
- [mem0-ts/src/client/index.ts](file://mem0-ts/src/client/index.ts)
- [mem0-ts/src/client/mem0.ts](file://mem0-ts/src/client/mem0.ts)
</cite>

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Installation](#installation)
3. [Configuration](#configuration)
4. [Basic Usage](#basic-usage)
5. [Troubleshooting](#troubleshooting)
6. [Next Steps](#next-steps)

## Prerequisites

Before getting started with Mem0, ensure you have the following prerequisites:

- **Python 3.8+**: The Python SDK requires Python 3.8 or higher. You can verify your Python version by running `python --version` in your terminal.
- **Node.js 18+**: The TypeScript client requires Node.js version 18 or higher. Verify your Node.js version with `node --version`.
- **API Key**: You'll need a Mem0 API key to authenticate with the service. You can obtain your API key by signing up on the [Mem0 Platform](https://app.mem0.ai/dashboard/api-keys).
- **LLM Provider**: Mem0 requires a Large Language Model (LLM) provider to function. By default, it uses `gpt-4o-mini` from OpenAI, but it supports various LLMs including Anthropic, Cohere, and others. For a complete list, refer to the [Supported LLMs documentation](https://docs.mem0.ai/components/llms/overview).

**Section sources**
- [README.md](file://README.md#L56-L138)
- [mem0-ts/README.md](file://mem0-ts/README.md#L1-L40)

## Installation

### Python SDK Installation

Install the Mem0 Python SDK using pip:

```bash
pip install mem0ai
```

### TypeScript Client Installation

Install the Mem0 TypeScript client using npm:

```bash
npm install mem0ai
```

**Section sources**
- [README.md](file://README.md#L85-L94)
- [mem0-ts/README.md](file://mem0-ts/README.md#L12-L14)

## Configuration

### Setting Environment Variables

After installation, configure your environment by setting the required environment variables. The primary configuration is your Mem0 API key:

```bash
export MEM0_API_KEY=your_api_key_here
```

For cloud-based usage, you can also set optional organization and project identifiers:

```bash
export MEM0_ORG_ID=your_org_id
export MEM0_PROJECT_ID=your_project_id
```

### Creating a Configuration Object

You can also configure the client programmatically by passing options directly to the constructor:

**Python Configuration**
```python
from mem0 import Memory

# Initialize with API key
memory = Memory(api_key="your_api_key_here")

# Or with additional configuration
memory = Memory(
    api_key="your_api_key_here",
    host="https://api.mem0.ai",  # Optional custom host
    org_id="your_org_id",       # Optional organization ID
    project_id="your_project_id" # Optional project ID
)
```

**TypeScript Configuration**
```typescript
import { MemoryClient } from "mem0ai";

// Initialize with API key
const client = new MemoryClient({
    apiKey: "your_api_key_here"
});

// Or with additional configuration
const client = new MemoryClient({
    apiKey: "your_api_key_here",
    host: "https://api.mem0.ai",  // Optional custom host
    organizationId: "your_org_id", // Optional organization ID
    projectId: "your_project_id"  // Optional project ID
});
```

**Section sources**
- [mem0/client/main.py](file://mem0/client/main.py#L39-L106)
- [mem0-ts/src/client/mem0.ts](file://mem0-ts/src/client/mem0.ts#L28-L89)

## Basic Usage

This section demonstrates the core functionality of Mem0: initialization, adding memories, searching, and retrieving results.

### Python SDK Usage

```python
from openai import OpenAI
from mem0 import Memory

# Initialize OpenAI client and Mem0 memory
openai_client = OpenAI()
memory = Memory()

def chat_with_memories(message: str, user_id: str = "default_user") -> str:
    # Retrieve relevant memories
    relevant_memories = memory.search(query=message, user_id=user_id, limit=3)
    memories_str = "\n".join(f"- {entry['memory']}" for entry in relevant_memories["results"])

    # Generate Assistant response
    system_prompt = f"You are a helpful AI. Answer the question based on query and memories.\nUser Memories:\n{memories_str}"
    messages = [{"role": "system", "content": system_prompt}, {"role": "user", "content": message}]
    response = openai_client.chat.completions.create(model="gpt-4o-mini", messages=messages)
    assistant_response = response.choices[0].message.content

    # Create new memories from the conversation
    messages.append({"role": "assistant", "content": assistant_response})
    memory.add(messages, user_id=user_id)

    return assistant_response

# Example usage
print("Chat with AI (type 'exit' to quit)")
while True:
    user_input = input("You: ").strip()
    if user_input.lower() == 'exit':
        print("Goodbye!")
        break
    print(f"AI: {chat_with_memories(user_input)}")
```

### TypeScript Client Usage

```typescript
import { MemoryClient } from "mem0ai";
import OpenAI from "openai";

// Initialize clients
const openai = new OpenAI();
const client = new MemoryClient({ apiKey: process.env.MEM0_API_KEY! });

async function chatWithMemories(message: string, userId: string = "default_user"): Promise<string> {
    // Retrieve relevant memories
    const relevantMemories = await client.search(message, { user_id: userId, limit: 3 });
    const memoriesStr = relevantMemories.map(entry => `- ${entry.memory}`).join('\n');

    // Generate Assistant response
    const systemPrompt = `You are a helpful AI. Answer the question based on query and memories.\nUser Memories:\n${memoriesStr}`;
    const messages = [
        { role: "system", content: systemPrompt },
        { role: "user", content: message }
    ];
    
    const response = await openai.chat.completions.create({
        model: "gpt-4o-mini",
        messages: messages as any
    });
    
    const assistantResponse = response.choices[0].message.content;

    // Create new memories from the conversation
    messages.push({ role: "assistant", content: assistantResponse });
    await client.add(messages as any, { user_id: userId });

    return assistantResponse || "";
}

// Example usage
console.log("Chat with AI (type 'exit' to quit)");
// Note: In a real application, you would use readline or similar for input
```

**Section sources**
- [README.md](file://README.md#L100-L137)
- [mem0/memory/main.py](file://mem0/memory/main.py#L195-L308)
- [mem0-ts/src/client/mem0.ts](file://mem0-ts/src/client/mem0.ts#L214-L252)

## Troubleshooting

This section addresses common setup issues and their solutions.

### Missing Dependencies

If you encounter dependency-related errors during installation:

1. **Python**: Ensure you're using a compatible Python version (3.8+) and consider using a virtual environment:
   ```bash
   python -m venv mem0-env
   source mem0-env/bin/activate  # On Windows: mem0-env\Scripts\activate
   pip install mem0ai
   ```

2. **Node.js**: Ensure your npm is up to date:
   ```bash
   npm install -g npm@latest
   npm install mem0ai
   ```

### Authentication Errors

Common authentication issues and solutions:

- **"Mem0 API Key not provided"**: Ensure your API key is properly set in the environment or passed to the constructor:
  ```python
  # Check if environment variable is set
  import os
  print("MEM0_API_KEY is set:", "MEM0_API_KEY" in os.environ)
  ```

- **Invalid API Key**: Verify your API key is correct and hasn't expired. You can regenerate it from the [Mem0 Platform](https://app.mem0.ai/dashboard/api-keys).

- **Network Issues**: If you're behind a firewall or proxy, ensure outbound connections to `https://api.mem0.ai` are allowed.

### Configuration Issues

- **Organization/Project ID Errors**: If using organization and project IDs, ensure both are provided together:
  ```python
  memory = Memory(
      api_key="your_key",
      org_id="your_org_id",      # Required if using project_id
      project_id="your_project_id" # Required if using org_id
  )
  ```

- **Custom Host Configuration**: If using a self-hosted instance, ensure the host URL is correctly specified:
  ```python
  memory = Memory(
      api_key="your_key",
      host="https://your-custom-host.com"
  )
  ```

**Section sources**
- [mem0/client/main.py](file://mem0/client/main.py#L70-L71)
- [mem0-ts/src/client/mem0.ts](file://mem0-ts/src/client/mem0.ts#L48-L58)
- [mem0-ts/src/client/mem0.ts](file://mem0-ts/src/client/mem0.ts#L60-L79)

## Next Steps

Now that you've successfully set up Mem0, consider exploring these advanced features:

- **Advanced Memory Operations**: Learn about updating, deleting, and retrieving memory history.
- **Vector Store Integration**: Explore different vector store providers for efficient memory retrieval.
- **LLM Integration**: Configure Mem0 to work with various LLM providers beyond the default OpenAI integration.
- **Production Deployment**: Review best practices for deploying Mem0 in production environments.

For comprehensive documentation, visit the [Mem0 Documentation](https://docs.mem0.ai) portal.

**Section sources**
- [README.md](file://README.md#L149-L152)
- [mem0-ts/README.md](file://mem0-ts/README.md#L5-L6)