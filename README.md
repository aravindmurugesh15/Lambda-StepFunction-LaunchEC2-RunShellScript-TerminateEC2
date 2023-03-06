# Lambda-StepFunction-LaunchEC2-RunShellScript-TerminateEC2
Lambda and StepFunction to LaunchEC2 then RunShellScript (Aurora DB Refresh) then TerminateEC2. 
1. Crete 4 lambda function launch-ec2-instance, startssmcommand, checkssmcomman and terminate-ec2-instance. 
2. Create Step funtion to create the workflow and copy the jason from the link. 

# Create the State Machine and Provision Resources
Open the Step Functions console and choose Create state machine.

# Choose Run a sample project, and then choose Job Poller.

The state machine Definition and Visual Workflow are displayed.
      
Note
The Definition section in this state machine references the AWS resources that will be created for this sample project.

Choose Next.

The Deploy resources page is displayed, listing the resources that will be created. For this sample project, the resources include:

A SubmitJob Lambda function

A CheckJob Lambda function

A SampleJobQueue Batch Job Queue

Choose Deploy resources.
