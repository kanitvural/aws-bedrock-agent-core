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
agentcore invoke '{"prompt": "Data, who was Lal?"}'
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
agentcore invoke '{"prompt": "Data, who was Lal?"}'

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

## AgentCore Observability and CloudWatch Integration

Go to CloudWatch > Application Signals > GenAI Observability > Bedrock AgentCore

## Inbound and outbound OAuth integration with Cognito and AgentCore

- Just set up Cognito user pool for OAuth / JWT

- Specify the cliendID(s) and discovery URL when running `agentcore configure`

### Outbound authorization

- if you are using an external MCP server set uo credential providers with `aws agent-credential-provider` cli command

- use `@requres_access_token` decorator on functions that access the external API
- 
### Inbound authorization

```bash
cd AgentCoreAuth
python SetupCognito.py  

Enter User Pool Name: agentcore
Enter App Client Name: agentcore-app
Enter Username: kvural
Enter Permanent Password (will be hidden): 


✅ Setup Complete
Pool ID: eu-central-1_Btjy33tH1
Discovery URL: https://cognito-idp.eu-central-1.amazonaws.com/eu-central-1_Btjy33tH1/.well-known/openid-configuration
Client ID: 22artl47oq27reuv5chlinb4l9
Bearer Token: eyJraWQiOiJOZEZ2MVBnd01LVmRCaER3YUZlY2VvYjR3VHlkbWQrVXZJOGVDNW1la1BJPSIsImFsZyI6IlJTMjU2In0.eyJzdWIiOiJkMzc0ZDgyMi01MGUxLTcwNjUtYzg0Ny1hZjliZDE4MzJhOWIiLCJpc3MiOiJodHRwczpcL1wvY29nbml0by1pZHAuZXUtY2VudHJhbC0xLmFtYXpvbmF3cy5jb21cL2V1LWNlbnRyYWwtMV9CdGp5MzN0SDEiLCJjbGllbnRfaWQiOiIyMmFydGw0N29xMjdyZXV2NWNobGluYjRsOSIsIm9yaWdpbl9qdGkiOiI3M2VhMGYzYi03ZjYzLTQ5YzYtOGM1OS02MDUzYTk0NTViNGEiLCJldmVudF9pZCI6IjUxNzhlZTlhLWU0ODctNDk4NC04Mzc3LTIxNGZhZmY4MGU3MiIsInRva2VuX3VzZSI6ImFjY2VzcyIsInNjb3BlIjoiYXdzLmNvZ25pdG8uc2lnbmluLnVzZXIuYWRtaW4iLCJhdXRoX3RpbWUiOjE3NTg5MDExNDYsImV4cCI6MTc1ODkwNDc0NiwiaWF0IjoxNzU4OTAxMTQ2LCJqdGkiOiIyN2YzMzg1ZC1iZTk4LTRhZDEtYjc5My00ZWU4ZTVlMjVkZTgiLCJ1c2VybmFtZSI6Imt2dXJhbCJ9.BHz1l6JHYyDWe7qunx4jzTJYaSsMGd8BJ99GqCVVV3Szw56-_7X4zKFHDMrTAN5p-TVINo_iA3E3LvHTL0wBdazfKvKZoiAXM3GWrAKTWMRQcYEhLvltmoduRPqgAwjqZswF6etf4Z1B77EtyR1rwWG-1TRhB6RjLkmHsPzB7m5ErybHcRItUPoEVG6-qThCVNoP1OhW6vtf4W38g65ggN7JbERTGS7x1IN9Khp4pmESqeLvAimuJRbAcl9El82Pq5ebneID-tcN5hFbMbEyVCTI8mCrqDlVYtqXArDtVp9CH_oQB6ZokNCKiVi_TezcE2zIFG6X4Hl20FyhtTngcw
```

Go to Cognito > User pools

Build the agent again

```bash
 cd AgentCoreRuntime 
 agentcore configure -e data_agent_agentcore.py
```

press enter for steps and finally `yes` for OAuth authorizer

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
Configure OAuth authorizer instead? (yes/no) [no]: yes

🔒 Request Header Allowlist
Configure which request headers are allowed to pass through to your agent.
Common headers: Authorization, X-Amzn-Bedrock-AgentCore-Runtime-Custom-*
Configure request header allowlist? (yes/no) [no]:
✓ Using default request header configuration
Configuring BedrockAgentCore agent: data_agent_agentcore
```

```bash

agentcore invoke "{\"prompt\": \"Data, who was Lal?\"}" --bearer-token eyJraWQiOiJOZEZ2MVBnd01LVmRCaER3YUZlY2VvYjR3VHlkbWQrVXZJOGVDNW1la1BJPSIsImFsZyI6IlJTMjU2In0.eyJzdWIiOiJkMzc0ZDgyMi01MGUxLTcwNjUtYzg0Ny1hZjliZDE4MzJhOWIiLCJpc3MiOiJodHRwczpcL1wvY29nbml0by1pZHAuZXUtY2VudHJhbC0xLmFtYXpvbmF3cy5jb21cL2V1LWNlbnRyYWwtMV9CdGp5MzN0SDEiLCJjbGllbnRfaWQiOiIyMmFydGw0N29xMjdyZXV2NWNobGluYjRsOSIsIm9yaWdpbl9qdGkiOiI3M2VhMGYzYi03ZjYzLTQ5YzYtOGM1OS02MDUzYTk0NTViNGEiLCJldmVudF9pZCI6IjUxNzhlZTlhLWU0ODctNDk4NC04Mzc3LTIxNGZhZmY4MGU3MiIsInRva2VuX3VzZSI6ImFjY2VzcyIsInNjb3BlIjoiYXdzLmNvZ25pdG8uc2lnbmluLnVzZXIuYWRtaW4iLCJhdXRoX3RpbWUiOjE3NTg5MDExNDYsImV4cCI6MTc1ODkwNDc0NiwiaWF0IjoxNzU4OTAxMTQ2LCJqdGkiOiIyN2YzMzg1ZC1iZTk4LTRhZDEtYjc5My00ZWU4ZTVlMjVkZTgiLCJ1c2VybmFtZSI6Imt2dXJhbCJ9.BHz1l6JHYyDWe7qunx4jzTJYaSsMGd8BJ99GqCVVV3Szw56-_7X4zKFHDMrTAN5p-TVINo_iA3E3LvHTL0wBdazfKvKZoiAXM3GWrAKTWMRQcYEhLvltmoduRPqgAwjqZswF6etf4Z1B77EtyR1rwWG-1TRhB6RjLkmHsPzB7m5ErybHcRItUPoEVG6-qThCVNoP1OhW6vtf4W38g65ggN7JbERTGS7x1IN9Khp4pmESqeLvAimuJRbAcl9El82Pq5ebneID-tcN5hFbMbEyVCTI8mCrqDlVYtqXArDtVp9CH_oQB6ZokNCKiVi_TezcE2zIFG6X4Hl20FyhtTngcw

```
## AgentCore Memory

### Short-term
- Chat history within a session / immediate context  
- Enables conversations  
- API centered around **Session objects** that contain **Events**  

### Long-term
- Stores **“extracted insights”**  
- Summaries of past sessions  
- Preferences (your coding style and favorite tools, for example)  
- Facts you gave it in the past  
- API involves **“Memory Records”** that store structured information derived from agent interactions  
- **“Strategies”** for user preferences, semantic facts, session summaries  

---

### Storage
- This all needs to be stored somewhere!  
- The **OpenAI Agents SDK** gives you a SQLite implementation  
- But maybe you need something that scales better, and is serverless  
- Enter **AgentCore Memory**  
### AgentCore Memory Integration

- You’ll need to **modify your agent code** to integrate the AgentCore Memory API calls  
- You need to explicitly **store, retrieve, and delete** these memories  
- AWS’s own **Strands framework** makes this pretty easy  
- Sample code is available for **LangChain / LangGraph** as well  
- But for **OpenAI**, we’re on our own  

---

### OpenAI Agents
- OpenAI Agents use **“Session” objects** for memory  
- They don’t match up really well… but we can make it work…  

##  Integrating short-term memory from AgentCore with OpenAI Agents

Go to Amazon Bedrock AgentCore > Memory > Create memory

You can create 

- Short-term memory (raw event) expiration

- Long-term memory extraction strategies - optional
  - Summarization
  - Semantic Memory
  - User preferences

### İmplementation

1. Create a shorterm memory from AWS console
2. 

```bash
cd AgentCoreMemory 
```
3. Open `data_agent_agentcore_memory.py`

4. Get the `memory_id` from the console
- `session_id` in real app you have a session id. We wrote mock data for this example.
- `actor_id` the user id in the session

```python
#Session for memory, integrating AgentCore's memory features
session = AgentCoreSession(
    session_id="user-1234-convo-abcdef",
    memory_id="memory_wyyo7-UQXcX18hTU",
    actor_id="app/user-1234",
    region="eu-central-1"
)

```

Add session object At the bottom of the script

```python
@app.entrypoint
async def invoke(payload):
    user_message = payload.get("prompt", "Data, reverse the main deflector array!")
    output = ''
    try:
        result = await Runner.run(data_agent, user_message, session=session) # here
        output = result.final_output
    except InputGuardrailTripwireTriggered:
        output = "I'd really rather not talk about Tasha."

    return {"result": output}

if __name__ == "__main__":
    app.run()
```
5. Build and deploy the agent
  
No auth 

```bash
agentcore configure -e data_agent_agentcore_memory.py
export OPENAI_API_KEY="your_openai_api_key"
agentcore launch --env OPENAI_API_KEY=$OPENAI_API_KEY
agentcore invoke "{\"prompt\": \"Data, eject the warp core.\"}" 

Response:
{"result": "Ejecting the warp core is a critical procedure typically reserved for emergencies. 
Please confirm the situation and provide authorization, or specify the emergency protocol to 
proceed."}

agentcore invoke "{\"prompt\": \"Confirmed, authorization code Picard-1\"}"

Response:
{"result": "Authorization code accepted. Initiating warp core ejection sequence as per Starfleet 
emergency protocols. Please stand by for confirmation of successful ejection and containment 
procedures."}

agentcore invoke "{\"prompt\": \"What authorization code did i just use?\"}" 

Response:
{"result": "The authorization code you just used was \"Picard-1.\""}


agentcore destroy
```

## Amazon Bedrock AgentCore Tools, and integrating the code interpreter

- Code Interpreter
  
Lets you run code (in an isolated container)
Python, JavaScript, TypeScript

```bash
 cd AgentCoreCodeInterpreter/
```

open `data_agent_agentcore_memory_interpreter.py` and set the `memory_id` like before.

see the `function_tool` in the script

```python
# ------------------------------------------------------
# NEW: AgentCore Code Interpreter tool (execute_python)
# ------------------------------------------------------
@function_tool
def execute_python(code: str, description: str = "", clear_context: bool = False) -> str:
...
```
```bash
python data_agent_agentcore_memory_interpreter.py

```

```bash
curl -X POST http://localhost:8080/invocations \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Execute this Python code: print(\"Hello world!\")"}'

{"result": "The Python code executed successfully and output: Hello world!"}%  

```

- Browser Tool
  
Allows control of your browser to interact with
the web

## Importing Amazon Bedrock Agents + S3 vectors into AgentCore projects

Bedrock has its own system for endpoints…

* But maybe you want to build on that or something.
* Building agents in Bedrock is super easy.
* Importing is just a matter of running:

```bash
agentcore import-agent
```

* This generates Strands code (or LangChain / LangGraph) in an output directory.
* From there you can test or deploy it like any other AgentCore agent.
  
**"You can import the agent you created in Bedrock into AgentCore and test or deploy it within your own code."**

**!!! Importand Note:**

**Now you don’t have to use OpenSearch for vector storage in Bedrock. You can store embeddings or RAG data directly in S3, making it simpler and serverless. OpenSearch is still optional for large-scale or complex search scenarios.**

### Implementation

1. Create an S3 Bucket for vector store `kntbucket`
2. Upload `data_lines.txt`
3. Go to Bedrock Service > Knowledge Bases
4. Create > Unstructured data -knowledgebase with vector store call it `data-lines`. Select s3 as a data source.
5. Data source name is `data-lines` as well.
6. Select the bucket that you created before.
7. Parsing strategy - Amazon Bedrock default parser - next
8. Select embedding model as `Titan Text Embeddings V2 ` and s3 vector store - next
9. Create Knowledge Base
10. Select data-lines and hit `sync` button.
11. Test Knowledge Base > Retrieval only: data sources and type: "Where was Data Created?"
12. Go to Agents > Create agent name:`LtDataTest`
13. Select model > `Claude 3.5 Sonnet` 
14. Type "You are Lt. Commander Data from Star Trek The Next Generation. Answer all quieris in the syle of the character Data, using the provided knowledge base to ground your responses."
15. Knowledge Bases > Add > select the `data-lines` > Save and Exit > Prepare
16. "Data, how does your brain work?" investigate `Show trace`
17.  We created the agent go back the agentcore
18.  Create BedrockImport folder `cd BedrockImport`
19.  `agentcore import-agent`
20.  Select region as `Frankfurt`
21.  Select the AgentTestAlias
22.  - langchain (0.3.x) + langgraph (0.5.x) -> it bedrock converts agent to langchain
     - » strands (1.0.x) -> select it for easy implementation. (AWS Bedrock framework)
23. Enable verbose output for the generated agent? N
24. ? Would you like to deploy the agent to AgentCore Runtime? (This will take
a few minutes) (y/N) -Yes
25. configure and launch process starts like before. And a bedrock agent deployed via agentcore.
26. ? How would you like to run the agent? (Use arrow keys)
 » Install dependencies and run locally
   Run on AgentCore Runtime
   Don't run now

27.   Enter your question (or 'exit' to quit): "Tell me about Counselor Troi."
28.   Go to AWS Console and delete agent and knowledge base.


## Introducing Amazon Bedrock AgentCore Gateway

### AgentCore Gateway

- Addresses the problem of using external tools at scale.
- Converts APIs, Lambda functions, or other services into **MCP tools**.
- Targets can be:
  - **OpenAPI (REST)**
  - **Smithy models** (AWS-specific)
  - **Lambda**
- Agents can then access them through **Gateway endpoints**.
- Manages **OAuth security / credentials**.
- Supports **semantic tool selection**.

### AgentCore Identity

- Different from OAuth identity for users and connecting to services.
- Focuses on your **agent’s identity / identities**.
- Provides **secure access to external tools and AWS services**.
- Acts as a **central repository** for all of your agent identities.
  - Similar to a **Cognito user pool**.
- Supports **secure credential storage**.
- OAuth 2.0 support:
  - Built-in support for **Google, GitHub, Slack, Salesforce, Atlassian**.
- There is a lot of depth to this, but you probably don’t need it right away.
- Reference: [AWS Bedrock AgentCore Identity Docs](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/identity.html)


## Quick Start

```bash
agentcore configure \
  --entrypoint multi_agent_restaurant.py \
  --name multi_agent_restaurant \
  --execution-role arn:aws:iam::058264126563:role/BedrockAgentCoreS3 \
  --ecr 058264126563.dkr.ecr.eu-central-1.amazonaws.com/bedrock-agentcore-multi_agent_restaurant \
  --requirements-file requirements.txt \
  --authorizer-config 'null' \
  --request-header-allowlist '' \
  --region eu-central-1 \
  --non-interactive

 agentcore launch --env OPENAI_API_KEY=$OPENAI_API_KEY
```
