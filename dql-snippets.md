# Parse Argo Rollout Logs

```
// time="2023-11-15T05:36:42Z" level=info msg="Rollout step 8/8 completed (pause: 2s)" event_reason=RolloutStepCompleted namespace=repo2 rollout=rollouts-demo
fetch logs
//| limit 1
//| fields content = "time=\"2023-11-15T05:36:42Z\" level=info msg=\"Rollout step 8/8 completed (pause: 2s)\" event_reason=RolloutStepCompleted namespace=repo2 rollout=rollouts-demo"
| filter contains(content, "event_reason")
| filter contains(content, "Rollout")
| parse content, "'time=\"' LD:time '\" level=' LD:level ' msg=\"' LD:msg '\" event_reason=' LD:event_reason ' namespace=' LD:namespace ' rollout=' LD:rollout"
| sort timestamp asc
```

# Parse kubebench logs

```
fetch logs
| filter contains(content, "checks")
| parse content, "INT:number ' checks ' ALPHA:level"
| sort timestamp desc
```

# Parse kubehunter logs

```
fetch `logs`
| filter contains(`content`, "found vulnerability", caseSensitive: false)
| filter `k8s.cronjob.name` == "kubehunter"
| parse content, "LD SPACE LD SPACE LD:loglevel SPACE LD:source SPACE 'Found vulnerability' SPACE '\"' LD:vuln '\" in' SPACE LD:vuln_location"
| fieldsKeep timestamp, loglevel, source, vuln, vuln_location
```