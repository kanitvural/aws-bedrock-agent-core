import boto3
import json

client = boto3.client('bedrock-agentcore', region_name='eu-central-1')
payload = json.dumps({
    "prompt": "i want to stay in houston in hotel tonight"
})

response = client.invoke_agent_runtime(
    agentRuntimeArn='arn:aws:bedrock-agentcore:eu-central-1:058264126563:runtime/multi_agent_restaurant-ctzDy45ULO',
    runtimeSessionId='dfmeoagmreaklgmrkleafremoigrmtesogmtrskhmtkrlshmtkanit',  # Must be 33+ chars
    payload=payload,
    qualifier="DEFAULT" # Optional
)
response_body = response['response'].read()
response_data = json.loads(response_body)
print("Agent Response:", response_data)