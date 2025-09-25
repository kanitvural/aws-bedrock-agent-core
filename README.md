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

---

### When Deployed to AWS

When you move the code to Lambda or another production environment:

- Your code will run entirely inside Lambda.
- `BedrockAgentCoreApp` + `@entrypoint` will now act as the Lambda handler.
- Frontend requests will flow like this: `API Gateway → Lambda → BedrockAgentCoreApp.invoke`.
- The user will no longer be hitting a local server but will instead send requests to the agent running in the **AWS environment**.
