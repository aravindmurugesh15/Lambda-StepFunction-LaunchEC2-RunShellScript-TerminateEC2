import boto3
import time
def lambda_handler(event, context):
    
    ssm_client = boto3.client('ssm')
    instance_id = ssm_client.get_parameter(Name="/db/db_refresh/instanceid")
    command_id = ssm_client.get_parameter(Name="/db/db_refresh/cmdid")
    
    ins_id=instance_id['Parameter']['Value']
    cmd_id=command_id['Parameter']['Value']
    
    target_id= ins_id
    

    currentPollCount = 0
    try:
        currentPollCount=event['result']["CurrentPollCount"]
    except:
        pass
    poll_result={"status": "","CurrentPollCount":0, "ContinueToPoll":"TRUE"}
    
    response = ssm_client.get_command_invocation(CommandId=cmd_id,InstanceId=target_id)
    poll_result["status"]=response['Status']
    poll_result["CurrentPollCount"]=currentPollCount+1
    
    return poll_result
