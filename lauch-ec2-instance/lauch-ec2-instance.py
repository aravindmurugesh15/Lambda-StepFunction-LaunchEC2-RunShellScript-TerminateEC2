import json
import os
import boto3
from time import sleep
client = boto3.client('ec2')

ssm_client = boto3.client('ssm')

REGION = os.environ['REGION']
AMI_IMAGE_ID = os.environ['AMI_IMAGE_ID']
INSTANCE_TYPE = os.environ['INSTANCE_TYPE']
DISK_SIZE_GB = os.environ['DISK_SIZE_GB']
DEVICE_NAME = os.environ['DEVICE_NAME']
KEY_NAME= os.environ['KEY_NAME']
NAME = os.environ['NAME']
OWNER = os.environ['OWNER']
RUNID = os.environ['RUNID']
SUBNET_ID = os.environ['SUBNET_ID']
SECURITY_GROUPS_IDS = ['sg-xxxxxxxxxxxxxxxxf']
PUBLIC_IP = os.environ['PUBLIC_IP']

ec2 = boto3.resource('ec2')

USERDATA_SCRIPT = """
#!/bin/bash
cd /tmp curl https://s3.amazonaws.com/ec2-downloads-windows/SSMAgent/latest/linux_amd64/amazon-ssm-agent.rpm sudo yum install -y amazon-ssm-agent.rpm
sudo yum update -y
sudo amazon-linux-extras enable postgresql13
sudo yum install postgresql-server -y
sudo postgresql-setup initdb
sudo systemctl start postgresql
sudo systemctl enable postgresql
sudo systemctl status postgresql
sudo yum install ec2-instance-connect
sudo yum install awscli
chmod 777 /home/ec2-user/
mkdir -m777 /home/ec2-user/dbrefresh
aws s3 cp s3://test-cjams/test/testaravind.sh /home/ec2-user/dbrefresh
sudo chmod a+x /home/ec2-user/dbrefresh/testaravind.sh
"""

def lambda_handler(event, context):
    
    # Create Elastic/Public IP for instance
    instance = ec2.create_instances(ImageId=AMI_IMAGE_ID,
                                        InstanceType=INSTANCE_TYPE,
                                        SubnetId=SUBNET_ID,
                                        SecurityGroupIds=SECURITY_GROUPS_IDS,
                                        UserData=USERDATA_SCRIPT,
                                        MinCount=1, MaxCount=1,
                                        KeyName=KEY_NAME,
                                        TagSpecifications=[
                                        {
                                        'ResourceType': 'instance',
                                        'Tags': [{
                                        'Key': 'Name',
                                        'Value': 'dbrefresh-machine'
                                        }]
                                        }
                                        ],
                                        BlockDeviceMappings=[
                                        {
                                        'DeviceName': DEVICE_NAME,
                                        'Ebs': {
                                        'DeleteOnTermination': True,
                                        'VolumeSize': 10,
                                        'VolumeType': 'gp2'
                                        }},
                                        ]
                                        )
                                          
    instance = instance[0]                                    
                                        
    if instance is None:
        raise Exception("Failed to create instance! Check the AWS console to verify creation or try again")
 
    print("Instance created and launched successfully!")
    print("#### Instance id: " + instance.id)
    
    instance.wait_until_running()
    
    response = client.associate_iam_instance_profile(
    IamInstanceProfile={
        'Arn': 'arn:aws:iam::1234567890:instance-profile/cloud9/AWSCloud9SSMInstanceProfile',
        'Name': 'AWSCloud9SSMAccessRole'
    },
    InstanceId= instance.id
    )
    
    intance = instance.id
    
    ssm_client.put_parameter(
         Name='/db/db_refresh/instanceid',
         Value= instance.id,
         Type='String',
         Overwrite=True
       )
    
    return {**event, "instanceId": instance.id,'instanceresult':intance}
