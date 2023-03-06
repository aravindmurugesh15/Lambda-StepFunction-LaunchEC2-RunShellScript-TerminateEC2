# Lambda-StepFunction-LaunchEC2-RunShellScript-TerminateEC2
Lambda and StepFunction to LaunchEC2 then RunShellScript (Aurora DB Refresh) then TerminateEC2

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
