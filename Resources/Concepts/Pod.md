---
type: "Concept"
hub: "[[Hubs/Kubernetes]]"
tags: [concept, pod]
---
# Pod

The smallest deployable unit in Kubernetes, representing a single instance of a running process in a cluster. A Pod encapsulates one or more containers, storage resources, a unique network IP, and options that govern how the containers run.

## Technologies
- 

## Excerpts & Key Information


> From: [[Processed_Transcripts/Kubernetes Nodes.md]] (Added on 2026-03-01 16:43)

*   Kubernetes runs your workload by placing containers into Pods to run on Nodes.

*   If the node is healthy (i.e. all necessary services are running), then it is eligible to run a Pod. Otherwise, that node is ignored for any cluster activity until it becomes healthy.

*   You can use labels on Nodes in conjunction with node selectors on Pods to control scheduling. For example, you can constrain a Pod to only be eligible to run on a subset of the available nodes.

*   Marking a node as unschedulable prevents the scheduler from placing new pods onto that Node but does not affect existing Pods on the Node.

*   The Kubernetes ensures that there are enough resources for all the Pods on a Node. The scheduler checks that the sum of the requests of containers on the node is no greater than the node's capacity.



## Further Reading

> Core Node: [[Projects/Second_Brain]]