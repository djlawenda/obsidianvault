---
type: "Concept"
hub: "[[Hubs/Kubernetes]]"
tags: [concept, tolerations]
---
# Tolerations

A mechanism in Kubernetes applied to Pods that allows them to be scheduled on nodes with matching taints. A pod with a toleration for a node's taint will be scheduled on that node.

## Technologies
- 

## Excerpts & Key Information


> From: [[Processed_Transcripts/Kubernetes Nodes.md]] (Added on 2026-03-01 16:43)

*   The node controller is also responsible for evicting pods running on nodes with `NoExecute` taints, unless those pods tolerate that taint.



## Further Reading

> Core Node: [[Projects/Second_Brain]]