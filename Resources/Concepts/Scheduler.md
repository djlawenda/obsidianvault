---
type: "Concept"
hub: "[[Hubs/Control_Plane]]"
tags: [concept, scheduler]
---
# Scheduler

A control plane component that watches for newly created Pods with no assigned node and selects a node for them to run on, considering various factors like resource requirements, constraints, and affinity.

## Technologies
- 

- [[Technologies/Kube_Scheduler]]
## Excerpts & Key Information


> From: [[Processed_Transcripts/Cluster Architecture.md]] (Added on 2026-03-01 16:42)


> From: [[Processed_Transcripts/Kubernetes Nodes.md]] (Added on 2026-03-01 16:43)

*   Marking a node as unschedulable prevents the scheduler from placing new pods onto that Node but does not affect existing Pods on the Node.

*   You can use labels on Nodes in conjunction with node selectors on Pods to control scheduling. For example, you can constrain a Pod to only be eligible to run on a subset of the available nodes.

*   The Kubernetes ensures that there are enough resources for all the Pods on a Node. The scheduler checks that the sum of the requests of containers on the node is no greater than the node's capacity.

*   The node controller also adds corresponding to node problems like node unreachable or not ready. This means that the scheduler won't place Pods onto unhealthy nodes.



*   Control plane component that watches for newly created with no assigned, and selects a node for them to run on.

*   Factors taken into account for scheduling decisions include: individual and collective requirements, hardware/software/policy constraints, affinity and anti-affinity specifications, data locality, inter-workload interference, and deadlines.



## Further Reading

> Core Node: [[Projects/Second_Brain]]