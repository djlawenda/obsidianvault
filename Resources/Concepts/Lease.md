---
type: "Concept"
hub: "[[Hubs/Kubernetes]]"
tags: [concept, lease]
---
# Lease

In Kubernetes, Lease objects within the `kube-node-lease` namespace are used by nodes to send heartbeats, helping the cluster determine their availability and allowing the control plane to take action when failures are detected.

## Technologies
- 

## Excerpts & Key Information


> From: [[Processed_Transcripts/Kubernetes Nodes.md]] (Added on 2026-03-01 16:43)

*   Heartbeats, sent by Kubernetes nodes, help your cluster determine the availability of each node, and to take action when failures are detected.

*   For nodes there are two forms of heartbeats: Updates to the `.status` of a Node. Lease objects within the `kube-node-lease`. Each Node has an associated Lease object.



## Further Reading

> Core Node: [[Projects/Second_Brain]]