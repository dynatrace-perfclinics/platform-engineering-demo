## Hands-On 1: Explore the Platform we have built for you

The following shows the IPD (Internal Development Platform), how it was built and how it will work:
![](https://raw.githubusercontent.com/dynatrace-perfclinics/platform-engineering-demo/main/images/platform_setup_animation_animated.gif)

### 1.1 Observability: Dynatrace, OpenTelemetry & Keptn 

#### 1.1.1 Dynatrace: Our Observability, Security & Automation Platform Capability

Lets explore our Dynatrace setup!

The Dynatrace Operator was rolled out by ArgoCD as part of the initial IDP setup. This allows Dynatrace to 
* **MONITOR** our whole K8s cluster through the K8s APIs (See Kubernetes App)
* **OBSERVE** all workloads through OneAgent (See Kubernetes Workloads)
* **INGEST** *logs and events* from all K8s components (See Logs sections in K8s)
* **INGEST** OpenTelemetry data from the OTel collector (See Traces)
* **SCRAPE** Prometheus metrics via the deployed ActiveGate (See Metrics)

![](https://raw.githubusercontent.com/dynatrace-perfclinics/platform-engineering-demo/main/images/dynatrace_overview.png)

Please follow the instructor and explore some of the core screens in Dynatrace such as the Kubernetes App, Kubernetes Workloads or the Platform Observability Dashboard!

What you should have learned:
* How Dynatrace was deployed on this IDP
* How to find K8s workload observability data
* How to find lots created by different IDP components
* Which core dashboards we have

#### 1.1.2 OpenTelemetry: Ingesting all observability data in cloud native!

To learn more about OpenTelemetry go to [OpenTelemetry homepage](https://opentelemetry.io/) and get more hands-on from [IsItObservable](https://isitobservable.io/open-telemetry)

In our IDP we have an OpenTelemetry Collector that sends collected observability data to Dynatrace's OTLP endpoint. In our default setup we mainly collect OpenTelemetry traces from tools like ArgoCD, GitLab and Keptn. If we would deploy any apps that create any OpenTelemetry signals this data could automatically be collected and sent to Dynatrace as well.

Those traces can then for instanced be analyzed in our **Dynatrace Distributed Traces app**

![](https://raw.githubusercontent.com/dynatrace-perfclinics/platform-engineering-demo/main/images/platform_overview_otel_argocd.png)

For reference. It literally only takes a handful of config files in the OpenTelemetry Collector ConfigMap to send data to Dynatrace:
```
    exporters:
      debug: {}
      logging: {}
      otlphttp:
        endpoint: $DT_URL/api/v2/otlp
        headers:
          Authorization: Api-Token $DT_OTEL_ALL_INGEST_TOKEN
```

What you should have learned:
* That OpenTelemetry is a standard component available in our IDP
* How easy it is to send OpenTelemetry data to Dynatrace
* Where to find OpenTelemetry data in Dynatrace

#### 1.1.3 Keptn: Providing Cloud Native Application Lifecycle Observability

To learn more about Keptn please visit [Keptn Website](https://lifecycle.keptn.sh/)

In our IDP we are using Keptn to provide observability into the deployment lifecycle of our cloud native custom applications. Keptn's Lifecycle Operator can be enabled per k8s namespace via a simple annotation:
```
apiVersion: v1
kind: Namespace
metadata:
  name: "your-namespace"
  annotations:
    keptn.sh/lifecycle-toolkit: "enabled"
```

Once enabled, it automatically created OpenTelemetry traces to trace the deployment of all application workloads. Keptn also emits Prometheus metrics that are also sent to OpenTelemetry.

![](https://raw.githubusercontent.com/dynatrace-perfclinics/platform-engineering-demo/main/images/platform_overview_otel_keptn.png)

The benefit of having Keptn is that we automatically get a base set of the DORA metrics (deployment frequency, deployment time, deployment failure rate) as well as distributed traces to troubleshoot failed or long running deployments

We can observe Keptn created data either in the **Dynatrace Distributed Traces app**, by viewing the Keptn metrics in custom dashboards or by looking at the Lifecycle Operator Service!

What you should have learned:
* What Keptn does and which data it provides
* How to enable Keptn on a namespace level

---

### 1.2 ArgoCD: Our GitOps tool to synchronize our deployment configuration to K8s

Want to learn more about ArgoCD? [Check out the ArgoCD Website](https://argoproj.github.io/cd/)

In our IDP, ArgoCD on the one hand is used to deploy the core platform components: Backstage, GitLab, Argo Rollouts, OpenTelemetry, Keptn, Dynatrace ...
On the other hand ArgoCD also deploys any custom application repository on our GitLab instance that follows a certain naming schema (those repositories will later be created through Backstage).

Lets start with exploring ArgoCD by navigating to our ArgoCD UI. Please login with the credentials given and then follow the guidance of your instructor:
![](https://raw.githubusercontent.com/dynatrace-perfclinics/platform-engineering-demo/main/images/argocd_overview.png)

What you should have learned:
* How to access ArgoCD
* How to find specific Argo applications
* How to detect the status of an application
* How to read the deployed artifacts of an application

---

### 1.3 GitLab: Our Configuration Source of Truth in Git!

Want to learn more about GitLab? [Check out their GitLab website](https://about.gitlab.com/)

While our Core IDP components was created from configuration files that are hosted on a public GitHub repository our IDP itself is hosting a GitLab instance that will be used manage all custom applications that we will deploy later on! GitLab has many more features - in our IDP we are only using it for Git-based Version Control!

Lets start with exploring our GitLab instance by navigating to the GitLab UI. Login and then follow the instructor!

![](https://raw.githubusercontent.com/dynatrace-perfclinics/platform-engineering-demo/main/images/gitlab_overview.png)

What you should have learned:
* How to access GitLab
* What the template repositories are
* How user application repositories look like

### 1.4 Backstage: Our Developer Portal, Our Notification Center!

Want to learn more about Backstage? [Check out the Backstage website](https://backstage.io/)

In our IDP, Backstage is used as a Software Catalog as well as our self-service portal to create new applications from templates. Additionally to that we also extended Backstage to provide a simple chat/notification feature which allows us to send messages back to our teams (this is due to the lack of a shared Slack, MS Teams or other chat solutions)!

Lets start with exploring Backstage by navigating to the Backstage UI, then follow the guidance of your instructor:

![](https://raw.githubusercontent.com/dynatrace-perfclinics/platform-engineering-demo/main/images/backstage_overview.png)

What you should have learned:
* How to access Backstage
* How to browse the Software Catalog
* Where to create new software components (will need this later)
* Where to find notifications

---