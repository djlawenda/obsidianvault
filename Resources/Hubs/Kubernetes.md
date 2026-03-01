---
type: "Hub"
tags: [hub, kubernetes]
---
# Kubernetes

Kubernetes is a portable, extensible, open source platform for managing containerized workloads and services that facilitates both declarative configuration and automation. It ensures high availability and simplifies the management of distributed systems.

## Concepts
- 

- [[Concepts/Containerized_Workloads]]
- [[Concepts/Declarative_Configuration]]
- [[Concepts/Automation]]
- [[Concepts/Service_Discovery]]
- [[Concepts/Load_Balancing]]
- [[Concepts/Storage_Orchestration]]
- [[Concepts/Automated_Rollouts_And_Rollbacks]]
- [[Concepts/Automatic_Bin_Packing]]
- [[Concepts/Self_Healing]]
- [[Concepts/Secret_And_Configuration_Management]]
- [[Concepts/Batch_Execution]]
- [[Concepts/Horizontal_Scaling]]
- [[Concepts/Ipv4Ipv6_Dual_Stack]]
- [[Concepts/Extensibility]]
- [[Concepts/Platform_As_A_Service_Paas]]
- [[Concepts/Orchestration]]
- [[Concepts/Application_Services_Integration]]
- [[Concepts/Addons]]
- [[Concepts/Architecture_Variations]]
- [[Concepts/Node]]
- [[Concepts/Pod]]
- [[Concepts/Node_Object]]
- [[Concepts/Lease]]
- [[Concepts/Taints]]
- [[Concepts/Tolerations]]
- [[Concepts/Labels]]
- [[Concepts/Cloud_Provider]]
- [[Concepts/Virtual_Machine_Vm]]
## Excerpts & Key Information


> From: [[Processed_Transcripts/Kubernetes Overview.md]] (Added on 2026-03-01 16:42)


> From: [[Processed_Transcripts/Kubernetes Nodes.md]] (Added on 2026-03-01 16:43)

*   Kubernetes runs your workload by placing containers into Pods to run on Nodes.

*   Kubernetes creates a Node object internally (the representation).

*   Kubernetes checks that a kubelet has registered to the API server that matches the `metadata.name` field of the Node.

*   Kubernetes also assumes that a resource with the same name is the same object.

*   Heartbeats, sent by Kubernetes nodes, help your cluster determine the availability of each node, and to take action when failures are detected.

*   The Kubernetes ensures that there are enough resources for all the Pods on a Node.



*   Kubernetes is a portable, extensible, open source platform for managing containerized workloads and services that facilitate both declarative configuration and automation.

*   That's how Kubernetes comes to the rescue! Kubernetes provides you with a framework to run distributed systems resiliently. It takes care of scaling and failover for your application, provides deployment patterns, and more.



## Further Reading

> Core Node: [[Projects/Second_Brain]]