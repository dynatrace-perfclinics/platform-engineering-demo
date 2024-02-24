### Hands-On 2: Create a new Service, Deploy it, Explore with Dynatrace

Now that we are familiar with the core components of our IDP we are ready to use it to 
1. **ONBOARD** a new service via Backstage
2. **DEPLOY** the new GitLab repository by ArgoCD
3. **OBSERVE** the deployment by Dynatrace
4. **NOTIFY** about the status by Dynatrace Workflows

The following animation shows what we are planning to do in this Hands-On:

![](https://raw.githubusercontent.com/dynatrace-perfclinics/platform-engineering-demo/main/images/handson2_animation_animated.gif)

#### 2.1: Onboarding a new service through Backstage

We start in Backstage and walk through the **Create a New Component** workflow. 

**TEAM IDENTIFIER: Use your unique training attendee number, e.g: 08,09,10,11, ...**

As we walk through the workflow please use your unique team identifier. 

**For example:** if your attendee ID is 13 then you would use the following values on the team's details page:
* **ID:** team13
* **Name:** Team 13
* **Email:** team13@somedomain.com

![](https://raw.githubusercontent.com/dynatrace-perfclinics/platform-engineering-demo/main/images/handson2_21_createinbackstage.png)

What you should have learned is:
* How to create a new service in Backstage based on a Template
* How to find the created resources

---

#### 2.2: Lets explore the GitLab repository that was created

Now lets explore the GitLab repository a bit closer. There are a couple of interesting things

**1: NAME of the Repository**

The name of the repository ends in `-cd`. This is important as we have configured ArgoCD through a so called **ApplicationSet** to automatically watch out for GitLab repositories that end with `-cd`

**2: ARGOCD folder with deployment CRDs**

This folder contains all CRDs (Custom Resource Definitions) that ArgoCD will deploy/synchronize with K8s. To have a closer look:
* **CRDs:** for namespace (enables Keptn), ingress (exposes our service to the internet), rollout (Blue/Green Definition), RoleBinding for Dynatrace Monitoring and the Service Definition 
* **ArgoCD Workflow:** which pushes Dynatrace Observability as Code via Monaco
* **ArgoCD Webhooks:** which push Lifecycle Events to Dynatrace for PreSync, Sync, PostSync and SyncFail

**3: MONACO folder with Dynatrace Configuration as Code**

This folder contains Monaco definitions for SLOs, Ownership and Synthetic Tests. This could be replaced with other Config As Code tools such as Terraform, Ansible, Crossplane (support for Crossplane is currently in the works)

![](https://raw.githubusercontent.com/dynatrace-perfclinics/platform-engineering-demo/main/images/handson2_22_explorerepo_1.png)

---

ArgoCD in the meantime has started to synchronize this new repository on GitLab with K8s:

![](https://raw.githubusercontent.com/dynatrace-perfclinics/platform-engineering-demo/main/images/handson2_22_explore_argo_1.png)

---

#### 2.3 How we made Dynatrace Release Aware!

The GitLab repository contains a lot of pre-populated meta data in the different CRDs. This meta data includes
* Version, e.g: 1.0.2
* Stage, e.g: pre-prod
* Application, e.g: simplenodetest-team02
* Owner, e.g: team02

Dynatrace automatically extracts this metadata as part of our [Version detection stragety](https://docs.dynatrace.com/docs/platform-modules/automations/release-monitoring/version-detection-strategies) as well as for [Entity ownership](https://docs.dynatrace.com/docs/manage/ownership/best-practices)

![](https://raw.githubusercontent.com/dynatrace-perfclinics/platform-engineering-demo/main/images/handson2_22_releaseawareness_1.png)

---

#### 2.4 Owners, SLOs and Synthetics through Observability as Code

Right now we have Dynatrace automatically detect newly deployed services. Dynatrace also has some meta data such as release version, stage or team identifier of the owner. What we are missing however are some additional observability configuration such as
1. What's the email of teamXX?
2. How to validate the system is available?
3. Are we meeting our SLOs?

For this we can use Dynatrace Ownership, Dynatrace Synthetics and Dynatrace SLOs. And instead of manually configuring it we can fully automate the configuration through **Observability as Code**. This can be done by calling the Dynatrace API or using tools such as Terraform, Ansible, Crossplane or Monaco. Our IDP setup uses Monaco which gets executed through an Argo Workflow as a PreSync action. Lets have a quick look at the configuration in GitLab and how this configuration looks in Dynatrace:

![](https://raw.githubusercontent.com/dynatrace-perfclinics/platform-engineering-demo/main/images/handson2_24_configascode_1.png)

#### Explore our App Yourself

As you have seen - we have Dynatrace Synthetic Tests that are testing our application. Its time to also browse to our app as it is exposed via an Ingress to the internet. There are several ways we can find the URL
1. We can take it from the Dynatrace Synthetic Test
2. We can see it in ArgoCD
3. We can get it from the Ingress Definition in GitLab

![](https://raw.githubusercontent.com/dynatrace-perfclinics/platform-engineering-demo/main/images/handson2_24_exploreourapp_1.png)

---

#### 2.5 How we make Dynatrace Lifecycle Event Aware!

There are many lifecycle stages that an artifact goes through: Build, Prepare, Deploy, Test, Validate, Release, Operate, Retire ...

At Dynatrace we are working on standardizing those lifecycle events and define semantics behind the meta data which will allow future Dynatrace Apps that are being built to provide better out-of-the-box features.

As of today we are suggesting that CI/CD tools use our BizEvents ingest API to make Dynatrace aware of a Lifecycle event. Alternatively we could also use the Events APIv2. In our IDP we are using BizEvents that are being sent from ArgoCD as part of a PreSync, Sync, PostSync and SyncFail Webhook. Those events are then triggering the `Dynatrace Lifecycle Workflow` which does the following:
1. (for any event) Sends a Notification to the Backstage Notification Page
2. (for sync finished) Waits until Dynatrace sees the PGI with all metadata
3. (for sync finished) Creates Classic Deployment Events and a Deployment Validated Lifecycle Event
4. (for sync finished) Sends a Notification to the Backstage Notification Page

![](https://raw.githubusercontent.com/dynatrace-perfclinics/platform-engineering-demo/main/images/handson2_22_lifecycleevents_1.png)

Besides the BizEvents we can also use other events and ways to trigger events:

![](https://raw.githubusercontent.com/dynatrace-perfclinics/platform-engineering-demo/main/images/handson2_22_lifecycleevents_2.png)

Let's also have a closer look at the Workflow itself. You can view it by opening the Workflow App and Opening the `Lifecycle Event Workflow`

![](https://raw.githubusercontent.com/dynatrace-perfclinics/platform-engineering-demo/main/images/handson2_25_understandworkflow_1.png)

---

#### 2.6 Lets explore all our Lifecycle Events so far!

With the current setup we should get 4 different Lifecycle Events:
* sync.prepare
* sync.started
* sync.finished
* deployment.validated

The easiest to query this information is by executing a DQL to get us exactly that data!

In the following DQL Query put in your team name and run the query. It will give you a table of all events.

As additional tasks you can `filter` or `summarize` on `event.provider` as well as `event.type`