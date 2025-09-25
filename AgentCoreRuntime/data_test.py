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