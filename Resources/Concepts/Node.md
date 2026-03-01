---
type: "Concept"
hub: "[[Hubs/Kubernetes]]"
tags: [concept, node]
---
# Node

A virtual or physical machine in a Kubernetes cluster where Pods are run. It is managed by the control plane and hosts the necessary services to execute containerized workloads.

## Technologies
- 

## Excerpts & Key Information


> From: [[Processed_Transcripts/Kubernetes Nodes.md]] (Added on 2026-03-01 16:43)

*   Kubernetes runs your workload by placing containers into Pods to run on Nodes. A node may be a virtual or physical machine, depending on the cluster. Each node is managed by the control plane and contains the services necessary to run Pods.

*   Typically you have several nodes in a cluster; in a learning or resource-limited environment, you might have only one node.

*   The name of a Node object must be a valid DNS subdomain name.

*   Node objects track information about the Node's resource capacity: for example, the amount of memory available and the number of CPUs.



## Further Reading

> Core Node: [[Projects/Second_Brain]]