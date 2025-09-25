# AWS BEDROCK AGENT CORE 

## Installation

```bash
git clone https://github.com/kanitvural/aws-bedrock-agent-core.git
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Create OpenAI Vector Store

```bash
python CreateOpenAIVectorStore.py
```

### Localhost Execution

```bash
python /AgentCoreRuntime/data_agent_agentcore.py 
```

```bash
curl -X POST http://localhost:8080/invocations \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Hello, Data! Summarize your ethical subroutines."}'

```


The `app.run()` command launches a local HTTP server (by default most frameworks use something like `localhost:8080`).

This means that **BedrockAgentCoreApp does not create any AWS endpoint** at this stage.

When you send a request to this local server (e.g., `POST /invoke`), the agents defined in your code run **directly on your computer**.

**Summary:** This setup is meant only for development and testing. No AWS deployment is involved yet.



## Deploy To AWS

AgentCore is actually a containerized system. You write your agent code, and it:

- Wraps it into a Docker container
- Pushes it to ECR (Elastic Container Registry)
- Runs it as a serverless container runtime
- Handles auto-scaling automatically
  
1. Go to Cloudwatch -> Application Signals -> Transaction Search and enable it.
2. Go to bash and type

```bash
agentcore configure -e data_agent_agentcore.py
```

press enter for steps and finally `no` for OAuth authorizer

```
✓ Will auto-create execution role

🏗️  ECR Repository
Press Enter to auto-create ECR repository, or provide ECR Repository URI to use 
existing
ECR Repository URI (or press Enter to auto-create):
✓ Will auto-create ECR repository

🔍 Detected dependency file: requirements.txt
Press Enter to use this file, or type a different path (use Tab for autocomplete):
Path or Press Enter to use detected dependency file:
✓ Using detected file: requirements.txt

🔐 Authorization Configuration
By default, Bedrock AgentCore uses IAM authorization.
Configure OAuth authorizer instead? (yes/no) [no]: no

🔒 Request Header Allowlist
Configure which request headers are allowed to pass through to your agent.
Common headers: Authorization, X-Amzn-Bedrock-AgentCore-Runtime-Custom-*
Configure request header allowlist? (yes/no) [no]:
✓ Using default request header configuration
Configuring BedrockAgentCore agent: data_agent_agentcore
```

```bash
agentcore launch
```

For local deployment

```bash
agentcore launch --local
```

```
 ✅ CodeBuild Deployment Successful!                                                 │
│                                                                                     │
│ Agent Details:                                                                      │
│ Agent Name: data_agent_agentcore                                                    │
│ Agent ARN:                                                                          │
│ arn:aws:bedrock-agentcore:eu-central-1:058264126563:runtime/data_agent_agentcore-po │
│ pt2eDyyh                                                                            │
│ ECR URI:                                                                            │
│ 058264126563.dkr.ecr.eu-central-1.amazonaws.com/bedrock-agentcore-data_agent_agentc │
│ ore:latest                                                                          │
│ CodeBuild ID:                                                                       │
│ bedrock-agentcore-data_agent_agentcore-builder:517690e0-048f-4de7-9930-8b9b1b71e070 │
│                                                                                     │
│ 🚀 ARM64 container deployed to Bedrock AgentCore                                    │
│                                                                                     │
│ Next Steps:                                                                         │
│    agentcore status                                                                 │
│    agentcore invoke '{"prompt": "Hello"}'                                           │
│                                                                                     │
│ 📋 CloudWatch Logs:                                                                 │
│    /aws/bedrock-agentcore/runtimes/data_agent_agentcore-popt2eDyyh-DEFAULT          │
│ --log-stream-name-prefix "2025/09/25/[runtime-logs]"                                │
│    /aws/bedrock-agentcore/runtimes/data_agent_agentcore-popt2eDyyh-DEFAULT          │
│ --log-stream-names "otel-rt-logs"                                                   │
│                                                                                     │
│ 🔍 GenAI Observability Dashboard:                                                   │
│    https://console.aws.amazon.com/cloudwatch/home?region=eu-central-1#gen-ai-observ │
│ ability/agent-core                                                                  │
│                                                                                     │
│ ⏱️  Note: Observability data may take up to 10 minutes to appear after first launch  │
│                                                                                     │
│ 💡 Tail logs with:                                                                  │
│    aws logs tail                                                                    │
│ /aws/bedrock-agentcore/runtimes/data_agent_agentcore-popt2eDyyh-DEFAULT             │
│ --log-stream-name-prefix "2025/09/25/[runtime-logs]" --follow                       │
│    aws logs tail                                                                    │
│ /aws/bedrock-agentcore/runtimes/data_agent_agentcore-popt2eDyyh-DEFAULT             │
│ --log-stream-name-prefix "2025/09/25/[runtime-logs]" --since 1h    
```

**See the container in Codebuild and ECR**

**Go to AWS Console > Amazon Bedrock AgentCore > Agent Runtime > data_agent_agentcore**

## Running AgentCore App Using the Starter Toolkit

Test

```bash
agentcore invoke "{\"prompt\": \"Data, who was Lal?\"}"
```
```bash
Invocation failed: An error occurred (RuntimeClientError) when calling the 
InvokeAgentRuntime operation: An error occurred when starting the runtime. Please check
your CloudWatch logs for more information.
```

see the cloudwatch logs: `  raise RuntimeError("Please set OPENAI_API_KEY.")`


```bash
export OPENAI_API_KEY="your_openai_api_key"
agentcore launch --env OPENAI_API_KEY=$OPENAI_API_KEY
agentcore invoke "{\"prompt\": \"Data, who was Lal?\"}"

Response:
{"result": "Lal was my daughter, an android I created using myself as a model. She 
possessed a positronic brain similar to my own, but her matrix was unstable, and she 
only lived a short time. I created Lal because I wished to procreate and continue the 
work of Dr. Soong, my own creator."}
```

Go to AWS Console > Amazon Bedrock AgentCore > Agent Runtime > data_agent_agentcore and copy the python code. Change region. Save as `data_test.py`

```python
import boto3
import json

client = boto3.client('bedrock-agentcore', region_name='eu-central-1')
payload = json.dumps({
    "prompt": "Explain machine learning in simple terms"
})

response = client.invoke_agent_runtime(
    agentRuntimeArn='arn:aws:bedrock-agentcore:eu-central-1:058264126563:runtime/data_agent_agentcore-popt2eDyyh',
    runtimeSessionId='dfmeoagmreaklgmrkleafremoigrmtesogmtrskhmtkrlshmt',  # Must be 33+ chars
    payload=payload,
    qualifier="DEFAULT"
)
response_body = response['response'].read()
response_data = json.loads(response_body)
print("Agent Response:", response_data)
```
```bash
python data_test.py
```

## Destroy AgentCore App

```bash
agentcore destroy
```