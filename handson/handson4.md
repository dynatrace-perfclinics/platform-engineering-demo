### Hands-On 4: Deploy a new version of our app

Now that we have extended our automation in our platform to automatically execute an additional workflow when a new deployment is successfully detected we can deploy a new version of the app. 

In our tutorial we already have multiple versions of our application available. So far we have deployed version 1.0.2. We can now go ahead and deploy 2.0.2, 3.0.2 or 4.0.2.

How do we do this?
1. Find our `rollout.yaml` in our GitLab repository
2. Change the two version fields from the current version to the desired version
3. Commit the changes and let the automation do the rest!

![](https://raw.githubusercontent.com/dynatrace-perfclinics/platform-engineering-demo/main/images/handson4_41_update_version_1.png)

--- 

Now we can observe how ArgoCD is picking up that change, syncs it with K8s and with this triggers all the automation in Dynatrace.

Our final result should be that we see all notifications in our Backstage Notification Plugin!

![](https://raw.githubusercontent.com/dynatrace-perfclinics/platform-engineering-demo/main/images/handson4_41_update_version_2.png)
