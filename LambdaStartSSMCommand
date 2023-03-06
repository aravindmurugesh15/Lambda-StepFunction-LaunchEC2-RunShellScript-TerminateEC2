import boto3
import time
def lambda_handler(event, context):


    target_id=''
    cmd_id=''
    ExecutionName=''
    cmd='/home/ec2-user/dbrefresh/testaravind.sh'

    ssm_client = boto3.client('ssm')
    
    instance_id = ssm_client.get_parameter(Name="/db/cjams_refresh/instanceid")
    
    ins_id=instance_id['Parameter']['Value']

    target_id=ins_id
    document="shellscriptauroradb"
    ExecutionName="Startssmcommand"
    
    response = ssm_client.send_command(
        InstanceIds=[target_id],
        DocumentName=document,
        Comment="Test run",
        #Parameters= { "commands": ["echo \" Hello! Start\" ","sleep 1m","echo \"Exit\""]},
        Parameters= { "commands": [cmd] , 'executionTimeout': ['36000']},
        CloudWatchOutputConfig={"CloudWatchOutputEnabled":True}
        )
    cmd_id= response['Command']['CommandId']
    
    ssm_result = {"SsmCommandId":cmd_id,"InstanceId":target_id,"ExecutionName":ExecutionName}
    
    ssm_client.put_parameter(
         Name='/db/db_refresh/cmdid',
         Value= cmd_id,
         Type='String',
         Overwrite=True
       )
    
    return ssm_result
    
