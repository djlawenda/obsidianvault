---
type: "Concept"
hub: "[[Hubs/Control_Plane]]"
tags: [concept, api_server]
---
# API Server

The central management entity in Kubernetes, exposing the Kubernetes API. It acts as the frontend for the control plane, handling all REST requests for cluster management.

## Technologies
- 

## Excerpts & Key Information


> From: [[Processed_Transcripts/Kubernetes Nodes.md]] (Added on 2026-03-01 16:43)

*   The kubelet on a node self-registers to the control plane

*   Kubernetes checks that a kubelet has registered to the API server that matches the `metadata.name` field of the Node.

*   When the kubelet flag `--register-node` is true (the default), the kubelet will attempt to register itself with the API server.

*   `--kubeconfig` - Path to credentials to authenticate itself to the API server.

*   When the Node authorization mode and NodeRestriction admission plugin are enabled, kubelets are only authorized to create/modify their own Node resource.

*   If the Node needs to be replaced or updated significantly, the existing Node object needs to be removed from API server first and re-added after the update.

*   `--node-status-update-frequency` - Specifies how often kubelet posts its node status to the API server.



## Further Reading

> Core Node: [[Projects/Second_Brain]]