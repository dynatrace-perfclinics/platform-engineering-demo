### Hands-On 3: Setting up an SRG (Site Reliability Guardian)

Now that we have our first version of our applications deployed we want to validate that the next time a new version gets deployed our applications are still healthy and running!

For this we will be doing three steps:
1. Create a Site Reliability Guardian (SRG) to validate our key objectives of our service
2. Trigger that SRG from a Workflow for a `deployment.validated` lifecycle event
3. Send a notification message to our Backstage Notification Plugin

Here is a quick overview of what we want to achieve:

![](https://raw.githubusercontent.com/dynatrace-perfclinics/platform-engineering-tutorial/main/images/handson3_srgoverview_animated.gif)

--- 

#### 3.1 Create a Site Reliability Guardian (SRG) for our service

To learn more about the Site Reliability Guardian (SRG) also watch [Dynatrace App Spotlight: SRG](https://www.youtube.com/watch?v=s3KG4kn-ymY)

As indicated in the video, creating an SRG can start with picking an existing template or creating one from scratch. In our Hands-On we will create an SRG from scratch. Here are the steps:
1. Open the SRG App and click on `+ Guardian`
2. Select `create without template` and give it a good name
3. Add one objective 
4. Specify `Availability` and choose the `Availability SLO` for your service
5. `Create and Validate` 
6. Validate the result

Here are those steps visually explained

![](https://raw.githubusercontent.com/dynatrace-perfclinics/platform-engineering-tutorial/main/images/handson3_31_createsrg_1.png)

#### 3.2 Create a Workflow for the Guardian

As we have validated that the guardian works based on our current set of objectives its time to automate the execution. For this we can create a workflow straight from the Guardian App. What we need to adjust is 
1. The trigger of the workflow should be from a successful `deployment.validated` for our respective application
2. Using the last 30 minutes as evaluation timeframe (NOT BEST PRACTICE - BUT GOOD FOR THE START)

Here are those steps visually explained

![](https://raw.githubusercontent.com/dynatrace-perfclinics/platform-engineering-tutorial/main/images/handson3_32_automate_srg_1.png)

#### 3.3 Execute the Workflow and validate its working

We can manually trigger a workflow at any time. When clicking `Run` we will be prompted with a sample event that will be used to execute the workflow. As we have earlier queried the events that match our filter the event proposed will be one of our previous `deployment.validated` lifecycle events.

![](https://raw.githubusercontent.com/dynatrace-perfclinics/platform-engineering-tutorial/main/images/handson3_33_run_srg_workflow_1.png)

#### 3.4 Extend Workflow with a Notification

As a last step we can extend the Workflow to also send the result of the Guardian to our Notification system. In *the real world* this could be Slack, EMail, creating a JIRA Ticket. In our case our Backstage Notification plugin will do.

Lets therefore add a new HTTP Request task as shown below in the image. Here the additional information you need for setting up this task:
1. URL: `https://backstage.dtulabXXXXXXXXXXXX.dynatrace.training/api/notifications`
2. Payload
```
{
  "message": "SRG Result for {{ event()["app_name"] }}: {{ result("run_validation").validation_status }}! See result: {{ result("run_validation").validation_url }} ",
  "channel": "{{event()["owner"] }}",
  "origin": "Guardian Workflow"
}
```

![](https://raw.githubusercontent.com/dynatrace-perfclinics/platform-engineering-tutorial/main/images/handson3_34_add_notifications_1.png)

---

### (Optional) Hands-On 3: Extending the Guardian with more objectives

The power of Dynatrace is that we have all relevant data in Grail which makes it usable for the Site Reliability Guardian (SRG)
In this optional Hands-On we can extend the guardian we just created with additional objectives such as
1. Validate that there are no error logs
2. Validate that response time is within a certain threshold
3. Validate that there are no HTTP 5xx
4. Validate that there are no security vulnerabilities
5. Validate that memory and cpu usage is within expectations

#### 3.5 Adding Error Log Objective

We can easily add a new objective to validate whether we have any error logs. Our application creates error logs when 
1. We `Invoke` passing a Server URL that is invalid, e.g: www.wrongdomain.abc
2. We call the URL: `/api/causeerror`

To create such an objective we should first define and test a DQL query that gives us the number of error logs created by our app. Once we have it we can add this query as an objective and specify a threshold that should not be higher than 0.

To make it easier for you see the `Query Error Logs` DQL query below. Modify it by using your `team identifier`. Run it to make sure it works. Then update the Guardian!
```
fetch `logs`
| filter contains(`k8s.pod.name`, "team02")
| filter contains(content, "Error")
| summarize errorCount=count()
```