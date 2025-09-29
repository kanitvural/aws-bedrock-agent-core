import boto3
import json

def lambda_handler(event, context):
    # Preflight request (OPTIONS) için cevap
    if event.get("httpMethod") == "OPTIONS":
        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "Content-Type",
                "Access-Control-Allow-Methods": "OPTIONS,POST,GET"
            },
            "body": ""
        }

    try:
        body = json.loads(event.get("body", "{}"))
        prompt = body.get("prompt")
        session_id = body.get("sessionId")

        if not prompt or not session_id:
            return {
                "statusCode": 400,
                "body": json.dumps({"message": "Both 'prompt' and 'sessionId' are required."}),
                "headers": {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*"
                }
            }

        client = boto3.client('bedrock-agentcore', region_name='eu-central-1')
        payload = json.dumps({"prompt": prompt})

        response = client.invoke_agent_runtime(
            agentRuntimeArn='arn:aws:bedrock-agentcore:eu-central-1:058264126563:runtime/multi_agent_restaurant-wg3fXH8MuC',
            runtimeSessionId=session_id,
            payload=payload,
            qualifier="DEFAULT"
        )

        response_body = response['response'].read()
        response_data = json.loads(response_body)

        return {
            "statusCode": 200,
            "body": json.dumps({"response": response_data.get("result")}),
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            }
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"message": str(e)}),
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            }
        }

        
# Postman test

# {
#   "prompt": "i want to stay in a hotel in houston to night",
#   "sessionId": "dfmeoagmreaklgmrkleafremoigrmtesogmtrskhmtkrlshmtkanit"
# }


