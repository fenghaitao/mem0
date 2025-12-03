# AWS Bedrock

<cite>
**Referenced Files in This Document**   
- [aws_bedrock.py](file://mem0/configs/llms/aws_bedrock.py)
- [aws_bedrock.py](file://mem0/llms/aws_bedrock.py)
- [aws_bedrock.py](file://mem0/embeddings/aws_bedrock.py)
- [aws_bedrock.yaml](file://embedchain/configs/aws_bedrock.yaml)
- [aws_bedrock.mdx](file://docs/components/llms/models/aws_bedrock.mdx)
- [aws_bedrock.mdx](file://docs/components/embedders/models/aws_bedrock.mdx)
- [aws-bedrock.ipynb](file://embedchain/notebooks/aws-bedrock.ipynb)
- [test_aws_bedrock.py](file://tests/llm/test_aws_bedrock.py)
- [exceptions.py](file://mem0/exceptions.py)
</cite>

## Table of Contents
1. [Introduction](#introduction)
2. [AWS Credential Configuration](#aws-credential-configuration)
3. [Region Specification](#region-specification)
4. [Supported Foundation Models](#supported-foundation-models)
5. [LLM Initialization with Custom Parameters](#llm-initialization-with-custom-parameters)
6. [AWS Signature Version 4 Signing](#aws-signature-version-4-signing)
7. [Error Handling](#error-handling)
8. [VPC Configuration, Encryption, and Compliance](#vpc-configuration-encryption-and-compliance)
9. [Cost Implications](#cost-implications)
10. [Best Practices and Recommendations](#best-practices-and-recommendations)

## Introduction

AWS Bedrock integration in Mem0 provides access to a wide range of foundation models from various providers including Anthropic, Amazon, Cohere, Meta, and others. This integration enables developers to leverage state-of-the-art language models for natural language processing tasks within their applications. The implementation supports both LLM inference and embedding generation through AWS Bedrock's managed service.

The integration is designed to be flexible, allowing configuration through multiple methods including IAM roles, access keys, environment variables, and AWS profiles. It supports all available Bedrock models with automatic provider detection and handles the complexities of AWS authentication and request signing internally.

**Section sources**
- [aws_bedrock.mdx](file://docs/components/llms/models/aws_bedrock.mdx)
- [aws_bedrock.mdx](file://docs/components/embedders/models/aws_bedrock.mdx)

## AWS Credential Configuration

AWS Bedrock integration in Mem0 supports multiple methods for configuring AWS credentials, providing flexibility for different deployment scenarios and security requirements.

### Environment Variables
The simplest method is to set AWS credentials as environment variables:
```bash
export AWS_ACCESS_KEY_ID=your-access-key
export AWS_SECRET_ACCESS_KEY=your-secret-key
export AWS_SESSION_TOKEN=your-session-token  # For temporary credentials
export AWS_REGION=us-west-2
```

### Configuration Parameters
Credentials can be passed directly in the configuration object:
```python
config = {
    "llm": {
        "provider": "aws_bedrock",
        "config": {
            "model": "anthropic.claude-3-5-sonnet-20240620-v1:0",
            "aws_access_key_id": "your-access-key",
            "aws_secret_access_key": "your-secret-key",
            "aws_region": "us-west-2"
        }
    }
}
```

### IAM Roles
For applications running on AWS infrastructure (EC2, ECS, Lambda), IAM roles provide a secure way to grant permissions without managing access keys. The AWS SDK automatically retrieves temporary credentials from the instance metadata service.

### AWS Profile
You can specify an AWS profile name that contains the credentials:
```python
config = {
    "llm": {
        "provider": "aws_bedrock",
        "config": {
            "model": "anthropic.claude-3-5-sonnet-20240620-v1:0",
            "aws_profile": "my-profile",
            "aws_region": "us-west-2"
        }
    }
}
```

The configuration follows a hierarchy where explicitly provided credentials take precedence over environment variables, which in turn take precedence over AWS profiles and IAM roles.

**Section sources**
- [aws_bedrock.py](file://mem0/configs/llms/aws_bedrock.py#L21-L25)
- [aws_bedrock.py](file://mem0/llms/aws_bedrock.py#L76-L107)
- [aws_bedrock.mdx](file://docs/components/llms/models/aws_bedrock.mdx)

## Region Specification

AWS Bedrock is available in specific regions, and the integration requires proper region configuration for optimal performance and compliance.

### Supported Regions
The following regions support AWS Bedrock:
- us-east-1
- us-west-2
- us-east-2
- eu-west-1
- ap-southeast-1
- ap-northeast-1

### Region Configuration
The region can be specified in multiple ways:
1. **Configuration parameter**: `aws_region` in the config object
2. **Environment variable**: `AWS_REGION`
3. **Default value**: If not specified, defaults to `us-west-2`

```python
config = {
    "llm": {
        "provider": "aws_bedrock",
        "config": {
            "model": "anthropic.claude-3-5-sonnet-20240620-v1:0",
            "aws_region": "us-east-1"  # Specify region
        }
    }
}
```

The integration validates the region against the list of supported regions and provides appropriate error messages if an unsupported region is specified.

**Section sources**
- [aws_bedrock.py](file://mem0/configs/llms/aws_bedrock.py#L23-L24)
- [aws_bedrock.py](file://mem0/configs/llms/aws_bedrock.py#L142-L151)

## Supported Foundation Models

Mem0's AWS Bedrock integration supports a wide range of foundation models from various providers, each with different capabilities and use cases.

### Model Providers
The integration supports models from the following providers:
- **Anthropic**: Claude series (Haiku, Sonnet, Opus)
- **Amazon**: Titan series (Text, Embed)
- **Cohere**: Command series
- **Meta**: Llama series
- **Mistral**: Mixtral, Mistral models
- **AI21**: Jurassic series
- **Stability AI**: Stable Diffusion

### Model Format
Models are identified using the format `provider.model-name:version`, for example:
- `anthropic.claude-3-5-sonnet-20240620-v1:0`
- `amazon.titan-text-express-v1`
- `meta.llama3-70b-instruct-v1:0`

The integration validates the model identifier format and provider against a list of known providers to ensure correctness.

### Capabilities by Provider
Different providers offer different capabilities:
- **Anthropic**: Supports tools, vision, streaming, and multimodal inputs
- **Amazon**: Supports tools, vision, streaming, and multimodal inputs
- **Cohere**: Supports tools and streaming
- **Meta**: Supports vision and streaming
- **Mistral**: Supports vision and streaming

**Section sources**
- [aws_bedrock.py](file://mem0/configs/llms/aws_bedrock.py#L127-L130)
- [aws_bedrock.py](file://mem0/llms/aws_bedrock.py#L18-L21)
- [aws_bedrock.py](file://mem0/llms/aws_bedrock.py#L162-L190)

## LLM Initialization with Custom Parameters

The AWS Bedrock LLM in Mem0 can be initialized with various custom parameters to control the behavior of the language model.

### Initialization Parameters
```python
from mem0.configs.llms.aws_bedrock import AWSBedrockConfig

config = AWSBedrockConfig(
    model="anthropic.claude-3-5-sonnet-20240620-v1:0",
    temperature=0.2,
    max_tokens=2000,
    top_p=0.9,
    top_k=1,
    aws_access_key_id="your-access-key",
    aws_secret_access_key="your-secret-key",
    aws_region="us-west-2",
    model_kwargs={"param": "value"}
)
```

### Key Parameters
- **temperature**: Controls randomness (0.0 to 2.0). Lower values make output more deterministic.
- **max_tokens**: Maximum number of tokens to generate in the response.
- **top_p**: Nucleus sampling parameter (0.0 to 1.0). Controls diversity of output.
- **top_k**: Top-k sampling parameter (1 to 40). Limits sampling to top k tokens.
- **model_kwargs**: Additional model-specific parameters.

### Usage Example
```python
import os
from mem0 import Memory

# Set environment variables
os.environ['AWS_REGION'] = 'us-west-2'
os.environ["AWS_ACCESS_KEY_ID"] = "your-access-key"
os.environ["AWS_SECRET_ACCESS_KEY"] = "your-secret-key"

config = {
    "llm": {
        "provider": "aws_bedrock",
        "config": {
            "model": "anthropic.claude-3-5-haiku-20241022-v1:0",
            "temperature": 0.2,
            "max_tokens": 2000,
        }
    }
}

m = Memory.from_config(config)
```

**Section sources**
- [aws_bedrock.py](file://mem0/configs/llms/aws_bedrock.py#L14-L60)
- [aws_bedrock.mdx](file://docs/components/llms/models/aws_bedrock.mdx)

## AWS Signature Version 4 Signing

AWS Signature Version 4 signing is handled internally by the AWS Bedrock integration in Mem0, abstracting the complexity from developers.

### Internal Implementation
The integration uses the `boto3` library, which automatically handles AWS Signature Version 4 signing for all API requests. This includes:
- Creating a canonical request
- Deriving a signing key from your AWS secret access key
- Creating a signature using the signing key
- Adding the signature to the request

### Prerequisites
To ensure proper signing:
1. Install the required dependency: `pip install boto3`
2. Configure AWS credentials through one of the supported methods
3. Ensure network connectivity to AWS Bedrock endpoints

### Security Considerations
- Credentials are never stored in the application code
- Temporary credentials (session tokens) are supported for enhanced security
- The integration follows AWS best practices for credential management

The signing process is transparent to the developer, with the `boto3` client handling all aspects of request authentication automatically.

**Section sources**
- [aws_bedrock.py](file://mem0/llms/aws_bedrock.py#L76-L107)
- [aws_bedrock.py](file://mem0/embeddings/aws_bedrock.py#L41-L47)

## Error Handling

The AWS Bedrock integration in Mem0 provides comprehensive error handling for common issues encountered when using the service.

### Common Errors and Solutions

#### AccessDeniedException
This error occurs when the AWS credentials don't have sufficient permissions to access Bedrock.

**Solution**:
- Ensure the IAM role or user has the `bedrock:InvokeModel` permission
- Verify the region is correct and supported
- Check that model access has been granted in the Bedrock console

```python
# Error raised internally
raise ValueError(
    f"Unauthorized access to Bedrock. Please ensure your AWS credentials "
    f"have permission to access Bedrock in region {self.config.aws_region}."
)
```

#### ResourceNotFoundException
This error occurs when attempting to access a model that doesn't exist or isn't available in the specified region.

**Solution**:
- Verify the model ID is correct
- Check that the model is available in the specified region
- Ensure model access has been granted in the Bedrock console

#### Throttling
AWS Bedrock may throttle requests if the rate limit is exceeded.

**Solution**:
- Implement exponential backoff in your application
- Monitor usage and request quota increases if needed
- Distribute requests across multiple regions if possible

### Error Types
The integration handles various error types:
- **NoCredentialsError**: Raised when AWS credentials are not found
- **ClientError**: Raised for AWS service errors
- **ValueError**: Raised for configuration errors
- **RuntimeError**: Raised for response generation failures

### Error Handling Implementation
```python
try:
    # AWS Bedrock API call
    response = self.client.invoke_model(...)
except NoCredentialsError:
    raise ValueError("AWS credentials not found. Please set AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, and AWS_REGION environment variables, or provide them in the config.")
except ClientError as e:
    if e.response["Error"]["Code"] == "UnauthorizedOperation":
        raise ValueError(f"Unauthorized access to Bedrock. Please ensure your AWS credentials have permission to access Bedrock in region {self.config.aws_region}.")
    else:
        raise ValueError(f"AWS Bedrock error: {e}")
```

**Section sources**
- [aws_bedrock.py](file://mem0/llms/aws_bedrock.py#L86-L99)
- [exceptions.py](file://mem0/exceptions.py)
- [aws_bedrock.py](file://mem0/llms/aws_bedrock.py#L454-L456)

## VPC Configuration, Encryption, and Compliance

When using AWS Bedrock with Mem0, several network, security, and compliance considerations must be addressed.

### VPC Configuration
AWS Bedrock can be accessed from within a VPC using VPC endpoints (AWS PrivateLink), which provide private connectivity to the service without requiring an internet gateway, NAT device, or VPN connection.

**Benefits**:
- Enhanced security by keeping traffic within the AWS network
- Reduced exposure to the public internet
- Simplified network architecture

### Encryption
AWS Bedrock automatically encrypts data at rest and in transit:
- **In transit**: All data is encrypted using TLS 1.2+
- **At rest**: Data is encrypted using AWS-managed keys or customer-managed keys (CMK) in AWS KMS

### Compliance Considerations
When using AWS Bedrock, consider the following compliance aspects:
- **Data residency**: Ensure the selected region complies with your data residency requirements
- **GDPR**: AWS Bedrock supports GDPR compliance for handling personal data
- **HIPAA**: AWS Bedrock is HIPAA eligible for handling protected health information
- **PCI DSS**: AWS Bedrock is PCI DSS compliant

### Security Best Practices
- Use IAM roles instead of long-term access keys when possible
- Apply the principle of least privilege to IAM policies
- Enable AWS CloudTrail for auditing API calls
- Use VPC endpoints for private connectivity
- Regularly rotate credentials and keys

The integration respects AWS security best practices and allows configuration of these security features through standard AWS mechanisms.

**Section sources**
- [aws_bedrock.mdx](file://docs/components/llms/models/aws_bedrock.mdx)
- [aws_bedrock.py](file://mem0/llms/aws_bedrock.py#L76-L107)

## Cost Implications

Understanding the cost implications of using AWS Bedrock with different models and regions is essential for budget planning and optimization.

### Pricing Model
AWS Bedrock pricing is based on:
- **Input tokens**: Number of tokens in the prompt
- **Output tokens**: Number of tokens generated in the response
- **Model type**: Different models have different pricing tiers

### Cost Comparison by Model
- **Claude Haiku**: Most cost-effective for simple tasks
- **Claude Sonnet**: Balance of cost and capability for most applications
- **Claude Opus**: Highest cost, for complex reasoning tasks
- **Titan models**: Generally more cost-effective than third-party models
- **Llama models**: Competitive pricing for open-source model performance

### Regional Pricing
Pricing may vary by region, with us-east-1 and us-west-2 typically having the most competitive rates. Other regions may have slightly higher costs due to infrastructure and operational differences.

### Cost Optimization Strategies
1. **Choose the right model**: Use Haiku for simple tasks, Sonnet for general purposes, and Opus only when necessary
2. **Control response length**: Set appropriate `max_tokens` values to avoid unnecessary generation
3. **Cache responses**: Implement caching for frequently requested content
4. **Monitor usage**: Use AWS Cost Explorer to track and analyze Bedrock usage
5. **Set budget alerts**: Configure AWS Budgets to receive notifications when spending thresholds are reached

### Example Cost Calculation
For a typical interaction:
- Input: 100 tokens
- Output: 200 tokens
- Model: Claude Sonnet ($3 per million input tokens, $15 per million output tokens)
- Cost: (100/1M * $3) + (200/1M * $15) = $0.0003 + $0.003 = $0.0033 per interaction

For high-volume applications, consider the total monthly cost based on expected usage patterns.

**Section sources**
- [aws_bedrock.mdx](file://docs/components/llms/models/aws_bedrock.mdx)
- [aws_bedrock.yaml](file://embedchain/configs/aws_bedrock.yaml)

## Best Practices and Recommendations

To ensure optimal performance, security, and cost-effectiveness when using AWS Bedrock with Mem0, follow these best practices.

### Configuration Best Practices
- **Use environment variables** for credentials in development, but **IAM roles** in production
- **Set appropriate timeouts** for API calls to handle network latency
- **Validate model availability** in your chosen region before deployment
- **Use the latest model versions** for improved performance and features

### Performance Optimization
- **Enable streaming** for large responses to improve user experience
- **Cache embeddings** to avoid redundant computation
- **Batch requests** when possible to reduce API call overhead
- **Monitor latency** and adjust configuration as needed

### Security Recommendations
- **Rotate credentials** regularly and use temporary credentials when possible
- **Restrict IAM policies** to the minimum required permissions
- **Use VPC endpoints** for private connectivity in production environments
- **Enable CloudTrail logging** for audit and compliance purposes

### Monitoring and Observability
- **Implement structured logging** to track API calls and responses
- **Monitor error rates** and set up alerts for unusual patterns
- **Track token usage** to understand cost drivers
- **Use AWS CloudWatch** for monitoring Bedrock metrics

### Development Workflow
1. Start with **Claude Haiku** for development and testing
2. Move to **Claude Sonnet** for production applications
3. Use **Claude Opus** only for complex reasoning tasks
4. Test with **Titan embeddings** for cost-effective vector storage

By following these best practices, you can ensure a secure, performant, and cost-effective integration of AWS Bedrock with Mem0.

**Section sources**
- [aws_bedrock.mdx](file://docs/components/llms/models/aws_bedrock.mdx)
- [aws_bedrock.mdx](file://docs/components/embedders/models/aws_bedrock.mdx)
- [aws-bedrock.ipynb](file://embedchain/notebooks/aws-bedrock.ipynb)