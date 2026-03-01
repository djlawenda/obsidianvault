---
type: "Concept"
hub: "[[Hubs/Node_Components]]"
tags: [concept, network_proxy]
---
# Network Proxy

A component that runs on each node in a Kubernetes cluster, implementing part of the Kubernetes Service concept by maintaining network rules to allow communication to Pods.

## Technologies
- 

- [[Technologies/Kube_Proxy]]
## Excerpts & Key Information


> From: [[Processed_Transcripts/Cluster Architecture.md]] (Added on 2026-03-01 16:42)

*   kube-proxy is a network proxy that runs on each in your cluster, implementing part of the Kubernetes concept.

*   kube-proxy maintains network rules on nodes. These network rules allow network communication to your Pods from network sessions inside or outside of your cluster.



## Further Reading

> Core Node: [[Projects/Second_Brain]]