---
type: "Technology"
concept: "[[Concepts/Network_Proxy]]"
tags: [technology, kube_proxy]
---
# kube-proxy

A network proxy that runs on each node in a Kubernetes cluster, maintaining network rules to enable communication to Pods, optionally using the operating system packet filtering layer.

## Excerpts & Key Information


> From: [[Processed_Transcripts/Cluster Architecture.md]] (Added on 2026-03-01 16:42)

*   kube-proxy is a network proxy that runs on each in your cluster, implementing part of the Kubernetes concept.

*   kube-proxy maintains network rules on nodes. These network rules allow network communication to your Pods from network sessions inside or outside of your cluster.

*   kube-proxy uses the operating system packet filtering layer if there is one and it's available. Otherwise, kube-proxy forwards the traffic itself.



## Further Reading

### Source
*   Original reference: [[Processed_Transcripts/Cluster Architecture.md]]

> Core Node: [[Projects/Second_Brain]]