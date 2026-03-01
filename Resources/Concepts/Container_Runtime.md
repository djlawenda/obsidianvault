---
type: "Concept"
hub: "[[Hubs/Node_Components]]"
tags: [concept, container_runtime]
---
# Container Runtime

A fundamental component that empowers Kubernetes to run containers effectively, responsible for managing the execution and lifecycle of containers within the Kubernetes environment.

## Technologies
- 

- [[Technologies/Containerd]]
- [[Technologies/Cri_O]]
- [[Technologies/Docker]]
## Excerpts & Key Information


> From: [[Processed_Transcripts/Cluster Architecture.md]] (Added on 2026-03-01 16:42)


> From: [[Processed_Transcripts/Kubernetes Nodes.md]] (Added on 2026-03-01 16:43)

*   The components on a node include the kubelet, a container runtime, and the kube-proxy.

*   The scheduler checks that the sum of the requests of containers on the node is no greater than the node's capacity. That sum of requests includes all containers managed by the kubelet, but excludes any containers started directly by the container runtime, and also excludes any processes running outside of the kubelet's control.



*   A fundamental component that empowers Kubernetes to run containers effectively. It is responsible for managing the execution and lifecycle of containers within the Kubernetes environment.

*   Kubernetes supports container runtimes such as, , and any other implementation of the Kubernetes CRI (Container Runtime Interface).



## Further Reading

> Core Node: [[Projects/Second_Brain]]