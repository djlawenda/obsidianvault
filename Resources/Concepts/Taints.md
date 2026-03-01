---
type: "Concept"
hub: "[[Hubs/Kubernetes]]"
tags: [concept, taints]
---
# Taints

A mechanism in Kubernetes that allows a node to repel a set of pods. Taints are used to ensure that pods are not scheduled onto inappropriate nodes.

## Technologies
- 

## Excerpts & Key Information


> From: [[Processed_Transcripts/Kubernetes Nodes.md]] (Added on 2026-03-01 16:43)

*   `--register-with-taints` - Register the node with the given list of (comma separated `<key>=<value>:<effect>`). No-op if `register-node` is false.

*   The node controller is also responsible for evicting pods running on nodes with `NoExecute` taints, unless those pods tolerate that taint.

*   The node controller also adds corresponding to node problems like node unreachable or not ready. This means that the scheduler won't place Pods onto unhealthy nodes.



## Further Reading

> Core Node: [[Projects/Second_Brain]]