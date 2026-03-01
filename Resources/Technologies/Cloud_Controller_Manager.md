---
type: "Technology"
concept: "[[Concepts/Controller]]"
tags: [technology, cloud_controller_manager]
---
# cloud-controller-manager

A Kubernetes component that embeds cloud-specific control logic, linking the cluster into a cloud provider's API and running controllers specific to that cloud environment.

## Excerpts & Key Information


> From: [[Processed_Transcripts/Cluster Architecture.md]] (Added on 2026-03-01 16:42)

*   A Kubernetes component that embeds cloud-specific control logic. The cloud controller manager lets you link your cluster into your cloud provider's API, and separates out the components that interact with that cloud platform from components that only interact with your cluster.

*   The cloud-controller-manager only runs controllers that are specific to your cloud provider. If you are running Kubernetes on your own premises, or in a learning environment inside your own PC, the cluster does not have a cloud controller manager.



## Further Reading

### Source
*   Original reference: [[Processed_Transcripts/Cluster Architecture.md]]

> Core Node: [[Projects/Second_Brain]]