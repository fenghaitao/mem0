import os
from typing import Literal, Optional

try:
    import litellm
except ImportError:
    raise ImportError("The 'litellm' library is required. Please install it using 'pip install litellm'.")

from mem0.configs.embeddings.base import BaseEmbedderConfig
from mem0.embeddings.base import EmbeddingBase


class GitHubCopilotEmbedding(EmbeddingBase):
    def __init__(self, config: Optional[BaseEmbedderConfig] = None):
        super().__init__(config)

        self.config.model = self.config.model or "github_copilot/text-embedding-3-small"
        self.config.embedding_dims = self.config.embedding_dims or 1536

        # GitHub Copilot uses OAuth2 authentication - no token setup needed

    def embed(self, text, memory_action: Optional[Literal["add", "search", "update"]] = None):
        """
        Get the embedding for the given text using GitHub Copilot.

        Args:
            text (str): The text to embed.
            memory_action (optional): The type of embedding to use. Must be one of "add", "search", or "update". Defaults to None.
        
        Returns:
            list: The embedding vector.
        """
        text = text.replace("\n", " ")
        
        try:
            response = litellm.embedding(
                model=self.config.model,
                input=[text],
                dimensions=self.config.embedding_dims
            )
            
            # Handle different response formats from GitHub Copilot
            if hasattr(response, 'data') and response.data:
                if hasattr(response.data[0], 'embedding'):
                    return response.data[0].embedding
                elif isinstance(response.data[0], dict) and 'embedding' in response.data[0]:
                    return response.data[0]['embedding']
            elif isinstance(response, list):
                return response[0] if response else []
            elif isinstance(response, dict):
                if 'data' in response and response['data']:
                    if isinstance(response['data'][0], dict) and 'embedding' in response['data'][0]:
                        return response['data'][0]['embedding']
                    return response['data'][0]
                return response.get('embedding', [])
            
            # Fallback
            return response
            
        except Exception as e:
            raise Exception(f"GitHub Copilot embedding failed: {str(e)}")